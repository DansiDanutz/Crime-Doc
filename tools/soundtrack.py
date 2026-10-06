#!/usr/bin/env python3
"""soundtrack.py — record an episode's music and sound effects with ElevenLabs and build its stems.

The plan is the episode's production/sound.json:
  music  one bed per section of chapters ({"from": "ch01", "to": "ch02", "prompt", "gain_db"}),
         made locally and free with ACE-Step 1.5 when it is installed (the `sound` skill,
         skills/sound/), else with the ElevenLabs Music API; if the account cannot use that
         either, the section falls back to a seamless ambient loop from the sound-effects API
  sfx    one-shot effects ({"chapter", "at" (s into the chapter), "dur", "prompt", "gain_db"}),
         recorded with the ElevenLabs sound-effects API
The channel outro's sting (the "music" of channels/<name>/outro.json) is recorded once per channel,
in channels/<name>/sound/, and reused by every episode, so every ending sounds the same.

Two stems come out, each exactly as long as the cut: production/sound/<slug>-music.mp3 and
<slug>-sfx.mp3 (git-ignored). tools/assemble-episode.py mixes them under the narration, with the
music dipping automatically whenever the narrator speaks, and loudness-normalises the result.

Every recording is kept under a fingerprint of its kind, prompt and length, and is reused, so a
re-run only records what changed. A recording is only kept after it decodes. Credentials come
from ELEVENLABS_API_KEY in the git-ignored .env.local, as for voiceover.py.

Usage:
    tools/soundtrack.py umbra ep03-ghost-characters --dry-run   # the plan, no request
    tools/soundtrack.py umbra ep03-ghost-characters             # record what is missing, build stems
Then:
    tools/assemble-episode.py umbra ep03-ghost-characters       # mixes the stems in by itself
"""
import argparse
import fcntl
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FORMAT = "mp3_44100_128"
MUSIC_MODEL = "music_v1"
MUSIC_MIN_S, MUSIC_MAX_S = 4, 300  # a section or sting; shorter than the APIs' 10 s is requested at 10 s and trimmed
API_MUSIC_MIN_S = 10               # the Music API's and ACE-Step's minimum length
FALLBACK_HTTP = ("HTTP 401", "HTTP 402", "HTTP 403", "HTTP 404")  # no access to music, not a bad request
EST_CREDITS_PER_S = 40             # a conservative ElevenLabs estimate, used only to refuse runs that can't finish
SFX_MIN_S, SFX_MAX_S = 0.5, 22      # what the sound-effects API accepts
LOOP_S = 22                         # length of a fallback ambient loop
FADE_IN_S, FADE_OUT_S = 1.5, 2.5    # music section edges


def load_tool(name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), Path(__file__).resolve().parent / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _number(value, lo, hi, what):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not lo <= value <= hi:
        raise ValueError(f"{what} must be a number from {lo} to {hi}")
    return float(value)


def _prompt(value, what):
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= 450:
        raise ValueError(f"{what}: prompt must be 1-450 characters")
    return " ".join(value.split())


