```python
import sys

def main():
    data = sys.stdin.read()
    if not data.endswith('\n'):
        sys.stdout.write('error\n')
        return
    line = data[:-1]
    if len(line) == 0:
        sys.stdout.write('error\n')
        return
    for ch in line:
        if ch < 'a' or ch > 'z':
            sys.stdout.write('error\n')
            return
    result = []
    i = 0
    while i < len(line):
        ch = line[i]
        count = 1
        while i + count < len(line) and line[i + count] == ch:
            count += 1
        result.append(ch)
        result.append(str(count))
        i += count
    result.append('\n')
    sys.stdout.write(''.join(result))

main()
```