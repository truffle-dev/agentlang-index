```python
import sys

def parse_csv_line(line):
    fields = []
    field = []
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if in_quotes:
            if char == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(char)
        else:
            if char == '"':
                in_quotes = True
            elif char == ',':
                fields.append(''.join(field))
                field = []
            else:
                field.append(char)
        i += 1
    fields.append(''.join(field))
    return fields

def main():
    input_line = sys.stdin.read().rstrip('\n')
    if input_line:
        fields = parse_csv_line(input_line)
        for field in fields:
            sys.stdout.write(field + '\n')

if __name__ == "__main__":
    main()
```