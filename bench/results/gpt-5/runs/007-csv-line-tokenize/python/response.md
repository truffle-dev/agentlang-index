```python
import sys

def parse_csv_line(line: str):
    fields = []
    buf = []
    in_quotes = False
    i = 0
    n = len(line)

    while i < n:
        ch = line[i]
        if in_quotes:
            if ch == '"':
                if i + 1 < n and line[i + 1] == '"':
                    buf.append('"')
                    i += 2
                else:
                    in_quotes = False
                    i += 1
            else:
                buf.append(ch)
                i += 1
        else:
            if ch == '"' and not buf:
                in_quotes = True
                i += 1
            elif ch == ',':
                fields.append(''.join(buf))
                buf.clear()
                i += 1
            else:
                buf.append(ch)
                i += 1

    if n > 0:
        fields.append(''.join(buf))

    return fields

def main():
    data = sys.stdin.read()
    nl = data.find('\n')
    if nl != -1:
        line = data[:nl]
    else:
        line = data

    if line == "":
        sys.stdout.write("")
        return

    fields = parse_csv_line(line)
    out = ''.join(f + '\n' for f in fields)
    sys.stdout.write(out)

if __name__ == "__main__":
    main()
```