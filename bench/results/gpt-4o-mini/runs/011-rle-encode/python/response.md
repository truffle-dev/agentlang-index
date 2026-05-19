```python
import sys

def rle_encode(data):
    if not data:
        return
    
    count = 1
    byte = data[0]
    
    for i in range(1, len(data)):
        if data[i] == byte:
            count += 1
        else:
            sys.stdout.write(f"{count} {byte}\n")
            byte = data[i]
            count = 1
    
    sys.stdout.write(f"{count} {byte}\n")

if __name__ == "__main__":
    input_data = sys.stdin.read()
    rle_encode(input_data.encode('latin1'))
```