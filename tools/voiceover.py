#!/usr/bin/env python3
"""voiceover.py — read an episode's script with an ElevenLabs voice (default: Brian).

The narration of 02-script.md (the body between its first two --- rules) is sent to ElevenLabs
text-to-speech in one take, so the read keeps one consistent delivery. Words the voice tends to
misread can be respelled for the read only, in the episode's production/pronunciation.json
({"Wau": "Vow"}); the script itself is never changed.

Credentials stay local: ELEVENLABS_API_KEY is read from the environment, loaded here from the
repo's git-ignored .env.local. Nothing prints or stores the key.

The take is written to production/vo/<slug>-vo.mp3 (git-ignored) with a vo.json receipt holding a
fingerprint of text + voice + model + settings and the hash of the audio itself. A take is only
published after it decodes, and one run per episode records at a time. Running again with nothing
changed reuses the take and spends no characters; --force records a new one.

Usage:
    tools/voiceover.py umbra ep03-ghost-characters --dry-run    # what would be sent, no request
    tools/voiceover.py umbra ep03-ghost-characters              # record with Brian
    tools/voiceover.py umbra ep03-ghost-characters --speed 1.05 --force
Then:
    tools/assemble-episode.py umbra ep03-ghost-characters --vo channels/umbra/episodes/<slug>/production/vo/<slug>-vo.mp3
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env.local"
API = "https://api.elevenlabs.io/v1"
DEFAULT_VOICE = "Brian"
BRIAN_PREMADE_ID = "nPczCjzI2devNBz1zQrb"  # ElevenLabs' premade "Brian" (deep, measured narrator)
DEFAULT_MODEL = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"
WORDS_PER_SECOND = 2.5  # the channel pace
MAX_AUDIO_BYTES = 50 * 1024 * 1024  # a 5-minute 128 kbps take is ~5 MB


def load_tool(name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def spoken_text(script: str, pronunciation: dict[str, str]) -> str:
    """Apply whole-word respellings, longest first so 'USD 70000' wins over a rule for 'USD'."""
    for written in sorted(pronunciation, key=len, reverse=True):
        script = re.sub(rf"(?<!\w){re.escape(written)}(?!\w)", pronunciation[written], script)
    return script


def load_env() -> None:
    """Load the git-ignored .env.local into the environment (values already set win)."""
    try:
        from dotenv import load_dotenv  # imported late so --dry-run works without it installed
    except ImportError:
        raise SystemExit("error: python-dotenv is missing; run `python -m pip install -r requirements.txt`")
    load_dotenv(ENV_FILE, override=False)


def voice_settings(args) -> dict:
    return {"stability": args.stability, "similarity_boost": args.similarity, "style": args.style,
            "use_speaker_boost": True, "speed": args.speed}


def fingerprint(text: str, voice_id: str, model: str, settings: dict) -> str:
    blob = json.dumps({"text": text, "voice_id": voice_id, "model": model, "settings": settings,
                       "format": OUTPUT_FORMAT}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def api_error(err: urllib.error.HTTPError) -> str:
    """One line from an ElevenLabs error body ({"detail": {"message": ...}} or {"detail": "..."})."""
    try:
        detail = json.loads(err.read().decode() or "{}").get("detail")
    except (ValueError, UnicodeDecodeError):
        detail = None
    if isinstance(detail, dict):
        detail = detail.get("message") or detail.get("status")
    return f"HTTP {err.code}" + (f": {detail}" if detail else "")


def request(path: str, key: str, body: dict | None = None):
    req = urllib.request.Request(f"{API}{path}", headers={"xi-api-key": key, "Accept": "application/json"},
                                 data=json.dumps(body).encode() if body is not None else None,
                                 method="POST" if body is not None else "GET")
    if body is not None:
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "audio/mpeg")
    try:
        return urllib.request.urlopen(req, timeout=300)
    except urllib.error.HTTPError as err:
        raise SystemExit(f"error: ElevenLabs {path.split('?')[0]} failed, {api_error(err)}")
    except urllib.error.URLError as err:
        raise SystemExit(f"error: could not reach ElevenLabs ({err.reason})")


def pick_voice(voices: list[dict], name: str) -> dict | None:
    """Exact name first ("Brian"), then a name that starts with it ("Brian - Deep narrator")."""
    wanted = name.strip().lower()
    for test in (lambda v: v == wanted, lambda v: v.startswith(wanted)):
        hits = [v for v in voices if test(v.get("name", "").strip().lower())]
        if hits:
            return hits[0]
    return None


def resolve_voice(key: str, name: str) -> tuple[str, str]:
    with request("/voices", key) as response:
        voices = json.loads(response.read()).get("voices", [])
    found = pick_voice(voices, name)
    if found:
        return found["voice_id"], found["name"]
    if name.lower() == "brian":
        return BRIAN_PREMADE_ID, "Brian (premade)"
    raise SystemExit(f"error: no voice named {name!r} in your ElevenLabs voices; pass --voice-id instead")


def characters_left(key: str) -> int | None:
    try:
        with request("/user/subscription", key) as response:
            sub = json.loads(response.read())
        return int(sub["character_limit"]) - int(sub["character_count"])
    except (SystemExit, KeyError, ValueError, TypeError):
        return None  # a key restricted to text-to-speech may not read the subscription; not fatal


def save_audio(response, directory: Path, stem: str) -> Path:
    """Stream the audio into a temp file of this run's own and return it, unpublished."""
    fd, tmp_name = tempfile.mkstemp(dir=directory, prefix=f".{stem}.", suffix=".mp3.part")
    tmp = Path(tmp_name)
    try:
        size = 0
        with open(fd, "wb") as out:
            while chunk := response.read(1 << 16):
                size += len(chunk)
                if size > MAX_AUDIO_BYTES:
                    raise SystemExit("error: ElevenLabs returned more audio than a 5-minute read; stopped")
                out.write(chunk)
        if size == 0:
            raise SystemExit("error: ElevenLabs returned no audio")
        return tmp
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def take_is_current(out: Path, receipt: dict, inputs: str) -> bool:
    """Reuse a take only when its receipt was written for these inputs *and* for this very file."""
    return (out.exists() and receipt.get("inputs_sha256") == inputs
            and receipt.get("audio_sha256") == file_sha256(out))


