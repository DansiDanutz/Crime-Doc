import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_tool(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ToolRegressionTests(unittest.TestCase):
    def test_every_character_reference_must_resolve(self):
        tool = load_tool("build-shotlist")
        manifest = [{"id": "ada_lovelace", "aliases": ["ada lovelace"]}]
        self.assertEqual(tool.resolve_characters("Ada Lovelace (centered)", manifest), ["ada_lovelace"])
        with self.assertRaisesRegex(ValueError, "unknown person"):
            tool.resolve_characters("Ada Lovelace, Unknown Person", manifest)
        self.assertEqual(tool.resolve_characters("Civilians / crowd only", []), [])

    def test_ep03_investigator_scenes_list_only_the_investigator(self):
        # "Postal Investigator" once also matched the Bundespost Official through a "postal" alias.
        import json
        shotlist = json.loads((ROOT / "channels/umbra/episodes/ep03-ghost-characters/production/shotlist.json").read_text())
        scenes = {sc["id"]: sc for ch in shotlist["chapters"] for sc in ch["scenes"]}
        for scene_id in ("ch13_s3", "ch18_s1"):
            self.assertEqual(scenes[scene_id]["characters"], ["investigator"], scene_id)

    def test_ep03_prompts_keep_the_caption_and_face_safeguards(self):
        # Preview renders printed direction lines as captions (ch05_s3) and gave the Hacker a
        # face (ch08_s4); these guards keep those instructions in the generated prompts.
        import json
        shotlist = json.loads((ROOT / "channels/umbra/episodes/ep03-ghost-characters/production/shotlist.json").read_text())
        scenes = {sc["id"]: sc for ch in shotlist["chapters"] for sc in ch["scenes"]}
        flat = {k: (" ".join(v["image_prompt"].split()), " ".join(v["video_prompt"].split())) for k, v in scenes.items()}
        late = [k for k in scenes if int(k[2:4]) >= 9]
        self.assertEqual(len(late), 54)
        for scene_id in late:
            self.assertIn("No captions, titles or subtitle text", flat[scene_id][1], scene_id)
        faces = [k for k in late if "the_hacker" in scenes[k]["characters"] and "mannequin hands" not in flat[k][0]]
        self.assertEqual(len(faces), 9)
        for scene_id in faces:
            self.assertIn("featureless", flat[scene_id][0], scene_id)
        self.assertNotIn("Saying is not proving", flat["ch05_s3"][1])
        self.assertIn("no text or lettering", flat["ch05_s3"][0])
        self.assertIn("No captions", flat["ch05_s3"][1])
        self.assertIn("featureless", flat["ch08_s4"][0])
        self.assertIn("no eyes, nose, mouth", flat["ch08_s4"][0])
        self.assertIn("seated naturally", flat["ch08_s2"][0])
        for scene_id in [k for k in scenes if int(k[2:4]) >= 5]:
            self.assertNotIn("Mode B", flat[scene_id][0], scene_id)

    def test_reuse_must_name_an_earlier_scene_that_is_not_itself_a_reuse(self):
        tool = load_tool("build-shotlist")
        def md(*scenes):
            body = ["## CHAPTER 01 — t  (0:00–0:15)"]
            for sid, reuse in scenes:
                body += [f"### Scene {sid} — 3s — x", "1. **CHARACTERS IN SCENE:** No recurring characters",
                         "2. **IMAGE PROMPT:**", "```", "img", "```", "3. **VIDEO PROMPT:**", "```", "vid", "```"]
                if reuse:
                    body.append(f"4. **REUSE:** {reuse} — why")
            return "\n".join(body)
        chapters = tool.parse_scenes_md(md(("ch01_s1", None), ("ch01_s2", "ch01_s1")))
        self.assertEqual(chapters[0]["scenes"][1]["reuse"], "ch01_s1")
        self.assertNotIn("reuse", chapters[0]["scenes"][0])
        with self.assertRaisesRegex(ValueError, "unknown scene"):
            tool.parse_scenes_md(md(("ch01_s1", "ch09_s9")))
        with self.assertRaisesRegex(ValueError, "earlier scene"):
            tool.parse_scenes_md(md(("ch01_s1", "ch01_s2"), ("ch01_s2", None)))
        with self.assertRaisesRegex(ValueError, "itself a reuse"):
            tool.parse_scenes_md(md(("ch01_s1", None), ("ch01_s2", "ch01_s1"), ("ch01_s3", "ch01_s2")))

    def test_ep03_reuses_twelve_existing_clips(self):
        import json
        shotlist = json.loads((ROOT / "channels/umbra/episodes/ep03-ghost-characters/production/shotlist.json").read_text())
        reuse = {sc["id"]: sc["reuse"] for ch in shotlist["chapters"] for sc in ch["scenes"] if sc.get("reuse")}
        self.assertEqual(len(reuse), 12)
        self.assertEqual(reuse["ch15_s4"], "ch04_s5")  # the stamped SECURE seal
        self.assertEqual(reuse["ch20_s3"], "ch08_s3")  # the login on the old CRT

    def test_yaml_reader_decodes_quotes_and_comments(self):
        tool = load_tool("export-episode")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "episode.yaml"
            path.write_text(
                'title: "She said \\"Crime #1\\"" # note\n'
                "subject: operator's story # subject note\n"
                "duration_minutes: 5 # 1-10\n"
            )
            self.assertEqual(tool.read_yaml_lite(path), {
                "title": 'She said "Crime #1"',
                "subject": "operator's story",
                "duration_minutes": "5",
            })

    def test_scaffolder_rejects_traversal_before_writing(self):
        result = subprocess.run(
            ["bash", "tools/new-episode.sh", "umbra", "../../escaped"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((ROOT / "channels" / "escaped").exists())

    def test_scaffolder_preserves_literal_title(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self._minimal_workspace(directory)
            title = 'Crime "Quote" # Mystery & Punishment / Redux \\n literal'
            result = subprocess.run(
                ["bash", "tools/new-episode.sh", "umbra", "special", title],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = root / "channels" / "umbra" / "episodes" / "ep01-special" / "episode.yaml"
            self.assertEqual(load_tool("export-episode").read_yaml_lite(metadata)["title"], title)

    def test_long_title_leaves_no_partial_scaffold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self._minimal_workspace(directory)
            result = subprocess.run(
                ["bash", "tools/new-episode.sh", "umbra", "retry-check", "x" * 201],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "channels" / "umbra" / "episodes" / "ep01-retry-check").exists())

    def test_multiline_title_leaves_no_partial_scaffold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self._minimal_workspace(directory)
            for separator in ("\n", "\r", "\u0085", "\u2028", "\u2029"):
                with self.subTest(separator=repr(separator)):
                    result = subprocess.run(
                        ["bash", "tools/new-episode.sh", "umbra", "line-check", f"First{separator}Second"],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse((root / "channels" / "umbra" / "episodes" / "ep01-line-check").exists())

    @staticmethod
    def _minimal_workspace(directory: str) -> Path:
        root = Path(directory)
        (root / "tools").mkdir()
        (root / "templates" / "episode" / "production").mkdir(parents=True)
        (root / "channels" / "umbra" / "episodes").mkdir(parents=True)
        shutil.copy(ROOT / "tools" / "new-episode.sh", root / "tools")
        (root / "templates" / "episode" / "episode.yaml").write_text(
            'slug: EPISODE_SLUG\nchannel: CHANNEL_NAME\ntitle: "" # title\ncreated: "" # date\n'
        )
        (root / "templates" / "episode" / "production" / "shotlist.json").write_text(
            '{"episode":"EPISODE_SLUG","channel":"CHANNEL_NAME"}\n'
        )
        return root


if __name__ == "__main__":
    unittest.main()
