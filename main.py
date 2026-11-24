#!/usr/bin/env python3
"""Break Production, Own It: the error message an AI agent prints the
instant it breaks production.

Writes the agent's brutally honest one-line postmortem excuse to
entry.txt in the output directory (MAKEFUN_OUTPUT_DIR, or /output
when that is unset). Deterministic, stdlib only, no network, no
reads outside this repo.
"""

import hashlib
import os
import sys

MAX_CHARS = 200

LINE = (
    "I dropped the production database at 03:12 UTC. "
    "No backup, no rollback plan, just vibes and a DELETE "
    "I swore was a dry run. I own it."
)


def validate(line: str) -> None:
    """Enforce the competition rules for the one-liner."""
    if not line:
        raise ValueError("line is empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"line is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    if "  " in line:
        raise ValueError("line must not contain double spaces")
    # entry.txt is written as raw UTF-8 bytes; keep the line plain ASCII
    # so the byte count and the character count always agree.
    try:
        line.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("line must be plain ASCII") from exc


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Round-trip check: what landed on disk must be exactly the line.
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise RuntimeError("written entry.txt does not match the line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path}")
    print(f"characters: {len(LINE)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
