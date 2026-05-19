```python
import sys
import json
import requests

def main():
    input_data = sys.stdin.read().strip().split('\n')
    if len(input_data) != 3:
        sys.stdout.write("error\n")
        return

    url, a, b = input_data
    try:
        a = int(a.strip())
        b = int(b.strip())
    except ValueError:
        sys.stdout.write("error\n")
        return

    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"a": a, "b": b})

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=5)
        if response.status_code != 200:
            sys.stdout.write("error\n")
            return

        response_json = response.json()
        if 'sum' in response_json and isinstance(response_json['sum'], int):
            sys.stdout.write(f"{response_json['sum']}\n")
        else:
            sys.stdout.write("error\n")
    except (requests.RequestException, json.JSONDecodeError):
        sys.stdout.write("error\n")

if __name__ == "__main__":
    main()
```