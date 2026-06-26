```python
import sys

data = sys.stdin.buffer.read()
if not data:
    sys.exit(0)

out = []
prev = data[0]
count = 1
for b in data[1:]:
    if b == prev:
        count += 1
    else:
        out.append(f"{count} {prev}\n")
        prev = b
        count = 1
out.append(f"{count} {prev}\n")
sys.stdout.write("".join(out))
```