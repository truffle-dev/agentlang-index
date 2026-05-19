```python
import sys

def is_balanced(s):
    stack = []
    matching_bracket = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != matching_bracket[char]:
                return False
            stack.pop()
    
    return not stack

def main():
    input_line = sys.stdin.read().strip()
    if is_balanced(input_line):
        sys.stdout.write("yes\n")
    else:
        sys.stdout.write("no\n")

if __name__ == "__main__":
    main()
```