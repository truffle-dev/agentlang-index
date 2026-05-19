```python
import sys
import math

def main():
    data = sys.stdin.read().strip()
    try:
        N = int(data)
    except Exception:
        # Input is expected to be a single integer; if not, print error as a safe fallback.
        sys.stdout.write("error\n")
        return

    if N < 2:
        sys.stdout.write("0\n")
        return

    is_prime = [True] * (N + 1)
    is_prime[0] = False
    is_prime[1] = False

    limit = math.isqrt(N)
    for p in range(2, limit + 1):
        if is_prime[p]:
            start = p * p
            for multiple in range(start, N + 1, p):
                is_prime[multiple] = False

    count = sum(1 for i in range(2, N + 1) if is_prime[i])
    sys.stdout.write(f"{count}\n")

if __name__ == "__main__":
    main()
```