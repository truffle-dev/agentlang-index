```python
import sys

def main():
    n = int(sys.stdin.read().strip())
    if n < 2:
        sys.stdout.write("0\n")
        return
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    i = 2
    while i * i <= n:
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
        i += 1
    sys.stdout.write(str(sum(sieve)) + "\n")

main()
```