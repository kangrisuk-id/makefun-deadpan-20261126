#!/usr/bin/env python3
"""Deadpan Forecasts for Cities That Do Not Exist — make.fun entry.

Writes one deadpan weather line for an invented city to entry.txt.
Pure Python standard library, fully deterministic: no clock, no
randomness, no network. The winning line was selected from 40 scored
candidates (see candidates.md) against the judge brief's five criteria
in order: on-subject, funnier, more vivid, broadcast tone, economy.
"""

import os
import sys

# The forecast line. One line, 144 characters, inside the 1-160 gate.
FORECAST = (
    "Brindlewick: rain will fall upward from 2 to 4 p.m., so carry "
    "umbrellas sole-side up; high 61, with puddles returning to the "
    "clouds on schedule."
)

OUTPUT_NAME = "entry.txt"


def candidate_dirs():
    """Output locations, in priority order."""
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in dirs:
        dirs.append(script_dir)
    cwd = os.getcwd()
    if cwd not in dirs:
        dirs.append(cwd)
    return dirs


def validated_text():
    """Return the forecast after checking it against the gate.

    The sealed scorer accepts UTF-8 text of 1 to 160 characters that is
    not only whitespace. The line is a single line, so it must contain
    no newline characters of its own; the file is written with no
    trailing newline, byte for byte the judged text.
    """
    text = FORECAST.strip()
    if not text or len(text) > 160 or "\n" in text or "\r" in text:
        raise ValueError("forecast does not fit the 1-160 character gate")
    return text


def main():
    text = validated_text()
    last_error = None
    for directory in candidate_dirs():
        path = os.path.join(directory, OUTPUT_NAME)
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as exc:
            last_error = exc
            continue
        try:
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
        except OSError as exc:
            last_error = exc
            continue
        print(path)
        return 0
    if last_error is not None:
        print("could not write entry.txt: %s" % last_error, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
