```python
import sys

data = sys.stdin.buffer.read()
if data:
    cur = data[0]
    count = 1
    for b in data[1:]:
        if b == cur:
            count += 1
        else:
            sys.stdout.write(f"{count} {cur}\n")
            cur = b
            count = 1
    sys.stdout.write(f"{count} {cur}\n")
```