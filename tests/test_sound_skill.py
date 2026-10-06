"""Tests for the `sound` skill client (skills/sound/scripts/sound.py) against fake local ACE-Step
and ElevenLabs servers, and for soundtrack.py using ACE-Step for music. No real service is called."""
import contextlib
import importlib.util
import io
import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sound = load(ROOT / "skills/sound/scripts/sound.py", "sound_skill_test")


class FakeServer:
    """A tiny HTTP server playing ACE-Step (/health, /release_task, /query_result, /v1/audio) and
    ElevenLabs (/sound-generation, /music). Records every request."""

    def __init__(self, fail_task=False, polls_before_done=1):
        self.requests, state = [], {"polls": 0}
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def reply(self, code, body, ctype="application/json"):
                data = body if isinstance(body, bytes) else json.dumps(body).encode()
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                outer.requests.append(("GET", self.path, None, dict(self.headers)))
                if self.path == "/health":
                    return self.reply(200, {"status": "ok"})
                if self.path.startswith("/v1/audio"):
                    return self.reply(200, b"ID3ace-audio", "audio/mpeg")
                self.reply(404, {"error": "nope"})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
                outer.requests.append(("POST", self.path, body, dict(self.headers)))
                if self.path == "/release_task":
                    return self.reply(200, {"data": {"task_id": "t1", "status": "queued"}, "code": 200})
                if self.path == "/query_result":
                    state["polls"] += 1
                    if state["polls"] <= polls_before_done:
                        return self.reply(200, {"data": [{"task_id": "t1", "status": 0}], "code": 200})
                    if fail_task:
                        return self.reply(200, {"data": [{"task_id": "t1", "status": 2, "result": "out of memory"}]})
                    result = json.dumps([{"file": "/v1/audio?path=%2Ftmp%2Fa.mp3", "seed_value": "7",
                                          "dit_model": "acestep-v15-turbo", "metas": {"bpm": 90}}])
                    return self.reply(200, {"data": [{"task_id": "t1", "status": 1, "result": result}], "code": 200})
                if self.path.startswith("/sound-generation") or self.path.startswith("/music"):
                    if self.headers.get("xi-api-key") != "test-key":
                        return self.reply(401, {"detail": {"message": "invalid key"}})
                    return self.reply(200, b"ID3eleven-audio", "audio/mpeg")
                self.reply(404, {"error": "nope"})

        self.httpd = HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_port}"

    def __enter__(self):
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc):
        self.httpd.shutdown()


class SkillClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        sleep = mock.patch.object(sound.time, "sleep")
        sleep.start()
        self.addCleanup(sleep.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_ace_step_music_submits_polls_and_downloads(self):
        with FakeServer() as srv, mock.patch.object(sound, "ACE_URL", srv.url), \
                mock.patch.dict(os.environ, {"ACESTEP_API_KEY": "ace-secret"}):
            out = self.dir / "bed.mp3"
            info = sound.ace_music("dark drone", 30, out)
            self.assertEqual(out.read_bytes(), b"ID3ace-audio")
            self.assertEqual((info["engine"], info["seed"], info["model"]), ("ace-step", "7", "acestep-v15-turbo"))
            task = next(b for m, p, b, h in srv.requests if p == "/release_task")
            self.assertEqual((task["prompt"], task["audio_duration"], task["batch_size"], task["lyrics"]),
                             ("dark drone", 30.0, 1, "[Instrumental]"))
            headers = next(h for m, p, b, h in srv.requests if p == "/release_task")
            self.assertEqual(headers.get("Authorization"), "Bearer ace-secret")
            self.assertEqual(sum(p == "/query_result" for m, p, b, h in srv.requests), 2)  # polled until done
            self.assertEqual(sorted(f.name for f in self.dir.iterdir()), ["bed.mp3"])  # no temp left

    def test_a_failed_ace_task_is_reported_and_nothing_is_written(self):
        with FakeServer(fail_task=True) as srv, mock.patch.object(sound, "ACE_URL", srv.url):
            with self.assertRaisesRegex(sound.SoundError, "failed the task: out of memory"):
                sound.ace_music("x", 30, self.dir / "x.mp3")
            self.assertEqual(list(self.dir.iterdir()), [])

    def test_sound_effects_go_to_elevenlabs_with_the_key_and_never_print_it(self):
        with FakeServer() as srv, mock.patch.object(sound, "ELEVEN", srv.url), \
                mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-key"}), \
                contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(sound.main(["sfx", "--prompt", "stamp thud", "--seconds", "1.5",
                                         "--out", str(self.dir / "s.mp3")]), 0)
        self.assertEqual((self.dir / "s.mp3").read_bytes(), b"ID3eleven-audio")
        body = next(b for m, p, b, h in srv.requests if p.startswith("/sound-generation"))
        self.assertEqual((body["text"], body["duration_seconds"]), ("stamp thud", 1.5))
        self.assertNotIn("test-key", out.getvalue() + err.getvalue())

    def test_the_key_is_found_in_a_project_env_file(self):
        (self.dir / "sub").mkdir()
        (self.dir / ".env.local").write_text('HF_KEY=x\nELEVENLABS_API_KEY="from-file"\n')
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(sound.Path, "cwd",
                                                                           return_value=self.dir / "sub"):
            self.assertEqual(sound.eleven_key(), "from-file")
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(sound.Path, "cwd", return_value=Path("/")), \
                mock.patch.object(sound.Path, "home", return_value=self.dir / "nohome"):
            with self.assertRaisesRegex(sound.SoundError, "no ElevenLabs key"):
                sound.eleven_key()

    def test_auto_engine_and_limits(self):
        with mock.patch.object(sound, "ace_running", return_value=False), \
                mock.patch.object(sound, "ace_installed", return_value=False), \
                mock.patch.object(sound, "eleven_music", return_value={"engine": "elevenlabs-music"}) as em:
            self.assertEqual(sound.music("x", 30, self.dir / "a.mp3")["engine"], "elevenlabs-music")
            em.assert_called_once()
            with self.assertRaisesRegex(sound.SoundError, "lyrics need ACE-Step"):
                sound.music("x", 30, self.dir / "a.mp3", lyrics="[verse] hi")
            with self.assertRaisesRegex(sound.SoundError, "at most 300 s"):
                sound.music("x", 400, self.dir / "a.mp3")
        with mock.patch.object(sound, "ace_installed", return_value=True), \
                mock.patch.object(sound, "ace_music", return_value={"engine": "ace-step"}) as am:
            self.assertEqual(sound.music("x", 400, self.dir / "a.mp3")["engine"], "ace-step")
            am.assert_called_once()
        for bad in (5, 700):
            with self.assertRaisesRegex(sound.SoundError, "10-600"):
                sound.music("x", bad, self.dir / "a.mp3")
        with self.assertRaisesRegex(sound.SoundError, "0.5-22"):
            sound.sfx("x", 30, self.dir / "a.mp3")

    def test_a_failed_start_leaves_no_pid_and_stop_never_signals_a_stranger(self):
        import subprocess, signal
        state = self.dir / "state"
        with mock.patch.object(sound, "STATE", state), mock.patch.object(sound, "ace_running", return_value=False), \
                mock.patch.object(sound, "ace_installed", return_value=True), \
                mock.patch.object(sound.subprocess, "Popen",
                                  return_value=mock.Mock(pid=999999, poll=mock.Mock(return_value=1), returncode=1)), \
                contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(sound.SoundError, "exited"):
                sound.server_start()
            self.assertFalse((state / "ace-step-api.pid").exists())
        # a stale PID file pointing at some other live process: stop must not signal it
        other = subprocess.Popen(["sleep", "30"], start_new_session=True)
        self.addCleanup(lambda: (other.poll() is None) and other.kill())
        state.mkdir(parents=True, exist_ok=True)
        (state / "ace-step-api.pid").write_text(str(other.pid))
        with mock.patch.object(sound, "STATE", state):
            self.assertFalse(sound.server_stop())
        self.assertIsNone(other.poll())  # still running
        self.assertFalse((state / "ace-step-api.pid").exists())
        with mock.patch.object(sound, "STATE", state), mock.patch.object(sound, "_is_ace_server", return_value=True), \
                mock.patch.object(sound.os, "killpg") as killpg:
            (state / "ace-step-api.pid").write_text("4242")
            self.assertTrue(sound.server_stop())
            killpg.assert_called_once_with(4242, signal.SIGTERM)

    def test_server_start_needs_an_install(self):
        with mock.patch.object(sound, "ace_running", return_value=False), \
                mock.patch.object(sound, "ace_installed", return_value=False):
            with self.assertRaisesRegex(sound.SoundError, "not installed"):
                sound.server_start()


