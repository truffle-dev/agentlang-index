```python
import sys
import json
import requests

def main():
    try:
        input_data = sys.stdin.read().strip().splitlines()
        url = input_data[0].strip()
        a = int(input_data[1].strip())
        b = int(input_data[2].strip())
        
        response = requests.post(url, json={"a": a, "b": b}, timeout=5)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'sum' in response_data and isinstance(response_data['sum'], int):
                sys.stdout.write(f"{response_data['sum']}\n")
                return
        sys.stdout.write("error\n")
    except Exception:
        sys.stdout.write("error\n")

if __name__ == "__main__":
    main()
```