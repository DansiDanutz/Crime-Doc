"""Tests for tools/render-scenes.py: scene selection, billing guards and terminal states.

CI installs no third-party packages, so the Higgsfield SDK and python-dotenv are replaced with
minimal stand-ins (as in test_higgsfield_example.py); the decisions under test are the script's.
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SECRET = "test-key-id:test-key-secret-do-not-print"


def _fake_modules():
    sdk = types.ModuleType("higgsfield_client")

    class Status:
        pass

    for name in ["Queued", "InProgress", "Completed", "Failed", "NSFW", "Cancelled"]:
        setattr(sdk, name, type(name, (Status,), {}))
    exc = types.ModuleType("higgsfield_client.exceptions")
    exc.CredentialsMissedError = type("CredentialsMissedError", (Exception,), {})
    exc.HiggsfieldClientError = type("HiggsfieldClientError", (Exception,), {})
    sdk.exceptions = exc
    sdk.subscribe = None
    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda *a, **k: False
    return {"higgsfield_client": sdk, "higgsfield_client.exceptions": exc, "dotenv": dotenv}


class RenderScenesTests(unittest.TestCase):
    def setUp(self):
        self.modules = _fake_modules()
        patcher = mock.patch.dict(sys.modules, self.modules)
        patcher.start()
        self.addCleanup(patcher.stop)
        spec = importlib.util.spec_from_file_location("render_scenes", ROOT / "tools" / "render-scenes.py")
        self.tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.tool)
        self.sdk = self.modules["higgsfield_client"]

        # Work on a copy of a real episode so renders.json never lands in the repo.
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        src = ROOT / "channels" / "umbra" / "episodes" / "ep03-ghost-characters" / "production"
        dst = self.tmp / "channels" / "umbra" / "episodes" / "ep03-ghost-characters" / "production"
        dst.mkdir(parents=True)
        shutil.copy(src / "shotlist.json", dst / "shotlist.json")
        self.renders = dst / "renders.json"
        self.tool.ROOT = self.tmp
        self.calls = []

    def _subscribe(self, outcomes):
        def fake(model, arguments, on_enqueue=None, on_queue_update=None):
            statuses, result = outcomes[len(self.calls)]
            self.calls.append((model, arguments))
            on_enqueue(f"req-{len(self.calls)}")
            for name in statuses:
                on_queue_update(getattr(self.sdk, name)())
            if isinstance(result, Exception):
                raise result
            return result
        self.sdk.subscribe = fake

    def _run(self, *argv, env=None):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, env if env is not None else {"HF_KEY": SECRET}, clear=True):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    code = self.tool.main(["umbra", "ep03-ghost-characters", *argv])
                except SystemExit as exc:
                    code = exc.code
        return code, out.getvalue(), err.getvalue()

    def test_pilot_scene_renders_and_is_recorded(self):
        self._subscribe([(["Queued", "Completed"], {"status": "completed", "video": {"url": "https://cdn/v.mp4"}})])
        code, out, err = self._run("--scene", "ch01_s1")
        self.assertEqual(code, 0)
        model, arguments = self.calls[0]
        self.assertEqual(model, "bytedance/seedance-2.5/text-to-video")
        self.assertEqual(arguments["duration"], 4)  # a 3 s scene is rendered at the 4 s minimum
        self.assertEqual(arguments["aspect_ratio"], "16:9")
        self.assertFalse(arguments["generate_audio"])
        self.assertIn("matte red mannequin", arguments["prompt"])
        self.assertIn("16:9. Static wide", arguments["prompt"])
        saved = json.loads(self.renders.read_text())
        self.assertEqual(saved["scenes"]["ch01_s1"]["video_url"], "https://cdn/v.mp4")
        self.assertNotIn(SECRET, out + err)

    def test_already_rendered_scene_is_skipped(self):
        self.renders.write_text(json.dumps({"model": "m", "scenes": {"ch01_s1": {"video_url": "x"}}}))
        self._subscribe([])
        code, out, _ = self._run("--scene", "ch01_s1")
        self.assertEqual(code, 0)
        self.assertEqual(self.calls, [])
        self.assertIn("already rendered", out)

    def test_failed_moderated_and_canceled_are_not_recorded(self):
        self._subscribe([
            (["InProgress", "Failed"], {"status": "failed"}),
            (["InProgress", "NSFW"], {"status": "nsfw", "video": {"url": "https://x"}}),
            (["Queued", "Cancelled"], {"status": "canceled"}),
        ])
        code, _, err = self._run("--scene", "ch01_s1", "--scene", "ch01_s2", "--scene", "ch01_s3")
        self.assertEqual(code, 1)
        for word in ("FAILED", "MODERATED", "CANCELED"):
            self.assertIn(word, err)
        self.assertFalse(self.renders.exists())

    def test_api_error_does_not_stop_later_scenes(self):
        error = self.modules["higgsfield_client.exceptions"].HiggsfieldClientError("402 insufficient credits")
        self._subscribe([
            (["Queued"], error),
            (["Completed"], {"status": "completed", "video": {"url": "https://cdn/2.mp4"}}),
        ])
        code, _, err = self._run("--scene", "ch01_s1", "--scene", "ch01_s2")
        self.assertEqual(code, 1)
        self.assertIn("402", err)
        self.assertEqual(list(json.loads(self.renders.read_text())["scenes"]), ["ch01_s2"])

    def test_whole_episode_needs_yes_and_nothing_is_sent_without_it(self):
        self._subscribe([])
        code, _, err = self._run("--all")
        self.assertEqual(code, 2)
        self.assertIn("--yes", err)
        self.assertEqual(self.calls, [])

    def test_dry_run_and_missing_key_submit_nothing(self):
        self._subscribe([])
        code, out, _ = self._run("--chapter", "ch01", "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("5 scene(s) to render", out)
        code, _, err = self._run("--scene", "ch01_s1", env={})
        self.assertEqual(code, 2)
        self.assertIn("Nothing was submitted", err)
        self.assertEqual(self.calls, [])

    def test_unknown_scene_is_rejected(self):
        self._subscribe([])
        code, _, _ = self._run("--scene", "ch99_s9")
        self.assertNotEqual(code, 0)
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
