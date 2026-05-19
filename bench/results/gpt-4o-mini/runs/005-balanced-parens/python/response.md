```python
import sys

def is_balanced(s):
    stack = []
    matching_bracket = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in matching_bracket.values():  # If it's an opener
            stack.append(char)
        elif char in matching_bracket.keys():  # If it's a closer
            if not stack or stack[-1] != matching_bracket[char]:
                return "no\n"
            stack.pop()
    
    return "yes\n" if not stack else "no\n"

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    result = is_balanced(input_line)
    sys.stdout.write(result)
```