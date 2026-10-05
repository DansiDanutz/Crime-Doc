#!/usr/bin/env python3
"""render-scenes.py — render PREVIEW clips of storyboard scenes with the Higgsfield API.

Renders the chosen scenes from an episode's production/shotlist.json as Seedance 2.5
text-to-video (the scene's IMAGE PROMPT + VIDEO PROMPT) and records them in
production/renders.json.

These are previews, not production shots: the API's documented Seedance 2.5 endpoint takes a
text prompt only, so the clips are not anchored to the locked cast elements or a keyframe.
Production shots still go through the reference-element path in docs/PRODUCTION_PIPELINE.md,
which is what fills `image_job_id` / `video_job_id` in the shotlist; this tool never writes them.

Credentials stay local: the SDK reads HF_KEY ("key-id:key-secret") from the environment,
loaded here from the repo's git-ignored .env.local. Nothing prints or stores the key.

Billing guards:
  * nothing is submitted without --scene, --chapter or --all;
  * more than one scene in a run, or re-rendering a scene that already has a clip, needs --yes;
    --dry-run shows exactly what would be sent;
  * a job's request id is saved the moment it is queued, so an interrupted run picks that job
    back up next time instead of paying for it again;
  * a scene is skipped only while its render inputs are unchanged; edited scenes re-render;
  * the first API error (e.g. no credits left), or 2 failed jobs in a row, stops the batch;
  * --max-new N refuses the whole run when it would need more than N new renders (a budget cap);
  * a scene marked REUSE in 04-scenes.md is never rendered: the edit uses the named earlier clip;
  * one render run per episode at a time (a lock file), and the ledger is replaced atomically.

Usage:
    tools/render-scenes.py umbra ep03-ghost-characters --scene ch01_s1          # the pilot
    tools/render-scenes.py umbra ep03-ghost-characters --chapter ch01 --dry-run
    tools/render-scenes.py umbra ep03-ghost-characters --chapter ch01 --yes
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = "bytedance/seedance-2.5/text-to-video"
MIN_DURATION_S = 4  # the model's shortest clip; shorter scenes are trimmed in the edit
MAX_FAILED_IN_A_ROW = 2  # consecutive failed jobs almost always mean an account problem
KIND = ("preview: prompt-only text-to-video, not anchored to the locked cast or a keyframe; "
        "production shots come from the reference-element path in docs/PRODUCTION_PIPELINE.md")


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


def fingerprint(arguments: dict) -> str:
    """Identifies the exact request: a scene is up to date only while this is unchanged."""
    blob = json.dumps({"model": MODEL, "arguments": arguments}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()


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


def failure_reason(result) -> str:
    """The reason Higgsfield gives for a failed job, when the response carries one."""
    if not isinstance(result, dict):
        return ""
    for key in ("error", "message", "detail", "reason", "failure_reason", "error_message"):
        value = result.get(key)
        if isinstance(value, dict):
            value = value.get("message") or value.get("detail") or json.dumps(value, ensure_ascii=False)
        if value:
            return " ".join(str(value).split())[:200]
    return ""


def classify(sdk, final, result: dict) -> tuple[str | None, str]:
    """Return (url, outcome); url is set only for a completed render that has a video."""
    if isinstance(final, sdk.Failed):
        reason = failure_reason(result)
        return None, f"FAILED: {reason}" if reason else "FAILED (Higgsfield gave no reason)"
    if isinstance(final, sdk.NSFW):
        return None, "MODERATED"
    if isinstance(final, sdk.Cancelled):
        return None, "CANCELED"
    if not isinstance(final, sdk.Completed) or result.get("status") != "completed":
        return None, f"unexpected state {type(final).__name__ if final else None}"
    url = video_url(result)
    if not url:
        return None, "completed without a video URL"
    return url, "completed"


class Ledger:
    """production/renders.json, written after every change so an interruption loses nothing."""

    def __init__(self, path: Path):
        self.path = path
        data = json.loads(path.read_text()) if path.exists() else {}
        self.data = {"kind": KIND, "model": MODEL, "scenes": data.get("scenes", {}),
                     "pending": data.get("pending", {})}

    def save(self) -> None:
        # Write a complete temporary file, then swap it in: an interruption never leaves half a ledger.
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, prefix=".renders.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as handle:
                handle.write(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, self.path)
        except BaseException:
            Path(tmp).unlink(missing_ok=True)
            raise

    def done(self, scene_id: str, inputs: str) -> bool:
        entry = self.data["scenes"].get(scene_id)
        if not entry:
            return False
        # Clips recorded before fingerprints existed carry none: keep them rather than pay to
        # render them again (re-render one deliberately with --force).
        return entry.get("inputs_sha256", inputs) == inputs

    def pending(self, scene_id: str, inputs: str) -> str | None:
        entry = self.data["pending"].get(scene_id)
        return entry["request_id"] if entry and entry.get("inputs_sha256") == inputs else None

    def mark_pending(self, scene_id: str, request_id: str, inputs: str) -> None:
        self.data["pending"][scene_id] = {"request_id": request_id, "inputs_sha256": inputs}
        self.save()

    def finish(self, scene_id: str, request_id: str | None, url: str | None, inputs: str, resolution: str) -> None:
        self.data["pending"].pop(scene_id, None)
        if url:
            self.data["scenes"][scene_id] = {"request_id": request_id, "video_url": url,
                                             "resolution": resolution, "inputs_sha256": inputs}
        self.save()


class StopBatch(Exception):
    pass


def brief(exc: Exception, limit: int = 200) -> str:
    """One readable line for an API error: a gateway's HTML error page becomes its <title>."""
    text = str(exc)
    match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    if match:
        text = match.group(1)
    elif "<html" in text.lower():
        text = re.sub(r"<[^>]+>", " ", text)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def lock_episode(production: Path):
    """Hold an exclusive lock for the whole run, so two runs never interleave ledger writes."""
    handle = open(production / "renders.lock", "w")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        raise SystemExit("error: another render run is already working on this episode. Nothing was submitted.")
    return handle


