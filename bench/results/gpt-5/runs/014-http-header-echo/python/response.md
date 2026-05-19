```python
import sys
import urllib.request
import urllib.error

def main():
    try:
        data = sys.stdin.read()
        lines = data.splitlines()
        if len(lines) < 2:
            sys.stdout.write("error\n")
            return

        url = lines[0].rstrip()
        header_name = lines[1].rstrip()

        if not url or not header_name:
            sys.stdout.write("error\n")
            return

        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                status = getattr(resp, "status", None)
                if status is None:
                    status = resp.getcode()
                if status != 200:
                    sys.stdout.write("error\n")
                    return
                value = resp.getheader(header_name)
                if value is None:
                    sys.stdout.write("error\n")
                    return
                sys.stdout.write(value + "\n")
        except Exception:
            sys.stdout.write("error\n")
            return
    except Exception:
        sys.stdout.write("error\n")
        return

if __name__ == "__main__":
    main()
```