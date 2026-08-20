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
