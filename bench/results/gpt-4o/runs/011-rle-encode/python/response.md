```python
import sys

def rle_encode(data):
    if not data:
        return
    
    current_byte = data[0]
    count = 1
    
    for byte in data[1:]:
        if byte == current_byte:
            count += 1
        else:
            yield f"{count} {current_byte}\n"
            current_byte = byte
            count = 1
    
    yield f"{count} {current_byte}\n"

def main():
    data = sys.stdin.read().encode('latin1')
    sys.stdout.write(''.join(rle_encode(data)))

if __name__ == "__main__":
    main()
```