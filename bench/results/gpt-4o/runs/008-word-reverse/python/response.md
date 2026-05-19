```python
import sys

def main():
    input_line = sys.stdin.read().strip()
    if input_line:
        words = input_line.split()
        if words:
            reversed_words = ' '.join(reversed(words))
            sys.stdout.write(reversed_words + '\n')

if __name__ == "__main__":
    main()
```