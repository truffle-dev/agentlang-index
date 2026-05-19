```python
import sys
import requests

def main():
    url = sys.stdin.read().strip()
    try:
        response = requests.get(url, timeout=5)
        sys.stdout.write(f"{response.status_code}\n")
    except Exception:
        sys.stdout.write("error\n")

if __name__ == "__main__":
    main()
```