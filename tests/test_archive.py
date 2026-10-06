"""Tests for tools/archive-to-drive.sh with a fake rclone (a local folder plays Google Drive) and a
fake curl: the archive is uploaded, checked and test-restored; --free deletes only media whose
contents are exactly what was archived, never credentials, source or history."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAKE_RCLONE = r"""#!/usr/bin/env bash
# fake rclone: "gd:" is $FAKE_DRIVE/<root-folder-id>/
set -e
cmd=$1; shift
root=""; args=()
while [ $# -gt 0 ]; do case "$1" in --drive-root-folder-id) root=$2; shift 2;; --one-way) shift;; *) args+=("$1"); shift;; esac; done
map() { case "$1" in gd:*) echo "$FAKE_DRIVE/$root/${1#gd:}";; *) echo "$1";; esac; }
case $cmd in
  listremotes) echo "gd:             drive";;
  copy) src=$(map "${args[0]}"); dst=$(map "${args[1]}"); mkdir -p "$dst"
        if [ -d "$src" ]; then cp -R "$src"/. "$dst"/; else cp "$src" "$dst"/; fi
        # simulate a render finishing mid-upload: same size, new bytes
        if [ -n "$FAKE_MUTATE" ] && [ ! -e "$FAKE_DRIVE/mutated" ]; then printf 'NEW!' > "$FAKE_MUTATE"; touch "$FAKE_DRIVE/mutated"; fi;;
  check) diff -r "$(map "${args[0]}")" "$(map "${args[1]}")" >/dev/null;;
esac
"""


@unittest.skipUnless(shutil.which("shasum") and shutil.which("git"), "needs git and shasum")
class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        d = Path(self.tmp.name)
        self.bin, self.drive, self.work, self.repo = d / "bin", d / "drive", d / "work", d / "repo"
        self.bin.mkdir()
        (self.bin / "rclone").write_text(FAKE_RCLONE)
        (self.bin / "curl").write_text("#!/bin/sh\nexit 22\n")  # no network in tests
        for f in ("rclone", "curl"):
            (self.bin / f).chmod(0o755)
        git = lambda *a: subprocess.run(["git", "-C", str(self.repo), *a], check=True, capture_output=True)
        self.repo.mkdir()
        git("init", "-q")
        git("config", "user.email", "t@t")
        git("config", "user.name", "t")
        (self.repo / "tools").mkdir()
        shutil.copy(ROOT / "tools/archive-to-drive.sh", self.repo / "tools/archive-to-drive.sh")
        (self.repo / "README.md").write_text("x\n")
        git("add", "-A")
        git("commit", "-qm", "init")
        prod = self.repo / "channels/umbra/episodes/ep03-ghost-characters/production"
        for sub in ("clips", "output", "vo/takes"):
            (prod / sub).mkdir(parents=True)
        self.clip = prod / "clips/ch01.mp4"
        self.clip.write_text("OLD!")
        (prod / "output/cut.mp4").write_text("video")
        (prod / "vo/takes/ch01.mp3").write_text("take")
        (prod / "vo/vo.lock").write_text("")
        (prod / "renders.json").write_text("{}")
        (self.repo / ".env.local").write_text("ELEVENLABS_API_KEY=secret\n")

    def run_script(self, *args, **env):
        e = {**os.environ, "PATH": f"{self.bin}:{os.environ['PATH']}", "FAKE_DRIVE": str(self.drive),
             "ARCHIVE_WORK": str(self.work), **env}
        return subprocess.run(["bash", str(self.repo / "tools/archive-to-drive.sh"), *args], env=e,
                              capture_output=True, text=True)

    def archived(self):
        folders = list((self.drive / "1-R3TgMpVOTjpxL73h1uzi0zl4JeSZ9mX").iterdir())
        self.assertEqual(len(folders), 1)
        return folders[0]

    def test_archive_verifies_then_free_removes_only_generated_media(self):
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stderr)
        folder = self.archived()
        self.assertEqual(sorted(p.name for p in folder.iterdir()),
                         ["MANIFEST.txt", "history.bundle", "media.tar.gz", "source.tar.gz"])
        listing = subprocess.run(["tar", "-tzf", str(folder / "media.tar.gz")], capture_output=True, text=True).stdout
        self.assertIn("clips/ch01.mp4", listing)
        self.assertNotIn(".env", listing)
        self.assertNotIn(".lock", listing)
        self.assertTrue(list((self.drive / "17ef8MgIcxCJegXDrm8ZeIw4NvxwrZ2AB").glob("*.manifest.txt")))
        r = self.run_script("--free")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.clip.exists())
        self.assertTrue((self.repo / ".env.local").exists())
        self.assertTrue((self.repo / "README.md").exists())
        self.assertTrue(self.clip.parent.parent.joinpath("renders.json").exists())

    def test_a_same_size_change_after_verification_blocks_free(self):
        self.assertEqual(self.run_script().returncode, 0)
        self.clip.write_text("NEW!")  # same size, new contents: not what the archive holds
        r = self.run_script("--free")
        self.assertEqual(r.returncode, 2)
        self.assertIn("changed since the verified archive", r.stderr)
        self.assertEqual(self.clip.read_text(), "NEW!")

    def test_a_change_during_the_upload_is_never_marked_verified(self):
        r = self.run_script(FAKE_MUTATE=str(self.clip))
        self.assertEqual(r.returncode, 2)
        self.assertIn("files changed while the archive was being made", r.stderr)
        r = self.run_script("--free")
        self.assertEqual(r.returncode, 2)
        self.assertTrue(self.clip.exists())

    def test_free_without_a_verified_archive_deletes_nothing(self):
        r = self.run_script("--free")
        self.assertEqual(r.returncode, 2)
        self.assertIn("no verified archive yet", r.stderr)
        self.assertTrue(self.clip.exists())


if __name__ == "__main__":
    unittest.main()
