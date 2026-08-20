#!/usr/bin/env python3
"""build-shotlist.py — generate production/shotlist.json from an episode's 04-scenes.md.

The markdown is the human-authored source of truth for the storyboard; this script mirrors
it into the machine-readable shotlist the generation pipeline consumes, so the two never
drift. The shotlist header (episode/channel/style_anchor/models/characters) and any existing
image_job_id / video_job_id values are preserved across regeneration.

Usage:
    tools/build-shotlist.py <channel> <episode-slug>
    tools/build-shotlist.py channels/umbra/episodes/ep01-the-man-who-said-no
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Scene "CHARACTERS IN SCENE" lines are resolved to ids using the EPISODE'S OWN manifest
# (shotlist.json `characters[]`) — no per-episode source edits. Each character matches on its
# `aliases` if present, else on the non-stopword tokens of its id (so `fbi_investigator`
# matches "FBI Investigator", `civilian` matches "Civilians"). Add an `aliases` list to a
# manifest character to cover names its id doesn't spell out (e.g. "System" for duty_officer).
STOPWORDS = {"the", "a", "an", "of", "and", "in", "on", "scene", "characters", "only",
             "recurring", "no", "none", "id", "character"}
# phrases that legitimately mean "no named cast in this scene" — never warn on these
_GENERIC_EMPTY = ("no recurring", "crowd only", "civilians / crowd", "no named", "none",
                  "anonymous")


def char_aliases(ch: dict) -> list[str]:
    if ch.get("aliases"):
        return [str(a).lower() for a in ch["aliases"]]
    toks = [t for t in re.split(r"[_\s]+", str(ch.get("id", "")).lower()) if t and t not in STOPWORDS]
    return toks or [str(ch.get("id", "")).lower()]


def resolve_characters(text: str, manifest: list[dict]) -> tuple[list[str], bool]:
    """Return (ids, unresolved) — unresolved is True when a real name matched nothing."""
    low = text.lower()
    found: list[str] = []
    for ch in manifest:
        cid = ch.get("id")
        if cid and cid not in found and any(a and a in low for a in char_aliases(ch)):
            found.append(cid)
    unresolved = (not found
                  and not any(g in low for g in _GENERIC_EMPTY)
                  and bool(re.search(r"[a-z]", low)))
    return found, unresolved


def parse_scenes_md(md: str) -> list[dict]:
    """Return a list of chapter dicts with nested scenes."""
    chapters: list[dict] = []
    chapter = None
    scene = None
    field = None  # 'image' | 'video' | None
    in_fence = False
    buf: list[str] = []

    chap_re = re.compile(r"^##\s+CHAPTER\s+(\d+)\s+[—-]\s+(.*?)\s*\(([^)]*)\)\s*$")
    scene_re = re.compile(r"^###\s+Scene\s+(\S+)\s+[—-]\s+(\d+)s")
    meta_re = re.compile(r"\*\*SFX:\*\*\s*(.*?)\s*·\s*\*\*Ambient:\*\*\s*(.*?)\s*·\s*\*\*Music:\*\*\s*(.*)")
    chars_re = re.compile(r"\*\*CHARACTERS IN SCENE:\*\*\s*(.*)")

    def close_field():
        nonlocal field, buf, scene
        if scene is not None and field in ("image", "video"):
            scene[f"{field}_prompt"] = "\n".join(buf).strip()
        field = None
        buf = []

    for raw in md.splitlines():
        line = raw.rstrip("\n")

        m = chap_re.match(line)
        if m:
            close_field()
            chapter = {
                "id": f"ch{int(m.group(1)):02d}",
                "title": m.group(2).strip(),
                "duration_s": 0,
                "sfx": "", "ambient": "", "music": "",
                "scenes": [],
            }
            chapters.append(chapter)
            scene = None
            continue

        if chapter is not None and not in_fence:
            mm = meta_re.search(line)
            if mm and not chapter["sfx"]:
                chapter["sfx"], chapter["ambient"], chapter["music"] = (
                    mm.group(1).strip(), mm.group(2).strip(), mm.group(3).strip())
                continue

        ms = scene_re.match(line)
        if ms:
            close_field()
            scene = {
                "id": ms.group(1),
                "duration_s": int(ms.group(2)),
                "characters": [],
                "characters_raw": "",
                "image_prompt": "", "video_prompt": "",
                "image_job_id": None, "video_job_id": None,
            }
            chapter["scenes"].append(scene)
            chapter["duration_s"] += scene["duration_s"]
            continue

        if scene is not None:
            mc = chars_re.search(line)
            if mc and not in_fence:
                scene["characters_raw"] = mc.group(1).strip()
                continue
            if not in_fence and "**IMAGE PROMPT:**" in line:
                close_field(); field = "image"; continue
            if not in_fence and "**VIDEO PROMPT:**" in line:
                close_field(); field = "video"; continue
            if line.strip().startswith("```"):
                if in_fence:
                    in_fence = False
                    close_field()
                elif field in ("image", "video"):
                    in_fence = True
                    buf = []
                continue
            if in_fence:
                buf.append(line)

    close_field()
    return chapters


def main() -> int:
    args = sys.argv[1:]
    if len(args) == 1:
        ep_dir = (ROOT / args[0]).resolve()
    elif len(args) == 2:
        ep_dir = (ROOT / "channels" / args[0] / "episodes" / args[1]).resolve()
    else:
        print(__doc__)
        return 1

    scenes_md = ep_dir / "04-scenes.md"
    shotlist_path = ep_dir / "production" / "shotlist.json"
    if not scenes_md.exists():
        print(f"error: {scenes_md} not found", file=sys.stderr)
        return 1

    # preserve the header + characters + any existing job ids
    header: dict = {}
    prior_jobs: dict[str, dict] = {}
    if shotlist_path.exists():
        old = json.loads(shotlist_path.read_text())
        for k in ("episode", "channel", "aspect_ratio", "style_anchor", "models", "characters"):
            if k in old:
                header[k] = old[k]
        for ch in old.get("chapters", []):
            for sc in ch.get("scenes", []):
                prior_jobs[sc["id"]] = {
                    "image_job_id": sc.get("image_job_id"),
                    "video_job_id": sc.get("video_job_id"),
                }

    manifest = header.get("characters", [])
    chapters = parse_scenes_md(scenes_md.read_text())
    unresolved: list[str] = []
    for ch in chapters:
        for sc in ch["scenes"]:
            ids, missing = resolve_characters(sc.pop("characters_raw", ""), manifest)
            sc["characters"] = ids
            if missing:
                unresolved.append(sc["id"])
            if sc["id"] in prior_jobs:
                sc["image_job_id"] = prior_jobs[sc["id"]]["image_job_id"]
                sc["video_job_id"] = prior_jobs[sc["id"]]["video_job_id"]

    out = {**header, "chapters": chapters}
    shotlist_path.parent.mkdir(parents=True, exist_ok=True)
    shotlist_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    n_scenes = sum(len(c["scenes"]) for c in chapters)
    print(f"wrote {shotlist_path.relative_to(ROOT)}: {len(chapters)} chapters, {n_scenes} scenes")
    if unresolved:
        print(f"warning: {len(unresolved)} scene(s) named a character absent from the manifest "
              f"characters[]; add it (or an alias) so the reference isn't dropped: "
              f"{', '.join(unresolved)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
