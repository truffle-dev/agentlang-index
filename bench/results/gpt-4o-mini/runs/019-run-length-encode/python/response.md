```python
import sys

def run_length_encode(s):
    if not s or any(c < 'a' or c > 'z' for c in s):
        return "error\n"
    
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(f"{s[i - 1]}{count}")
            count = 1
    result.append(f"{s[-1]}{count}")
    
    return ''.join(result) + '\n'

if __name__ == "__main__":
    input_string = sys.stdin.read().strip()
    output = run_length_encode(input_string)
    sys.stdout.write(output)
```