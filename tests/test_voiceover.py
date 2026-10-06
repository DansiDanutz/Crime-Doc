"""Tests for tools/voiceover.py: respellings, voice lookup, take reuse and the key guard. No network."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("voiceover", ROOT / "tools" / "voiceover.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class VoiceoverTests(unittest.TestCase):
    def test_load_env_loads_the_local_file_without_overriding_the_shell(self):
        fake = mock.Mock()
        with mock.patch.dict("sys.modules", {"dotenv": fake}):
            tool.load_env()
        fake.load_dotenv.assert_called_once_with(tool.ENV_FILE, override=False)
        self.assertEqual(tool.ENV_FILE, ROOT / ".env.local")
        with mock.patch.dict("sys.modules", {"dotenv": None}), self.assertRaisesRegex(SystemExit, "python-dotenv"):
            tool.load_env()

    def test_respellings_are_whole_words_and_longest_first(self):
        rules = {"Wau": "Vow", "USD": "U-S-D", "USD 70000": "U-S-D seventy thousand"}
        self.assertEqual(tool.spoken_text('They call him Wau. Wauwatosa. "USD 70000." USD', rules),
                         'They call him Vow. Wauwatosa. "U-S-D seventy thousand." U-S-D')

    def test_ep03_read_respells_and_fits_the_cut(self):
        assemble = tool.load_tool("assemble-episode")
        ep = ROOT / "channels/umbra/episodes/ep03-ghost-characters"
        rules = json.loads((ep / "production/pronunciation.json").read_text())
        text = tool.spoken_text(assemble.script_text((ep / "02-script.md").read_text()), rules)
        self.assertIn("They call him Vow.", text)
        self.assertIn('"U-S-D seventy thousand."', text)
        self.assertNotIn("Btx", text)
        self.assertLess(len(text), 5000)

    def test_voice_lookup_prefers_the_exact_name(self):
        voices = [{"name": "Brian Clone v2", "voice_id": "clone"}, {"name": "Brian", "voice_id": "exact"},
                  {"name": "Adam", "voice_id": "a"}]
        self.assertEqual(tool.pick_voice(voices, "brian")["voice_id"], "exact")
        self.assertEqual(tool.pick_voice(voices[:1], "Brian")["voice_id"], "clone")
        self.assertIsNone(tool.pick_voice(voices, "Rachel"))

    def test_fingerprint_changes_with_anything_that_changes_the_read(self):
        s = {"speed": 1.0}
        base = tool.fingerprint("t", "v", "m", s)
        self.assertEqual(base, tool.fingerprint("t", "v", "m", {"speed": 1.0}))
        for other in (("t2", "v", "m", s), ("t", "v2", "m", s), ("t", "v", "m2", s), ("t", "v", "m", {"speed": 1.1})):
            self.assertNotEqual(base, tool.fingerprint(*other))

    def test_no_key_sends_nothing(self):
        # load_env is replaced, so the guard is tested without python-dotenv (CI installs no packages)
        with mock.patch.dict("os.environ", {}, clear=True), mock.patch.object(tool, "load_env"), \
                mock.patch.object(tool, "request") as req, contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(tool.main(["umbra", "ep03-ghost-characters"]), 2)
        req.assert_not_called()
        self.assertIn("ELEVENLABS_API_KEY is not set", err.getvalue())

    def test_dry_run_needs_no_key(self):
        with mock.patch.object(tool, "request") as req, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(tool.main(["umbra", "ep03-ghost-characters", "--dry-run"]), 0)
        req.assert_not_called()
        self.assertIn("Nothing was sent", out.getvalue())




class RecordingTests(unittest.TestCase):
    """The record path against a mocked ElevenLabs. load_env is replaced, so these run without
    python-dotenv (CI installs no packages) and never skip."""

    @contextlib.contextmanager
    def fake_episode(self, seconds=2.0):
        """A one-scene episode in a temp root, a mocked ElevenLabs, and the sent requests."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            ep = root / "channels/c/episodes/e"
            (ep / "production").mkdir(parents=True)
            (ep / "02-script.md").write_text("# S\n\n---\n\nThey call him Wau.\n\n---\n\nend\n")
            (ep / "production/shotlist.json").write_text(json.dumps({"chapters": [{"scenes": [{"duration_s": 5}]}]}))
            (ep / "production/pronunciation.json").write_text('{"Wau": "Vow"}')
            assemble = tool.load_tool("assemble-episode")
            sent = []

            def fake_request(path, key, body=None):
                sent.append((path, body))
                payload = {"/voices": b'{"voices": [{"name": "Brian", "voice_id": "brian-id"}]}',
                           "/user/subscription": b'{"character_limit": 10000, "character_count": 100}'}
                return contextlib.closing(io.BytesIO(payload.get(path, b"ID3fake-mp3-bytes")))

            duration = mock.Mock(return_value=seconds) if not isinstance(seconds, BaseException) \
                else mock.Mock(side_effect=seconds)
            with mock.patch.object(assemble, "ROOT", root), mock.patch.object(tool, "ROOT", root), \
                    mock.patch.object(tool, "load_tool", return_value=assemble), \
                    mock.patch.object(assemble, "ffmpeg_binary", return_value="ffmpeg"), \
                    mock.patch.object(assemble, "media_seconds", duration), \
                    mock.patch.object(tool, "load_env"), \
                    mock.patch.dict("os.environ", {"ELEVENLABS_API_KEY": "k"}, clear=True), \
                    mock.patch.object(tool, "request", side_effect=fake_request), \
                    contextlib.redirect_stdout(io.StringIO()) as out:
                yield ep / "production/vo", sent, out, duration

    @staticmethod
    def takes(sent):
        return sum(p.startswith("/text-to-speech") for p, _ in sent)

    def test_records_once_then_reuses_the_take(self):
        with self.fake_episode() as (vo, sent, out, _):
            self.assertEqual(tool.main(["c", "e"]), 0)
            tts = [b for p, b in sent if p.startswith("/text-to-speech/brian-id")]
            self.assertEqual(len(tts), 1)
            self.assertEqual(tts[0]["text"], "They call him Vow.")
            self.assertEqual((vo / "e-vo.mp3").read_bytes(), b"ID3fake-mp3-bytes")
            receipt = json.loads((vo / "vo.json").read_text())
            self.assertEqual((receipt["voice_name"], receipt["characters"]), ("Brian", 18))
            self.assertEqual(set(receipt), {"voice_id", "voice_name", "model", "settings", "characters", "seconds",
                                            "inputs_sha256", "audio_sha256"})  # no credential is stored
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(self.takes(sent), 1)
            self.assertIn("nothing spent", out.getvalue())
            self.assertEqual(tool.main(["c", "e", "--force"]), 0)
            self.assertEqual(self.takes(sent), 2)
            self.assertEqual(sorted(f.name for f in vo.iterdir()), ["e-vo.mp3", "vo.json", "vo.lock"])

    def test_audio_that_does_not_decode_is_never_kept(self):
        with self.fake_episode(seconds=SystemExit("error: could not read the duration")) as (vo, sent, _, duration):
            with self.assertRaises(SystemExit):
                tool.main(["c", "e"])
            self.assertEqual(sorted(f.name for f in vo.iterdir()), ["vo.lock"])
            duration.side_effect, duration.return_value = None, 2.0
            self.assertEqual(tool.main(["c", "e"]), 0)  # the next run records again instead of reusing
            self.assertEqual(self.takes(sent), 2)

    def test_a_take_that_does_not_match_its_receipt_is_recorded_again(self):
        with self.fake_episode() as (vo, sent, _, _):
            self.assertEqual(tool.main(["c", "e"]), 0)
            (vo / "e-vo.mp3").write_bytes(b"ID3some-other-take")
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(self.takes(sent), 2)

    def test_a_second_run_on_the_same_episode_sends_nothing(self):
        with self.fake_episode() as (vo, sent, _, _):
            vo.mkdir(parents=True)
            with tool.lock_vo(vo):
                with self.assertRaisesRegex(SystemExit, "already recording"):
                    tool.main(["c", "e"])
            self.assertEqual(sent, [("/voices", None)])

if __name__ == "__main__":
    unittest.main()
