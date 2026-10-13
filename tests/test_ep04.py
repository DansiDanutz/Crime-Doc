"""EP04 "The Seventy-Five Cent Spy": built entirely from EP03's rendered clips (no render credits),
with the script, cards and sound plan kept inside the DNA rules."""
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "channels/umbra/episodes/ep04-seventy-five-cents"
EP3 = ROOT / "channels/umbra/episodes/ep03-ghost-characters"


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


assemble, cards, soundtrack = load("assemble-episode"), load("cards"), load("soundtrack")


class Ep04Tests(unittest.TestCase):
    def setUp(self):
        self.shot = json.loads((EP / "production/shotlist.json").read_text())
        self.segments = assemble.narration_segments((EP / "02-script.md").read_text())

    def test_every_scene_borrows_an_ep03_clip_and_none_that_shows_ep03_text(self):
        ep3 = json.loads((EP3 / "production/shotlist.json").read_text())
        own = {sc["id"] for ch in ep3["chapters"] for sc in ch["scenes"] if not sc.get("reuse")}
        scenes = [sc for ch in self.shot["chapters"] for sc in ch["scenes"]]
        self.assertEqual((len(scenes), sum(int(s["duration_s"]) for s in scenes)), (90, 300))
        for sc in scenes:
            slug, sid = sc["reuse"].split("/")
            self.assertEqual(slug, "ep03-ghost-characters")
            self.assertIn(sid, own, sc["id"])  # a clip EP03 actually rendered
            self.assertNotIn(sid, {"ch04_s5", "ch10_s1", "ch09_s1", "ch14_s2", "ch12_s1", "ch12_s2"}, sc["id"])

    def test_the_script_fits_and_keeps_the_dna_rules(self):
        windows = cards.chapter_windows(self.shot)
        self.assertEqual([c for c, _ in self.segments], list(windows))
        for chapter, text in self.segments:
            self.assertLessEqual(len(text.split()) / 2.5, windows[chapter][1] - 0.2, chapter)
        body = " ".join(t for _, t in self.segments).lower()
        for banned in ("in this video", "today we're going", "have you ever wondered", "subscribe"):
            self.assertNotIn(banned, body)
        self.assertTrue(self.segments[0][1].startswith("It's the summer of 1986. In a flat in Hanover"))
        self.assertIn("This is the story of", self.segments[1][1])
        last = re.split(r"(?<=[.?!])\s+", self.segments[-1][1])[-1]
        self.assertLessEqual(len(last.split()), 12)
        self.assertTrue(last.endswith("1989."))

    def test_cards_and_sound_plan_are_valid(self):
        placed = cards.load(EP, self.shot)
        self.assertEqual(len(placed), 25)
        cues, total = soundtrack.load_plan(EP)
        self.assertEqual(total, 312.0)
        # every cue is word-for-word one EP03 already recorded, so it is copied, not paid for
        ep3_keys = {soundtrack.fingerprint(c) for c in soundtrack.load_plan(EP3)[0]}
        self.assertTrue(all(soundtrack.fingerprint(c) in ep3_keys for c in cues))


if __name__ == "__main__":
    unittest.main()
