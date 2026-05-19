```python
import sys
import requests

def main():
    input_data = sys.stdin.read().strip().splitlines()
    
    if len(input_data) < 2:
        sys.stdout.write("error\n")
        return
    
    url = input_data[0].strip()
    header_name = input_data[1].strip()
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            header_value = response.headers.get(header_name)
            if header_value is not None:
                sys.stdout.write(f"{header_value}\n")
            else:
                sys.stdout.write("error\n")
        else:
            sys.stdout.write("error\n")
    except Exception:
        sys.stdout.write("error\n")

if __name__ == "__main__":
    main()
```