```python
import sys

def main():
    data = sys.stdin.read()
    if not data:
        return
    if data.endswith('\n'):
        data = data[:-1]
    # Split on ASCII spaces only and ignore empty parts
    words = [w for w in data.split(' ') if w]
    if not words:
        return
    out = ' '.join(reversed(words)) + '\n'
    sys.stdout.write(out)

if __name__ == "__main__":
    main()
```