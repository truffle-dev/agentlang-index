```python
import sys

def main():
    try:
        data = sys.stdin.buffer.read()
        try:
            sys.stdout.reconfigure(newline='\n')
        except Exception:
            pass

        if not data:
            return

        out = sys.stdout.write

        prev = data[0]
        count = 1
        n = len(data)

        for i in range(1, n):
            b = data[i]
            if b == prev:
                count += 1
            else:
                out(f"{count} {prev}\n")
                prev = b
                count = 1
        out(f"{count} {prev}\n")
    except SystemExit:
        pass
    except Exception:
        try:
            sys.stdout.write("error\n")
        except Exception:
            pass

if __name__ == "__main__":
    main()
```