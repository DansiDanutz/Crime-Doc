"""Tests for tools/assemble-episode.py: the edit plan (order, durations, REUSE) and the script text.

The ffmpeg steps are exercised by hand on real clips; CI has no ffmpeg, so these tests cover the
decisions that determine what goes into the cut.
"""
import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("assemble_episode", ROOT / "tools" / "assemble-episode.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def shotlist(*scenes):
    return {"chapters": [{"id": "ch01", "scenes": [
        {"id": sid, "duration_s": dur, **({"reuse": reuse} if reuse else {})} for sid, dur, reuse in scenes]}]}


class AssembleTests(unittest.TestCase):
    def test_plan_keeps_order_and_durations_and_maps_reuse(self):
        renders = {"scenes": {"ch01_s1": {"video_url": "u1"}, "ch01_s2": {"video_url": "u2"}}}
        segments, missing = tool.plan(
            shotlist(("ch01_s1", 3, None), ("ch01_s2", 4, None), ("ch01_s3", 2, "ch01_s1")), renders)
        self.assertEqual(missing, [])
        self.assertEqual([(s["id"], s["source"], s["url"], s["seconds"]) for s in segments],
                         [("ch01_s1", "ch01_s1", "u1", 3), ("ch01_s2", "ch01_s2", "u2", 4),
                          ("ch01_s3", "ch01_s1", "u1", 2)])

    def test_plan_reports_scenes_without_a_clip(self):
        segments, missing = tool.plan(shotlist(("ch01_s1", 3, None), ("ch01_s2", 3, "ch01_s1")), {"scenes": {}})
        self.assertEqual(segments, [])
        self.assertEqual(missing, ["ch01_s1", "ch01_s2 (via ch01_s1)"])

    def test_a_rerendered_clip_gets_a_new_cache_file(self):
        clips = Path("/tmp/clips")
        old = tool.cache_path(clips, "ch03_s5", "https://cdn/old.mp4")
        new = tool.cache_path(clips, "ch03_s5", "https://cdn/new.mp4")
        self.assertNotEqual(old, new)
        self.assertEqual(old, tool.cache_path(clips, "ch03_s5", "https://cdn/old.mp4"))
        self.assertTrue(old.name.startswith("ch03_s5-") and old.suffix == ".mp4")

    def test_script_text_is_the_narration_only(self):
        md = "# STATE 3 — Script\n\n**Target length:** 5 minutes\n\n---\n\nFirst line.\n\nSecond line.\n\n---\n\n**Word count:** 4\n"
        self.assertEqual(tool.script_text(md), "First line. Second line.")

    def test_ep03_plan_covers_five_minutes(self):
        shot = json.loads((ROOT / "channels/umbra/episodes/ep03-ghost-characters/production/shotlist.json").read_text())
        everything = {sc["id"]: {"video_url": "x"} for ch in shot["chapters"] for sc in ch["scenes"]}
        segments, missing = tool.plan(shot, {"scenes": everything})
        self.assertEqual(missing, [])
        self.assertEqual(sum(s["seconds"] for s in segments), 300)
        narration = tool.script_text((ROOT / "channels/umbra/episodes/ep03-ghost-characters/02-script.md").read_text())
        self.assertEqual(len(narration.split()), 698)


    def test_concat_entries_escape_apostrophes(self):
        self.assertEqual(tool.concat_line(Path("/Users/o'neil/clips/a.mp4")),
                         "file '/Users/o'\\''neil/clips/a.mp4'\n")

    def test_download_is_bounded_and_leaves_no_partial_file(self):
        with tempfile.TemporaryDirectory() as d:
            src, dest = Path(d) / "src.bin", Path(d) / "out" / "clip.mp4"
            dest.parent.mkdir()
            src.write_bytes(b"x" * 3000)
            with self.assertRaisesRegex(SystemExit, "over"):
                tool.download(src.as_uri(), dest, limit=1000)
            self.assertEqual(list(dest.parent.iterdir()), [])
            tool.download(src.as_uri(), dest, limit=5000)
            self.assertEqual(dest.read_bytes(), b"x" * 3000)
            self.assertEqual([f.name for f in dest.parent.iterdir()], ["clip.mp4"])

    def _episode(self, root: Path, renders: dict) -> None:
        ep = root / "channels" / "c" / "episodes" / "e" / "production"
        ep.mkdir(parents=True)
        (ep / "shotlist.json").write_text(json.dumps(shotlist(("ch01_s1", 3, None), ("ch01_s2", 2, None))))
        (ep / "renders.json").write_text(json.dumps(renders))

    def test_a_partial_cut_needs_allow_gaps(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(tool, "ROOT", Path(d)), \
                mock.patch.object(tool, "ffmpeg_binary", return_value="ffmpeg"), \
                mock.patch.object(tool, "download"), \
                mock.patch.object(tool, "trim", return_value=False) as trim, \
                mock.patch.object(tool, "run"), \
                mock.patch.object(tool, "media_seconds", return_value=3.0), \
                mock.patch.object(tool.shutil, "copyfile"), mock.patch.object(tool.shutil, "move"):
            self._episode(Path(d), {"scenes": {"ch01_s1": {"video_url": "u1"}}})
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(tool.main(["c", "e"]), 2)
                trim.assert_not_called()
                self.assertEqual(tool.main(["c", "e", "--allow-gaps"]), 0)
            self.assertEqual([c.args[2] for c in trim.call_args_list], [3])

    def test_a_cut_that_comes_out_the_wrong_length_is_not_written(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(tool, "ROOT", Path(d)), \
                mock.patch.object(tool, "ffmpeg_binary", return_value="ffmpeg"), \
                mock.patch.object(tool, "download"), mock.patch.object(tool, "trim", return_value=False), \
                mock.patch.object(tool, "run"), mock.patch.object(tool, "media_seconds", return_value=3.0), \
                mock.patch.object(tool.shutil, "copyfile"), mock.patch.object(tool.shutil, "move") as move:
            self._episode(Path(d), {"scenes": {"ch01_s1": {"video_url": "u1"}, "ch01_s2": {"video_url": "u2"}}})
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(SystemExit, "storyboard is 5 s"):
                tool.main(["c", "e"])
            move.assert_not_called()


def real_ffmpeg():
    try:
        return tool.ffmpeg_binary()
    except SystemExit:
        return None


@unittest.skipUnless(real_ffmpeg(), "needs ffmpeg (CI has none)")
class TrimWithFfmpegTests(unittest.TestCase):
    def test_the_outro_end_card_is_appended_after_the_story(self):
        ffmpeg = real_ffmpeg()
        with tempfile.TemporaryDirectory() as d, mock.patch.object(tool, "ROOT", Path(d)):
            root = Path(d)
            ep = root / "channels/c/episodes/e"
            (ep / "production").mkdir(parents=True)
            clip = root / "clip.mp4"
            subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=640x360:rate=24:duration=4",
                            "-pix_fmt", "yuv420p", str(clip)], check=True)
            (ep / "production/shotlist.json").write_text(json.dumps(shotlist(("ch01_s1", 2, None), ("ch01_s2", 1, None))))
            (ep / "production/renders.json").write_text(json.dumps(
                {"scenes": {"ch01_s1": {"video_url": clip.as_uri()}, "ch01_s2": {"video_url": clip.as_uri()}}}))
            (root / "channels/c/outro.json").write_text(json.dumps(
                {"seconds": 4, "text": "Subscribe.", "card": {"kind": "endcard", "wordmark": "umbra", "lines": ["SUBSCRIBE"]}}))
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(tool.main(["c", "e", "--no-vo"]), 0)
            self.assertIn("adding the channel outro", out.getvalue())
            cut = ep / "production/output/e-roughcut.mp4"
            self.assertAlmostEqual(tool.media_seconds(ffmpeg, cut), 7.0, delta=0.1)  # 3 s story + 4 s outro


    def test_a_short_clip_is_held_to_its_scene_length(self):
        ffmpeg = real_ffmpeg()
        with tempfile.TemporaryDirectory() as d:
            clip = Path(d) / "clip.mp4"
            subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=640x360:rate=24:duration=2",
                            "-pix_fmt", "yuv420p", str(clip)], check=True)
            for seconds, held in ((4, True), (1, False)):
                part = Path(d) / f"part{seconds}.mp4"
                self.assertEqual(tool.trim(ffmpeg, clip, seconds, part), held)
                self.assertAlmostEqual(tool.media_seconds(ffmpeg, part), seconds, delta=0.05)


if __name__ == "__main__":
    unittest.main()
