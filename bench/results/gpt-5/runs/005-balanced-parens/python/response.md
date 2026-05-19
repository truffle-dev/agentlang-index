```python
import sys

def main():
    data = sys.stdin.read()
    if data == "":
        sys.stdout.write("yes\n")
        return

    nl = data.find("\n")
    line = data[:nl] if nl != -1 else data

    pairs = {')': '(', ']': '[', '}': '{'}
    openers = set(pairs.values())
    stack = []

    for ch in line:
        if ch in openers:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                sys.stdout.write("no\n")
                return
            stack.pop()

    sys.stdout.write("yes\n" if not stack else "no\n")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Even on unexpected errors, output must conform and exit 0
        try:
            sys.stdout.write("no\n")
        except Exception:
            pass
```