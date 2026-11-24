"""Entry program for make.fun news-image-20261124.

Deterministic by design: it only copies the pre-rendered entry.png that
ships in this repository into $MAKEFUN_OUTPUT_DIR (default /output). No
timestamps, no randomness, no network — two runs write identical bytes.
The image is refused (exit 1) when it is missing, larger than the 1 MiB
gate limit, or does not start with the PNG magic bytes.
"""
import os
import shutil
import sys

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png is missing next to main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print("error: entry.png is %d bytes, over the 1048576 limit"
              % size, file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        if fh.read(len(PNG_MAGIC)) != PNG_MAGIC:
            print("error: entry.png is not a PNG file", file=sys.stderr)
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
