```python
import sys

def levenshtein(a, b):
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if a[i-1] == b[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])
            prev = temp
    return dp[n]

lines = sys.stdin.read().splitlines()
a = lines[0] if len(lines) > 0 else ""
b = lines[1] if len(lines) > 1 else ""
sys.stdout.write(str(levenshtein(a, b)) + "\n")
```