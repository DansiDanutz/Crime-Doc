#!/usr/bin/env python3
"""assemble-episode.py — cut an episode's rendered clips into one rough-cut video.

Reads production/shotlist.json (scene order and durations) and production/renders.json (the
clip each scene rendered). A scene marked REUSE takes the clip of the scene it names. Every clip
is trimmed to its scene's planned duration, scaled to 1280x720 at 24 fps, and joined in order,
so the cut runs exactly as long as the storyboard (EP03: 5:00).

Every episode ends with the channel's fixed outro (channels/<name>/outro.json): an end card
appended after the storyboard, under the narrator's sign-off.

The cards of production/cards.json (date stamps, name tags, figures, questions; see
tools/cards.py) fade in over the picture; --no-cards leaves them out.

A voiceover is laid under the picture:
  (default)        the track tools/voiceover.py wrote to production/vo/<slug>-vo.mp3, if any
  --vo FILE        any audio file (your own read, a TTS export, ...)
  --scratch-vo     macOS only: speak the script with the built-in `say` voice at the channel's
                   2.5 words/s, as a free timing guide (not a final voice)

Nothing here calls a paid API. Clips are downloaded once into production/clips/ (git-ignored).

Usage:
    tools/assemble-episode.py umbra ep03-ghost-characters
    tools/assemble-episode.py umbra ep03-ghost-characters --scratch-vo
    tools/assemble-episode.py umbra ep03-ghost-characters --vo ~/Desktop/ep03-vo.wav
"""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIDTH, HEIGHT, FPS = 1280, 720, 24
WORDS_PER_MINUTE = 150  # the channel pace: 2.5 words per second
MAX_CLIP_BYTES = 200 * 1024 * 1024  # a 4-15 s 1080p preview is ~2-30 MB; anything far larger is not a clip
DURATION_TOLERANCE_S = 0.1


def load_tool(name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), Path(__file__).resolve().parent / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def episode_dir(channel: str, slug: str) -> Path:
    path = (ROOT / "channels" / channel / "episodes" / slug).resolve()
    if ROOT / "channels" not in path.parents:
        raise SystemExit(f"error: {channel}/{slug} is outside channels/")
    return path


def plan(shotlist: dict, renders: dict) -> tuple[list[dict], list[str]]:
    """Return (segments in order, scene ids with no clip). Each segment: id, source, url, seconds."""
    clips = renders.get("scenes", {})
    segments, missing = [], []
    for chapter in shotlist["chapters"]:
        for scene in chapter["scenes"]:
            source = scene.get("reuse") or scene["id"]
            entry = clips.get(source)
            if not entry or not entry.get("video_url"):
                missing.append(scene["id"] if source == scene["id"] else f"{scene['id']} (via {source})")
                continue
            segments.append({"id": scene["id"], "source": source, "url": entry["video_url"],
                             "seconds": int(scene["duration_s"])})
    return segments, missing


CHAPTER_MARK = re.compile(r"<!--\s*(ch\d+)\s*-->")


def script_body(script_md: str) -> str:
    parts = script_md.split("\n---\n")
    return parts[1] if len(parts) >= 3 else script_md


def script_text(script_md: str) -> str:
    """The narration of 02-script.md: the body between the first two --- rules, markers removed."""
    return " ".join(re.sub(r"<!--.*?-->", " ", script_body(script_md), flags=re.S).split())


def narration_segments(script_md: str) -> list[tuple[str | None, str]]:
    """[(chapter id, its narration)] from the script's <!-- chNN --> markers, or [(None, all of it)]
    for a script without markers."""
    pieces = CHAPTER_MARK.split(script_body(script_md))
    if len(pieces) == 1:
        return [(None, script_text(script_md))]
    if " ".join(pieces[0].split()):
        raise ValueError("narration before the first <!-- chNN --> marker")
    segments = [(pieces[i], " ".join(re.sub(r"<!--.*?-->", " ", pieces[i + 1], flags=re.S).split()))
                for i in range(1, len(pieces), 2)]
    ids = [c for c, _ in segments]
    if len(set(ids)) != len(ids):
        raise ValueError("a chapter marker appears twice")
    return segments


