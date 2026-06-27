```python
import sys

def solve():
    line = sys.stdin.read().rstrip('\n')
    stack = []
    match = {')': '(', ']': '[', '}': '{'}
    for ch in line:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack[-1] != match[ch]:
                sys.stdout.write('no\n')
                return
            stack.pop()
    sys.stdout.write('yes\n' if not stack else 'no\n')

solve()
```