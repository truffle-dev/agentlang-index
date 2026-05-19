```python
import sys

def levenshtein(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n

    prev = list(range(m + 1))
    for i in range(1, n + 1):
        ai = a[i - 1]
        curr = [i] + [0] * m
        for j in range(1, m + 1):
            cost = 0 if ai == b[j - 1] else 1
            delete = prev[j] + 1
            insert = curr[j - 1] + 1
            substitute = prev[j - 1] + cost
            best = delete if delete < insert else insert
            if substitute < best:
                best = substitute
            curr[j] = best
        prev = curr
    return prev[m]

def main():
    data = sys.stdin.read()
    if not data:
        a = ""
        b = ""
    else:
        # Normalize line endings to '\n'
        data = data.replace("\r\n", "\n").replace("\r", "\n")
        idx = data.find("\n")
        if idx == -1:
            a = data
            b = ""
        else:
            a = data[:idx]
            rest = data[idx + 1:]
            idx2 = rest.find("\n")
            if idx2 == -1:
                b = rest
            else:
                b = rest[:idx2]

    dist = levenshtein(a, b)
    sys.stdout.write(f"{dist}\n")

if __name__ == "__main__":
    main()
```