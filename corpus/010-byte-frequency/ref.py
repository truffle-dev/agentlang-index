#!/usr/bin/env python3
"""Per-byte frequency table, Python reference."""

import sys


def main() -> None:
    data = sys.stdin.buffer.read()
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    out_parts = []
    for b in range(256):
        c = counts[b]
        if c > 0:
            out_parts.append(f"{b} {c}\n")
    sys.stdout.write("".join(out_parts))


if __name__ == "__main__":
    main()
