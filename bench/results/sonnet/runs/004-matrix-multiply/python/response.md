```python
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = []
    for i in range(N):
        row = [int(data[idx+j]) for j in range(N)]
        idx += N
        A.append(row)
    B = []
    for i in range(N):
        row = [int(data[idx+j]) for j in range(N)]
        idx += N
        B.append(row)
    out = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(sum(A[i][k] * B[k][j] for k in range(N)))
        out.append(' '.join(map(str, row)))
    sys.stdout.write('\n'.join(out) + '\n')

main()
```