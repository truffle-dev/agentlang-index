```python
import sys
sys.setrecursionlimit(10**6)

def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

def main():
    input_data = sys.stdin.read().strip()
    N = int(input_data)
    result = fib(N)
    sys.stdout.write(f"{result}\n")

if __name__ == "__main__":
    main()
```