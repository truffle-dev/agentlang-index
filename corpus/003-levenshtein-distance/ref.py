"""Levenshtein edit distance, Python reference.

Reads two lines from stdin (A and B), computes the classic two-row DP,
and writes the distance plus a trailing newline.
"""
import sys


def main() -> None:
    data = sys.stdin.read().split("\n")
    a = data[0] if len(data) >= 1 else ""
    b = data[1] if len(data) >= 2 else ""
    if len(a) > 50 or len(b) > 50:
        sys.stderr.write("each string must be at most 50 characters\n")
        sys.exit(1)
    m, n = len(a), len(b)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for i in range(m):
        curr[0] = i + 1
        ai = a[i]
        for k in range(n):
            del_cost = prev[k + 1] + 1
            ins_cost = curr[k] + 1
            sub_cost = prev[k] + (0 if ai == b[k] else 1)
            curr[k + 1] = min(del_cost, ins_cost, sub_cost)
        prev, curr = curr, prev
    sys.stdout.write(f"{prev[n]}\n")


if __name__ == "__main__":
    main()
