#!/usr/bin/env python3
import sys


def is_lowercase_letter(b: int) -> bool:
    return 97 <= b <= 122


def shift_letter(b: int, shift: int) -> int:
    zero_based = b - 97
    return 97 + ((zero_based + shift) % 26)


def parse_shift(s: str):
    t = s.strip()
    if not t:
        return None
    for ch in t:
        if not ('0' <= ch <= '9'):
            return None
    try:
        v = int(t)
    except ValueError:
        return None
    if v > 25:
        return None
    return v


def main() -> None:
    data = sys.stdin.read()
    lines = data.split("\n")
    if len(lines) < 2:
        sys.stdout.write("error\n")
        return
    shift = parse_shift(lines[0])
    if shift is None:
        sys.stdout.write("error\n")
        return
    text = lines[1]
    if not text:
        sys.stdout.write("error\n")
        return
    text_bytes = text.encode("utf-8")
    for b in text_bytes:
        if not is_lowercase_letter(b):
            sys.stdout.write("error\n")
            return
    out = bytes(shift_letter(b, shift) for b in text_bytes)
    sys.stdout.write(out.decode("ascii") + "\n")


if __name__ == "__main__":
    main()
