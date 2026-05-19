```python
import sys

def main():
    data = sys.stdin.read()
    toks = data.split()
    if not toks:
        sys.stdout.write("error\n")
        return
    try:
        n = int(toks[0])
    except Exception:
        sys.stdout.write("error\n")
        return
    if n < 1 or n > 5:
        sys.stdout.write("error\n")
        return
    need = 1 + 2 * n * n
    if len(toks) != need:
        sys.stdout.write("error\n")
        return
    vals = []
    for i in range(1, need):
        try:
            x = int(toks[i])
        except Exception:
            sys.stdout.write("error\n")
            return
        vals.append(x)
    A = [vals[i * n:(i + 1) * n] for i in range(n)]
    bstart = n * n
    B = [vals[bstart + i * n:bstart + (i + 1) * n] for i in range(n)]

    out_lines = []
    for i in range(n):
        Ai = A[i]
        row = []
        for j in range(n):
            s = 0
            for k in range(n):
                s += Ai[k] * B[k][j]
            row.append(str(s))
        out_lines.append(" ".join(row))
    sys.stdout.write("\n".join(out_lines) + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        try:
            sys.stdout.write("error\n")
        except Exception:
            pass
```