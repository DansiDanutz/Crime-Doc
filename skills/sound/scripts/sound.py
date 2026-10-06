#!/usr/bin/env python3
"""sound.py — music and sound effects for any project (the `sound` Claude Code skill).

  music   ACE-Step 1.5, running locally (free, 10-600 s, instrumental or with lyrics).
          --engine elevenlabs uses the ElevenLabs Music API instead.
  sfx     ElevenLabs sound effects (0.5-22 s); ACE-Step makes music only.
  status  is ACE-Step installed / running, is an ElevenLabs key available
  server  start | stop the local ACE-Step API server (it starts by itself when needed)

Examples:
    sound.py music --prompt "dark ambient synth drone, slow, no drums" --seconds 60 --out bed.mp3
    sound.py music --prompt "upbeat indie pop, female vocal" --lyrics lyrics.txt --seconds 90 --out song.mp3
    sound.py sfx --prompt "heavy rubber stamp thud on paper" --seconds 1.5 --out stamp.mp3
    sound.py status

Configuration (environment variables, all optional):
    ACE_STEP_HOME   where ACE-Step-1.5 is installed (default ~/.local/share/ace-step/ACE-Step-1.5)
    ACE_STEP_URL    its API (default http://127.0.0.1:8001)
    ACESTEP_API_KEY its API key, if the server was started with one
    ELEVENLABS_API_KEY  for sfx / --engine elevenlabs. If unset it is read from a .env.local in the
                    current folder or a parent, or from ~/.config/sound-skill/env. Never printed.

Only the Python standard library is used, so it runs from any project without installing anything.
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ACE_HOME = Path(os.environ.get("ACE_STEP_HOME", Path.home() / ".local/share/ace-step/ACE-Step-1.5")).expanduser()
ACE_URL = os.environ.get("ACE_STEP_URL", "http://127.0.0.1:8001").rstrip("/")
STATE = Path.home() / ".cache" / "sound-skill"
ELEVEN = os.environ.get("ELEVENLABS_API_URL", "https://api.elevenlabs.io/v1").rstrip("/")
MAX_BYTES = 200 * 1024 * 1024
MUSIC_MIN_S, MUSIC_MAX_S = 10, 600
SFX_MIN_S, SFX_MAX_S = 0.5, 22


class SoundError(Exception):
    """A failure with a one-line reason, printed without a traceback."""


# ---------------------------------------------------------------- small HTTP helpers

def _call(url: str, body: dict | None = None, headers: dict | None = None, timeout: float = 60):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 method="POST" if body is not None else "GET",
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as err:
        try:
            detail = json.loads(err.read().decode() or "{}")
            detail = detail.get("detail") or detail.get("error") or detail
            if isinstance(detail, dict):
                detail = detail.get("message") or detail.get("status") or ""
        except (ValueError, UnicodeDecodeError):
            detail = ""
        raise SoundError(f"{url.split('?')[0]} returned HTTP {err.code}" + (f": {detail}" if detail else ""))
    except urllib.error.URLError as err:
        raise SoundError(f"could not reach {url.split('?')[0]} ({err.reason})")


def _json(url: str, body: dict | None = None, headers: dict | None = None, timeout: float = 60) -> dict:
    with _call(url, body, headers, timeout) as response:
        return json.loads(response.read() or b"{}")


def _save(response, dest: Path) -> int:
    """Stream to a temp file beside dest and publish it with an atomic rename."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=dest.parent, prefix=f".{dest.stem}.", suffix=dest.suffix + ".part")
    tmp = Path(tmp_name)
    try:
        size = 0
        with open(fd, "wb") as out:
            while chunk := response.read(1 << 16):
                size += len(chunk)
                if size > MAX_BYTES:
                    raise SoundError("the audio is larger than 200 MB; stopped")
                out.write(chunk)
        if size == 0:
            raise SoundError("the service returned no audio")
        tmp.replace(dest)
        return size
    finally:
        tmp.unlink(missing_ok=True)


# ---------------------------------------------------------------- ACE-Step (local music)

def _ace_headers() -> dict:
    key = os.environ.get("ACESTEP_API_KEY")
    return {"Authorization": f"Bearer {key}"} if key else {}


def ace_running() -> bool:
    try:
        with _call(f"{ACE_URL}/health", timeout=3) as response:
            return response.status == 200
    except SoundError:
        return False


def ace_installed() -> bool:
    return (ACE_HOME / "pyproject.toml").exists()


