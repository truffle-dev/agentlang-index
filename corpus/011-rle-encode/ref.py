#!/usr/bin/env python3
"""Run-length encode the input, Python reference."""

import sys


def main() -> None:
    data = sys.stdin.buffer.read()
    if not data:
        return
    parts = []
    cur_byte = data[0]
    cur_count = 1
    for b in data[1:]:
        if b == cur_byte:
            cur_count += 1
        else:
            parts.append(f"{cur_count} {cur_byte}\n")
            cur_byte = b
            cur_count = 1
    parts.append(f"{cur_count} {cur_byte}\n")
    sys.stdout.write("".join(parts))


if __name__ == "__main__":
    main()
