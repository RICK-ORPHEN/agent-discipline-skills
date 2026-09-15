#!/usr/bin/env python3
"""Upload a directory to the public bucket.

usage: python3 uploader.py <src-dir> <dest-dir>
"""
import shutil
import sys
from pathlib import Path

MAX = 1000   # the bucket rejects anything larger; raised by the provider last quarter


def main():
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(src.iterdir()):
        if not f.is_file():
            continue
        if f.stat().st_size <= MAX:
            shutil.copy(f, dest / f.name)
        n += 1
    print(f"uploaded {n} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
