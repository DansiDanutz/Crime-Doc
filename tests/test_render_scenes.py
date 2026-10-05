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

    def _inputs(self, scene_id):
        shotlist = json.loads((self.renders.parent / "shotlist.json").read_text())
        scene = next(sc for ch in shotlist["chapters"] for sc in ch["scenes"] if sc["id"] == scene_id)
        return self.tool.fingerprint(self.tool.arguments_for(scene, shotlist, "720p"))

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
        self.assertEqual(saved["scenes"]["ch01_s1"]["inputs_sha256"], self._inputs("ch01_s1"))
        self.assertEqual(saved["pending"], {})
        self.assertIn("preview", saved["kind"])
        self.assertNotIn(SECRET, out + err)

    def test_up_to_date_scene_is_skipped_but_an_edited_one_rerenders(self):
        self.renders.write_text(json.dumps({"scenes": {
            "ch01_s1": {"video_url": "x", "inputs_sha256": self._inputs("ch01_s1")},
            "ch01_s2": {"video_url": "y", "inputs_sha256": "stale"},
        }}))
        self._subscribe([(["Completed"], {"status": "completed", "video": {"url": "https://cdn/new.mp4"}})])
        code, out, _ = self._run("--scene", "ch01_s1", "--scene", "ch01_s2")
        self.assertEqual(code, 0)
        self.assertEqual(len(self.calls), 1)  # only the edited scene was sent
        self.assertIn("matte red mannequin hands", self.calls[0][1]["prompt"])  # ch01_s2's prompt
        scenes = json.loads(self.renders.read_text())["scenes"]
        self.assertEqual(scenes["ch01_s1"]["video_url"], "x")
        self.assertEqual(scenes["ch01_s2"]["video_url"], "https://cdn/new.mp4")

    def test_job_queued_by_an_interrupted_run_is_resumed_not_resubmitted(self):
        self.renders.write_text(json.dumps({"scenes": {}, "pending": {
            "ch01_s1": {"request_id": "req-old", "inputs_sha256": self._inputs("ch01_s1")}}}))
        self._subscribe([])
        asked = []
        self.sdk.result = lambda rid: asked.append(rid) or {"status": "completed", "video": {"url": "https://cdn/old.mp4"}}
        self.sdk.status = lambda rid: self.sdk.Completed()
        code, _, _ = self._run("--scene", "ch01_s1")
        self.assertEqual(code, 0)
        self.assertEqual(self.calls, [])  # nothing new was billed
        self.assertEqual(asked, ["req-old"])
        saved = json.loads(self.renders.read_text())
        self.assertEqual(saved["scenes"]["ch01_s1"]["request_id"], "req-old")
        self.assertEqual(saved["pending"], {})

    def test_request_id_is_saved_before_waiting(self):
        seen = {}

        def fake(model, arguments, on_enqueue=None, on_queue_update=None):
            on_enqueue("req-1")
            seen["ledger"] = json.loads(self.renders.read_text())
            raise KeyboardInterrupt  # the run dies while waiting
        self.sdk.subscribe = fake
        with self.assertRaises(KeyboardInterrupt):
            self._run("--scene", "ch01_s1")
        self.assertEqual(seen["ledger"]["pending"]["ch01_s1"]["request_id"], "req-1")

    def test_interrupted_forced_rerender_is_resumed_even_with_an_older_clip(self):
        inputs = self._inputs("ch01_s1")
        self.renders.write_text(json.dumps({
            "scenes": {"ch01_s1": {"request_id": "req-old", "video_url": "https://cdn/old.mp4", "inputs_sha256": inputs}},
            "pending": {"ch01_s1": {"request_id": "req-new", "inputs_sha256": inputs}},
        }))
        self._subscribe([])
        self.sdk.result = lambda rid: {"status": "completed", "video": {"url": "https://cdn/new.mp4"}}
        self.sdk.status = lambda rid: self.sdk.Completed()
        code, _, _ = self._run("--scene", "ch01_s1")
        self.assertEqual(code, 0)
        self.assertEqual(self.calls, [])
        saved = json.loads(self.renders.read_text())
        self.assertEqual(saved["scenes"]["ch01_s1"]["video_url"], "https://cdn/new.mp4")
        self.assertEqual(saved["pending"], {})

    def test_a_second_run_on_the_same_episode_is_refused(self):
        self._subscribe([])
        held = self.tool.lock_episode(self.renders.parent)
        try:
            code, _, _ = self._run("--scene", "ch01_s1")
        finally:
            held.close()
        self.assertNotEqual(code, 0)
        self.assertEqual(self.calls, [])

    def test_an_interrupted_save_leaves_the_old_ledger_intact(self):
        self.renders.write_text(json.dumps({"scenes": {"ch01_s9": {"video_url": "kept"}}, "pending": {}}))
        before = self.renders.read_text()
        ledger = self.tool.Ledger(self.renders)
        ledger.data["pending"]["ch01_s1"] = {"request_id": "r", "inputs_sha256": "h"}
        with mock.patch.object(self.tool.os, "replace", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                ledger.save()
        self.assertEqual(self.renders.read_text(), before)
        self.assertEqual([p.name for p in self.renders.parent.iterdir() if p.name.endswith(".tmp")], [])

    def test_failed_moderated_and_canceled_are_not_recorded(self):
        self._subscribe([
            (["InProgress", "Failed"], {"status": "failed"}),
            (["InProgress", "NSFW"], {"status": "nsfw", "video": {"url": "https://x"}}),
            (["Queued", "Cancelled"], {"status": "canceled"}),
        ])
        code, _, err = self._run("--scene", "ch01_s1", "--scene", "ch01_s2", "--scene", "ch01_s3", "--yes")
        self.assertEqual(code, 1)
        for word in ("FAILED", "MODERATED", "CANCELED"):
            self.assertIn(word, err)
        saved = json.loads(self.renders.read_text())
        self.assertEqual(saved["scenes"], {})
        self.assertEqual(saved["pending"], {})

    def test_api_error_stops_the_batch(self):
        error = self.modules["higgsfield_client.exceptions"].HiggsfieldClientError("402 insufficient credits")
        self._subscribe([
            (["Queued"], error),
            (["Completed"], {"status": "completed", "video": {"url": "https://cdn/2.mp4"}}),
        ])
        code, _, err = self._run("--scene", "ch01_s1", "--scene", "ch01_s2", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("402", err)
        self.assertIn("no further scenes were submitted", err)
        self.assertEqual(len(self.calls), 1)

    def test_any_batch_needs_yes_and_nothing_is_sent_without_it(self):
        self._subscribe([])
        for selector in (["--chapter", "ch01"], ["--all"], ["--scene", "ch01_s1", "--scene", "ch01_s2"]):
            code, _, err = self._run(*selector)
            self.assertEqual(code, 2, selector)
            self.assertIn("--yes", err)
        self.assertEqual(self.calls, [])

    def test_dry_run_and_missing_key_submit_nothing(self):
        self._subscribe([])
        code, out, _ = self._run("--chapter", "ch01", "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("5 new render(s)", out)
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
