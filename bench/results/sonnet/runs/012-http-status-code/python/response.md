```python
import sys
import urllib.request

def main():
    url = sys.stdin.read().strip()
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            sys.stdout.write(f"{resp.status}\n")
    except Exception:
        sys.stdout.write("error\n")

main()
```