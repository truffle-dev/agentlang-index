```python
import sys
import urllib.request
import urllib.error

def main():
    data = sys.stdin.read()
    lines = data.splitlines()
    if len(lines) < 2:
        sys.stdout.write("error\n")
        return
    url = lines[0].rstrip()
    header_name = lines[1].rstrip()
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                sys.stdout.write("error\n")
                return
            val = resp.headers.get(header_name)
            if val is None:
                sys.stdout.write("error\n")
                return
            sys.stdout.write(val + "\n")
    except Exception:
        sys.stdout.write("error\n")

main()
```