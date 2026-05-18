"""Non-overlapping substring count, Python reference.

Reads pattern P from line 1 of stdin and text T from line 2. Counts greedy
non-overlapping occurrences and writes the decimal count followed by \\n.
"""
import sys


def main() -> None:
    raw = sys.stdin.read().split("\n", 2)
    p = raw[0] if len(raw) >= 1 else ""
    t = raw[1] if len(raw) >= 2 else ""
    count = 0
    if p:
        i = 0
        n = len(t)
        m = len(p)
        while i + m <= n:
            if t[i:i + m] == p:
                count += 1
                i += m
            else:
                i += 1
    sys.stdout.write(f"{count}\n")


if __name__ == "__main__":
    main()
