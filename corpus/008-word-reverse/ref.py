"""Reverse the order of words on a line, Python reference."""
import sys


def main() -> None:
    line = sys.stdin.readline()
    if line.endswith("\n"):
        line = line[:-1]
    words = line.split(" ")
    words = [w for w in words if w != ""]
    if not words:
        return
    words.reverse()
    sys.stdout.write(" ".join(words) + "\n")


if __name__ == "__main__":
    main()
