```python
import sys
import urllib.request
import urllib.error

def main():
    data = sys.stdin.read()
    lines = data.splitlines()
    url = lines[0].rstrip() if len(lines) > 0 else ""
    header_name = lines[1].rstrip() if len(lines) > 1 else ""

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                sys.stdout.write("error\n")
                return
            headers = resp.headers
            value = headers.get(header_name)
            if value is None:
                sys.stdout.write("error\n")
                return
            sys.stdout.write(value + "\n")
    except Exception:
        sys.stdout.write("error\n")

main()
```