def chapter_windows(shotlist: dict) -> list[tuple[str, int, int]]:
    """[(chapter id, start s, length s)] in storyboard order."""
    windows, t = [], 0
    for chapter in shotlist["chapters"]:
        length = sum(int(sc["duration_s"]) for sc in chapter["scenes"])
        windows.append((chapter.get("id"), t, length))
        t += length
    return windows


OUTRO_MIN_S, OUTRO_MAX_S = 4, 20


def load_outro(ep: Path) -> dict | None:
    """The channel's fixed outro (channels/<name>/outro.json), played after every episode's story:
    {"seconds", "text" (read by the narrator), "card" (the end card)}. None if the channel has none."""
    path = ep.parent.parent / "outro.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    seconds, text, card = data.get("seconds"), " ".join(str(data.get("text") or "").split()), data.get("card")
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds) \
            or not OUTRO_MIN_S <= seconds <= OUTRO_MAX_S:
        raise ValueError(f"outro.json: seconds must be a number from {OUTRO_MIN_S} to {OUTRO_MAX_S}")
    if not text or len(text) > 400:
        raise ValueError("outro.json: text must be 1-400 characters")
    if not isinstance(card, dict) or card.get("kind") != "endcard" or not card.get("wordmark"):
        raise ValueError('outro.json: card must be {"kind": "endcard", "wordmark": ..., "lines": [...]}')
    return {"seconds": float(seconds), "text": text, "card": card}


def narration_digest(script_md: str, pronunciation: dict, shotlist: dict, outro: dict | None = None) -> str:
    """Fingerprint of what the voiceover should say and where: every chapter's words, the
    respellings, the chapter windows the takes are laid on, and the channel outro."""
    blob = json.dumps({"segments": narration_segments(script_md), "pronunciation": pronunciation,
                       "windows": chapter_windows(shotlist),
                       "outro": [outro["text"], outro["seconds"]] if outro else None}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def current_vo_track(ep: Path, slug: str) -> Path | None:
    """The voiceover.py track, if this episode has one; refuses a track that is not the one its
    receipt describes or was recorded for different words, so stale narration is never muxed."""
    vo_dir = ep / "production" / "vo"
    track, receipt_path = vo_dir / f"{slug}-vo.mp3", vo_dir / "vo.json"
    if not track.exists() and not receipt_path.exists():
        return None
    hint = (f"run tools/voiceover.py {ep.parent.parent.name} {slug} (only changed chapters are re-recorded), "
            "or pass --no-vo / --vo FILE")
    try:
        built = json.loads(receipt_path.read_text()).get("track") if receipt_path.exists() else None
    except ValueError:
        built = None
    if not track.exists() or not isinstance(built, dict):
        raise SystemExit(f"error: the voiceover track is missing or unfinished; {hint}")
    if built.get("audio_sha256") != file_sha256(track):
        raise SystemExit(f"error: {track.name} is not the track vo.json describes; {hint}")
    pron_path = ep / "production" / "pronunciation.json"
    pronunciation = json.loads(pron_path.read_text()) if pron_path.exists() else {}
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    if built.get("narration_sha256") != narration_digest((ep / "02-script.md").read_text(), pronunciation, shotlist,
                                                         load_outro(ep)):
        raise SystemExit(f"error: the script or the chapter timing changed since the voiceover track was built; {hint}")
    return track


def ffmpeg_binary() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg  # pip install imageio-ffmpeg (in requirements.txt)
    except ImportError:
        raise SystemExit("error: ffmpeg not found. Install it (brew install ffmpeg) or "
                         "`python -m pip install imageio-ffmpeg`.")
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"error: {' '.join(cmd[:3])} … failed:\n{result.stderr[-2000:]}")
    return result


def media_seconds(ffmpeg: str, path: Path) -> float:
    """Duration of a media file, read from ffmpeg's own header dump (no ffprobe needed)."""
    result = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path)], capture_output=True, text=True)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr)
    if not match:
        raise SystemExit(f"error: could not read the duration of {path.name}")
    h, m, sec = match.groups()
    return int(h) * 3600 + int(m) * 60 + float(sec)


