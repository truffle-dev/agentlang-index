```python
import sys

def main():
    data = sys.stdin.read().split('\n')
    P = data[0]
    T = data[1] if len(data) > 1 else ''
    count = 0
    i = 0
    lp = len(P)
    while i <= len(T) - lp:
        if T[i:i+lp] == P:
            count += 1
            i += lp
        else:
            i += 1
    sys.stdout.write(f"{count}\n")

main()
```