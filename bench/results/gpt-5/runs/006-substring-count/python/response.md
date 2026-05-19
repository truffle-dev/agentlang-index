```python
import sys

def main():
    data = sys.stdin.read()
    lines = data.splitlines()
    P = lines[0] if len(lines) >= 1 else ""
    T = lines[1] if len(lines) >= 2 else ""

    if not P:
        sys.stdout.write("0\n")
        return

    count = 0
    i = 0
    L = len(P)
    while True:
        j = T.find(P, i)
        if j == -1:
            break
        count += 1
        i = j + L

    sys.stdout.write(str(count) + "\n")

if __name__ == "__main__":
    main()
```