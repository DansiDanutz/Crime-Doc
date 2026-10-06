"""Tests for tools/cards.py and the EP03 script v2: card validation, drawing, overlay graph, and
the script rules the cards and per-chapter voiceover depend on."""
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "channels/umbra/episodes/ep03-ghost-characters"


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cards = load("cards")
assemble = load("assemble-episode")
SHOT = {"chapters": [{"id": "ch01", "scenes": [{"duration_s": 5}, {"duration_s": 5}]},
                     {"id": "ch02", "scenes": [{"duration_s": 10}]}]}


class CardPlanTests(unittest.TestCase):
    def test_times_become_absolute_and_ordered(self):
        placed = cards.plan([{"chapter": "ch02", "at": 1, "dur": 2, "kind": "question", "text": "WHY?"},
                             {"chapter": "ch01", "at": 0.5, "dur": 3, "kind": "stamp", "lines": ["1984"]}], SHOT)
        self.assertEqual([(c["start"], c["end"]) for c in placed], [(0.5, 3.5), (11.0, 13.0)])

    def test_bad_cards_are_refused_with_the_reason(self):
        ok = {"chapter": "ch01", "at": 0, "dur": 2, "kind": "question", "text": "WHY?"}
        for change, reason in (({"kind": "banner"}, "unknown kind"), ({"text": ""}, "missing text"),
                               ({"chapter": "ch09"}, "no chapter"), ({"at": 9.0}, "past the end"),
                               ({"dur": 0.5}, "dur between"), ({"text": "X" * 60}, "over 48"),
                               ({"kind": "tag", "role": "hero"}, "role must be")):
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                cards.plan([{**ok, **change}], SHOT)
        with self.assertRaisesRegex(ValueError, "overlap"):
            cards.plan([ok, {**ok, "at": 1.0}], SHOT)

    def test_overlay_graph_fades_each_card_in_at_its_time(self):
        placed = cards.plan([{"chapter": "ch02", "at": 1, "dur": 2, "kind": "question", "text": "WHY?"}], SHOT)
        graph, label = cards.overlay_filter(placed)
        self.assertEqual(label, "v0")
        self.assertIn("fade=in:st=0:d=0.25:alpha=1", graph)
        self.assertIn("fade=out:st=1.750", graph)
        self.assertIn("setpts=PTS-STARTPTS+11.000/TB", graph)
        self.assertIn("enable='between(t,11.000,13.000)'", graph)

    def test_every_kind_draws_a_transparent_frame(self):
        samples = {"stamp": {"lines": ["16 NOVEMBER 1984", "HAMBURG"]},
                   "tag": {"text": "WAU HOLLAND", "sub": "CCC", "role": "institution", "pos": "br"},
                   "figure": {"value": "GHOST CHARACTERS", "label": "THE SPILL"},
                   "question": {"text": "WHAT WOULD YOU EXPECT TO FIND IN THE MORNING?"},
                   "act": {"part": "PART I", "title": "THE PROMISE"},
                   "flag": {"label": "KEEP IN MIND", "text": "ONLY THE CLUB SAYS IT"},
                   "file": {"header": "REPORT 1985", "rows": ["BUG | CONFIRMED", "ON SCREEN | NOT ESTABLISHED"]},
                   "list": {"rows": ["ONE?", "TWO?", "THREE?"]}}
        self.assertEqual(set(samples), set(cards.KINDS))
        for kind, fields in samples.items():
            with self.subTest(kind=kind):
                img = cards.render({"kind": kind, **fields})
                self.assertEqual((img.size, img.mode), ((1280, 720), "RGBA"))
                alpha = img.getchannel("A")
                self.assertGreater(alpha.getbbox()[2] - alpha.getbbox()[0], 100)  # something was drawn
                self.assertEqual(alpha.getpixel((640, 2)) if kind != "act" else 0, 0)  # the rest stays clear


class Ep03Tests(unittest.TestCase):
    def setUp(self):
        self.shot = json.loads((EP / "production/shotlist.json").read_text())
        self.md = (EP / "02-script.md").read_text()
        self.segments = assemble.narration_segments(self.md)

    def test_ep03_cards_are_valid_and_carry_the_questions(self):
        placed = cards.load(EP, self.shot)
        self.assertEqual(len(placed), 27)
        self.assertEqual([c["chapter"] for c in placed if c["kind"] == "question"],
                         ["ch02", "ch05", "ch11", "ch15", "ch17", "ch20"])
        self.assertEqual([c["title"] for c in placed if c["kind"] == "act"],
                         ["THE PROMISE", "THE FLAW", "THE NIGHT", "THE RETURN", "THE DOUBT"])
        self.assertLessEqual(placed[-1]["end"], 300)

    def test_every_chapter_has_narration_that_fits_its_window(self):
        windows = cards.chapter_windows(self.shot)
        self.assertEqual([c for c, _ in self.segments], list(windows))
        for chapter, text in self.segments:
            with self.subTest(chapter=chapter):
                self.assertLessEqual(len(text.split()) / 2.5, windows[chapter][1] - 0.2)  # DNA pace, 2.5 words/s
        self.assertEqual(sum(len(t.split()) for _, t in self.segments), 698)

    def test_script_keeps_the_dna_rules_and_the_mystery(self):
        body = " ".join(t for _, t in self.segments)
        for banned in ("in this video", "today we're going", "have you ever wondered"):
            self.assertNotIn(banned, body.lower())
        self.assertTrue(self.segments[0][1].startswith("It's the night of the 16th of November, 1984. In a flat in Hamburg"))
        self.assertIn("This is the story of a password", self.segments[1][1])
        asked = [c for c, t in self.segments if "?" in t]
        self.assertEqual(asked, ["ch05", "ch11", "ch13", "ch15", "ch17", "ch20"])
        last = re.split(r"(?<=[.?!])\s+", self.segments[-1][1])[-1]
        self.assertLessEqual(len(last.split()), 12)
        self.assertTrue(last.endswith("page."))

    def test_segments_without_markers_and_bad_markers(self):
        self.assertEqual(assemble.narration_segments("# x\n\n---\n\nOne. Two.\n\n---\n"), [(None, "One. Two.")])
        with self.assertRaisesRegex(ValueError, "before the first"):
            assemble.narration_segments("# x\n\n---\n\nStray.\n<!-- ch01 -->\nOne.\n\n---\n")
        with self.assertRaisesRegex(ValueError, "twice"):
            assemble.narration_segments("# x\n\n---\n\n<!-- ch01 -->\nA.\n<!-- ch01 -->\nB.\n\n---\n")


if __name__ == "__main__":
    unittest.main()
