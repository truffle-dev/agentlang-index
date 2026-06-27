```python
import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n == 0: return 0
    if n == 1: return 1
    return fib(n-1) + fib(n-2)

n = int(sys.stdin.read().strip())
sys.stdout.write(str(fib(n)) + "\n")
```