```python
import sys
import urllib.request
import json

def main():
    try:
        lines = sys.stdin.read().splitlines()
        url = lines[0].strip()
        a = int(lines[1].strip())
        b = int(lines[2].strip())
        body = json.dumps({"a": a, "b": b}, separators=(",", ":")).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                sys.stdout.write("error\n")
                return
            data = json.loads(resp.read())
            s = data["sum"]
            if not isinstance(s, int) or isinstance(s, bool):
                sys.stdout.write("error\n")
                return
            sys.stdout.write(f"{s}\n")
    except Exception:
        sys.stdout.write("error\n")

main()
```