```python
import sys

def main():
    data = sys.stdin.read()
    # Validate that input is exactly one line ending with a single newline
    if not data.endswith('\n') or '\n' in data[:-1]:
        sys.stdout.write("error\n")
        return

    s = data[:-1]
    # Non-empty check
    if not s:
        sys.stdout.write("error\n")
        return

    # Validate all characters are lowercase a-z
    for ch in s:
        if not ('a' <= ch <= 'z'):
            sys.stdout.write("error\n")
            return

    # Run-length encoding
    out_parts = []
    prev = s[0]
    count = 1
    for ch in s[1:]:
        if ch == prev:
            count += 1
        else:
            out_parts.append(prev)
            out_parts.append(str(count))
            prev = ch
            count = 1
    out_parts.append(prev)
    out_parts.append(str(count))
    out_parts.append('\n')
    sys.stdout.write(''.join(out_parts))

if __name__ == "__main__":
    main()
```