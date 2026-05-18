"""Balanced bracket checker, Python reference.

Reads one line of printable ASCII (up to 1000 chars), prints `yes` or `no`.
"""
import sys


def main() -> None:
    line = sys.stdin.readline()
    if line.endswith("\n"):
        line = line[:-1]
    stack: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    balanced = True
    for ch in line:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                balanced = False
                break
            stack.pop()
    if balanced and not stack:
        sys.stdout.write("yes\n")
    else:
        sys.stdout.write("no\n")


if __name__ == "__main__":
    main()