def cache_path(clips_dir: Path, source: str, url: str) -> Path:
    """Cache key includes the URL, so a re-rendered scene (new video_url) is downloaded afresh."""
    return clips_dir / f"{source}-{hashlib.sha1(url.encode()).hexdigest()[:12]}.mp4"


def download(url: str, dest: Path, limit: int = MAX_CLIP_BYTES) -> None:
    """Fetch url into dest at most once. Each run streams into its own temp file and publishes it
    with an atomic rename, so overlapping runs never share or half-read a download."""
    if dest.exists() and dest.stat().st_size > 0:
        return
    fd, tmp_name = tempfile.mkstemp(dir=dest.parent, prefix=f".{dest.stem}.", suffix=".part")
    tmp = Path(tmp_name)
    try:
        with open(fd, "wb") as out, urllib.request.urlopen(url, timeout=120) as response:
            size = 0
            while chunk := response.read(1 << 20):
                size += len(chunk)
                if size > limit:
                    raise SystemExit(f"error: {dest.name} is over {limit // (1024 * 1024)} MB; "
                                     "that is not a preview clip, refusing to keep downloading")
                out.write(chunk)
        if size == 0:
            raise SystemExit(f"error: {url} returned an empty file")
        tmp.replace(dest)
    finally:
        tmp.unlink(missing_ok=True)


def concat_line(path: Path) -> str:
    """One entry of an ffmpeg concat list; a ' inside the quoted path is written as '\\''."""
    return "file '" + path.as_posix().replace("'", "'\\''") + "'\n"


