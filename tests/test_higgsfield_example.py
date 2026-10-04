"""Regression tests for main.py's terminal-state handling.

CI does not install third-party packages, so the Higgsfield SDK and python-dotenv are
replaced with minimal stand-ins. The stand-ins only drive main.py's callbacks; the
success/failure decisions under test are main.py's own code.
"""
import contextlib
import importlib.util
import io
import os
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SECRET = "test-key-id:test-key-secret-do-not-print"


def _fake_sdk():
    sdk = types.ModuleType("higgsfield_client")

    class Status:
        pass

    names = ["Queued", "InProgress", "Completed", "Failed", "NSFW", "Cancelled"]
    for name in names:
        setattr(sdk, name, type(name, (Status,), {}))
    sdk.Status = Status

    exc = types.ModuleType("higgsfield_client.exceptions")
    exc.CredentialsMissedError = type("CredentialsMissedError", (Exception,), {})
    exc.HiggsfieldClientError = type("HiggsfieldClientError", (Exception,), {})
    sdk.exceptions = exc
    sdk.subscribe = None  # set per test

    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda *a, **k: False
    return {"higgsfield_client": sdk, "higgsfield_client.exceptions": exc, "dotenv": dotenv}


class HiggsfieldExampleTests(unittest.TestCase):
    def setUp(self):
        self.modules = _fake_sdk()
        patcher = mock.patch.dict(sys.modules, self.modules)
        patcher.start()
        self.addCleanup(patcher.stop)
        spec = importlib.util.spec_from_file_location("hf_example_main", ROOT / "main.py")
        self.main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.main)
        self.sdk = self.modules["higgsfield_client"]
        self.calls = []

    def _run(self, statuses, result, env=None):
        def fake_subscribe(model, arguments, on_enqueue=None, on_queue_update=None):
            self.calls.append((model, arguments))
            on_enqueue("req-123")
            for status_name in statuses:
                on_queue_update(getattr(self.sdk, status_name)())
            if isinstance(result, Exception):
                raise result
            return result

        self.sdk.subscribe = fake_subscribe
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, env if env is not None else {"HF_KEY": SECRET}, clear=True):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = self.main.main()
        return code, out.getvalue(), err.getvalue()

    def assertNoSecret(self, *texts):
        for text in texts:
            self.assertNotIn(SECRET, text)
            self.assertNotIn("test-key-secret", text)

    def test_completed_with_video_url_succeeds(self):
        code, out, err = self._run(
            ["Queued", "InProgress", "Completed"],
            {"status": "completed", "video": {"url": "https://cdn.example/v.mp4"}},
        )
        self.assertEqual(code, 0)
        self.assertIn("video_url: https://cdn.example/v.mp4", out)
        self.assertEqual(self.calls[0][0], "bytedance/seedance-2.5/text-to-video")
        self.assertEqual(
            self.calls[0][1],
            {"prompt": "A cinematic scene at sunset", "duration": 5, "resolution": "720p", "aspect_ratio": "16:9"},
        )
        self.assertNoSecret(out, err)

    def test_completed_without_video_url_is_not_success(self):
        code, out, err = self._run(["InProgress", "Completed"], {"status": "completed"})
        self.assertEqual(code, 1)
        self.assertNotIn("video_url:", out)
        self.assertIn("no video URL", err)

    def test_failed_is_not_success(self):
        code, out, err = self._run(["InProgress", "Failed"], {"status": "failed"})
        self.assertEqual(code, 1)
        self.assertNotIn("video_url:", out)
        self.assertIn("FAILED", err)

    def test_moderated_is_not_success(self):
        code, out, err = self._run(["InProgress", "NSFW"], {"status": "nsfw", "video": {"url": "https://x"}})
        self.assertEqual(code, 1)
        self.assertNotIn("video_url:", out)
        self.assertIn("MODERATED", err)

    def test_canceled_is_not_success(self):
        code, out, err = self._run(["Queued", "Cancelled"], {"status": "canceled"})
        self.assertEqual(code, 1)
        self.assertNotIn("video_url:", out)
        self.assertIn("CANCELED", err)

    def test_completed_status_with_mismatched_payload_is_not_success(self):
        code, out, _ = self._run(["Completed"], {"status": "failed", "video": {"url": "https://x"}})
        self.assertEqual(code, 1)
        self.assertNotIn("video_url:", out)

    def test_missing_key_submits_nothing(self):
        code, out, err = self._run(["Completed"], {"status": "completed"}, env={})
        self.assertEqual(code, 2)
        self.assertEqual(self.calls, [])
        self.assertIn("Nothing was submitted", err)

    def test_api_error_is_not_success_and_hides_key(self):
        error = self.modules["higgsfield_client.exceptions"].HiggsfieldClientError("402 insufficient credits")
        code, out, err = self._run(["Queued"], error)
        self.assertEqual(code, 1)
        self.assertNotIn("video_url:", out)
        self.assertNoSecret(out, err)


@unittest.skipUnless(importlib.util.find_spec("higgsfield_client"), "higgsfield-client not installed")
class RealSdkContractTests(unittest.TestCase):
    def test_sdk_exposes_names_main_relies_on(self):
        import higgsfield_client
        from higgsfield_client import exceptions

        for name in ("subscribe", "Completed", "Failed", "NSFW", "Cancelled", "Status"):
            self.assertTrue(hasattr(higgsfield_client, name), name)
        for name in ("CredentialsMissedError", "HiggsfieldClientError"):
            self.assertTrue(hasattr(exceptions, name), name)


if __name__ == "__main__":
    unittest.main()
