"""Tests for tools/soundtrack.py and the sound mix in tools/assemble-episode.py: plan validation,
recording with the Music API fallback, reuse, stale-stem refusal, and (with real ffmpeg) the stems
and the ducked, loudness-normalised mix."""
import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = load("soundtrack")
assemble = load("assemble-episode")
SHOT = {"chapters": [{"id": "ch01", "scenes": [{"duration_s": 10}]}, {"id": "ch02", "scenes": [{"duration_s": 10}]}]}
OUTRO = {"seconds": 12.0, "text": "x", "card": {}, "music": {"prompt": "a sting", "gain_db": -2.0}}


class PlanTests(unittest.TestCase):
    def test_cues_get_absolute_times_and_the_outro_sting(self):
        cues = tool.plan({"music": [{"from": "ch01", "to": "ch02", "prompt": "drone"}],
                          "sfx": [{"chapter": "ch02", "at": 2, "dur": 1, "prompt": "click", "gain_db": -6}]},
                         SHOT, OUTRO)
        self.assertEqual([(c["label"], c["start"], c["dur"]) for c in cues],
                         [("music-ch01-ch02", 0.0, 20.0), ("sfx-ch02-01", 12.0, 1.0), ("outro", 20.0, 12.0)])
        self.assertTrue(cues[-1]["channel"])

    def test_bad_plans_are_refused_with_the_cue_named(self):
        ok_m = {"from": "ch01", "to": "ch02", "prompt": "drone"}
        ok_s = {"chapter": "ch01", "at": 1, "dur": 1, "prompt": "click"}
        for sound, reason in (({"music": [{**ok_m, "to": "ch09"}]}, "from/to"),
                              ({"music": [{**ok_m, "from": "ch02", "to": "ch01"}]}, "before"),
                              ({"music": [ok_m, {**ok_m, "from": "ch02"}]}, "overlap"),
                              ({"sfx": [{**ok_s, "at": 9.5}]}, "past the end"),
                              ({"sfx": [{**ok_s, "dur": float("nan")}]}, "dur"),
                              ({"sfx": [{**ok_s, "prompt": ""}]}, "prompt"),
                              ({"sfx": [{**ok_s, "gain_db": 20}]}, "gain_db"),
                              ({"music": "drone"}, "lists"),
                              ([], "object")):
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                tool.plan(sound, SHOT, None)
        tiny = {"chapters": [{"id": "ch01", "scenes": [{"duration_s": 2}]}]}
        with self.assertRaisesRegex(ValueError, "length"):
            tool.plan({"music": [{"from": "ch01", "to": "ch01", "prompt": "x"}]}, tiny, None)
        short = {"chapters": [{"id": "ch01", "scenes": [{"duration_s": 5}]}]}  # under the APIs' 10 s: allowed,
        self.assertEqual(tool.plan({"music": [{"from": "ch01", "to": "ch01", "prompt": "x"}]}, short, None)[0]["dur"],
                         5.0)  # requested at 10 s and trimmed

    def test_ep03_plan_is_valid_and_leaves_ch13_silent(self):
        cues, total = tool.load_plan(ROOT / "channels/umbra/episodes/ep03-ghost-characters")
        self.assertEqual(total, 312.0)
        music = [c for c in cues if c["kind"] == "music"]
        self.assertEqual([c["label"] for c in music][-1], "outro")
        self.assertFalse(any(c["start"] <= 185 < c["start"] + c["dur"] for c in music))  # "music drops out" in ch13
        self.assertEqual(sum(c["kind"] == "sfx" for c in cues), 33)


