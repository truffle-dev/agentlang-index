```python
import sys

def reverse_words(line):
    words = line.split()
    if words:
        return ' '.join(reversed(words)) + '\n'
    return ''

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    output = reverse_words(input_line)
    sys.stdout.write(output)
```