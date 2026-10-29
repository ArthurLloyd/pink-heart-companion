"""Scan tracked files, Git history and optional release packages for private data.

Findings show relative filenames and categories, never the matched private values.
This pattern/metadata check supplements human review; it is not a proof that every
possible form of sensitive information is absent.
"""

from __future__ import annotations

import argparse
import io
import re
import subprocess
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "personal-home-path": re.compile(
        r"(?i)(?:[a-z]:[\\/]+users[\\/]+[^\s/\\`]+|/(?:Users|home)/[^\s/`]+/)"),
    "local-workspace-path": re.compile(r"(?i)[a-z]:[\\/]+(?:Project|Downloads|AI)[\\/]+"),
    "credential": re.compile(
        r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
        r"sk-[A-Za-z0-9_-]{24,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)"),
    "session-id": re.compile(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"),
    "email-address": re.compile(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b"),
}
IMAGE_TYPES = {".png", ".gif", ".webp"}
IMAGE_METADATA = {"exif", "xmp", "XML:com.adobe.xmp", "comment", "icc_profile"}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def inspect(name: str, data: bytes) -> list[str]:
    if Path(name).suffix.lower() in IMAGE_TYPES:
        with Image.open(io.BytesIO(data)) as image:
            fields = set(image.info) & IMAGE_METADATA
            if image.format == "PNG":
                fields |= set(image.text)
            return [f"{name}: embedded image metadata ({key})" for key in sorted(fields)]
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return [f"{name}: unrecognized binary file requires manual review"]
    return [f"{name}:{number}: {category}"
            for number, line in enumerate(text.splitlines(), 1)
            for category, pattern in PATTERNS.items() if pattern.search(line)]


def audit(distribution: Path | None = None) -> list[str]:
    findings = []
    current = [name for name in git("ls-files", "-z").decode("utf-8").split("\0") if name]
    for name in current:
        findings.extend(inspect(name, (ROOT / name).read_bytes()))

    seen = set()
    commits = git("rev-list", "--all").decode("ascii").splitlines()
    for commit in commits:
        for row in git("ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
            if not row:
                continue
            metadata, filename = row.split(b"\t", 1)
            mode, kind, blob = metadata.split()
            if kind != b"blob":
                findings.append(f"history/{commit[:7]}: unexpected non-blob entry")
                continue
            if blob in seen:
                continue
            seen.add(blob)
            name = filename.decode("utf-8")
            findings.extend(inspect(f"history/{commit[:7]}/{name}", git("cat-file", "blob", blob.decode())))
        emails = git("show", "-s", "--format=%ae%n%ce", commit).decode("utf-8").splitlines()
        if any(not email.endswith("@users.noreply.github.com") for email in emails):
            findings.append(f"history/{commit[:7]}: author/committer email requires manual review")

    if distribution:
        for path in sorted(distribution.iterdir()):
            if not path.is_file():
                continue
            if path.suffix == ".zip":
                with zipfile.ZipFile(path) as archive:
                    for name in archive.namelist():
                        if name.startswith(("/", "\\")) or ".." in Path(name).parts:
                            findings.append(f"{path.name}: unsafe ZIP member path")
                        if not name.endswith("/"):
                            findings.extend(inspect(f"{path.name}/{name}", archive.read(name)))
            else:
                findings.extend(inspect(path.name, path.read_bytes()))
    print(f"Checked {len(current)} tracked files, {len(commits)} commits, {len(seen)} historical blobs")
    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, help="Also inspect generated release files")
    args = parser.parse_args()
    results = audit(args.dist)
    for finding in results:
        print(finding)
    print("PASS" if not results else f"FAIL: {len(results)} findings require review")
    raise SystemExit(bool(results))
