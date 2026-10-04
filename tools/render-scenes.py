#!/usr/bin/env python3
"""render-scenes.py — render storyboard scenes with the Higgsfield API (Seedance 2.5).

Reads an episode's production/shotlist.json and renders the chosen scenes as text-to-video
(the scene's IMAGE PROMPT + VIDEO PROMPT), then records each finished clip in
production/renders.json so a re-run skips what is already done.

Credentials stay local: the SDK reads HF_KEY ("key-id:key-secret") from the environment,
loaded here from the repo's git-ignored .env.local. Nothing prints or stores the key.

Each render is billable. Nothing is submitted without --scene, --chapter or --all, and
--all also needs --yes. Use --dry-run first to see exactly what would be sent.

Usage:
    tools/render-scenes.py umbra ep03-ghost-characters --scene ch01_s1          # the pilot
    tools/render-scenes.py umbra ep03-ghost-characters --chapter ch01 --dry-run
    tools/render-scenes.py umbra ep03-ghost-characters --all --yes
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = "bytedance/seedance-2.5/text-to-video"
MIN_DURATION_S = 4  # the model's shortest clip; shorter scenes are trimmed in the edit


def episode_dir(channel: str, slug: str) -> Path:
    path = (ROOT / "channels" / channel / "episodes" / slug).resolve()
    if ROOT / "channels" not in path.parents:
        raise SystemExit(f"error: {channel}/{slug} is outside channels/")
    return path


def select_scenes(shotlist: dict, scene_ids: list[str], chapter_ids: list[str], every: bool) -> list[dict]:
    chosen = []
    known = set()
    for chapter in shotlist["chapters"]:
        for scene in chapter["scenes"]:
            known.add(scene["id"])
            if every or scene["id"] in scene_ids or chapter["id"] in chapter_ids:
                chosen.append(scene)
    missing = [s for s in scene_ids if s not in known]
    if missing:
        raise SystemExit(f"error: unknown scene id(s): {', '.join(missing)}")
    chapters = {c["id"] for c in shotlist["chapters"]}
    missing = [c for c in chapter_ids if c not in chapters]
    if missing:
        raise SystemExit(f"error: unknown chapter id(s): {', '.join(missing)}")
    return chosen


def arguments_for(scene: dict, shotlist: dict, resolution: str) -> dict:
    image = " ".join(scene["image_prompt"].split()).rstrip(".")
    prompt = f"{image}. {' '.join(scene['video_prompt'].split())}"
    return {
        "prompt": prompt,
        "duration": max(MIN_DURATION_S, int(scene["duration_s"])),
        "resolution": resolution,
        "aspect_ratio": shotlist.get("aspect_ratio", "16:9"),
        "generate_audio": False,  # VO, SFX and music are laid in the edit
    }


def video_url(result: dict) -> str | None:
    video = result.get("video")
    if isinstance(video, dict):
        return video.get("url")
    if isinstance(video, str):
        return video
    videos = result.get("videos")
    if isinstance(videos, list) and videos and isinstance(videos[0], dict):
        return videos[0].get("url")
    return None


def render_one(sdk, scene_id: str, arguments: dict) -> tuple[str | None, str | None, str]:
    """Return (request_id, url, outcome); url is set only for a completed render with a video."""
    statuses = []
    request = {}

    def on_enqueue(request_id: str) -> None:
        request["id"] = request_id
        print(f"  {scene_id}: submitted {request_id}", flush=True)

    def on_queue_update(status) -> None:
        if not statuses or type(status) is not type(statuses[-1]):
            print(f"  {scene_id}: {type(status).__name__}", flush=True)
        statuses.append(status)

    try:
        result = sdk.subscribe(MODEL, arguments=arguments, on_enqueue=on_enqueue, on_queue_update=on_queue_update)
    except sdk.exceptions.CredentialsMissedError:
        raise SystemExit("error: Higgsfield credentials missing (HF_KEY). Nothing was submitted.")
    except sdk.exceptions.HiggsfieldClientError as exc:
        return request.get("id"), None, f"API error: {exc}"

    final = statuses[-1] if statuses else None
    if isinstance(final, sdk.Failed):
        return request.get("id"), None, "FAILED"
    if isinstance(final, sdk.NSFW):
        return request.get("id"), None, "MODERATED"
    if isinstance(final, sdk.Cancelled):
        return request.get("id"), None, "CANCELED"
    if not isinstance(final, sdk.Completed) or result.get("status") != "completed":
        return request.get("id"), None, f"unexpected state {type(final).__name__ if final else None}"
    url = video_url(result)
    if not url:
        return request.get("id"), None, "completed without a video URL"
    return request.get("id"), url, "completed"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("episode")
    ap.add_argument("--scene", action="append", default=[], help="scene id, e.g. ch01_s1 (repeatable)")
    ap.add_argument("--chapter", action="append", default=[], help="chapter id, e.g. ch01 (repeatable)")
    ap.add_argument("--all", action="store_true", help="every scene in the episode (needs --yes)")
    ap.add_argument("--yes", action="store_true", help="confirm a full-episode render")
    ap.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p"])
    ap.add_argument("--force", action="store_true", help="re-render scenes already in renders.json")
    ap.add_argument("--dry-run", action="store_true", help="print what would be sent; submit nothing")
    args = ap.parse_args(argv)

    if not (args.scene or args.chapter or args.all):
        ap.error("choose what to render: --scene, --chapter or --all")
    if args.all and not args.yes and not args.dry_run:
        ap.error("--all renders the whole episode (billable); add --yes to confirm, or --dry-run")

    ep = episode_dir(args.channel, args.episode)
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    renders_path = ep / "production" / "renders.json"
    renders = json.loads(renders_path.read_text()) if renders_path.exists() else {"model": MODEL, "scenes": {}}

    scenes = select_scenes(shotlist, args.scene, args.chapter, args.all)
    todo = [s for s in scenes if args.force or s["id"] not in renders["scenes"]]
    skipped = len(scenes) - len(todo)
    seconds = sum(max(MIN_DURATION_S, int(s["duration_s"])) for s in todo)
    print(f"{len(todo)} scene(s) to render, {seconds} s of video at {args.resolution}"
          + (f" ({skipped} already rendered, skipped)" if skipped else ""))

    if args.dry_run:
        for scene in todo:
            print(f"\n[{scene['id']}] {json.dumps(arguments_for(scene, shotlist, args.resolution), indent=2)}")
        return 0
    if not todo:
        return 0

    from dotenv import load_dotenv  # imported late so --dry-run works without the SDK installed

    load_dotenv(ROOT / ".env.local", override=False)
    if not (os.getenv("HF_KEY") or (os.getenv("HF_API_KEY") and os.getenv("HF_API_SECRET"))):
        print("error: HF_KEY is not set. Add HF_KEY=<key-id>:<key-secret> to .env.local "
              "(or set it as an environment variable). Nothing was submitted.", file=sys.stderr)
        return 2
    import higgsfield_client as sdk
    import higgsfield_client.exceptions  # noqa: F401  (makes sdk.exceptions available)

    failures = 0
    for scene in todo:
        request_id, url, outcome = render_one(sdk, scene["id"], arguments_for(scene, shotlist, args.resolution))
        if url:
            renders["scenes"][scene["id"]] = {"request_id": request_id, "video_url": url,
                                              "resolution": args.resolution}
            renders_path.write_text(json.dumps(renders, indent=2, ensure_ascii=False) + "\n")
            print(f"  {scene['id']}: {url}")
        else:
            failures += 1
            print(f"  {scene['id']}: NOT rendered ({outcome})", file=sys.stderr)

    done = len(todo) - failures
    print(f"done: {done} rendered, {failures} not rendered; results in {renders_path.relative_to(ROOT)}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
