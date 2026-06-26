```python
import sys

def main():
    data = sys.stdin.read()
    lines = data.split('\n')
    if len(lines) < 2:
        sys.stdout.write("error\n")
        return
    line1 = lines[0].rstrip()
    line2 = lines[1]
    if not line1 or not line1.isdigit():
        sys.stdout.write("error\n")
        return
    shift = int(line1)
    if shift > 25:
        sys.stdout.write("error\n")
        return
    if not line2:
        sys.stdout.write("error\n")
        return
    for c in line2:
        if c < 'a' or c > 'z':
            sys.stdout.write("error\n")
            return
    out = []
    for c in line2:
        out.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
    sys.stdout.write(''.join(out) + '\n')

main()
```