def plan(sound: dict, shotlist: dict, outro: dict | None) -> list[dict]:
    """Validate sound.json against the storyboard; return every cue with its absolute start.
    Raises ValueError naming the cue at fault."""
    cards = load_tool("cards")
    windows = cards.chapter_windows(shotlist)
    order = list(windows)
    story = sum(length for _, length in windows.values())
    if not isinstance(sound, dict):
        raise ValueError("sound.json must be an object with music and sfx lists")
    music, sfx = sound.get("music", []), sound.get("sfx", [])
    if not isinstance(music, list) or not isinstance(sfx, list):
        raise ValueError("sound.json: music and sfx must be lists")
    cues, spans = [], []
    for i, m in enumerate(music):
        what = f"music {i + 1}"
        if not isinstance(m, dict) or m.get("from") not in windows or m.get("to") not in windows:
            raise ValueError(f"{what}: from/to must name storyboard chapters")
        if order.index(m["to"]) < order.index(m["from"]):
            raise ValueError(f"{what}: 'to' comes before 'from'")
        start = windows[m["from"]][0]
        end = windows[m["to"]][0] + windows[m["to"]][1]
        dur = _number(end - start, MUSIC_MIN_S, MUSIC_MAX_S, f"{what}: its length")
        spans.append((start, end, what))
        cues.append({"kind": "music", "label": f"music-{m['from']}-{m['to']}", "prompt": _prompt(m.get("prompt"), what),
                     "start": start, "dur": dur, "gain_db": _number(m.get("gain_db", 0), -40, 6, f"{what}: gain_db")})
    spans.sort()
    for (a0, a1, an), (b0, b1, bn) in zip(spans, spans[1:]):
        if b0 < a1:
            raise ValueError(f"{an} and {bn} overlap")
    for j, s in enumerate(sfx):
        what = f"sfx {j + 1}"
        if not isinstance(s, dict) or s.get("chapter") not in windows:
            raise ValueError(f"{what}: chapter must name a storyboard chapter")
        start, length = windows[s["chapter"]]
        at = _number(s.get("at"), 0, length, f"{what}: at")
        dur = _number(s.get("dur"), SFX_MIN_S, SFX_MAX_S, f"{what}: dur")
        if at + dur > length + 1e-6:
            raise ValueError(f"{what}: runs past the end of {s['chapter']}")
        cues.append({"kind": "sfx", "label": f"sfx-{s['chapter']}-{j + 1:02d}", "prompt": _prompt(s.get("prompt"), what),
                     "start": start + at, "dur": dur, "gain_db": _number(s.get("gain_db", 0), -40, 6, f"{what}: gain_db")})
    if outro and outro.get("music"):
        cues.append({"kind": "music", "label": "outro", "channel": True, "prompt": outro["music"]["prompt"],
                     "start": float(story), "dur": _number(outro["seconds"], MUSIC_MIN_S, MUSIC_MAX_S, "the outro"),
                     "gain_db": outro["music"]["gain_db"]})
    return cues


def load_plan(ep: Path) -> tuple[list[dict], float] | None:
    """(cues, cut length) from the episode's sound.json, or None if the episode has none."""
    path = ep / "production" / "sound.json"
    if not path.exists():
        return None
    assemble = load_tool("assemble-episode")
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    outro = assemble.load_outro(ep)
    try:
        sound = json.loads(path.read_text())
    except ValueError as err:
        raise ValueError(f"sound.json: not valid JSON ({err})")
    cues = plan(sound, shotlist, outro)
    story = sum(sum(int(sc["duration_s"]) for sc in ch["scenes"]) for ch in shotlist["chapters"])
    return cues, story + (outro["seconds"] if outro else 0.0)


