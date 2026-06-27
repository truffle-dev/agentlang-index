```python
import sys

def main():
    data = sys.stdin.read()
    lines = data.split('\n')
    P = lines[0]
    T = lines[1] if len(lines) > 1 else ''
    
    count = 0
    i = 0
    plen = len(P)
    while i <= len(T) - plen:
        if T[i:i+plen] == P:
            count += 1
            i += plen
        else:
            i += 1
    
    sys.stdout.write(str(count) + '\n')

main()
```