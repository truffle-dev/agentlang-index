```python
import sys

def count_non_overlapping(pattern, text):
    count = 0
    start = 0
    while True:
        start = text.find(pattern, start)
        if start == -1:
            break
        count += 1
        start += len(pattern)
    return count

def main():
    input_data = sys.stdin.read().strip().splitlines()
    if len(input_data) < 2:
        sys.stdout.write("0\n")
        return
    
    pattern = input_data[0]
    text = input_data[1]
    
    result = count_non_overlapping(pattern, text)
    sys.stdout.write(f"{result}\n")

if __name__ == "__main__":
    main()
```