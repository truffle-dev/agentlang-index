#!/usr/bin/env python3
import sys

U32_MAX = 4294967295


def parse_u32(s: str):
    s = s.strip()
    if not s:
        return None
    for ch in s:
        if not ('0' <= ch <= '9'):
            return None
    try:
        v = int(s)
    except ValueError:
        return None
    if v > U32_MAX:
        return None
    return v


def main() -> None:
    data = sys.stdin.read()
    lines = data.split("\n")
    if len(lines) < 2:
        sys.stdout.write("error\n")
        return
    a = parse_u32(lines[0])
    b = parse_u32(lines[1])
    if a is None or b is None:
        sys.stdout.write("error\n")
        return
    s = a + b
    if s > U32_MAX:
        sys.stdout.write("error\n")
        return
    sys.stdout.write(f"{s}\n")


if __name__ == "__main__":
    main()
