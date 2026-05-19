```python
import sys
from collections import defaultdict

def main():
    input_bytes = sys.stdin.read().encode('latin1')
    byte_count = defaultdict(int)

    for byte in input_bytes:
        byte_count[byte] += 1

    for byte in range(256):
        if byte_count[byte] > 0:
            sys.stdout.write(f"{byte} {byte_count[byte]}\n")

if __name__ == "__main__":
    main()
```