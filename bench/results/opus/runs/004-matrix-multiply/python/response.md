```python
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    A = []
    for i in range(n):
        row = [int(data[idx + j]) for j in range(n)]
        idx += n
        A.append(row)
    B = []
    for i in range(n):
        row = [int(data[idx + j]) for j in range(n)]
        idx += n
        B.append(row)
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
            row.append(str(s))
        out.append(' '.join(row))
    sys.stdout.write('\n'.join(out) + '\n')

main()
```