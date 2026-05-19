```python
import sys
import re

def tokenize_csv_line(line):
    # Regular expression to match CSV fields
    pattern = r'''
        (                   # Start of group for capturing fields
            "([^"]|"")*"   # Quoted field: starts and ends with ", can contain "" for a literal "
            |              # OR
            [^,""]+       # Unquoted field: any sequence of characters except , and "
        )
    '''
    return re.findall(pattern, line, re.VERBOSE)

def main():
    line = sys.stdin.read().strip()
    if line:
        fields = tokenize_csv_line(line)
        for field in fields:
            sys.stdout.write(field[0] + '\n')

if __name__ == "__main__":
    main()
```