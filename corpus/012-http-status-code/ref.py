#!/usr/bin/env python3
import sys
import urllib.request
import urllib.error


def main() -> int:
    url = sys.stdin.read().strip()
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
    except (urllib.error.URLError, ValueError, OSError, TimeoutError):
        sys.stdout.write("error\n")
        return 0
    sys.stdout.write(f"{status}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
