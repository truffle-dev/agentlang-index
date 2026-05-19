```python
import sys
import requests

def main():
    input_data = sys.stdin.read().strip().split('\n')
    if len(input_data) != 2:
        sys.stdout.write("error\n")
        return

    url = input_data[0].strip()
    header_name = input_data[1].strip()

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            headers = response.headers
            for key, value in headers.items():
                if key.lower() == header_name.lower():
                    sys.stdout.write(f"{value}\n")
                    return
        sys.stdout.write("error\n")
    except requests.RequestException:
        sys.stdout.write("error\n")

if __name__ == "__main__":
    main()
```