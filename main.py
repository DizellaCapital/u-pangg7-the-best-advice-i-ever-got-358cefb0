#!/usr/bin/env python3
"""The Best Advice I Ever Got — V3 entry writer (stdlib only).

Writes one sentence (149 chars) to $MAKEFUN_OUTPUT_DIR/entry.txt,
falling back to /output, with no trailing newline. Aborts if the
on-disk bytes differ from the line.
"""

import os
import sys

LINE = (
    "When Grandpa's hands shook too much to hold his chisel, "
    "he pressed it into mine and whispered, "
    "'A steady hand is just a scared hand that kept going.'"
)

MAX_CHARS = 200
TERMINATORS = ".!?"
CLOSERS = "'\""


def sentence_total(text):
    """Count sentence terminators, ignoring a trailing closing quote.

    A quoted sentence ends with its period before the closing quote,
    so strip trailing quote chars first, then count terminators.
    """
    body = text.rstrip(CLOSERS)
    return sum(1 for ch in body if ch in TERMINATORS)


def assert_single_line(text):
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line (no newline characters)")


def emit_entry(line):
    if not isinstance(line, str):
        raise TypeError("entry must be a string")
    if line.strip() == "":
        raise ValueError("entry must not be empty")
    if line != line.strip():
        raise ValueError("entry must not start or end with whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} chars, over the {MAX_CHARS}-char limit"
        )
    assert_single_line(line)
    if sentence_total(line) != 1:
        raise ValueError("entry must be exactly one sentence")
    if not line.rstrip(CLOSERS).endswith(tuple(TERMINATORS)):
        raise ValueError("entry must end with a sentence terminator")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)

    with open(target, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != line:
        raise RuntimeError("read-back mismatch: bytes on disk differ from entry")
    return target


def main():
    try:
        target = emit_entry(LINE)
    except (TypeError, ValueError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(LINE)} chars to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
