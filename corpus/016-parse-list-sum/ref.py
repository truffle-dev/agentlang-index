#!/usr/bin/env python3
import sys

U32_MAX = 4294967295
N_MAX = 1000


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
    if len(lines) < 1:
        sys.stdout.write("error\n")
        return
    n = parse_u32(lines[0])
    if n is None or n > N_MAX:
        sys.stdout.write("error\n")
        return
    if len(lines) < n + 1:
        sys.stdout.write("error\n")
        return
    total = 0
    for i in range(1, n + 1):
        v = parse_u32(lines[i])
        if v is None:
            sys.stdout.write("error\n")
            return
        total += v
        if total > U32_MAX:
            sys.stdout.write("error\n")
            return
    sys.stdout.write(f"{total}\n")


if __name__ == "__main__":
    main()
