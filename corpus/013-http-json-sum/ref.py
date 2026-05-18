#!/usr/bin/env python3
"""HTTP POST + JSON sum reference for AgentLang Index."""
import json
import sys
import urllib.error
import urllib.request


def main() -> int:
    try:
        lines = sys.stdin.read().splitlines()
        url = lines[0].strip()
        a = int(lines[1].strip())
        b = int(lines[2].strip())
    except (IndexError, ValueError, OSError):
        sys.stdout.write("error\n")
        return 0

    body = f'{{"a":{a},"b":{b}}}'.encode("ascii")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                sys.stdout.write("error\n")
                return 0
            response_body = resp.read()
    except urllib.error.HTTPError:
        sys.stdout.write("error\n")
        return 0
    except (urllib.error.URLError, ValueError, OSError, TimeoutError):
        sys.stdout.write("error\n")
        return 0

    try:
        parsed = json.loads(response_body.decode("utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError
        s = parsed.get("sum")
        if not isinstance(s, int) or isinstance(s, bool):
            raise ValueError
        sys.stdout.write(f"{s}\n")
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        sys.stdout.write("error\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
