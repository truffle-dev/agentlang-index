```python
import sys

def main():
    data = sys.stdin.read()
    lines = data.split('\n')
    if len(lines) < 2:
        sys.stdout.write("error\n")
        return
    a_str = lines[0].rstrip()
    b_str = lines[1].rstrip()
    for s in (a_str, b_str):
        if len(s) == 0:
            sys.stdout.write("error\n")
            return
        if s[0] == '+':
            sys.stdout.write("error\n")
            return
        for c in s:
            if c < '0' or c > '9':
                sys.stdout.write("error\n")
                return
    a = int(a_str)
    b = int(b_str)
    if a > 4294967295 or b > 4294967295:
        sys.stdout.write("error\n")
        return
    if b == 0:
        sys.stdout.write("error\n")
        return
    sys.stdout.write(str(a // b) + "\n")

main()
```