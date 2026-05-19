```python
import sys

def run_length_encode(input_string):
    if not input_string or any(c < 'a' or c > 'z' for c in input_string):
        return "error\n"
    
    result = []
    current_char = input_string[0]
    count = 1
    
    for char in input_string[1:]:
        if char == current_char:
            count += 1
        else:
            result.append(f"{current_char}{count}")
            current_char = char
            count = 1
    
    result.append(f"{current_char}{count}")
    return ''.join(result) + '\n'

def main():
    input_data = sys.stdin.read().strip()
    output = run_length_encode(input_data)
    sys.stdout.write(output)

if __name__ == "__main__":
    main()
```