"""Validate the current local Codex Desktop V1 pet payload.

The V1 geometry was checked in OpenAI.Codex 26.924.2738.0 and rechecked
in 26.1023.6123.0. See docs/compatibility.md for evidence and limits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image


STATES = [
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
]
EXPECTED_FILES = {"pet.json", "spritesheet.webp"}
EXPECTED_FIELDS = {
    "id",
    "displayName",
    "description",
    "spriteVersionNumber",
    "spritesheetPath",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def webp_chunks(blob: bytes) -> list[str]:
    if blob[:4] != b"RIFF" or blob[8:12] != b"WEBP":
        raise ValueError("Not a WebP RIFF file")
    chunks = []
    offset = 12
    while offset + 8 <= len(blob):
        tag = blob[offset : offset + 4].decode("ascii")
        size = int.from_bytes(blob[offset + 4 : offset + 8], "little")
        end = offset + 8 + size
        if end > len(blob):
            raise ValueError("Malformed WebP chunk length")
        chunks.append(tag)
        offset = end + (size & 1)
    if offset != len(blob):
        raise ValueError("Malformed WebP trailing bytes")
    return chunks


def validate(package: Path) -> dict:
    package = package.resolve(strict=True)
    files = {p.name for p in package.iterdir() if p.is_file()}
    if files != EXPECTED_FILES or any(p.is_dir() for p in package.iterdir()):
        raise ValueError(f"Payload must contain exactly two files; found {sorted(files)}")

    manifest_path = package / "pet.json"
    image_path = package / "spritesheet.webp"
    raw_manifest = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(raw_manifest)
    if set(manifest) != EXPECTED_FIELDS:
        raise ValueError("Unexpected manifest fields")
    if manifest != {
        "id": "pink-heart-companion",
        "displayName": "Pink Heart Companion",
        "description": "A gentle pink-themed chibi companion for Codex Desktop.",
        "spriteVersionNumber": 1,
        "spritesheetPath": "spritesheet.webp",
    }:
        raise ValueError("Manifest does not match the approved V1 identity and path")
    if type(manifest["spriteVersionNumber"]) is not int:
        raise ValueError("spriteVersionNumber must be an integer")
    private_patterns = [
        r"(?i)[a-z]:\\users\\",
        r"(?i)(?:^|\W)/(?:users|home)/[^/\s]+/",
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        r"(?i)\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b",
        r"(?i)(?:api[-_]?key|password|access[-_]?token)",
    ]
    if any(re.search(p, raw_manifest) for p in private_patterns):
        raise ValueError("Manifest contains potentially private text")

    blob = image_path.read_bytes()
    chunks = webp_chunks(blob)
    if chunks != ["VP8L"]:
        raise ValueError(f"Expected metadata-free lossless WebP; found {chunks}")
    if len(blob) > 20 * 1024 * 1024:
        raise ValueError("WebP exceeds the current UI's 20 MiB limit")
    with Image.open(image_path) as decoded:
        if decoded.format != "WEBP" or decoded.size != (1536, 1872):
            raise ValueError("V1 atlas format or dimensions mismatch")
        rgba = np.asarray(decoded.convert("RGBA"))

    alpha = rgba[:, :, 3]
    hidden_rgb = int(np.count_nonzero((alpha == 0) & np.any(rgba[:, :, :3] != 0, axis=2)))
    if hidden_rgb:
        raise ValueError(f"Hidden RGB pixels: {hidden_rgb}")
    if not np.any(alpha == 0) or not np.any(alpha > 0):
        raise ValueError("Expected both transparent and visible pixels")

    row_results = []
    min_margin = 999
    for row, (name, used) in enumerate(STATES):
        frame_counts = []
        for col in range(8):
            cell = alpha[row * 208 : (row + 1) * 208, col * 192 : (col + 1) * 192]
            visible = int(np.count_nonzero(cell))
            if col < used:
                if visible == 0:
                    raise ValueError(f"Empty used frame: {name} {col}")
                ys, xs = np.nonzero(cell)
                margin = min(int(xs.min()), int(191 - xs.max()), int(ys.min()), int(207 - ys.max()))
                min_margin = min(min_margin, margin)
                frame_counts.append(visible)
            elif visible or np.any(rgba[row * 208 : (row + 1) * 208, col * 192 : (col + 1) * 192]):
                raise ValueError(f"Nonempty unused cell: {name} {col}")
        row_results.append({"state": name, "rowIndex": row, "usedFrames": used, "visiblePixelsByFrame": frame_counts})
    if min_margin < 8:
        raise ValueError(f"Unsafe cell margin: {min_margin} px")

    return {
        "pass": True,
        "contract": "running Codex Desktop V1",
        "manifest": manifest,
        "atlas": {
            "format": "WEBP",
            "webpSubtype": "VP8L lossless",
            "width": 1536,
            "height": 1872,
            "cellWidth": 192,
            "cellHeight": 208,
            "columns": 8,
            "rows": 9,
            "hasAlpha": True,
            "transparentPixels": int(np.count_nonzero(alpha == 0)),
            "hiddenRgbPixels": hidden_rgb,
            "minimumUsedCellMarginPx": min_margin,
            "chunks": chunks,
            "fileBytes": len(blob),
        },
        "states": row_results,
        "privacy": {"manifestPatterns": "none", "embeddedWebpMetadata": False, "payloadFilesOnly": True},
        "sha256": {"pet.json": sha256(manifest_path), "spritesheet.webp": sha256(image_path)},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = validate(args.package)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": True, "sha256": result["sha256"], "minimumMarginPx": result["atlas"]["minimumUsedCellMarginPx"]}))


if __name__ == "__main__":
    main()
