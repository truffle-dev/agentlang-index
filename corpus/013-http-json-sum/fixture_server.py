#!/usr/bin/env python3
"""Local HTTP fixture for task 013-http-json-sum.

Listens on 127.0.0.1:<port> (default 18013), serves four POST routes:

- /sum      -> parse JSON {"a":n,"b":m}, return {"sum":n+m}, HTTP 200
- /missing  -> return {"other":99}, HTTP 200
- /badjson  -> return literal body `not-json`, HTTP 200
- /404      -> return HTTP 404 with empty body

Other paths return 404. Prints `ready` to stdout once listening so
the verifier can poll for readiness.
"""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args, **_kwargs):
        pass

    def _send(self, status: int, body: bytes, content_type: str = "application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length > 0 else b""
        path = self.path
        if path == "/sum":
            try:
                data = json.loads(raw.decode("utf-8"))
                a = int(data["a"])
                b = int(data["b"])
                body = json.dumps({"sum": a + b}, separators=(",", ":")).encode("utf-8")
                self._send(200, body)
            except Exception:
                self._send(400, b"{}")
        elif path == "/missing":
            body = json.dumps({"other": 99}, separators=(",", ":")).encode("utf-8")
            self._send(200, body)
        elif path == "/badjson":
            self._send(200, b"not-json", content_type="application/json")
        elif path == "/404":
            self._send(404, b"")
        else:
            self._send(404, b"")

    def do_GET(self):
        self._send(404, b"")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18013
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    sys.stdout.write("ready\n")
    sys.stdout.flush()
    try:
        t.join()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