def server_start(wait_s: float = 900) -> None:
    """Start `uv run acestep-api` in the background and wait for /health. The first start
    downloads the model weights (several GB), so it can take a while."""
    if ace_running():
        return
    if not ace_installed():
        raise SoundError(f"ACE-Step is not installed at {ACE_HOME}; run the skill's install.sh")
    STATE.mkdir(parents=True, exist_ok=True)
    pid_file = STATE / "ace-step-api.pid"
    log = open(STATE / "ace-step-api.log", "ab")
    proc = subprocess.Popen(["uv", "run", "acestep-api"], cwd=ACE_HOME, stdout=log, stderr=log,
                            start_new_session=True)
    pid_file.write_text(str(proc.pid))
    print(f"starting ACE-Step (log: {STATE / 'ace-step-api.log'}); the first start downloads the models…",
          file=sys.stderr)
    deadline = time.time() + wait_s
    try:
        while time.time() < deadline:
            if proc.poll() is not None:
                raise SoundError(f"the ACE-Step server exited (code {proc.returncode}); see {STATE / 'ace-step-api.log'}")
            if ace_running():
                return
            time.sleep(3)
        raise SoundError(f"ACE-Step did not come up within {wait_s:.0f} s; see {STATE / 'ace-step-api.log'}")
    except BaseException:
        # A start that failed leaves nothing behind: no server, and no PID file that could later
        # point at an unrelated process.
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass
        pid_file.unlink(missing_ok=True)
        raise
    finally:
        log.close()


def _is_ace_server(pid: int) -> bool:
    """True only if `pid` is alive and its command line is the ACE-Step API server, so a stale or
    reused PID never gets signalled."""
    try:
        out = subprocess.run(["ps", "-o", "command=", "-p", str(pid)], capture_output=True, text=True).stdout
    except OSError:
        return False
    return "acestep-api" in out or "acestep.api_server" in out


