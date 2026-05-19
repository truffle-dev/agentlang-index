```python
import sys

def main():
    data = sys.stdin.read()
    lines = data.splitlines()

    # Prepare shift line with trailing whitespace trimmed
    shift_line = lines[0].rstrip() if len(lines) >= 1 else ""

    # Get plaintext verbatim (no trimming)
    plaintext = lines[1] if len(lines) >= 2 else ""

    # Validate shift line
    if shift_line == "":
        sys.stdout.write("error\n")
        return
    if not all('0' <= ch <= '9' for ch in shift_line):
        sys.stdout.write("error\n")
        return
    try:
        shift = int(shift_line)
    except Exception:
        sys.stdout.write("error\n")
        return
    if shift < 0 or shift > 25:
        sys.stdout.write("error\n")
        return

    # Validate plaintext
    if plaintext == "":
        sys.stdout.write("error\n")
        return
    if not all('a' <= ch <= 'z' for ch in plaintext):
        sys.stdout.write("error\n")
        return

    # Caesar cipher
    a_ord = ord('a')
    res_chars = []
    s = shift % 26
    for ch in plaintext:
        offset = ord(ch) - a_ord
        res_chars.append(chr(a_ord + ((offset + s) % 26)))
    sys.stdout.write("".join(res_chars) + "\n")

if __name__ == "__main__":
    main()
```