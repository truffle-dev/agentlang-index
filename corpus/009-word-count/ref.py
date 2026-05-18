#!/usr/bin/env python3
"""Count whitespace-separated tokens in input, Python reference."""

import sys


def main() -> None:
    data = sys.stdin.buffer.read()
    count = 0
    in_word = False
    for b in data:
        is_ws = b == 32 or b == 9 or b == 10 or b == 13
        if is_ws:
            in_word = False
        elif not in_word:
            count += 1
            in_word = True
    sys.stdout.write(f"{count}\n")


if __name__ == "__main__":
    main()
