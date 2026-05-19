```python
import sys
import urllib.request
import urllib.error

def main():
    data = sys.stdin.read()
    if data is None:
        data = ""
    url = data.rstrip("\r\n")
    timeout = 5.0

    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        req = urllib.request.Request(url=url, method="GET")
        try:
            with opener.open(req, timeout=timeout) as resp:
                status = resp.getcode()
                if status is None:
                    raise Exception("No status code")
                sys.stdout.write(f"{int(status)}\n")
        except urllib.error.HTTPError as e:
            # HTTPError indicates a valid HTTP response with a non-2xx status
            sys.stdout.write(f"{int(e.code)}\n")
    except Exception:
        sys.stdout.write("error\n")

if __name__ == "__main__":
    main()
```