class RecordTests(unittest.TestCase):
    @contextlib.contextmanager
    def episode(self, music_api=True, credits=100000, music_error="HTTP 403: plan does not include music"):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            ep = root / "channels/c/episodes/e"
            (ep / "production").mkdir(parents=True)
            (ep / "production/shotlist.json").write_text(json.dumps(SHOT))
            (ep / "production/sound.json").write_text(json.dumps({
                "music": [{"from": "ch01", "to": "ch01", "prompt": "drone one"},
                          {"from": "ch02", "to": "ch02", "prompt": "drone two"}],
                "sfx": [{"chapter": "ch01", "at": 1, "dur": 1, "prompt": "click"}]}))
            (root / "channels/c/outro.json").write_text(json.dumps({
                "seconds": 12, "text": "Subscribe.", "card": {"kind": "endcard", "wordmark": "u", "lines": ["X"]},
                "music": {"prompt": "sting"}}))
            sent, access = [], {"music": music_api}

            def fake_request(path, key, body=None):
                sent.append((path.split("?")[0], body))
                if path.startswith("/music") and not access["music"]:
                    raise SystemExit(f"error: ElevenLabs /music failed, {music_error}")
                if path.startswith("/user/subscription"):
                    return contextlib.closing(io.BytesIO(json.dumps(
                        {"character_limit": credits, "character_count": 0}).encode()))
                return contextlib.closing(io.BytesIO(b"ID3" + json.dumps(body).encode()))

            vo = load("voiceover")
            a = load("assemble-episode")
            stems = []
            with mock.patch.object(a, "ROOT", root), mock.patch.object(tool, "ROOT", root), \
                    mock.patch.object(tool, "load_tool",
                                      side_effect=lambda n: {"assemble-episode": a, "voiceover": vo}.get(n) or load(n)), \
                    mock.patch.object(a, "ffmpeg_binary", return_value="ffmpeg"), \
                    mock.patch.object(a, "media_seconds", side_effect=lambda f, p: 32.0 if ".e-" in p.name else 3.0), \
                    mock.patch.object(tool, "build_stem", side_effect=lambda f, cues, total, dest: (
                        stems.append([c["label"] for c in cues]), dest.write_bytes(json.dumps([c["label"] for c in cues]).encode()))), \
                    mock.patch.object(vo, "request", side_effect=fake_request), mock.patch.object(vo, "load_env"), \
                    mock.patch.dict("os.environ", {"ELEVENLABS_API_KEY": "k"}, clear=True), \
                    contextlib.redirect_stdout(io.StringIO()) as out:
                self.access = access
                yield ep, root, sent, out, stems

    @staticmethod
    def generated(sent):
        return [p for p, _ in sent if p in ("/music", "/sound-generation")]

    def test_records_every_cue_once_then_reuses_them(self):
        with self.episode() as (ep, root, sent, out, stems):
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(self.generated(sent), ["/music", "/music", "/sound-generation", "/music"])
            bodies = [b for p, b in sent if p == "/music"]
            self.assertEqual([b["music_length_ms"] for b in bodies], [10000, 10000, 12000])
            self.assertEqual(stems[0], ["music-ch01-ch01", "music-ch02-ch02", "outro"])
            self.assertTrue(list((root / "channels/c/sound/takes").glob("music-*.mp3")))  # the sting lives per channel
            mix = json.loads((ep / "production/sound/mix.json").read_text())
            self.assertEqual(set(mix), {"music_sha256", "sfx_sha256", "plan_sha256", "seconds"})
            self.assertEqual(tool.current_stems(ep, "e"), tool.stem_paths(ep, "e")[:2])
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(len(self.generated(sent)), 4)
            self.assertIn("nothing spent", out.getvalue())

    def test_without_the_music_api_sections_become_looped_ambient_beds(self):
        with self.episode(music_api=False) as (ep, root, sent, out, stems):
            self.assertEqual(tool.main(["c", "e"]), 0)
            # one refused /music call, then every music cue goes to the sound-effects API
            self.assertEqual(self.generated(sent), ["/music"] + ["/sound-generation"] * 4)
            loops = [b for p, b in sent if p == "/sound-generation" and b["text"].startswith("seamless")]
            self.assertEqual(len(loops), 3)
            receipt = json.loads((ep / "production/sound/receipt.json").read_text())
            self.assertEqual(sorted(t["source"] for t in receipt["takes"].values()), ["sfx", "sfx-loop", "sfx-loop"])
            # next run: the Music API is asked again (once), the loops are reused, nothing else is paid for
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(self.generated(sent)[5:], ["/music"])
            self.assertIn("reusing its ambient loop", out.getvalue())

    def test_real_music_replaces_the_loops_once_the_music_api_is_available(self):
        with self.episode(music_api=False) as (ep, root, sent, out, stems):
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.access["music"] = True  # the plan now includes music
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(self.generated(sent)[5:], ["/music", "/music", "/music"])  # all three re-made as music
            receipt = json.loads((ep / "production/sound/receipt.json").read_text())
            sources = sorted(t["source"] for t in receipt["takes"].values())
            self.assertEqual(sources, ["music", "music", "sfx", "sfx-loop", "sfx-loop"])  # (+ channel sting elsewhere)
            self.assertEqual(tool.current_stems(ep, "e"), tool.stem_paths(ep, "e")[:2])

    def test_a_rejected_music_prompt_is_an_error_not_a_fallback(self):
        with self.episode(music_api=False, music_error="HTTP 422: prompt rejected") as (ep, root, sent, out, stems):
            with self.assertRaisesRegex(SystemExit, "422"):
                tool.main(["c", "e"])
            self.assertEqual(self.generated(sent), ["/music"])

    def test_cached_loops_do_not_count_against_the_credit_check(self):
        with self.episode(music_api=False) as (ep, root, sent, out, stems):
            self.assertEqual(tool.main(["c", "e"]), 0)  # fallback loops cached for all three music cues
            n = len(self.generated(sent))
            vo_mod = tool.load_tool("voiceover")  # the fixture's module, the one main() uses
            # 100 credits would not cover three fresh music cues (32 s, about 1,280), but the loops are free
            with mock.patch.object(vo_mod, "characters_left", return_value=100), \
                    contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(tool.main(["c", "e"]), 0, err.getvalue())
            self.assertEqual(self.generated(sent)[n:], ["/music"])  # one refused try, then the cached loops

    def test_a_run_the_credits_cannot_cover_sends_nothing(self):
        with self.episode(credits=100) as (ep, root, sent, out, stems):
            with contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(tool.main(["c", "e"]), 2)
            self.assertIn("not enough ElevenLabs credits", err.getvalue())
            self.assertEqual(self.generated(sent), [])

    def test_a_changed_plan_makes_the_stems_stale(self):
        with self.episode() as (ep, root, sent, out, stems):
            self.assertEqual(tool.main(["c", "e"]), 0)
            sound = json.loads((ep / "production/sound.json").read_text())
            sound["sfx"][0]["gain_db"] = -3  # only the level changed: no new recording, but new stems
            (ep / "production/sound.json").write_text(json.dumps(sound))
            with self.assertRaisesRegex(SystemExit, "changed since the stems were built"):
                tool.current_stems(ep, "e")
            self.assertEqual(tool.main(["c", "e"]), 0)
            self.assertEqual(len(self.generated(sent)), 4)
            self.assertEqual(tool.current_stems(ep, "e"), tool.stem_paths(ep, "e")[:2])
            tool.stem_paths(ep, "e")[1].write_bytes(b"other")
            with self.assertRaisesRegex(SystemExit, "not the ones mix.json describes"):
                tool.current_stems(ep, "e")
            for p in tool.stem_paths(ep, "e")[:2]:
                p.unlink()
            with self.assertRaisesRegex(SystemExit, "missing or unfinished"):
                tool.current_stems(ep, "e")

    def test_an_episode_without_sound_json_has_no_stems(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(tool.current_stems(Path(d), "e"))


def real_ffmpeg():
    try:
        return assemble.ffmpeg_binary()
    except SystemExit:
        return None


@unittest.skipUnless(real_ffmpeg(), "needs ffmpeg (pip install -r requirements.txt provides one)")
class MixWithFfmpegTests(unittest.TestCase):
    def rms_db(self, ffmpeg, path, start, dur):
        log = subprocess.run([ffmpeg, "-hide_banner", "-ss", str(start), "-t", str(dur), "-i", str(path),
                              "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        return float(log.split("mean_volume: ")[1].split()[0])

    def test_stems_loop_music_to_length_and_the_mix_ducks_it_under_the_voice(self):
        ffmpeg = real_ffmpeg()
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            gen = lambda name, src, sec: subprocess.run(
                [ffmpeg, "-y", "-v", "error", "-f", "lavfi", "-i", f"{src}:duration={sec}", str(d / name)], check=True)
            gen("bed.mp3", "anoisesrc=color=pink:amplitude=0.3", 4)   # shorter than its 12 s section
            gen("click.mp3", "sine=frequency=2000", 1)
            gen("voice.mp3", "sine=frequency=300", 4)                 # speaks 0-4 s only
            music = d / "music.mp3"
            tool.build_stem(ffmpeg, [{"kind": "music", "path": d / "bed.mp3", "start": 0.0, "dur": 12.0, "gain_db": 0}],
                            12.0, music)
            self.assertAlmostEqual(assemble.media_seconds(ffmpeg, music), 12.0, delta=0.1)
            self.assertGreater(self.rms_db(ffmpeg, music, 8, 1), -40)  # still playing after the 4 s source: looped
            sfx = d / "sfx.mp3"
            tool.build_stem(ffmpeg, [{"kind": "sfx", "path": d / "click.mp3", "start": 6.0, "dur": 1.0, "gain_db": 0}],
                            12.0, sfx)
            self.assertLess(self.rms_db(ffmpeg, sfx, 1, 1), -60)  # silent before its cue
            self.assertGreater(self.rms_db(ffmpeg, sfx, 6.2, 0.5), -40)

            voice = d / "voice-12.mp3"
            subprocess.run([ffmpeg, "-y", "-v", "error", "-i", str(d / "voice.mp3"), "-af", "apad", "-t", "12", str(voice)],
                           check=True)
            graph, label = assemble.sound_mix_graph(True, 12.0)
            bed_only = d / "bed-only.wav"
            # the music alone, through the same ducker, with the voice as the key: louder when the voice stops
            subprocess.run([ffmpeg, "-y", "-v", "error", "-i", str(music), "-i", str(voice), "-filter_complex",
                            "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[key];"
                            "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[mus];"
                            "[mus][key]sidechaincompress=threshold=0.02:ratio=10:attack=20:release=600[out]",
                            "-map", "[out]", str(bed_only)], check=True)
            self.assertGreater(self.rms_db(ffmpeg, bed_only, 9, 1) - self.rms_db(ffmpeg, bed_only, 1, 2), 3)
            mixed = d / "mixed.m4a"
            subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=320x180:d=12",
                            "-i", str(voice), "-i", str(music), "-i", str(sfx), "-filter_complex", graph,
                            "-map", f"[{label}]", "-c:a", "aac", "-t", "12", str(mixed)], check=True)
            self.assertAlmostEqual(assemble.media_seconds(ffmpeg, mixed), 12.0, delta=0.1)


if __name__ == "__main__":
    unittest.main()
