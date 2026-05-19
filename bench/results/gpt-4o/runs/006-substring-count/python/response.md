```python
import sys

def count_non_overlapping_occurrences(pattern, text):
    count = 0
    i = 0
    pattern_length = len(pattern)
    text_length = len(text)
    
    while i <= text_length - pattern_length:
        if text[i:i + pattern_length] == pattern:
            count += 1
            i += pattern_length
        else:
            i += 1
    
    return count

def main():
    input_data = sys.stdin.read().strip().split('\n')
    if len(input_data) != 2:
        sys.stdout.write("error\n")
        return
    
    pattern = input_data[0]
    text = input_data[1]
    
    result = count_non_overlapping_occurrences(pattern, text)
    sys.stdout.write(f"{result}\n")

if __name__ == "__main__":
    main()
```