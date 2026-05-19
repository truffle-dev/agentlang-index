```python
import sys

def count_primes(n):
    if n < 2:
        return 0
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for start in range(2, int(n**0.5) + 1):
        if sieve[start]:
            for multiple in range(start*start, n + 1, start):
                sieve[multiple] = False
    return sum(sieve)

def main():
    n = int(sys.stdin.read().strip())
    prime_count = count_primes(n)
    sys.stdout.write(f"{prime_count}\n")

if __name__ == "__main__":
    main()
```