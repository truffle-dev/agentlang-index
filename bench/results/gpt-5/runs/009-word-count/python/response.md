```python
import sys

def main():
    data = sys.stdin.buffer.read()
    whitespace = {0x20, 0x09, 0x0A, 0x0D}
    count = 0
    in_word = False

    for b in data:
        if b in whitespace:
            if in_word:
                in_word = False
        else:
            if not in_word:
                count += 1
                in_word = True

    sys.stdout.write(f"{count}\n")

if __name__ == "__main__":
    main()
```