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
    def fake_episode(self, take_seconds=2.0):
        """A two-chapter episode (5 s each) in a temp root, a mocked ElevenLabs, the sent requests.
        take_seconds: the length every take decodes to, or an exception for a take that won't decode."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            ep = root / "channels/c/episodes/e"
            (ep / "production").mkdir(parents=True)
            (ep / "02-script.md").write_text("# S\n\n---\n\n<!-- ch01 -->\nThey call him Wau.\n\n"
                                             "<!-- ch02 -->\nHe dials in.\n\n---\n\nend\n")
            (ep / "production/shotlist.json").write_text(json.dumps({"chapters": [
                {"id": "ch01", "scenes": [{"duration_s": 5}]}, {"id": "ch02", "scenes": [{"duration_s": 5}]}]}))
            (ep / "production/pronunciation.json").write_text('{"Wau": "Vow"}')
            assemble = tool.load_tool("assemble-episode")
            sent, state = [], {"take": take_seconds}

            def fake_request(path, key, body=None):
                sent.append((path, body))
                payload = {"/voices": b'{"voices": [{"name": "Brian", "voice_id": "brian-id"}]}',
                           "/user/subscription": b'{"character_limit": 10000, "character_count": 100}'}
                return contextlib.closing(io.BytesIO(payload.get(path, b"ID3" + (body or {}).get("text", "").encode())))

            def duration(ffmpeg, path):
                if path.name.startswith(".e-vo"):
                    return 10.0  # the built track: the whole 10 s cut
                if isinstance(state["take"], BaseException):
                    raise state["take"]
                return state["take"]

            def fake_build(ffmpeg, items, total, dest):
                dest.write_bytes(b"TRACK" + b"|".join(f"{i['label']}@{i['start']}x{i['tempo']}".encode() for i in items))

            with mock.patch.object(assemble, "ROOT", root), mock.patch.object(tool, "ROOT", root), \
                    mock.patch.object(assemble, "ffmpeg_binary", return_value="ffmpeg"), \
                    mock.patch.object(assemble, "media_seconds", side_effect=duration), \
                    mock.patch.object(tool, "build_track", side_effect=fake_build), \
                    mock.patch.object(tool, "load_env"), \
                    mock.patch.dict("os.environ", {"ELEVENLABS_API_KEY": "k"}, clear=True), \
                    mock.patch.object(tool, "request", side_effect=fake_request), \
                    contextlib.redirect_stdout(io.StringIO()) as out:
                real_load = tool.load_tool
                with mock.patch.object(tool, "load_tool",
                                       side_effect=lambda n: assemble if n == "assemble-episode" else real_load(n)):
                    yield ep / "production/vo", sent, out, state

    @staticmethod
    def tts(sent):
        return [b for p, b in sent if p.startswith("/text-to-speech")]

    def test_records_each_chapter_once_with_its_neighbours_then_reuses(self):
        with self.fake_episode() as (vo, sent, out, _):
            self.assertEqual(tool.main(["c", "e"]), 0)
            bodies = self.tts(sent)
            self.assertEqual([b["text"] for b in bodies], ["They call him Vow.", "He dials in."])
            self.assertEqual((bodies[0].get("previous_text"), bodies[0]["next_text"]), (None, "He dials in."))
            self.assertEqual((bodies[1]["previous_text"], bodies[1].get("next_text")), ("They call him Vow.", None))
            self.assertEqual((vo / "e-vo.mp3").read_bytes(), b"TRACKch01@0.0x1.0|ch02@5.0x1.0")
            receipt = json.loads((vo / "vo.json").read_text())
            self.assertEqual(set(receipt), {"voice_id", "voice_name", "model", "settings", "takes", "track"})
            self.assertEqual(set(receipt["takes"]), {"ch01", "ch02"})
            self.assertEqual(set(receipt["takes"]["ch01"]),  # no credential is stored
                             {"inputs_sha256", "audio_sha256", "seconds", "characters", "file"})
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(len(self.tts(sent)), 2)
            self.assertIn("nothing spent", out.getvalue())
            self.assertEqual(tool.main(["c", "e", "--force"]), 0)
            self.assertEqual(len(self.tts(sent)), 4)

    def test_changing_one_chapter_records_it_and_its_neighbours_only(self):
        with self.fake_episode() as (vo, sent, _, _):
            self.assertEqual(tool.main(["c", "e"]), 0)
            script = vo.parent.parent / "02-script.md"
            script.write_text(script.read_text().replace("He dials in.", "He dials in again."))
            self.assertEqual(tool.main(["c", "e"]), 0)
            # ch02 changed; ch01 carries ch02 as its context, so it is re-read too for continuity
            self.assertEqual([b["text"] for b in self.tts(sent)[2:]], ["They call him Vow.", "He dials in again."])

    def test_a_take_too_long_for_its_window_is_reported_not_laid(self):
        with self.fake_episode(take_seconds=6.0) as (vo, sent, out, state):
            with contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(tool.main(["c", "e"]), 2)
            self.assertIn("ch01, ch02 run more than 8%", err.getvalue())
            self.assertFalse((vo / "e-vo.mp3").exists())
            state["take"] = 4.7  # 4.7 s in a 4.5 s usable window: tightened ~4%, laid
            self.assertEqual(tool.main(["c", "e", "--force"]), 0)
            self.assertIn(b"x1.04", (vo / "e-vo.mp3").read_bytes())

    def test_audio_that_does_not_decode_is_never_kept(self):
        with self.fake_episode(take_seconds=SystemExit("error: could not read the duration")) as (vo, sent, _, state):
            with self.assertRaises(SystemExit):
                tool.main(["c", "e"])
            self.assertEqual(list((vo / "takes").iterdir()), [])
            self.assertFalse((vo / "e-vo.mp3").exists())
            state["take"] = 2.0
            self.assertEqual(tool.main(["c", "e"]), 0)  # the next run records again instead of reusing
            self.assertEqual(len(self.tts(sent)), 3)

    def test_a_take_that_does_not_match_its_receipt_is_recorded_again(self):
        with self.fake_episode() as (vo, sent, _, _):
            self.assertEqual(tool.main(["c", "e"]), 0)
            next((vo / "takes").glob("ch02-*.mp3")).write_bytes(b"ID3some-other-take")
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual([b["text"] for b in self.tts(sent)[2:]], ["He dials in."])

    def test_a_second_run_on_the_same_episode_sends_nothing(self):
        with self.fake_episode() as (vo, sent, _, _):
            vo.mkdir(parents=True)
            with tool.lock_vo(vo):
                with self.assertRaisesRegex(SystemExit, "already recording"):
                    tool.main(["c", "e"])
            self.assertEqual(sent, [("/voices", None)])


def real_ffmpeg():
    try:
        return tool.load_tool("assemble-episode").ffmpeg_binary()
    except SystemExit:
        return None


@unittest.skipUnless(real_ffmpeg(), "needs ffmpeg (pip install -r requirements.txt provides one)")
class TrackWithFfmpegTests(unittest.TestCase):
    def test_takes_land_on_their_windows_and_the_track_is_the_cut(self):
        import subprocess
        ffmpeg, assemble = real_ffmpeg(), tool.load_tool("assemble-episode")
        with tempfile.TemporaryDirectory() as d:
            items = []
            for i, seconds in enumerate((3.0, 4.8)):  # the second is 4.8 s in a 4.5 s usable window
                path = Path(d) / f"t{i}.mp3"
                subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "lavfi", "-i",
                                f"sine=frequency={400 + 200 * i}:duration={seconds}", "-ac", "1", str(path)], check=True)
                item = {"path": path, "start": 5.0 * i, "window": 5.0, "lead": tool.LEAD_S}
                item["tempo"] = tool.fit(assemble.media_seconds(ffmpeg, path), item)
                items.append(item)
            self.assertEqual(items[0]["tempo"], 1.0)
            self.assertAlmostEqual(items[1]["tempo"], 4.8 / 4.5, delta=0.02)
            track = Path(d) / "track.mp3"
            tool.build_track(ffmpeg, items, 10.0, track)
            self.assertAlmostEqual(assemble.media_seconds(ffmpeg, track), 10.0, delta=0.1)
            log = subprocess.run([ffmpeg, "-hide_banner", "-i", str(track), "-af", "silencedetect=n=-40dB:d=0.1",
                                  "-f", "null", "-"], capture_output=True, text=True).stderr
            ends = [float(x.split("silence_end: ")[1].split()[0]) for x in log.splitlines() if "silence_end" in x]
            self.assertAlmostEqual(ends[0], tool.LEAD_S, delta=0.05)        # ch01 starts after its breath
            self.assertAlmostEqual(ends[1], 5.0 + tool.LEAD_S, delta=0.05)  # ch02 starts on its own window


if __name__ == "__main__":
    unittest.main()
