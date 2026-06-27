```python
import sys
import json
import urllib.request
import urllib.error

def main():
    data = sys.stdin.read().splitlines()
    url = data[0].strip()
    a = data[1].strip()
    b = data[2].strip()

    body = f'{{"a":{a},"b":{b}}}'.encode()

    try:
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                sys.stdout.write("error\n")
                return
            raw = resp.read()
    except Exception:
        sys.stdout.write("error\n")
        return

    try:
        obj = json.loads(raw)
        s = obj["sum"]
        if not isinstance(s, int) or isinstance(s, bool):
            sys.stdout.write("error\n")
            return
        sys.stdout.write(f"{s}\n")
    except Exception:
        sys.stdout.write("error\n")

main()
```