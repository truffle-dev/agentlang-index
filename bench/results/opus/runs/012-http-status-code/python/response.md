```python
import sys
import urllib.request
import urllib.error

def main():
    url = sys.stdin.read().strip()
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=5)
        sys.stdout.write(f"{resp.status}\n")
    except urllib.error.HTTPError as e:
        sys.stdout.write(f"{e.code}\n")
    except Exception:
        sys.stdout.write("error\n")

main()
```