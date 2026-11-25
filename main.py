#!/usr/bin/env python3
"""The Best Advice I Ever Got — V2 revised entry writer.

Assembles the one-sentence V2 advice line from fragments, runs it through
a pipeline of small validators, writes it to entry.txt inside the make.fun
output directory, then reads the file back and aborts when the bytes on
disk are not exactly the intended line. Standard library only.
"""

import os
import sys
from pathlib import Path

# Fragments of the entry, joined with single spaces. The line itself is
# fixed (136 characters, one sentence); splitting it here only keeps the
# source readable and makes the assembly step explicit.
ENTRY_PARTS = (
    "After Dad lost his job in 2009, he still ironed his shirt every",
    "morning and told me, 'Dress for the job you want, not the luck",
    "you got.'",
)
ENTRY = " ".join(ENTRY_PARTS)

CHAR_LIMIT = 200
END_MARKS = frozenset(".!?")
CLOSING_QUOTES = "'\""


def die(reason):
    """Print the failure reason and stop with a non-zero exit code."""
    sys.stderr.write("entry rejected: " + reason + "\n")
    raise SystemExit(1)


def _single_line(line):
    if "\n" in line or "\r" in line:
        return "entry spans more than one line"
    return None


def _within_limit(line):
    if len(line) > CHAR_LIMIT:
        return "entry is %d characters, limit is %d" % (len(line), CHAR_LIMIT)
    return None


def _not_blank(line):
    if not isinstance(line, str) or line.strip() == "":
        return "entry is empty"
    return None


def _no_surrounding_space(line):
    if line != line.strip():
        return "entry must not start or end with whitespace"
    return None


def _one_sentence(line):
    # A trailing quote may follow the final terminator, as in ...got.'
    body = line
    while body and body[-1] in CLOSING_QUOTES:
        body = body[:-1]
    marks = sum(1 for ch in body if ch in END_MARKS)
    if marks != 1:
        return "entry must contain exactly one sentence, found %d end marks" % marks
    if not body or body[-1] not in END_MARKS:
        return "entry must end with a sentence terminator"
    return None


# Validators run in this order: line shape first, then size, then content.
VALIDATORS = (_single_line, _within_limit, _not_blank, _no_surrounding_space, _one_sentence)


def validate(line):
    """Run every validator; stop at the first problem found."""
    for check in VALIDATORS:
        problem = check(line)
        if problem is not None:
            die(problem)


def destination():
    """Resolve entry.txt under $MAKEFUN_OUTPUT_DIR, defaulting to /output."""
    root = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    return root / "entry.txt"


def write_entry(line, target):
    """Write the line with no trailing newline, then verify the bytes."""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(line.encode("utf-8"))
    if target.read_bytes() != line.encode("utf-8"):
        die("read-back mismatch: bytes on disk differ from the entry")
    return target


def run():
    validate(ENTRY)
    target = write_entry(ENTRY, destination())
    print("wrote %d characters to %s" % (len(ENTRY), target))


if __name__ == "__main__":
    run()
