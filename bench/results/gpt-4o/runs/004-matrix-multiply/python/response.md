```python
import sys

def read_matrix(input_lines, start_index, N):
    matrix = []
    for i in range(N):
        row = list(map(int, input_lines[start_index + i].split()))
        matrix.append(row)
    return matrix

def multiply_matrices(A, B, N):
    C = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
    return C

def main():
    input_data = sys.stdin.read().strip().split('\n')
    N = int(input_data[0])
    
    A = read_matrix(input_data, 1, N)
    B = read_matrix(input_data, 1 + N, N)
    
    C = multiply_matrices(A, B, N)
    
    for row in C:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    main()
```