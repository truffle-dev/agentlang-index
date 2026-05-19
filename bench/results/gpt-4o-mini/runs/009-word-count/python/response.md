```python
import sys

def count_words(input_bytes):
    whitespace = {b' ', b'\t', b'\n', b'\r'}
    in_word = False
    word_count = 0

    for byte in input_bytes:
        if byte in whitespace:
            if in_word:
                in_word = False
        else:
            if not in_word:
                in_word = True
                word_count += 1

    return word_count

def main():
    input_bytes = sys.stdin.read().encode('utf-8')
    word_count = count_words(input_bytes)
    sys.stdout.write(f"{word_count}\n")

if __name__ == "__main__":
    main()
```