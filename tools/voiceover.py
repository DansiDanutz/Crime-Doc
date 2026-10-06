#!/usr/bin/env python3
"""voiceover.py — read an episode's script with an ElevenLabs voice (default: Brian).

A script whose narration carries <!-- chNN --> markers is recorded chapter by chapter: each
chapter is one take (sent with the lines around it, so the delivery stays continuous) and is
placed at the start of its own window in the cut. The finished track therefore runs the full
length of the picture and every line lands on its own shots. A take that runs a little long for
its window is tightened (up to 8%, pitch kept); one that would need more is reported so its line
can be shortened. A script without markers is read in one take from the top.

Words the voice tends to misread can be respelled for the read only, in the episode's
production/pronunciation.json ({"Wau": "Vow"}); the script itself is never changed.

Credentials stay local: ELEVENLABS_API_KEY is read from the environment, loaded here from the
repo's git-ignored .env.local. Nothing prints or stores the key.

Takes are kept in production/vo/takes/ and the track is production/vo/<slug>-vo.mp3 (all
git-ignored), with a vo.json receipt: per take a fingerprint of text + context + voice + model +
settings and the hash of the audio. A take is only kept after it decodes, one run per episode
records at a time, and a re-run only records the chapters whose words changed (--force: all).

Usage:
    tools/voiceover.py umbra ep03-ghost-characters --dry-run    # what would be sent, no request
    tools/voiceover.py umbra ep03-ghost-characters              # record with Brian, build the track
    tools/voiceover.py umbra ep03-ghost-characters --speed 0.95 --force
Then:
    tools/assemble-episode.py umbra ep03-ghost-characters        # picks the track up by itself
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
LEAD_S, TAIL_S = 0.35, 0.15  # breath before a chapter's first word / after its last
MAX_TEMPO = 1.08  # tighten a long take by at most 8%; past that, shorten the line


def load_tool(name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), Path(__file__).resolve().parent / f"{name}.py")
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


def fingerprint(text: str, voice_id: str, model: str, settings: dict,
                previous: str = "", following: str = "") -> str:
    blob = json.dumps({"text": text, "voice_id": voice_id, "model": model, "settings": settings,
                       "format": OUTPUT_FORMAT, "previous": previous, "next": following}, sort_keys=True)
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


def take_is_current(path: Path, entry: dict | None, inputs: str) -> bool:
    """Reuse a take only when its receipt entry was written for these inputs *and* this very file."""
    return bool(entry) and path.exists() and entry.get("inputs_sha256") == inputs \
        and entry.get("audio_sha256") == file_sha256(path)


def segment_plan(segments: list[tuple[str | None, str]], windows: dict, cut_seconds: float,
                 pronunciation: dict) -> list[dict]:
    """One entry per take: label, spoken text, its neighbours (for continuity) and its window."""
    marked = [chapter for chapter, _ in segments if chapter is not None]
    if marked and marked != list(windows):
        missing = [c for c in windows if c not in marked]
        extra = [c for c in marked if c not in windows]
        raise SystemExit("error: 02-script.md's <!-- chNN --> markers must name every storyboard chapter once, in "
                         f"order ({', '.join(windows)}); "
                         + "; ".join(x for x in (f"missing {', '.join(missing)}" if missing else "",
                                                 f"unknown {', '.join(extra)}" if extra else "",
                                                 "out of order" if not missing and not extra else "") if x)
                         + ". Nothing was sent.")
    spoken = [spoken_text(text, pronunciation) for _, text in segments]
    plan = []
    for i, (chapter, text) in enumerate(segments):
        if chapter is None:
            start, length, lead = 0.0, float(cut_seconds), 0.0
        elif chapter not in windows:
            raise SystemExit(f"error: the script has a <!-- {chapter} --> marker but the shotlist has no {chapter}")
        else:
            (start, length), lead = windows[chapter], LEAD_S
        plan.append({"label": chapter or "full", "words": len(text.split()), "text": spoken[i],
                     "previous": spoken[i - 1] if i else "", "next": spoken[i + 1] if i + 1 < len(spoken) else "",
                     "start": start, "window": length, "lead": lead})
    return plan


def fit(seconds: float, item: dict) -> float:
    """The tempo that makes a take fit its window (1.0 when it already fits)."""
    usable = item["window"] - item["lead"] - (TAIL_S if item["lead"] else 0.0)
    return max(1.0, seconds / usable)


def build_track(ffmpeg: str, items: list[dict], total: float, dest: Path) -> None:
    """Lay each take at its window start (tightened by its tempo), pad every window to length and
    join them: one mono track exactly as long as the cut."""
    inputs, chains = [], []
    for i, item in enumerate(items):
        inputs += ["-i", str(item["path"])]
        chains.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=mono,"
                      + (f"atempo={item['tempo']:.4f}," if item["tempo"] > 1.0 else "")
                      + f"adelay=delays={int(round(item['lead'] * 1000))}:all=1,apad,"
                      f"atrim=0:{item['window']:.3f},asetpts=N/SR/TB[a{i}]")
    graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(items))) \
        + f"concat=n={len(items)}:v=0:a=1[out]"
    result = subprocess.run([ffmpeg, "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]",
                             "-t", f"{total:.3f}", "-c:a", "libmp3lame", "-b:a", "192k", str(dest)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"error: building the voiceover track failed:\n{result.stderr[-1500:]}")


def write_json(path: Path, data: dict) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.stem}.", suffix=".json.part")
    try:
        with open(fd, "w") as f:
            f.write(json.dumps(data, indent=2) + "\n")
        Path(tmp).replace(path)
    finally:
        Path(tmp).unlink(missing_ok=True)


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
    cards = load_tool("cards")
    ep = assemble.episode_dir(args.channel, args.episode)
    script_md = (ep / "02-script.md").read_text()
    try:
        segments = assemble.narration_segments(script_md)
    except ValueError as err:
        raise SystemExit(f"error: 02-script.md: {err}")
    pron_path = ep / "production" / "pronunciation.json"
    pronunciation = json.loads(pron_path.read_text()) if pron_path.exists() else {}
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    windows = cards.chapter_windows(shotlist)
    cut_seconds = sum(length for _, length in windows.values())
    items = segment_plan(segments, windows, cut_seconds, pronunciation)
    words = sum(i["words"] for i in items)
    print(f"{words} words in {len(items)} take(s), {sum(len(i['text']) for i in items)} characters; "
          f"the cut is {cut_seconds:g} s")
    if pronunciation:
        print("respelled for the read: " + ", ".join(f"{k} -> {v}" for k, v in pronunciation.items()))
    if args.dry_run:
        for i in items:
            print(f"  {i['label']:>5}  {i['start']:6.1f} s  {i['words']:3d} words  ~{i['words'] / WORDS_PER_SECOND:4.1f} s "
                  f"of {i['window']:g} s")
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
    vo_dir = ep / "production" / "vo"
    takes_dir = vo_dir / "takes"
    takes_dir.mkdir(parents=True, exist_ok=True)
    out, receipt_path = vo_dir / f"{args.episode}-vo.mp3", vo_dir / "vo.json"
    ffmpeg = assemble.ffmpeg_binary()
    with lock_vo(vo_dir):
        try:
            receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
        except ValueError:
            receipt = {}
        taken = receipt.get("takes", {}) if isinstance(receipt.get("takes"), dict) else {}
        for item in items:
            item["inputs"] = fingerprint(item["text"], voice_id, args.model, settings, item["previous"], item["next"])
            item["path"] = takes_dir / f"{item['label']}-{item['inputs'][:12]}.mp3"
        todo = [i for i in items if args.force or not take_is_current(i["path"], taken.get(i["label"]), i["inputs"])]
        needed = sum(len(i["text"]) for i in todo)
        if todo:
            left = characters_left(key)
            if left is not None:
                print(f"ElevenLabs characters left this period: {left:,}")
                if left < needed:
                    print(f"error: {len(todo)} take(s) need {needed:,} characters. Nothing was sent.", file=sys.stderr)
                    return 2
            print(f"recording {len(todo)} of {len(items)} take(s) with {voice_name} "
                  f"({args.model}, speed {args.speed}, {needed:,} characters)…")
        else:
            print(f"all {len(items)} take(s) already recorded with {receipt.get('voice_name')} (nothing spent)")

        narration = assemble.narration_digest(script_md, pronunciation, shotlist)
        built = receipt.get("track") if isinstance(receipt.get("track"), dict) else {}
        if todo or built.get("takes") != [i["inputs"] for i in items] or built.get("narration_sha256") != narration:
            # This run changes the narration or its timing, and the quota check has passed: the old
            # track goes now, so a run that stops later can never leave obsolete narration behind.
            out.unlink(missing_ok=True)
            if receipt.pop("track", None) is not None:
                write_json(receipt_path, receipt)

        for item in todo:
            body = {"text": item["text"], "model_id": args.model, "voice_settings": settings}
            if item["previous"]:
                body["previous_text"] = item["previous"]
            if item["next"]:
                body["next_text"] = item["next"]
            with request(f"/text-to-speech/{voice_id}?output_format={OUTPUT_FORMAT}", key, body) as response:
                audio = save_audio(response, takes_dir, item["label"])
            try:
                # A take must decode before it is kept, so a broken response never reaches the track.
                seconds = assemble.media_seconds(ffmpeg, audio)
                if seconds <= 0:
                    raise SystemExit("error: ElevenLabs returned audio with no length; nothing was kept")
                digest = file_sha256(audio)
                audio.replace(item["path"])
            finally:
                audio.unlink(missing_ok=True)
            taken[item["label"]] = {"inputs_sha256": item["inputs"], "audio_sha256": digest,
                                    "seconds": round(seconds, 2), "characters": len(item["text"]),
                                    "file": item["path"].name}
            receipt = {"voice_id": voice_id, "voice_name": voice_name, "model": args.model,
                       "settings": settings, "takes": taken}
            write_json(receipt_path, receipt)  # after every take, so an interrupted run keeps what it paid for
            print(f"  {item['label']}: {seconds:.1f} s")

        too_long = []
        for item in items:
            item["seconds"] = float(taken[item["label"]]["seconds"])
            item["tempo"] = fit(item["seconds"], item)
            if item["tempo"] > MAX_TEMPO:
                too_long.append(item)
        print(" take   start  length  window  fit")
        for item in items:
            note = "" if item["tempo"] == 1.0 else f"tightened {100 * (item['tempo'] - 1):.0f}%"
            if item in too_long:
                note = "TOO LONG"
            print(f"  {item['label']:>5} {item['start']:6.1f} {item['seconds']:6.1f} s {item['window']:5.0f} s  {note}")
        if too_long:
            print(f"error: {', '.join(i['label'] for i in too_long)} run more than {100 * (MAX_TEMPO - 1):.0f}% past "
                  "their window. Shorten those lines in 02-script.md (or raise --speed) and run again; only "
                  "the changed chapters are recorded again.", file=sys.stderr)
            return 2

        fd, tmp_name = tempfile.mkstemp(dir=vo_dir, prefix=f".{out.stem}.", suffix=".mp3")
        os.close(fd)
        tmp = Path(tmp_name)
        try:
            build_track(ffmpeg, items, cut_seconds, tmp)
            length = assemble.media_seconds(ffmpeg, tmp)
            if abs(length - cut_seconds) > 0.5:
                raise SystemExit(f"error: the track came out {length:.1f} s for a {cut_seconds:g} s cut; not kept")
            tmp.replace(out)
        finally:
            tmp.unlink(missing_ok=True)
        receipt["track"] = {"audio_sha256": file_sha256(out), "seconds": round(length, 2),
                            "takes": [i["inputs"] for i in items],
                            "narration_sha256": narration}
        write_json(receipt_path, receipt)

    print(f"done: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} ({length:.1f} s, "
          f"{len(items)} take(s), narration ends at {items[-1]['start'] + items[-1]['lead'] + items[-1]['seconds'] / items[-1]['tempo']:.1f} s)")
    print(f"next: tools/assemble-episode.py {args.channel} {args.episode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
