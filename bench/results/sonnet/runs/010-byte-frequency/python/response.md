```python
import sys
from collections import Counter

data = sys.stdin.buffer.read()
counts = Counter(data)
for b in range(256):
    if counts[b]:
        sys.stdout.write(f"{b} {counts[b]}\n")
```