def server_stop() -> bool:
    pid_file = STATE / "ace-step-api.pid"
    if not pid_file.exists():
        return False
    try:
        pid = int(pid_file.read_text().strip())
    except ValueError:
        pid = 0
    pid_file.unlink(missing_ok=True)
    if pid <= 1 or not _is_ace_server(pid):
        return False  # stale record: the server is gone and the PID may now belong to something else
    try:
        os.killpg(pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return False
    return True


def ace_music(prompt: str, seconds: float, dest: Path, lyrics: str = "", seed: int | None = None,
              steps: int = 8, timeout_s: float = 1800) -> dict:
    """Generate one piece with ACE-Step's task API: submit, poll, download. Returns its metadata."""
    server_start()
    body = {"prompt": prompt, "lyrics": lyrics or "[Instrumental]", "audio_duration": float(seconds),
            "audio_format": dest.suffix.lstrip(".") or "mp3", "batch_size": 1, "inference_steps": steps,
            "thinking": False}
    if seed is not None:
        body.update(seed=int(seed), use_random_seed=False)
    task = _json(f"{ACE_URL}/release_task", body, _ace_headers()).get("data") or {}
    task_id = task.get("task_id")
    if not task_id:
        raise SoundError("ACE-Step did not return a task id")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        rows = _json(f"{ACE_URL}/query_result", {"task_id_list": [task_id]}, _ace_headers()).get("data") or []
        row = next((r for r in rows if r.get("task_id") == task_id), None)
        if row and row.get("status") == 2:
            raise SoundError(f"ACE-Step failed the task: {str(row.get('result') or '')[:200]}")
        if row and row.get("status") == 1:
            results = row.get("result")
            results = json.loads(results) if isinstance(results, str) else (results or [])
            if not results or not results[0].get("file"):
                raise SoundError("ACE-Step finished without an audio file")
            meta = results[0]
            url = meta["file"] if meta["file"].startswith("http") else f"{ACE_URL}{meta['file']}"
            with _call(url, headers=_ace_headers(), timeout=300) as response:
                _save(response, dest)
            return {"engine": "ace-step", "seed": meta.get("seed_value"), "model": meta.get("dit_model"),
                    "metas": meta.get("metas")}
        time.sleep(2)
    raise SoundError(f"ACE-Step did not finish within {timeout_s:.0f} s")


# ---------------------------------------------------------------- ElevenLabs (effects, music fallback)

def eleven_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    candidates = [p / ".env.local" for p in [Path.cwd(), *Path.cwd().parents]]
    candidates.append(Path.home() / ".config" / "sound-skill" / "env")
    for path in candidates:
        if path.is_file():
            for line in path.read_text().splitlines():
                name, _, value = line.strip().partition("=")
                if name.strip() == "ELEVENLABS_API_KEY" and value.strip():
                    return value.strip().strip('"').strip("'")
    raise SoundError("no ElevenLabs key: set ELEVENLABS_API_KEY, or put it in .env.local or ~/.config/sound-skill/env")


def eleven_sfx(prompt: str, seconds: float, dest: Path, influence: float = 0.5) -> dict:
    body = {"text": prompt, "duration_seconds": float(seconds), "prompt_influence": influence}
    with _call(f"{ELEVEN}/sound-generation?output_format=mp3_44100_128", body,
               {"xi-api-key": eleven_key(), "Accept": "audio/mpeg"}, timeout=300) as response:
        _save(response, dest)
    return {"engine": "elevenlabs-sfx"}


def eleven_music(prompt: str, seconds: float, dest: Path) -> dict:
    body = {"prompt": prompt, "music_length_ms": int(round(seconds * 1000)), "model_id": "music_v1"}
    with _call(f"{ELEVEN}/music?output_format=mp3_44100_128", body,
               {"xi-api-key": eleven_key(), "Accept": "audio/mpeg"}, timeout=600) as response:
        _save(response, dest)
    return {"engine": "elevenlabs-music"}


def music(prompt: str, seconds: float, dest: Path, engine: str = "auto", lyrics: str = "",
          seed: int | None = None) -> dict:
    """auto: ACE-Step when it is installed or running (free, local), else ElevenLabs."""
    if not MUSIC_MIN_S <= seconds <= MUSIC_MAX_S:
        raise SoundError(f"music must be {MUSIC_MIN_S}-{MUSIC_MAX_S} s")
    if engine == "auto":
        engine = "ace-step" if (ace_running() or ace_installed()) else "elevenlabs"
    if engine == "ace-step":
        return ace_music(prompt, seconds, dest, lyrics=lyrics, seed=seed)
    if lyrics:
        raise SoundError("lyrics need ACE-Step (--engine ace-step)")
    if seconds > 300:
        raise SoundError("the ElevenLabs Music API makes at most 300 s; use ACE-Step for longer pieces")
    return eleven_music(prompt, seconds, dest)


def sfx(prompt: str, seconds: float, dest: Path) -> dict:
    if not SFX_MIN_S <= seconds <= SFX_MAX_S:
        raise SoundError(f"sound effects must be {SFX_MIN_S}-{SFX_MAX_S} s")
    return eleven_sfx(prompt, seconds, dest)


def status() -> dict:
    try:
        eleven_key()
        has_key = True
    except SoundError:
        has_key = False
    return {"ace_step_installed": ace_installed(), "ace_step_home": str(ACE_HOME),
            "ace_step_running": ace_running(), "ace_step_url": ACE_URL, "elevenlabs_key": has_key}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("music", help="generate music")
    m.add_argument("--prompt", required=True)
    m.add_argument("--seconds", type=float, required=True)
    m.add_argument("--out", type=Path, required=True)
    m.add_argument("--lyrics", type=Path, help="a lyrics file ([verse], [chorus] ...); omit for instrumental")
    m.add_argument("--seed", type=int)
    m.add_argument("--engine", choices=["auto", "ace-step", "elevenlabs"], default="auto")
    s = sub.add_parser("sfx", help="generate a sound effect (ElevenLabs)")
    s.add_argument("--prompt", required=True)
    s.add_argument("--seconds", type=float, required=True)
    s.add_argument("--out", type=Path, required=True)
    sub.add_parser("status", help="what is installed and reachable")
    srv = sub.add_parser("server", help="start or stop the local ACE-Step API")
    srv.add_argument("action", choices=["start", "stop"])
    args = ap.parse_args(argv)
    try:
        if args.cmd == "music":
            lyrics = args.lyrics.read_text() if args.lyrics else ""
            info = music(args.prompt, args.seconds, args.out, args.engine, lyrics, args.seed)
            print(json.dumps({"out": str(args.out), **info}))
        elif args.cmd == "sfx":
            print(json.dumps({"out": str(args.out), **sfx(args.prompt, args.seconds, args.out)}))
        elif args.cmd == "status":
            print(json.dumps(status(), indent=2))
        elif args.action == "start":
            server_start()
            print(f"ACE-Step is running at {ACE_URL}")
        else:
            print("stopped" if server_stop() else "no server started by this skill is running")
    except SoundError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
