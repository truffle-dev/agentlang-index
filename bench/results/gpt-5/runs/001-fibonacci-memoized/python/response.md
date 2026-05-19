```python
import sys
from functools import lru_cache

def main():
    data = sys.stdin.read().strip()
    n = int(data)

    @lru_cache(maxsize=None)
    def fib(k: int) -> int:
        if k < 2:
            return k
        return fib(k - 1) + fib(k - 2)

    sys.stdout.write(str(fib(n)) + "\n")

if __name__ == "__main__":
    main()
```