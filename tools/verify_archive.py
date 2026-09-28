"""Verify every file listed in the frozen V1.0 archive manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    root = args.archive.resolve(strict=True)
    manifest_path = root / "02-qa" / "archive-file-hashes.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = set(manifest["files"]) | {"02-qa/archive-file-hashes.json"}
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if actual != expected:
        raise RuntimeError(f"Archive file set differs: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
    for relative, digest in manifest["files"].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"Archive hash mismatch: {relative}")
    print(json.dumps({"pass": True, "version": manifest["archiveVersion"], "files": len(actual)}))


if __name__ == "__main__":
    main()