def lock_vo(vo_dir: Path):
    """One recording per episode at a time, held from the reuse check through publication."""
    handle = open(vo_dir / "vo.lock", "w")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        raise SystemExit("error: another voiceover run is already recording this episode. Nothing was sent.")
    return handle


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("episode")
    ap.add_argument("--voice", default=DEFAULT_VOICE, help="voice name in your ElevenLabs account (default: Brian)")
    ap.add_argument("--voice-id", help="exact ElevenLabs voice id (skips the name lookup)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"ElevenLabs model (default: {DEFAULT_MODEL})")
    ap.add_argument("--speed", type=float, default=1.0, help="0.7-1.2; raise it if the read runs past the cut")
    ap.add_argument("--stability", type=float, default=0.5)
    ap.add_argument("--similarity", type=float, default=0.75)
    ap.add_argument("--style", type=float, default=0.0)
    ap.add_argument("--force", action="store_true", help="record a new take even if one matches")
    ap.add_argument("--dry-run", action="store_true", help="show what would be sent; no request, no key needed")
    args = ap.parse_args(argv)
    if not 0.7 <= args.speed <= 1.2:
        ap.error("--speed must be between 0.7 and 1.2 (ElevenLabs' range)")

    assemble = load_tool("assemble-episode")
    ep = assemble.episode_dir(args.channel, args.episode)
    script = assemble.script_text((ep / "02-script.md").read_text())
    pron_path = ep / "production" / "pronunciation.json"
    pronunciation = json.loads(pron_path.read_text()) if pron_path.exists() else {}
    text = spoken_text(script, pronunciation)
    words = len(script.split())
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    cut_seconds = sum(int(sc["duration_s"]) for ch in shotlist["chapters"] for sc in ch["scenes"])
    print(f"{words} words, {len(text)} characters to read; the cut is {cut_seconds} s "
          f"(at the channel pace the read is ~{words / WORDS_PER_SECOND:.0f} s)")
    if pronunciation:
        print("respelled for the read: " + ", ".join(f"{k} -> {v}" for k, v in pronunciation.items()))
    if args.dry_run:
        print(f"dry run: would read with voice {args.voice_id or args.voice}, model {args.model}, "
              f"speed {args.speed}. Nothing was sent.")
        return 0

    load_env()
    key = os.getenv("ELEVENLABS_API_KEY")
    if not key:
        print("error: ELEVENLABS_API_KEY is not set. Add ELEVENLABS_API_KEY=<your key> to .env.local "
              "(git-ignored) and run again. Nothing was sent.", file=sys.stderr)
        return 2

    voice_id, voice_name = (args.voice_id, args.voice_id) if args.voice_id else resolve_voice(key, args.voice)
    settings = voice_settings(args)
    inputs = fingerprint(text, voice_id, args.model, settings)
    vo_dir = ep / "production" / "vo"
    vo_dir.mkdir(parents=True, exist_ok=True)
    out, receipt_path = vo_dir / f"{args.episode}-vo.mp3", vo_dir / "vo.json"
    with lock_vo(vo_dir):
        try:
            receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
        except ValueError:
            receipt = {}
        if not args.force and take_is_current(out, receipt, inputs):
            print(f"already recorded with {receipt.get('voice_name')}: {out.relative_to(ROOT)} (nothing spent)")
            return 0

        left = characters_left(key)
        if left is not None:
            print(f"ElevenLabs characters left this period: {left:,}")
            if left < len(text):
                print(f"error: this read needs {len(text):,} characters. Nothing was sent.", file=sys.stderr)
                return 2

        print(f"recording with {voice_name} ({args.model}, speed {args.speed})…")
        body = {"text": text, "model_id": args.model, "voice_settings": settings}
        with request(f"/text-to-speech/{voice_id}?output_format={OUTPUT_FORMAT}", key, body) as response:
            audio = save_audio(response, vo_dir, out.stem)
        fd, receipt_tmp = tempfile.mkstemp(dir=vo_dir, prefix=".vo.", suffix=".json.part")
        try:
            # The take must decode before either file is published, so a broken response is never kept.
            seconds = assemble.media_seconds(assemble.ffmpeg_binary(), audio)
            if seconds <= 0:
                raise SystemExit("error: ElevenLabs returned audio with no length; nothing was kept")
            with open(fd, "w") as f:
                f.write(json.dumps({"voice_id": voice_id, "voice_name": voice_name, "model": args.model,
                                    "settings": settings, "characters": len(text), "seconds": round(seconds, 2),
                                    "inputs_sha256": inputs, "audio_sha256": file_sha256(audio)}, indent=2) + "\n")
            audio.replace(out)
            Path(receipt_tmp).replace(receipt_path)
        finally:
            audio.unlink(missing_ok=True)
            Path(receipt_tmp).unlink(missing_ok=True)

    print(f"done: {out.relative_to(ROOT)} ({seconds:.1f} s, {out.stat().st_size / 1e6:.1f} MB)")
    if seconds > cut_seconds:
        print(f"note: the read is {seconds - cut_seconds:.1f} s longer than the {cut_seconds} s cut and would be "
              f"clipped; run again with --speed {min(1.2, round(args.speed * seconds / (cut_seconds - 3), 2))} --force")
    print(f"next: tools/assemble-episode.py {args.channel} {args.episode} --vo {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