class InstallerTests(unittest.TestCase):
    """install.sh with fake git/uv/curl on PATH: no piped downloads, a pinned and verified commit,
    and locked dependencies."""

    def run_install(self, head=None, with_uv=True, commit=None, dirty=False, existing=False):
        import subprocess
        d = Path(self.tmp.name)
        bin_dir, log = d / "bin", d / "calls.log"
        bin_dir.mkdir(exist_ok=True)
        pinned = commit or "ca1e85fe9430179831e6bc6be790c332190a3866"
        fake = {
            "git": f"""#!/bin/sh
echo "git $*" >> {log}
case "$*" in
  *"clone"*) eval last=\\${{$#}}; mkdir -p "$last/.git"; touch "$last/uv.lock";;
  *"rev-parse HEAD"*) echo "{head or pinned}";;
  *"status --porcelain"*) [ -n "$FAKE_DIRTY" ] && echo " M acestep/api_server.py";;
esac
exit 0
""",
            "curl": f"#!/bin/sh\necho \"curl $*\" >> {log}\nexit 0\n",
            "uv": f"#!/bin/sh\necho \"uv $*\" >> {log}\nexit 0\n",
        }
        for name, body in fake.items():
            if name == "uv" and not with_uv:
                continue
            (bin_dir / name).write_text(body)
            (bin_dir / name).chmod(0o755)
        if existing:
            (d / "ace" / ".git").mkdir(parents=True, exist_ok=True)
        env = {"PATH": f"{bin_dir}:/usr/bin:/bin", "HOME": str(d / "home"), "ACE_STEP_HOME": str(d / "ace"),
               **({"ACE_STEP_COMMIT": commit} if commit else {}), **({"FAKE_DIRTY": "1"} if dirty else {})}
        r = subprocess.run(["bash", str(ROOT / "skills/sound/install.sh")], env=env, capture_output=True, text=True)
        return r, (log.read_text() if log.exists() else "")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_installs_the_pinned_commit_with_locked_dependencies(self):
        r, calls = self.run_install()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("checkout --quiet ca1e85fe9430179831e6bc6be790c332190a3866", calls)
        self.assertNotIn("--force", calls)
        self.assertIn("uv sync --frozen", calls)
        self.assertNotIn("curl", calls)
        self.assertTrue((Path(self.tmp.name) / "home/.claude/skills/sound/scripts/sound.py").exists())

    def test_refuses_a_checkout_that_is_not_the_pinned_commit(self):
        r, calls = self.run_install(head="0" * 40)
        self.assertEqual(r.returncode, 2)
        self.assertIn("not the pinned commit", r.stderr)
        self.assertNotIn("uv sync", calls)

    def test_local_edits_in_an_existing_checkout_are_never_overwritten(self):
        r, calls = self.run_install(existing=True, dirty=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("has local changes", r.stderr)
        self.assertNotIn("checkout", calls)  # refused before anything was switched
        self.assertNotIn("fetch", calls)

    def test_without_uv_it_stops_and_never_downloads_an_installer(self):
        r, calls = self.run_install(with_uv=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("brew install uv", r.stderr)
        self.assertNotIn("curl", calls)

    def test_a_commit_must_be_a_full_hash(self):
        r, _ = self.run_install(commit="main")
        self.assertEqual(r.returncode, 2)
        self.assertIn("full 40-character", r.stderr)


class SoundtrackWithAceStepTests(unittest.TestCase):
    def test_music_is_made_locally_and_effects_still_go_to_elevenlabs(self):
        tool = load(ROOT / "tools/soundtrack.py", "soundtrack_ace_test")
        vo = load(ROOT / "tools/voiceover.py", "voiceover_ace_test")
        a = load(ROOT / "tools/assemble-episode.py", "assemble_ace_test")
        shot = {"chapters": [{"id": "ch01", "scenes": [{"duration_s": 10}]}]}
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            ep = root / "channels/c/episodes/e"
            (ep / "production").mkdir(parents=True)
            (ep / "production/shotlist.json").write_text(json.dumps(shot))
            (ep / "production/sound.json").write_text(json.dumps({
                "music": [{"from": "ch01", "to": "ch01", "prompt": "drone"}],
                "sfx": [{"chapter": "ch01", "at": 1, "dur": 1, "prompt": "click"}]}))
            made, sent = [], []
            fake_skill = mock.Mock(SoundError=Exception, ace_running=mock.Mock(return_value=True))
            fake_skill.ace_music.side_effect = lambda prompt, dur, dest: (made.append((prompt, dur)),
                                                                          Path(dest).write_bytes(b"ID3ace"))

            def fake_request(path, key, body=None):
                sent.append(path.split("?")[0])
                if path.startswith("/user"):
                    return contextlib.closing(io.BytesIO(b'{"character_limit": 100000, "character_count": 0}'))
                return contextlib.closing(io.BytesIO(b"ID3eleven"))

            with mock.patch.object(a, "ROOT", root), mock.patch.object(tool, "ROOT", root), \
                    mock.patch.object(tool, "sound_skill", return_value=fake_skill), \
                    mock.patch.object(tool, "load_tool",
                                      side_effect=lambda n: {"assemble-episode": a, "voiceover": vo}.get(n)
                                      or load(ROOT / "tools" / f"{n}.py", n)), \
                    mock.patch.object(a, "ffmpeg_binary", return_value="ffmpeg"), \
                    mock.patch.object(a, "media_seconds", side_effect=lambda f, p: 10.0 if ".e-" in p.name else 3.0), \
                    mock.patch.object(tool, "build_stem", side_effect=lambda f, c, t, dest: dest.write_bytes(b"stem")), \
                    mock.patch.object(vo, "request", side_effect=fake_request), mock.patch.object(vo, "load_env"), \
                    mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "k"}, clear=True), \
                    contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertIn("music engine: ace-step (local, free)", out.getvalue())
            self.assertEqual(made, [("drone", 10.0)])
            self.assertEqual([p for p in sent if not p.startswith("/user")], ["/sound-generation"])
            receipt = json.loads((ep / "production/sound/receipt.json").read_text())
            self.assertEqual(sorted(t["source"] for t in receipt["takes"].values()), ["ace-step", "sfx"])
            cue = tool.plan(json.loads((ep / "production/sound.json").read_text()), shot, None)[0]
            self.assertNotEqual(tool.take_key(cue, "ace-step"), tool.take_key(cue, "elevenlabs"))
            self.assertEqual(tool.take_key(cue, "elevenlabs"), tool.fingerprint(cue))  # existing takes stay valid


if __name__ == "__main__":
    unittest.main()
