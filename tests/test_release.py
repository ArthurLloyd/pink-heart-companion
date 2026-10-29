"""Exercise the distributable ZIP in isolated homes, never the real Codex home."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_release import build  # noqa: E402
from validate_pet import validate  # noqa: E402

POWERSHELL = shutil.which("powershell.exe")


class ReleaseTests(unittest.TestCase):
    def test_deterministic_packages_and_checksums(self):
        with tempfile.TemporaryDirectory(prefix="pink-heart-build-") as tmp:
            first = build(Path(tmp) / "first")
            second = build(Path(tmp) / "second")
            self.assertEqual([p.name for p in first], [p.name for p in second])
            self.assertEqual([p.read_bytes() for p in first], [p.read_bytes() for p in second])
            sums = first[-1].read_text(encoding="ascii").splitlines()
            for line in sums:
                expected, name = line.split("  ")
                self.assertEqual(expected, hashlib.sha256((first[0].parent / name).read_bytes()).hexdigest())
            with zipfile.ZipFile(first[0]) as archive:
                for line in archive.read("PAYLOAD-SHA256SUMS.txt").decode("ascii").splitlines():
                    expected, name = line.split("  ")
                    self.assertEqual(expected, hashlib.sha256(archive.read(name)).hexdigest())
            with zipfile.ZipFile(first[1]) as archive:
                self.assertEqual(sorted(archive.namelist()), [
                    "pink-heart-companion/pet.json", "pink-heart-companion/spritesheet.webp"])
                archive.extractall(Path(tmp) / "portable")
            self.assertTrue(validate(Path(tmp) / "portable" / "pink-heart-companion")["pass"])


@unittest.skipUnless(os.name == "nt" and POWERSHELL, "Windows PowerShell required")
class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release_tmp = tempfile.TemporaryDirectory(prefix="pink-heart-release-")
        output = Path(cls.release_tmp.name)
        windows = build(output / "artifacts")[0]
        cls.package = output / "extracted package 中文"
        with zipfile.ZipFile(windows) as archive:
            archive.extractall(cls.package)

    @classmethod
    def tearDownClass(cls):
        cls.release_tmp.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="pink-heart-install-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.codex_home = self.root / "Codex home 中文"
        self.target = self.codex_home / "pets" / "pink-heart-companion"
        self.env = os.environ.copy()
        self.env["CODEX_HOME"] = str(self.codex_home)
        self.env["USERPROFILE"] = str(self.root / "isolated user")
        self.env["PINK_HEART_NO_PAUSE"] = "1"

    def run_script(self, name="Install", *args, success=True, package=None):
        result = subprocess.run([
            POWERSHELL, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", str((package or self.package) / "scripts" / f"{name}.ps1"), *args,
        ], env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        self.assertEqual(result.returncode, 0 if success else 1,
                         (result.stdout + result.stderr).decode(errors="replace"))
        return result

    def test_install_reinstall_uninstall_and_other_pet_preserved(self):
        other = self.codex_home / "pets" / "other-pet"
        other.mkdir(parents=True)
        (other / "keep.txt").write_text("keep", encoding="utf-8")
        self.run_script()
        validate(self.target)
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.target.iterdir()}
        self.run_script()
        self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
                                  for p in self.target.iterdir()})
        self.assertEqual(sorted(p.name for p in self.target.parent.iterdir()),
                         ["other-pet", "pink-heart-companion"])
        self.run_script("Uninstall")
        self.run_script("Uninstall")
        self.assertFalse(self.target.exists())
        self.assertEqual((other / "keep.txt").read_text(), "keep")

    def test_explicit_home_overrides_environment(self):
        explicit = self.root / "explicit home"
        self.run_script("Install", "-CodexHome", str(explicit))
        self.assertFalse(self.target.exists())
        validate(explicit / "pets" / "pink-heart-companion")
        self.run_script("Uninstall", "-CodexHome", str(explicit))

    def test_default_userprofile_home(self):
        del self.env["CODEX_HOME"]
        self.run_script()
        target = Path(self.env["USERPROFILE"]) / ".codex" / "pets" / "pink-heart-companion"
        validate(target)
        self.run_script("Uninstall")
        self.assertFalse(target.exists())

    def test_tampered_payload_rejected_before_writing(self):
        broken = self.root / "broken package"
        shutil.copytree(self.package, broken)
        (broken / "release" / "pink-heart-companion" / "pet.json").write_text("{}")
        result = self.run_script(package=broken, success=False)
        self.assertIn(b'File differs from the approved pet', result.stderr)
        self.assertFalse(self.codex_home.exists())

    def test_existing_custom_content_preserved(self):
        self.target.mkdir(parents=True)
        custom = self.target / "my-work.txt"
        custom.write_text("preserve")
        result = self.run_script(success=False)
        self.assertIn(b'Expected exactly pet.json and spritesheet.webp', result.stderr)
        result = self.run_script("Uninstall", success=False)
        self.assertIn(b'Expected exactly pet.json and spritesheet.webp', result.stderr)
        self.assertEqual(custom.read_text(), "preserve")

    def test_extra_file_prevents_uninstall(self):
        self.run_script()
        (self.target / "keep.txt").write_text("preserve")
        self.run_script("Uninstall", success=False)
        self.assertEqual(len(list(self.target.iterdir())), 3)

    def test_modified_installed_asset_prevents_uninstall(self):
        self.run_script()
        sprite = self.target / "spritesheet.webp"
        sprite.write_bytes(b"modified")
        self.run_script("Uninstall", success=False)
        self.assertEqual(sprite.read_bytes(), b"modified")
        self.assertTrue((self.target / "pet.json").exists())

    def test_relative_home_rejected(self):
        for value in ("relative", "C:drive-relative", "\\root-relative"):
            result = self.run_script("Install", "-CodexHome", value, success=False)
            self.assertIn(b'must be an absolute filesystem path', result.stderr)
        self.assertFalse(self.target.exists())

    def test_cmd_entrypoints(self):
        for name in ("install.cmd", "uninstall.cmd"):
            result = subprocess.run(["cmd.exe", "/d", "/c", name], cwd=self.package,
                                    env=self.env, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(self.target.exists(), name == "install.cmd")

    def test_cmd_propagates_failure(self):
        self.target.mkdir(parents=True)
        (self.target / "keep.txt").write_text("preserve")
        result = subprocess.run(["cmd.exe", "/d", "/c", "install.cmd"], cwd=self.package,
                                env=self.env, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 1)
        self.assertTrue((self.target / "keep.txt").exists())

    def test_junction_destination_refused(self):
        outside = self.root / "outside"
        shutil.copytree(self.package / "release" / "pink-heart-companion", outside)
        self.target.parent.mkdir(parents=True)
        result = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J",
                                 str(self.target), str(outside)], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        try:
            result = self.run_script(success=False)
            self.assertIn(b'no symlink or junction', result.stderr)
            result = self.run_script("Uninstall", success=False)
            self.assertIn(b'no symlink or junction', result.stderr)
            validate(outside)
        finally:
            self.target.rmdir()  # Remove junction itself, never its contents.


if __name__ == "__main__":
    unittest.main()
