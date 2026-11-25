#!/usr/bin/env python3
"""The Best Advice I Ever Got — entry V1.

Writes one sentence (152 characters) to entry.txt.
Stdlib only.
"""

import os
import sys

LINE = (
    "On my first morning at the warehouse, Dad pressed his old lunchbox "
    "into my hands and said, 'Pack your own lunch \u2014 nobody will "
    "feed your future for you.'"
)


def validate(line):
    if not isinstance(line, str):
        raise ValueError("entry must be text")
    if not line.strip():
        raise ValueError("entry must not be empty or whitespace only")
    if len(line) > 200:
        raise ValueError(
            "entry is %d characters, over the 200-character limit" % len(line)
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    stripped = line.rstrip()
    # A quoted sentence ends with .' or ." — strip a closing quote first.
    if stripped and stripped[-1] in ("'", '"'):
        stripped = stripped[:-1].rstrip()
    if not stripped.endswith("."):
        raise ValueError("entry must be a single sentence ending with '.'")
    # Only one sentence: exactly one sentence-ending period, at the end.
    if stripped.count(".") != 1:
        raise ValueError("entry must be exactly one sentence")
    return line


def main():
    try:
        line = validate(LINE)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)

    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != line.encode("utf-8"):
        print("error: read-back mismatch in %s" % path, file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (path, len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
