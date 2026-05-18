"""Prime count via Sieve of Eratosthenes, Python reference.

Reads N from stdin, runs a standard byte-flag sieve over [0, N], counts
unmarked indices in [2, N]. N is bounded by 10000 by the task spec but
nothing here would change for a larger N apart from the allocation.
"""
import sys


def main() -> None:
    n = int(sys.stdin.readline().strip())
    if n < 0:
        sys.stderr.write("N must be a non-negative integer\n")
        sys.exit(1)
    if n < 2:
        sys.stdout.write("0\n")
        return
    composite = bytearray(n + 1)
    i = 2
    while i * i <= n:
        if composite[i] == 0:
            j = i * i
            while j <= n:
                composite[j] = 1
                j += i
        i += 1
    count = sum(1 for k in range(2, n + 1) if composite[k] == 0)
    sys.stdout.write(f"{count}\n")


if __name__ == "__main__":
    main()
