```python
import sys
import re

def parse_u32(s):
    s = s.rstrip()
    if not re.fullmatch(r'[0-9]+', s):
        return None
    v = int(s)
    if v > 4294967295:
        return None
    return v

def main():
    data = sys.stdin.read()
    lines = data.split('\n')
    if len(lines) < 2:
        sys.stdout.write('error\n')
        return
    a = parse_u32(lines[0])
    b = parse_u32(lines[1])
    if a is None or b is None or b == 0:
        sys.stdout.write('error\n')
        return
    sys.stdout.write(str(a // b) + '\n')

main()
```