def render_one(sdk, ledger: Ledger, scene_id: str, arguments: dict, inputs: str) -> tuple[str | None, str]:
    statuses = []
    request = {}

    def on_enqueue(request_id: str) -> None:
        request["id"] = request_id
        ledger.mark_pending(scene_id, request_id, inputs)  # saved before any waiting
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
        queued = f"; job {request['id']} was queued and is resumed on the next run" if "id" in request else ""
        raise StopBatch(f"{scene_id}: API error: {brief(exc)}{queued}") from exc
    url, outcome = classify(sdk, statuses[-1] if statuses else None, result)
    ledger.finish(scene_id, request.get("id"), url, inputs, arguments["resolution"])
    return url, outcome


def resume_one(sdk, ledger: Ledger, scene_id: str, request_id: str, inputs: str, resolution: str) -> tuple[str | None, str]:
    """Wait on a job an earlier run queued but never recorded, instead of submitting it again."""
    print(f"  {scene_id}: resuming {request_id} from an earlier run", flush=True)
    try:
        result = sdk.result(request_id)  # waits until the job is done
        final = sdk.status(request_id)
    except sdk.exceptions.HiggsfieldClientError as exc:
        raise StopBatch(f"{scene_id}: API error while resuming {request_id}: {brief(exc)}; "
                        "it is resumed again on the next run") from exc
    url, outcome = classify(sdk, final, result)
    ledger.finish(scene_id, request_id, url, inputs, resolution)
    return url, outcome


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("episode")
    ap.add_argument("--scene", action="append", default=[], help="scene id, e.g. ch01_s1 (repeatable)")
    ap.add_argument("--chapter", action="append", default=[], help="chapter id, e.g. ch01 (repeatable)")
    ap.add_argument("--all", action="store_true", help="every scene in the episode")
    ap.add_argument("--yes", action="store_true", help="confirm a billable run of more than one scene")
    ap.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p"])
    ap.add_argument("--force", action="store_true", help="re-render scenes that are already up to date")
    ap.add_argument("--dry-run", action="store_true", help="print what would be sent; submit nothing")
    ap.add_argument("--max-new", type=int, default=None, metavar="N",
                    help="spending cap: refuse to submit anything if the run needs more than N new renders")
    args = ap.parse_args(argv)

    if not (args.scene or args.chapter or args.all):
        ap.error("choose what to render: --scene, --chapter or --all")

    ep = episode_dir(args.channel, args.episode)
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    lock = None if args.dry_run else lock_episode(ep / "production")
    try:
        return run(args, ep, shotlist)
    finally:
        if lock is not None:
            lock.close()  # releases the lock


