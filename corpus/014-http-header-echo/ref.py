#!/usr/bin/env python3
"""Reference implementation for 014-http-header-echo (Python)."""
import sys
import urllib.request
import urllib.error


def main() -> int:
    try:
        lines = sys.stdin.read().splitlines()
        if len(lines) < 2:
            sys.stdout.write("error\n")
            return 0
        url = lines[0].strip()
        name = lines[1].strip()
        if not url or not name:
            sys.stdout.write("error\n")
            return 0
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                if resp.status != 200:
                    sys.stdout.write("error\n")
                    return 0
                value = resp.headers.get(name)
                if value is None:
                    sys.stdout.write("error\n")
                    return 0
                sys.stdout.write(value + "\n")
                return 0
        except Exception:
            sys.stdout.write("error\n")
            return 0
    except Exception:
        sys.stdout.write("error\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
