```python
import sys

def caesar_cipher(shift_str, plaintext):
    # Validate and parse shift
    shift_str = shift_str.strip()
    if not shift_str.isdigit():
        return "error\n"
    
    shift = int(shift_str)
    if shift < 0 or shift > 25:
        return "error\n"
    
    # Validate plaintext
    if not plaintext or any(c < 'a' or c > 'z' for c in plaintext):
        return "error\n"
    
    # Perform the shift
    ciphertext = []
    for char in plaintext:
        new_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
        ciphertext.append(new_char)
    
    return ''.join(ciphertext) + '\n'

def main():
    input_data = sys.stdin.read().splitlines()
    if len(input_data) != 2:
        sys.stdout.write("error\n")
        return
    
    shift_str, plaintext = input_data
    result = caesar_cipher(shift_str, plaintext)
    sys.stdout.write(result)

if __name__ == "__main__":
    main()
```