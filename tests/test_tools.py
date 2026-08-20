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
    def test_dynamic_character_ids_are_resolved(self):
        tool = load_tool("build-shotlist")
        self.assertEqual(
            tool.resolve_characters("Ada Lovelace (centered)", ["ada_lovelace"]),
            ["ada_lovelace"],
        )
        with self.assertRaisesRegex(ValueError, "unresolved character"):
            tool.resolve_characters("Unknown Person", ["ada_lovelace"])
        with self.assertRaisesRegex(ValueError, "unknown person"):
            tool.resolve_characters("Ada Lovelace, Unknown Person", ["ada_lovelace"])

    def test_yaml_reader_removes_only_unquoted_comments(self):
        tool = load_tool("export-episode")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "episode.yaml"
            path.write_text(
                'title: "She said \\"Crime #1\\"" # note\n'
                "subject: operator's story # subject note\n"
                'duration_minutes: 5 # 1-10\n'
            )
            self.assertEqual(
                tool.read_yaml_lite(path),
                {
                    "title": 'She said "Crime #1"',
                    "subject": "operator's story",
                    "duration_minutes": "5",
                },
            )

    def test_scaffolder_rejects_traversal_before_writing(self):
        result = subprocess.run(
            ["bash", "tools/new-episode.sh", "umbra", "../../escaped"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("slug must match", result.stderr)
        self.assertFalse((ROOT / "channels" / "escaped").exists())

    def test_scaffolder_preserves_title_replacement_characters(self):
        with tempfile.TemporaryDirectory() as directory:
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
            result = subprocess.run(
                ["bash", "tools/new-episode.sh", "umbra", "special", "Crime & Punishment / Redux"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = (root / "channels" / "umbra" / "episodes" / "ep01-special" / "episode.yaml").read_text()
            self.assertIn('title: "Crime & Punishment / Redux"', metadata)

    def test_scaffolder_rejects_long_title_without_partial_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            (root / "templates" / "episode").mkdir(parents=True)
            (root / "channels" / "umbra" / "episodes").mkdir(parents=True)
            shutil.copy(ROOT / "tools" / "new-episode.sh", root / "tools")
            result = subprocess.run(
                ["bash", "tools/new-episode.sh", "umbra", "retry-check", "x" * 201],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "channels" / "umbra" / "episodes" / "ep01-retry-check").exists())


if __name__ == "__main__":
    unittest.main()
