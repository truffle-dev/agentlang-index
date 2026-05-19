```python
import sys
from collections import Counter

def main():
    # Read all bytes from standard input
    data = sys.stdin.read()
    
    # Count occurrences of each byte value
    byte_counts = Counter(data)
    
    # Prepare output
    output_lines = []
    for byte_value in range(256):
        count = byte_counts.get(bytes([byte_value]), 0)
        if count > 0:
            output_lines.append(f"{byte_value} {count}\n")
    
    # Write output to standard output
    sys.stdout.write(''.join(output_lines))

if __name__ == "__main__":
    main()
```