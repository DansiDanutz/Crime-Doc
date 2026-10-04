#!/usr/bin/env python3
"""Higgsfield API example: Seedance 2.5 text-to-video via the official Python SDK.

Credentials stay server-side. The SDK reads HF_KEY ("key-id:key-secret") from the
environment; this script only loads it from .env.local (git-ignored) and never prints,
logs, or otherwise exposes its value.

Usage:
    pip install -r requirements.txt
    # put HF_KEY=<key-id>:<key-secret> in .env.local (see .env.example)
    python3 main.py

Exit status is 0 only when the request completed AND returned a video URL.
"""
import os
import sys
from pathlib import Path

import higgsfield_client
from dotenv import load_dotenv
from higgsfield_client import Cancelled, Completed, Failed, NSFW, Status
from higgsfield_client.exceptions import CredentialsMissedError, HiggsfieldClientError

MODEL = "bytedance/seedance-2.5/text-to-video"
ARGUMENTS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}

# A real environment variable (e.g. a cloud secret) wins over the file.
load_dotenv(Path(__file__).resolve().parent / ".env.local", override=False)


def _video_url(result: dict) -> str | None:
    """Pull the video URL out of a completed response ("video" field per the API reference)."""
    video = result.get("video")
    if isinstance(video, dict):
        return video.get("url")
    if isinstance(video, str):
        return video
    videos = result.get("videos")
    if isinstance(videos, list) and videos and isinstance(videos[0], dict):
        return videos[0].get("url")
    return None


def main() -> int:
    has_key = bool(os.getenv("HF_KEY")) or bool(os.getenv("HF_API_KEY") and os.getenv("HF_API_SECRET"))
    if not has_key:
        print("error: HF_KEY is not set. Add HF_KEY=<key-id>:<key-secret> to .env.local "
              "(or set it as an environment variable). Nothing was submitted.", file=sys.stderr)
        return 2

    last_status: list[Status] = []

    def on_enqueue(request_id: str) -> None:
        print(f"submitted: request_id={request_id}", flush=True)

    def on_queue_update(status: Status) -> None:
        if not last_status or type(status) is not type(last_status[-1]):
            print(f"status: {type(status).__name__}", flush=True)
        last_status.append(status)

    try:
        # subscribe() returns the final JSON for EVERY terminal state (completed, failed,
        # nsfw, canceled) without raising, so the terminal status is tracked explicitly.
        result = higgsfield_client.subscribe(
            MODEL, arguments=ARGUMENTS, on_enqueue=on_enqueue, on_queue_update=on_queue_update,
        )
    except CredentialsMissedError:
        print("error: Higgsfield credentials missing (HF_KEY). Nothing was submitted.", file=sys.stderr)
        return 2
    except HiggsfieldClientError as exc:
        print(f"error: Higgsfield API request failed: {exc}", file=sys.stderr)
        return 1

    final = last_status[-1] if last_status else None
    if isinstance(final, Failed):
        print(f"FAILED: generation failed. status={result.get('status')!r}", file=sys.stderr)
        return 1
    if isinstance(final, NSFW):
        print("MODERATED: the request was flagged by content moderation (nsfw); no video.", file=sys.stderr)
        return 1
    if isinstance(final, Cancelled):
        print("CANCELED: the request was canceled before processing; no video.", file=sys.stderr)
        return 1
    if not isinstance(final, Completed) or result.get("status") != "completed":
        print(f"error: unexpected terminal state {type(final).__name__ if final else None} / "
              f"{result.get('status')!r}; not treating as success.", file=sys.stderr)
        return 1

    url = _video_url(result)
    if not url:
        print(f"error: request completed but no video URL was returned (keys: {sorted(result)}).",
              file=sys.stderr)
        return 1

    print(f"video_url: {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
