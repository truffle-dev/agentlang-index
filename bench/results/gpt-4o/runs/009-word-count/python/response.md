```python
import sys

def count_words(input_bytes):
    in_word = False
    word_count = 0

    for byte in input_bytes:
        if byte in (0x20, 0x09, 0x0A, 0x0D):  # whitespace bytes
            if in_word:
                in_word = False
        else:
            if not in_word:
                word_count += 1
                in_word = True

    return word_count

def main():
    input_bytes = sys.stdin.read().encode('utf-8')
    word_count = count_words(input_bytes)
    sys.stdout.write(f"{word_count}\n")

if __name__ == "__main__":
    main()
```