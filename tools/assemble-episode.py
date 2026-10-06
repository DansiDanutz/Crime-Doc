#!/usr/bin/env python3
"""assemble-episode.py — cut an episode's rendered clips into one rough-cut video.

Reads production/shotlist.json (scene order and durations) and production/renders.json (the
clip each scene rendered). A scene marked REUSE takes the clip of the scene it names. Every clip
is trimmed to its scene's planned duration, scaled to 1280x720 at 24 fps, and joined in order,
so the cut runs exactly as long as the storyboard (EP03: 5:00).

Optionally a voiceover is laid under the picture:
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
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIDTH, HEIGHT, FPS = 1280, 720, 24
WORDS_PER_MINUTE = 150  # the channel pace: 2.5 words per second


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


def script_text(script_md: str) -> str:
    """The narration of 02-script.md: the body between the first two --- rules."""
    parts = script_md.split("\n---\n")
    body = parts[1] if len(parts) >= 3 else script_md
    return " ".join(body.split())


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


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"error: {' '.join(cmd[:3])} … failed:\n{result.stderr[-2000:]}")


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    tmp = dest.with_suffix(".part")
    with urllib.request.urlopen(url, timeout=120) as response, open(tmp, "wb") as out:
        shutil.copyfileobj(response, out)
    tmp.replace(dest)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("episode")
    ap.add_argument("--vo", type=Path, help="voiceover audio to lay under the picture")
    ap.add_argument("--scratch-vo", action="store_true", help="macOS: make a free `say` voiceover from the script")
    ap.add_argument("--voice", default="Daniel", help="macOS `say` voice for --scratch-vo (default: Daniel)")
    ap.add_argument("--out", type=Path, help="output file (default: production/output/<slug>-roughcut.mp4)")
    ap.add_argument("--allow-gaps", action="store_true", help="assemble even if some scenes have no clip yet")
    args = ap.parse_args(argv)
    if args.vo and args.scratch_vo:
        ap.error("use --vo or --scratch-vo, not both")

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

    ffmpeg = ffmpeg_binary()
    clips_dir = ep / "production" / "clips"
    parts_dir = clips_dir / "trimmed"
    parts_dir.mkdir(parents=True, exist_ok=True)

    print("downloading and trimming clips…")
    for seg in segments:
        source = clips_dir / f"{seg['source']}.mp4"
        download(seg["url"], source)
        part = parts_dir / f"{seg['id']}.mp4"
        run([ffmpeg, "-y", "-v", "error", "-i", str(source), "-t", str(seg["seconds"]), "-an",
             "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
                    f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={FPS},setsar=1",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", str(part)])

    concat_list = parts_dir / "concat.txt"
    concat_list.write_text("".join(f"file '{(parts_dir / (s['id'] + '.mp4')).as_posix()}'\n" for s in segments))
    out = args.out or (ep / "production" / "output" / f"{args.episode}-roughcut.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    picture = parts_dir / "picture.mp4"
    run([ffmpeg, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
         "-c", "copy", str(picture)])

    vo = args.vo
    if args.scratch_vo:
        if not shutil.which("say"):
            raise SystemExit("error: --scratch-vo needs macOS `say`; pass --vo with an audio file instead.")
        text_file = parts_dir / "script.txt"
        text_file.write_text(script_text((ep / "02-script.md").read_text()))
        vo = parts_dir / "scratch-vo.aiff"
        run(["say", "-v", args.voice, "-r", str(WORDS_PER_MINUTE), "-f", str(text_file), "-o", str(vo)])
        print(f"scratch voiceover written with macOS voice {args.voice}")

    if vo:
        run([ffmpeg, "-y", "-v", "error", "-i", str(picture), "-i", str(vo), "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(total), str(out)])
    else:
        shutil.copyfile(picture, out)
    print(f"done: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} ({total} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
