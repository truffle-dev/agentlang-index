```python
import sys

def main():
    data = sys.stdin.read()
    if not data.endswith('\n'):
        sys.stdout.write("error\n")
        return
    line = data[:-1]
    if len(line) == 0:
        sys.stdout.write("error\n")
        return
    for c in line:
        if c < 'a' or c > 'z':
            sys.stdout.write("error\n")
            return
    result = []
    i = 0
    while i < len(line):
        c = line[i]
        count = 1
        while i + count < len(line) and line[i + count] == c:
            count += 1
        result.append(c)
        result.append(str(count))
        i += count
    sys.stdout.write("".join(result) + "\n")

main()
```