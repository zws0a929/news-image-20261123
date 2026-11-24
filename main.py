#!/usr/bin/env python3
"""Deliver the bounty entry image to the expected output location.

This entry is a newspaper front-page image for the "Sum up 23 November's
world news in one image" bounty. The image itself is entry.png, sitting
next to this script; this program's only job is to place an exact copy
of it at /output/entry.png so the grader can find it.

The copy is verified, not assumed: after copying we check that the
destination has the same byte size and the same SHA-256 digest as the
source. Any problem -- a missing source file, a short copy, a digest
mismatch -- aborts with a clear message on stderr and a non-zero exit
code, so a silent bad output can never slip through.
"""

import hashlib
import shutil
import sys
from pathlib import Path

OUTPUT_PATH = Path("/output/entry.png")
ENTRY_NAME = "entry.png"


def entry_path() -> Path:
    """Return the path of entry.png next to this script."""
    return Path(__file__).resolve().parent / ENTRY_NAME


def digest(path: Path) -> str:
    """Return the SHA-256 hex digest of the file at ``path``."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_verified(src: Path, dst: Path) -> tuple[int, str | None]:
    """Copy ``src`` to ``dst`` and verify the copy byte for byte.

    Returns ``(bytes_written, None)`` when the destination matches the
    source in both size and SHA-256 digest, otherwise ``(0, problem)``
    with a human-readable description of what does not match.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)

    src_size = src.stat().st_size
    dst_size = dst.stat().st_size
    if src_size != dst_size:
        return 0, f"size mismatch after copy: {src_size} != {dst_size}"
    if digest(src) != digest(dst):
        return 0, "sha256 mismatch after copy"
    return dst_size, None


def main() -> int:
    src = entry_path()
    if not src.is_file():
        print(f"ERROR: entry.png not found at {src}", file=sys.stderr)
        return 1

    dst = OUTPUT_PATH
    size, problem = copy_verified(src, dst)
    if problem is not None:
        print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    print(f"Wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
