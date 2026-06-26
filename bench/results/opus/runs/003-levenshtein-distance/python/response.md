```python
import sys

def main():
    data = sys.stdin.read().split('\n')
    a = data[0] if len(data) > 0 else ''
    b = data[1] if len(data) > 1 else ''
    m, n = len(a), len(b)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
        prev = curr
    sys.stdout.write(f"{prev[n]}\n")

main()
```