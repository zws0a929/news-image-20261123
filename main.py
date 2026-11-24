#!/usr/bin/env python3
"""Copy the bounty entry image (entry.png) to /output/entry.png.

Deterministic: the output is a byte-for-byte copy of entry.png next to
this script. Fails loudly if entry.png is missing or the copy is
incomplete.
"""

import hashlib
import shutil
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    src = Path(__file__).parent / "entry.png"
    if not src.is_file():
        print(f"ERROR: entry.png not found at {src}", file=sys.stderr)
        return 1

    dst = Path("/output/entry.png")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)

    src_size = src.stat().st_size
    dst_size = dst.stat().st_size
    if src_size != dst_size:
        print(
            f"ERROR: size mismatch after copy: {src_size} != {dst_size}",
            file=sys.stderr,
        )
        return 1
    if sha256(src) != sha256(dst):
        print("ERROR: sha256 mismatch after copy", file=sys.stderr)
        return 1

    print(f"Wrote {dst} ({dst_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
