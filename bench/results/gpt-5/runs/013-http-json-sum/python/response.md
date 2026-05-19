```python
import sys
import json
from urllib import request, error

def main():
    try:
        data = sys.stdin.read().splitlines()
        if len(data) < 3:
            raise Exception("insufficient input")
        url = data[0]
        try:
            a = int(data[1].strip())
            b = int(data[2].strip())
        except Exception:
            raise

        body_str = f'{{"a":{a},"b":{b}}}'
        body = body_str.encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        req = request.Request(url, data=body, headers=headers, method='POST')

        try:
            with request.urlopen(req, timeout=5.0) as resp:
                status = getattr(resp, 'status', resp.getcode())
                if status != 200:
                    raise Exception("non-200")
                resp_body = resp.read()
        except error.HTTPError:
            raise
        except Exception:
            raise

        try:
            text = resp_body.decode('utf-8')
            obj = json.loads(text)
            if not isinstance(obj, dict):
                raise Exception("not object")
            val = obj.get('sum', None)
            if not (isinstance(val, int) and not isinstance(val, bool)):
                raise Exception("sum not int")
        except Exception:
            raise

        sys.stdout.write(f"{val}\n")
    except Exception:
        sys.stdout.write("error\n")

if __name__ == "__main__":
    main()
```