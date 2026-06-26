```python
import sys

words = sys.stdin.read().split()
if words:
    sys.stdout.write(" ".join(reversed(words)) + "\n")
```