```python
import sys

def main():
    input_data = sys.stdin.read().strip().splitlines()
    
    if len(input_data) < 2:
        sys.stdout.write("error\n")
        return
    
    shift_line = input_data[0].strip()
    plaintext = input_data[1]
    
    if not shift_line or not shift_line.isdigit():
        sys.stdout.write("error\n")
        return
    
    shift = int(shift_line)
    
    if shift < 0 or shift > 25:
        sys.stdout.write("error\n")
        return
    
    if not plaintext or any(c < 'a' or c > 'z' for c in plaintext):
        sys.stdout.write("error\n")
        return
    
    ciphertext = ''.join(chr((ord(c) - ord('a') + shift) % 26 + ord('a')) for c in plaintext)
    sys.stdout.write(ciphertext + "\n")

if __name__ == "__main__":
    main()
```