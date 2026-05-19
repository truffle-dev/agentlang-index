#!/usr/bin/env python3
import sys


def is_lowercase_letter(b: int) -> bool:
    return 97 <= b <= 122


def main() -> None:
    data = sys.stdin.read()
    lines = data.split("\n")
    if len(lines) < 1:
        sys.stdout.write("error\n")
        return
    text = lines[0]
    if not text:
        sys.stdout.write("error\n")
        return
    text_bytes = text.encode("utf-8")
    for b in text_bytes:
        if not is_lowercase_letter(b):
            sys.stdout.write("error\n")
            return
    out = []
    i = 0
    n = len(text_bytes)
    while i < n:
        run_byte = text_bytes[i]
        run_len = 1
        j = i + 1
        while j < n and text_bytes[j] == run_byte:
            run_len += 1
            j += 1
        out.append(bytes([run_byte]).decode("ascii"))
        out.append(str(run_len))
        i = j
    sys.stdout.write("".join(out) + "\n")


if __name__ == "__main__":
    main()
