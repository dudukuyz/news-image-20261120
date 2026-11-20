#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

The poster image is built ahead of time (see render_poster.py) and shipped
in this repository as entry.png. This program only places that image where
the grader expects it: /output/entry.png (or $MAKEFUN_OUTPUT_DIR when the
variable is set, which is how the kit runs it locally).

Standard library only, no network, deterministic: every run copies the
same bytes, so the two grading runs agree byte for byte.
"""

import hashlib
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
MAX_BYTES = 1_048_576  # the gate's 1 MiB cap


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_png(path):
    """Refuse to ship a file the gate would reject: not a PNG, or too big."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"entry image is not a PNG: {path}")
    width, height = struct.unpack(">II", head[16:24])
    if width > 1024 or height > 1024:
        raise ValueError(f"entry image too large: {width}x{height}")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError(f"entry image over 1 MiB: {path.stat().st_size} bytes")
    return width, height


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing: {SOURCE}")
    width, height = _check_png(SOURCE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUTPUT_DIR / "entry.png"
    shutil.copyfile(SOURCE, dest)
    if _sha256(dest) != _sha256(SOURCE):
        raise IOError(f"entry image copy corrupt: {dest}")
    print(f"wrote {dest} ({width}x{height}, {_sha256(dest)[:12]}...)")


if __name__ == "__main__":
    main()
