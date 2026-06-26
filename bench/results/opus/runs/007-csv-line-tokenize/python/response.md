```python
import sys

def main():
    line = sys.stdin.read()
    if line.endswith('\n'):
        line = line[:-1]
    if not line:
        return
    fields = []
    i = 0
    while i <= len(line):
        if i < len(line) and line[i] == '"':
            i += 1
            f = []
            while True:
                if i < len(line) and line[i] == '"':
                    if i + 1 < len(line) and line[i + 1] == '"':
                        f.append('"')
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    f.append(line[i])
                    i += 1
            fields.append(''.join(f))
            if i < len(line) and line[i] == ',':
                i += 1
        else:
            j = i
            while j < len(line) and line[j] != ',':
                j += 1
            fields.append(line[i:j])
            i = j + 1
    sys.stdout.write(''.join(f + '\n' for f in fields))

main()
```