def trim(ffmpeg: str, source: Path, seconds: int, part: Path) -> bool:
    """Cut source to exactly `seconds` of 1280x720/24 fps picture. A clip shorter than its scene is
    held on its last frame for the rest. Returns True when that hold was needed."""
    short = media_seconds(ffmpeg, source) + DURATION_TOLERANCE_S < seconds
    run([ffmpeg, "-y", "-v", "error", "-i", str(source), "-an",
         "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
                f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={FPS},setsar=1,"
                f"tpad=stop_mode=clone:stop_duration={seconds}",
         "-t", str(seconds), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
         "-pix_fmt", "yuv420p", str(part)])
    return short


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("episode")
    ap.add_argument("--vo", type=Path, help="voiceover audio to lay under the picture "
                    "(default: the voiceover.py track in production/vo/, if there is one)")
    ap.add_argument("--no-vo", action="store_true", help="picture only, even if a voiceover track exists")
    ap.add_argument("--no-cards", action="store_true", help="leave out the on-screen cards of production/cards.json")
    ap.add_argument("--scratch-vo", action="store_true", help="macOS: make a free `say` voiceover from the script")
    ap.add_argument("--voice", default="Daniel", help="macOS `say` voice for --scratch-vo (default: Daniel)")
    ap.add_argument("--out", type=Path, help="output file (default: production/output/<slug>-roughcut.mp4)")
    ap.add_argument("--allow-gaps", action="store_true", help="assemble even if some scenes have no clip yet")
    args = ap.parse_args(argv)
    if sum(map(bool, (args.vo, args.scratch_vo, args.no_vo))) > 1:
        ap.error("use only one of --vo, --scratch-vo and --no-vo")

    ep = episode_dir(args.channel, args.episode)
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    renders_path = ep / "production" / "renders.json"
    renders = json.loads(renders_path.read_text()) if renders_path.exists() else {}
    segments, missing = plan(shotlist, renders)
    total = sum(s["seconds"] for s in segments)
    print(f"{len(segments)} scene(s) with a clip, {total} s of picture"
          + (f"; {len(missing)} without a clip: {', '.join(missing[:12])}"
             + (f" … and {len(missing) - 12} more" if len(missing) > 12 else "") if missing else ""))
    if missing and not args.allow_gaps:
        print("error: render the missing scenes first (or pass --allow-gaps for a partial cut).",
              file=sys.stderr)
        return 2

    try:
        outro = None if missing else load_outro(ep)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    default_vo = None if (args.vo or args.scratch_vo or args.no_vo) else current_vo_track(ep, args.episode)
    cards_tool = load_tool("cards")
    try:
        cards = [] if args.no_cards else cards_tool.load(ep, shotlist)
    except ValueError as err:
        print(f"error: cards.json: {err}", file=sys.stderr)
        return 2
    if cards and missing:
        print("note: cards left out of a cut with gaps; their times follow the full storyboard")
        cards = []

    ffmpeg = ffmpeg_binary()
    clips_dir = ep / "production" / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    out = args.out or (ep / "production" / "output" / f"{args.episode}-roughcut.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)

    # Intermediates live in a directory of this run's own, so two runs never mix their files.
    with tempfile.TemporaryDirectory(dir=clips_dir, prefix=".assemble-") as work:
        parts_dir = Path(work)
        print("downloading and trimming clips…")
        held = []
        for seg in segments:
            source = cache_path(clips_dir, seg["source"], seg["url"])
            download(seg["url"], source)
            if trim(ffmpeg, source, seg["seconds"], parts_dir / f"{seg['id']}.mp4"):
                held.append(seg["id"])
        if held:
            print(f"note: {len(held)} clip(s) shorter than their scene, held on the last frame: {', '.join(held)}")

        concat_list = parts_dir / "concat.txt"
        concat_list.write_text("".join(concat_line(parts_dir / f"{s['id']}.mp4") for s in segments))
        picture = parts_dir / "picture.mp4"
        run([ffmpeg, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
             "-c", "copy", str(picture)])

        if cards:
            print(f"laying {len(cards)} card(s) over the picture…")
            card_files = cards_tool.render_all(cards, parts_dir)
            graph, label = cards_tool.overlay_filter(cards)
            inputs = []
            for card, path in zip(cards, card_files):
                inputs += ["-loop", "1", "-t", f"{card['end'] - card['start']:.3f}", "-i", str(path)]
            carded = parts_dir / "picture-cards.mp4"
            run([ffmpeg, "-y", "-v", "error", "-i", str(picture), *inputs, "-filter_complex", graph,
                 "-map", f"[{label}]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                 "-pix_fmt", "yuv420p", "-t", str(total), str(carded)])
            picture = carded

        if outro:
            print(f"adding the channel outro ({outro['seconds']:g} s end card)…")
            card_png = parts_dir / "endcard.png"
            cards_tool.render(outro["card"]).save(card_png)
            tail = parts_dir / "outro.mp4"
            run([ffmpeg, "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-t", f"{outro['seconds']:g}",
                 "-i", str(card_png), "-vf", "format=yuv420p,fade=in:st=0:d=0.6", "-r", str(FPS),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", str(tail)])
            joined_list = parts_dir / "with-outro.txt"
            joined_list.write_text(concat_line(picture) + concat_line(tail))
            joined = parts_dir / "picture-outro.mp4"
            run([ffmpeg, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(joined_list),
                 "-c", "copy", str(joined)])
            picture = joined
            total += outro["seconds"]

        vo = args.vo
        if not (vo or args.scratch_vo or args.no_vo):
            vo = default_vo
            if vo:
                print(f"voiceover: {vo.relative_to(ROOT) if vo.is_relative_to(ROOT) else vo}")
        if args.scratch_vo:
            if not shutil.which("say"):
                raise SystemExit("error: --scratch-vo needs macOS `say`; pass --vo with an audio file instead.")
            text_file = parts_dir / "script.txt"
            text_file.write_text(script_text((ep / "02-script.md").read_text()))
            vo = parts_dir / "scratch-vo.aiff"
            run(["say", "-v", args.voice, "-r", str(WORDS_PER_MINUTE), "-f", str(text_file), "-o", str(vo)])
            print(f"scratch voiceover written with macOS voice {args.voice}")

        staged = parts_dir / ("final" + out.suffix)
        if vo:
            run([ffmpeg, "-y", "-v", "error", "-i", str(picture), "-i", str(vo), "-map", "0:v", "-map", "1:a",
                 "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(total), str(staged)])
        else:
            shutil.copyfile(picture, staged)

        length = media_seconds(ffmpeg, staged)
        if abs(length - total) > 0.5:
            raise SystemExit(f"error: the cut runs {length:.2f} s but the storyboard is {total} s; not writing {out.name}")
        shutil.move(str(staged), out)  # same filesystem in the usual case, so the finished file appears at once
    print(f"done: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} ({length:.2f} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
