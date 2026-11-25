"""The Best Advice I Ever Got — V2 entry writer.

Writes exactly one sentence (the V2 advice line) to entry.txt inside the
make.fun output directory, then reads it back and aborts if the bytes on
disk differ from the intended line. Stdlib only.
"""

import os
import sys

SENTENCE = (
    "After Dad lost his job in 2009, he still ironed his shirt every "
    "morning and told me, 'Dress for the job you want, not the luck you got.'"
)

MAX_CHARS = 200
TERMINATORS = (".", "!", "?")


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def check_sentence(text):
    """Validate the line against the bounty rules; exit 1 on any violation."""
    if not isinstance(text, str):
        fail("entry is not a string")
    if not text.strip():
        fail("entry is empty")
    if len(text) > MAX_CHARS:
        fail(f"entry is {len(text)} characters, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        fail("entry must be a single line")
    closing = [c for c in text if c in TERMINATORS]
    if len(closing) != 1:
        fail(f"entry must be exactly one sentence, found {len(closing)} terminators")
    # The sentence may end inside a closing quote, e.g. ...got.'
    tail = text.rstrip("'\"")
    if not tail or tail[-1] not in TERMINATORS:
        fail("entry must end with a sentence terminator")


def output_path():
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(base, "entry.txt")


def main():
    check_sentence(SENTENCE)
    target = output_path()
    directory = os.path.dirname(target)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(SENTENCE)
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != SENTENCE.encode("utf-8"):
        fail("read-back mismatch: bytes on disk differ from the entry")
    print(f"wrote {len(SENTENCE)} characters to {target}")


if __name__ == "__main__":
    main()
