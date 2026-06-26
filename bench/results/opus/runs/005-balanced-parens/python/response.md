```python
import sys

def main():
    line = sys.stdin.read().strip('\n')
    stack = []
    match = {')': '(', ']': '[', '}': '{'}
    for c in line:
        if c in '([{':
            stack.append(c)
        elif c in ')]}':
            if not stack or stack[-1] != match[c]:
                sys.stdout.write('no\n')
                return
            stack.pop()
    sys.stdout.write('yes\n' if not stack else 'no\n')

main()
```