def run(args, ep: Path, shotlist: dict) -> int:
    ledger = Ledger(ep / "production" / "renders.json")

    jobs = []
    reused = []
    for scene in select_scenes(shotlist, args.scene, args.chapter, args.all):
        arguments = arguments_for(scene, shotlist, args.resolution)
        if scene.get("reuse"):
            # The edit uses an earlier scene's clip here; nothing new to render or pay for. A job
            # queued before the scene was marked REUSE is already paid for, so still collect it.
            reused.append((scene["id"], scene["reuse"]))
            queued = ledger.data["pending"].get(scene["id"])
            if queued:
                jobs.append((scene, arguments, queued["inputs_sha256"]))
            continue
        inputs = fingerprint(arguments)
        # A queued job is always picked up, even when an older clip with the same inputs exists
        # (an interrupted --force re-render), so a paid replacement is never left behind.
        if args.force or ledger.pending(scene["id"], inputs) or not ledger.done(scene["id"], inputs):
            jobs.append((scene, arguments, inputs))
    resuming = [j for j in jobs if ledger.pending(j[0]["id"], j[2])]
    new = [j for j in jobs if not ledger.pending(j[0]["id"], j[2])]
    # Scenes that already have a clip: rendering them again pays a second time.
    replacing = [j[0]["id"] for j in new if j[0]["id"] in ledger.data["scenes"]]
    seconds = sum(a["duration"] for _, a, _ in new)
    print(f"{len(new)} new render(s), {seconds} s of video at {args.resolution}"
          + (f"; {len(resuming)} queued earlier, to be resumed" if resuming else "")
          + "  [previews: prompt-only, not cast-locked]")
    if reused:
        pairs = ", ".join(f"{sid} uses {src}" for sid, src in reused)
        print(f"  {len(reused)} scene(s) reuse an existing clip, not rendered: {pairs}")
        missing = sorted({src for _, src in reused if src not in ledger.data["scenes"]})
        if missing:
            print(f"  note: no clip yet for {', '.join(missing)}; render it before the edit")
    if replacing:
        why = "--force" if args.force else "their prompt or settings changed since they were rendered"
        print(f"  replaces existing clips ({why}): {', '.join(replacing)}")

    if args.dry_run:
        for scene, arguments, _ in new:
            print(f"\n[{scene['id']}] {json.dumps(arguments, indent=2)}")
        return 0
    if not jobs:
        return 0
    if args.max_new is not None and len(new) > args.max_new:
        print(f"error: {len(new)} new renders exceed --max-new {args.max_new}. Nothing was submitted.",
              file=sys.stderr)
        return 2
    if (len(new) > 1 or replacing) and not args.yes:
        what = f"{len(new)} billable render(s)" + (
            f", replacing {len(replacing)} existing clip(s)" if replacing else "")
        print(f"error: {what}; re-run with --yes to confirm "
              "(or --dry-run to see them). Nothing was submitted.", file=sys.stderr)
        return 2

    from dotenv import load_dotenv  # imported late so --dry-run works without the SDK installed

    load_dotenv(ROOT / ".env.local", override=False)
    if not (os.getenv("HF_KEY") or (os.getenv("HF_API_KEY") and os.getenv("HF_API_SECRET"))):
        print("error: HF_KEY is not set. Add HF_KEY=<key-id>:<key-secret> to .env.local "
              "(or set it as an environment variable). Nothing was submitted.", file=sys.stderr)
        return 2
    import higgsfield_client as sdk
    import higgsfield_client.exceptions  # noqa: F401  (makes sdk.exceptions available)

    # Collect jobs queued by an earlier run first: they are already paid for, so a stop on new
    # submissions below must never leave one of them uncollected.
    ordered = resuming + new
    rendered = failed = failed_in_a_row = 0
    try:
        for position, (scene, arguments, inputs) in enumerate(ordered):
            if scene.get("image_job_id"):
                print(f"  {scene['id']}: note: this scene has a keyframe; the preview does not use it")
            request_id = ledger.pending(scene["id"], inputs)
            if request_id:
                url, outcome = resume_one(sdk, ledger, scene["id"], request_id, inputs, arguments["resolution"])
            else:
                url, outcome = render_one(sdk, ledger, scene["id"], arguments, inputs)
            if url:
                rendered += 1
                failed_in_a_row = 0
                print(f"  {scene['id']}: {url}")
            else:
                failed += 1
                print(f"  {scene['id']}: NOT rendered ({outcome})", file=sys.stderr)
                if request_id:  # a resumed job: nothing new was submitted, so no stop
                    continue
                failed_in_a_row = failed_in_a_row + 1 if outcome.startswith("FAILED") else 0
                if failed_in_a_row == MAX_FAILED_IN_A_ROW and position + 1 < len(ordered):
                    raise StopBatch(
                        f"{MAX_FAILED_IN_A_ROW} renders failed in a row, which usually means an account "
                        "problem (credits, plan or rate limit) rather than the prompts. Check the reason "
                        f"above and your Higgsfield balance, then re-run: the {len(ordered) - position - 1} "
                        "remaining new scene(s) were not submitted, and rendered ones are skipped.")
    except StopBatch as stop:
        if not str(stop).startswith(f"{MAX_FAILED_IN_A_ROW} renders failed in a row"):
            failed += 1
        print(f"  {stop}\nstopped: no further scenes were submitted.", file=sys.stderr)

    print(f"done: {rendered} rendered, {failed} not rendered; "
          f"results in {ledger.path.relative_to(ROOT)}")
    return 0 if failed == 0 and rendered == len(jobs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
