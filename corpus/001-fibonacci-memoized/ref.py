"""Fibonacci with memoization, Python reference.

Reads N from stdin, caches fib(i) in a dict. Python ints are arbitrary
precision so no overflow concerns regardless of N.
"""
import sys


def main() -> None:
    n = int(sys.stdin.readline().strip())
    if n < 0:
        sys.stderr.write("N must be a non-negative integer\n")
        sys.exit(1)
    memo: dict[int, int] = {0: 0, 1: 1}

    def fib(k: int) -> int:
        if k in memo:
            return memo[k]
        v = fib(k - 1) + fib(k - 2)
        memo[k] = v
        return v

    sys.stdout.write(f"{fib(n)}\n")


if __name__ == "__main__":
    main()
