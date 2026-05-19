```python
import sys

def read_matrix(n):
    return [list(map(int, sys.stdin.readline().strip().split())) for _ in range(n)]

def matrix_multiply(A, B, n):
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return C

def main():
    n = int(sys.stdin.readline().strip())
    A = read_matrix(n)
    B = read_matrix(n)
    C = matrix_multiply(A, B, n)
    
    for row in C:
        sys.stdout.write(' '.join(map(str, row)) + '\n')

if __name__ == "__main__":
    main()
```