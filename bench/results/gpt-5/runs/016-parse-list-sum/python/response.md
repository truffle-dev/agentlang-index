```python
import sys

MAX_U32 = 4294967295

def parse_u32_line(line: str):
    s = line.rstrip()
    if not s:
        return None
    for ch in s:
        if ch < '0' or ch > '9':
            return None
    try:
        val = int(s)
    except Exception:
        return None
    if val < 0 or val > MAX_U32:
        return None
    return val

def main():
    data = sys.stdin.read()
    lines = data.splitlines()

    if not lines:
        sys.stdout.write("error\n")
        return

    n = parse_u32_line(lines[0])
    if n is None or n > 1000:
        sys.stdout.write("error\n")
        return

    if len(lines) - 1 < n:
        sys.stdout.write("error\n")
        return

    total = 0
    for i in range(n):
        v = parse_u32_line(lines[1 + i])
        if v is None:
            sys.stdout.write("error\n")
            return
        if total > MAX_U32 - v:
            sys.stdout.write("error\n")
            return
        total += v

    sys.stdout.write(f"{total}\n")

if __name__ == "__main__":
    main()
```