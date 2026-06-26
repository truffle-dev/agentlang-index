```python
import sys

def solve():
    n = int(sys.stdin.read())
    fib = [0] * max(2, n + 1)
    fib[1] = 1
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    sys.stdout.write(f"{fib[n]}\n")

solve()
```