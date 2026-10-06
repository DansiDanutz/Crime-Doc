"""Tests for tools/assemble-episode.py: the edit plan (order, durations, REUSE) and the script text.

The ffmpeg steps are exercised by hand on real clips; CI has no ffmpeg, so these tests cover the
decisions that determine what goes into the cut.
"""
import importlib.util
import json
import unittest
from pathlib import Path

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
        self.assertEqual(len(narration.split()), 732)


if __name__ == "__main__":
    unittest.main()
