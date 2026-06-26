```python
import sys

def main():
    N = int(sys.stdin.read())
    if N < 2:
        sys.stdout.write("0\n")
        return
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, N + 1, i):
                sieve[j] = False
    sys.stdout.write(f"{sum(sieve)}\n")

main()
```