```python
import sys

data = sys.stdin.buffer.read()
counts = [0] * 256
for b in data:
    counts[b] += 1
out = []
for i in range(256):
    if counts[i]:
        out.append(f"{i} {counts[i]}\n")
sys.stdout.write("".join(out))
```