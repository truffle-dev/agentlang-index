```python
import sys

def main():
    counts = [0] * 256
    buf = sys.stdin.buffer

    # Read input in chunks to handle large inputs efficiently
    read = buf.read
    chunk_size = 1 << 20  # 1 MiB
    while True:
        chunk = read(chunk_size)
        if not chunk:
            break
        for b in chunk:
            counts[b] += 1

    # Build output
    out_lines = []
    append = out_lines.append
    for i, c in enumerate(counts):
        if c:
            append(f"{i} {c}\n")

    sys.stdout.write(''.join(out_lines))

if __name__ == "__main__":
    main()
```