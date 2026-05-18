"""Square integer matrix multiply, Python reference.

Reads N, then N rows of A, then N rows of B. Writes the N rows of C = A * B,
each row as space-separated decimal integers terminated by a single newline.
"""
import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    pos = 0
    n = int(tokens[pos]); pos += 1
    if n < 1 or n > 5:
        sys.stderr.write("N must be in [1, 5]\n")
        sys.exit(1)
    a = [[0] * n for _ in range(n)]
    b = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            a[i][j] = int(tokens[pos]); pos += 1
    for i in range(n):
        for j in range(n):
            b[i][j] = int(tokens[pos]); pos += 1
    out_rows: list[str] = []
    for i in range(n):
        row_vals = []
        for j in range(n):
            s = 0
            for k in range(n):
                s += a[i][k] * b[k][j]
            row_vals.append(str(s))
        out_rows.append(" ".join(row_vals))
    sys.stdout.write("\n".join(out_rows) + "\n")


if __name__ == "__main__":
    main()
