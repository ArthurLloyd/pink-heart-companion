"""Build deterministic, offline release ZIPs from the approved pet payload."""

from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path

from validate_pet import validate

ROOT = Path(__file__).resolve().parents[1]
STAMP = (2026, 10, 29, 0, 0, 0)
PAYLOAD = ROOT / "release" / "pink-heart-companion"
WINDOWS_FILES = [
    "install.cmd",
    "uninstall.cmd",
    "scripts/Install.ps1",
    "scripts/Uninstall.ps1",
    "scripts/PetPackage.ps1",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_zip(path: Path, files: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compresslevel=9)
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise RuntimeError(f"Corrupt ZIP: {path}")
        if {name: archive.read(name) for name in archive.namelist()} != files:
            raise RuntimeError(f"ZIP contents differ: {path}")


def build(output: Path) -> list[Path]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must be a numeric semantic version")
    validate(PAYLOAD)
    output.mkdir(parents=True, exist_ok=True)
    stem = f"pink-heart-companion-v{version}"
    pet_files = {f"pink-heart-companion/{name}": (PAYLOAD / name).read_bytes()
                 for name in ("pet.json", "spritesheet.webp")}
    payload_sums = "".join(f"{digest(data)}  release/{name}\n" for name, data in sorted(pet_files.items()))
    windows_files = {name: (ROOT / name).read_bytes() for name in WINDOWS_FILES}
    windows_files.update({f"release/{name}": data for name, data in pet_files.items()})
    windows_files["INSTALL.txt"] = (ROOT / "docs" / "INSTALL.txt").read_bytes()
    windows_files["PAYLOAD-SHA256SUMS.txt"] = payload_sums.encode("ascii")

    # Keep .cmd files usable in cmd.exe regardless of Git checkout line endings.
    for name in ("install.cmd", "uninstall.cmd"):
        windows_files[name] = windows_files[name].replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")

    windows = output / f"{stem}-windows.zip"
    portable = output / f"{stem}-portable.zip"
    sprite = output / f"{stem}.webp"
    make_zip(windows, windows_files)
    make_zip(portable, pet_files)
    sprite.write_bytes((PAYLOAD / "spritesheet.webp").read_bytes())
    artifacts = [windows, portable, sprite]
    sums = output / "SHA256SUMS.txt"
    sums.write_text("".join(f"{digest(path.read_bytes())}  {path.name}\n" for path in artifacts),
                    encoding="ascii", newline="\n")
    artifacts.append(sums)
    return artifacts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for artifact in build(args.output.resolve()):
        print(f"{artifact.name}: {artifact.stat().st_size:,} bytes")