def fingerprint(cue: dict) -> str:
    """What decides the recording itself (not where it sits or how loud): kind, prompt, length."""
    blob = json.dumps({"kind": cue["kind"], "prompt": cue["prompt"], "dur": round(cue["dur"], 2),
                       "format": OUTPUT_FORMAT}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def take_key(cue: dict, engine: str) -> str:
    """Where a recording is kept: its fingerprint, plus the engine for ACE-Step music, so music from
    different engines never stands in for each other (ElevenLabs keys stay as they were)."""
    base = fingerprint(cue)
    if cue["kind"] == "music" and engine == "ace-step":
        return hashlib.sha256(f"{base}|ace-step".encode()).hexdigest()
    return base


def sound_skill():
    """The skill's own client (skills/sound/scripts/sound.py), loaded from this repo."""
    import importlib.util
    path = Path(__file__).resolve().parent.parent / "skills" / "sound" / "scripts" / "sound.py"
    spec = importlib.util.spec_from_file_location("sound_skill", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def music_engine(choice: str) -> str:
    if choice != "auto":
        return choice
    skill = sound_skill()
    return "ace-step" if (skill.ace_running() or skill.ace_installed()) else "elevenlabs"


def plan_digest(cues: list[dict], total: float) -> str:
    """What decides the stems: every cue's recording, place and level, and the cut length."""
    blob = json.dumps({"cues": [[fingerprint(c), round(c["start"], 3), c["gain_db"]] for c in cues],
                       "total": round(total, 3)}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


class Store:
    """A folder of recordings with a receipt: fingerprint -> audio hash, length and source."""

    def __init__(self, folder: Path):
        self.folder = folder
        self.takes = folder / "takes"
        self.receipt_path = folder / "receipt.json"

    def __enter__(self):
        self.takes.mkdir(parents=True, exist_ok=True)
        self.lock = open(self.folder / "sound.lock", "w")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock.close()
            raise SystemExit(f"error: another soundtrack run is using {self.folder}. Nothing was sent.")
        try:
            self.receipt = json.loads(self.receipt_path.read_text()) if self.receipt_path.exists() else {}
        except ValueError:
            self.receipt = {}
        if not isinstance(self.receipt.get("takes"), dict):
            self.receipt["takes"] = {}
        return self

    def __exit__(self, *exc):
        self.lock.close()

    engine = "elevenlabs"  # set per run: the music engine in use

    def key(self, cue: dict, variant: str = "") -> str:
        """variant "loop": a fallback ambient loop, kept apart so it never passes for the real music."""
        base = take_key(cue, self.engine)
        return hashlib.sha256(f"{base}|{variant}".encode()).hexdigest() if variant else base

    def path(self, cue: dict, variant: str = "") -> Path:
        return self.takes / f"{cue['kind']}-{self.key(cue, variant)[:16]}.mp3"

    def current(self, cue: dict, vo, variant: str = "") -> bool:
        entry = self.receipt["takes"].get(self.key(cue, variant))
        path = self.path(cue, variant)
        return bool(entry) and path.exists() and entry.get("audio_sha256") == vo.file_sha256(path)

    def best(self, cue: dict, vo) -> Path | None:
        """The take to lay: the real recording, else (music only) its fallback loop."""
        if self.current(cue, vo):
            return self.path(cue)
        if cue["kind"] == "music" and self.current(cue, vo, "loop"):
            return self.path(cue, "loop")
        return None

    def keep(self, cue: dict, vo, audio: Path, seconds: float, source: str, variant: str = "") -> None:
        digest = vo.file_sha256(audio)
        audio.replace(self.path(cue, variant))
        self.receipt["takes"][self.key(cue, variant)] = {"audio_sha256": digest, "seconds": round(seconds, 2),
                                                         "source": source, "prompt": cue["prompt"][:80]}
        vo.write_json(self.receipt_path, self.receipt)


def record(cue: dict, store: Store, key: str, vo, assemble, ffmpeg: str, state: dict) -> None:
    """Record one cue into the store. Music uses the Music API unless it is unavailable to this
    account, in which case (for this and every later section) a looped ambient effect stands in."""
    if cue["kind"] == "music" and store.engine == "ace-step":
        fd, tmp_name = tempfile.mkstemp(dir=store.takes, prefix=".ace.", suffix=".mp3")
        os.close(fd)
        audio = Path(tmp_name)
        try:
            skill = state.setdefault("skill", sound_skill())
            try:
                skill.ace_music(cue["prompt"], max(API_MUSIC_MIN_S, cue["dur"]), audio)
            except skill.SoundError as err:
                raise SystemExit(f"error: ACE-Step: {err}")
            seconds = assemble.media_seconds(ffmpeg, audio)  # must decode before it is kept
            if seconds <= 0:
                raise SystemExit("error: ACE-Step returned audio with no length; nothing was kept")
            store.keep(cue, vo, audio, seconds, "ace-step")
        finally:
            audio.unlink(missing_ok=True)
        print(f"  {cue['label']}: {seconds:.1f} s (ace-step, local)")
        return
    if cue["kind"] == "music" and not state.get("no_music_api"):
        body = {"prompt": cue["prompt"], "music_length_ms": int(round(max(API_MUSIC_MIN_S, cue["dur"]) * 1000)),
                "model_id": MUSIC_MODEL}
        try:
            response = vo.request(f"/music?output_format={OUTPUT_FORMAT}", key, body)
            source, variant = "music", ""
        except SystemExit as err:
            if not any(code in str(err) for code in FALLBACK_HTTP):
                raise  # a rejected prompt or request (400/422) is an error to fix, not a reason to substitute
            print(f"  note: the Music API is not available ({str(err).split('failed, ')[-1]}); "
                  "using looped ambient beds from the sound-effects API instead")
            state["no_music_api"] = True
            return record(cue, store, key, vo, assemble, ffmpeg, state)
    elif cue["kind"] == "music" and store.current(cue, vo, "loop"):
        print(f"  {cue['label']}: reusing its ambient loop (real music once the Music API is available)")
        return
    elif cue["kind"] == "music":
        body = {"text": f"seamless loopable ambient background bed, {cue['prompt']}"[:450],
                "duration_seconds": min(LOOP_S, cue["dur"]), "prompt_influence": 0.5}
        response = vo.request(f"/sound-generation?output_format={OUTPUT_FORMAT}", key, body)
        source, variant = "sfx-loop", "loop"
    else:
        body = {"text": cue["prompt"], "duration_seconds": cue["dur"], "prompt_influence": 0.5}
        response = vo.request(f"/sound-generation?output_format={OUTPUT_FORMAT}", key, body)
        source, variant = "sfx", ""
    with response as stream:
        audio = vo.save_audio(stream, store.takes, cue["kind"])
    try:
        seconds = assemble.media_seconds(ffmpeg, audio)  # must decode before it is kept
        if seconds <= 0:
            raise SystemExit("error: ElevenLabs returned audio with no length; nothing was kept")
        store.keep(cue, vo, audio, seconds, source, variant)
    finally:
        audio.unlink(missing_ok=True)
    print(f"  {cue['label']}: {seconds:.1f} s ({source})")


def build_stem(ffmpeg: str, cues: list[dict], total: float, dest: Path) -> None:
    """Lay every cue at its start (music looped to length and faded at its edges, effects with a
    short tail fade), at its gain, on one stereo stem exactly `total` seconds long."""
    if not cues:
        subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                        "-t", f"{total:.3f}", "-c:a", "libmp3lame", "-b:a", "192k", str(dest)], check=True)
        return
    inputs, chains = [], []
    for i, cue in enumerate(cues):
        if cue["kind"] == "music":
            inputs += ["-stream_loop", "-1"]  # a section longer than its recording loops it
        inputs += ["-i", str(cue["path"])]
        dur = cue["dur"]
        fades = (f"afade=t=in:d={min(FADE_IN_S, dur / 4):.3f},afade=t=out:st={max(0.0, dur - FADE_OUT_S):.3f}:d={min(FADE_OUT_S, dur):.3f}"
                 if cue["kind"] == "music" else f"afade=t=out:st={max(0.0, dur - 0.3):.3f}:d=0.3")
        chains.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo,atrim=0:{dur:.3f},asetpts=N/SR/TB,"
                      f"{fades},volume={cue['gain_db']}dB,adelay=delays={int(round(cue['start'] * 1000))}:all=1[a{i}]")
    graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(cues))) \
        + f"amix=inputs={len(cues)}:normalize=0:dropout_transition=0,apad,atrim=0:{total:.3f}[out]"
    result = subprocess.run([ffmpeg, "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]",
                             "-t", f"{total:.3f}", "-c:a", "libmp3lame", "-b:a", "192k", str(dest)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"error: building the {dest.name} stem failed:\n{result.stderr[-1500:]}")


def stem_paths(ep: Path, slug: str) -> tuple[Path, Path, Path]:
    folder = ep / "production" / "sound"
    return folder / f"{slug}-music.mp3", folder / f"{slug}-sfx.mp3", folder / "mix.json"


def current_stems(ep: Path, slug: str) -> tuple[Path, Path] | None:
    """The stems the assembler should mix, or None if the episode has no sound.json. Refuses stems
    that are missing or were built for another plan, so a stale soundtrack is never mixed in."""
    loaded = load_plan(ep)
    if loaded is None:
        return None
    cues, total = loaded
    music, sfx, mix = stem_paths(ep, slug)
    hint = (f"run tools/soundtrack.py {ep.parent.parent.name} {slug} (only new cues are recorded), "
            "or pass --no-sound")
    try:
        built = json.loads(mix.read_text()) if mix.exists() else None
    except ValueError:
        built = None
    vo = load_tool("voiceover")
    if not (music.exists() and sfx.exists() and isinstance(built, dict)):
        raise SystemExit(f"error: the soundtrack stems are missing or unfinished; {hint}")
    if built.get("music_sha256") != vo.file_sha256(music) or built.get("sfx_sha256") != vo.file_sha256(sfx):
        raise SystemExit(f"error: the soundtrack stems are not the ones mix.json describes; {hint}")
    if built.get("plan_sha256") != plan_digest(cues, total):
        raise SystemExit(f"error: sound.json, the outro or the chapter timing changed since the stems were built; {hint}")
    return music, sfx


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("episode")
    ap.add_argument("--dry-run", action="store_true", help="show the plan; no request, no key needed")
    ap.add_argument("--music-engine", choices=["auto", "ace-step", "elevenlabs"], default="auto",
                    help="auto (default): ACE-Step when installed (free, local), else ElevenLabs")
    args = ap.parse_args(argv)

    assemble, vo = load_tool("assemble-episode"), load_tool("voiceover")
    ep = assemble.episode_dir(args.channel, args.episode)
    try:
        loaded = load_plan(ep)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    if loaded is None:
        print("error: this episode has no production/sound.json", file=sys.stderr)
        return 2
    cues, total = loaded
    music_cues = [c for c in cues if c["kind"] == "music"]
    sfx_cues = [c for c in cues if c["kind"] == "sfx"]
    print(f"{len(music_cues)} music section(s) ({sum(c['dur'] for c in music_cues):.0f} s), "
          f"{len(sfx_cues)} sound effect(s) ({sum(c['dur'] for c in sfx_cues):.0f} s); the cut is {total:g} s")
    if args.dry_run:
        for c in cues:
            print(f"  {c['start']:6.1f} s  {c['dur']:5.1f} s  {c['gain_db']:+5.1f} dB  {c['label']:<16} {c['prompt'][:60]}")
        print("dry run: nothing was sent.")
        return 0

    engine = music_engine(args.music_engine)
    print(f"music engine: {engine}" + (" (local, free)" if engine == "ace-step" else ""))
    vo.load_env()
    key = os.getenv("ELEVENLABS_API_KEY")
    if not key:
        print("error: ELEVENLABS_API_KEY is not set. Add it to .env.local (git-ignored). Nothing was sent.",
              file=sys.stderr)
        return 2
    ffmpeg = assemble.ffmpeg_binary()
    state: dict = {}
    episode_store, channel_store = Store(ep / "production" / "sound"), Store(ep.parent.parent / "sound")
    episode_store.engine = channel_store.engine = engine
    with episode_store as es, channel_store as cs:
        todo = [c for c in cues if not (cs if c.get("channel") else es).current(c, vo)]
        if todo:
            # ACE-Step music is free; a music cue that already has a cached fallback loop can finish
            # on that loop at no cost (if the Music API is still unavailable, or out of credits), so
            # neither counts toward what the run must be able to pay for.
            paid = [c for c in todo if not (c["kind"] == "music" and (
                engine == "ace-step" or (cs if c.get("channel") else es).current(c, vo, "loop")))]
            estimate = int(sum(max(API_MUSIC_MIN_S, c["dur"]) if c["kind"] == "music" else c["dur"] for c in paid)
                           * EST_CREDITS_PER_S)
            left = vo.characters_left(key)
            if left is not None:
                print(f"ElevenLabs credits left this period: {left:,}; this run needs about {estimate:,} at most")
                if left < estimate:
                    print("error: not enough ElevenLabs credits to finish this run. Nothing was sent.", file=sys.stderr)
                    return 2
            print(f"recording {len(todo)} of {len(cues)} cue(s)…")
        else:
            print(f"all {len(cues)} cue(s) already recorded (nothing spent)")
        for cue in todo:
            record(cue, cs if cue.get("channel") else es, key, vo, assemble, ffmpeg, state)
        for cue in cues:
            cue["path"] = (cs if cue.get("channel") else es).best(cue, vo)
            if cue["path"] is None:
                raise SystemExit(f"error: {cue['label']} has no recording; run again")
        if todo:
            left = vo.characters_left(key)
            if left is not None:
                print(f"ElevenLabs credits left now: {left:,}")

        music, sfx, mix = stem_paths(ep, args.episode)
        built = {}
        for dest, group in ((music, music_cues), (sfx, sfx_cues)):
            fd, tmp_name = tempfile.mkstemp(dir=dest.parent, prefix=f".{dest.stem}.", suffix=".mp3")
            os.close(fd)
            tmp = Path(tmp_name)
            try:
                build_stem(ffmpeg, group, total, tmp)
                length = assemble.media_seconds(ffmpeg, tmp)
                if abs(length - total) > 0.5:
                    raise SystemExit(f"error: the {dest.name} stem came out {length:.1f} s for a {total:g} s cut")
                tmp.replace(dest)
            finally:
                tmp.unlink(missing_ok=True)
            built[f"{dest.stem.rsplit('-', 1)[-1]}_sha256"] = vo.file_sha256(dest)
        vo.write_json(mix, {**built, "plan_sha256": plan_digest(cues, total), "seconds": total})

    print(f"done: {music.relative_to(ROOT) if music.is_relative_to(ROOT) else music} and {sfx.name} ({total:g} s each)")
    print(f"next: tools/assemble-episode.py {args.channel} {args.episode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
