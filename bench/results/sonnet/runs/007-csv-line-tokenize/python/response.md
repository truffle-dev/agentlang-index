```python
import sys

def parse_csv(line):
    fields = []
    i = 0
    n = len(line)
    if n == 0:
        return fields
    while True:
        if i < n and line[i] == '"':
            i += 1
            field = []
            while i < n:
                if line[i] == '"':
                    if i + 1 < n and line[i+1] == '"':
                        field.append('"')
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    field.append(line[i])
                    i += 1
            fields.append(''.join(field))
        else:
            j = i
            while i < n and line[i] != ',':
                i += 1
            fields.append(line[j:i])
        if i < n and line[i] == ',':
            i += 1
        else:
            break
    return fields

line = sys.stdin.read()
if line.endswith('\n'):
    line = line[:-1]
for field in parse_csv(line):
    sys.stdout.write(field + '\n')
```