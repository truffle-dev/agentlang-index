#!/usr/bin/env python3
"""Local HTTP fixture for task 014-http-header-echo.

Listens on 127.0.0.1:<port> (default 18014), serves four GET routes:

- /headers -> 200 with Content-Type, X-Echo, and X-Custom-Name
- /json    -> 200 with Content-Type only
- /empty   -> 200 with Content-Type text/plain, no extras
- /404     -> 404 with X-Echo: shouldnotappear

Other paths return 404. Prints `ready` to stdout once listening so
the verifier can poll for readiness.
"""
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args, **_kwargs):
        pass

    def _send(self, status: int, body: bytes, extra_headers=None):
        self.send_response(status)
        if extra_headers:
            for name, value in extra_headers:
                self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        path = self.path
        if path == "/headers":
            self._send(
                200,
                b"{}",
                extra_headers=[
                    ("Content-Type", "application/json"),
                    ("X-Echo", "hello-world"),
                    ("X-Custom-Name", "first-value"),
                ],
            )
        elif path == "/json":
            self._send(
                200,
                b"{}",
                extra_headers=[("Content-Type", "application/json")],
            )
        elif path == "/empty":
            self._send(
                200,
                b"",
                extra_headers=[("Content-Type", "text/plain")],
            )
        elif path == "/404":
            self._send(
                404,
                b"",
                extra_headers=[("X-Echo", "shouldnotappear")],
            )
        else:
            self._send(404, b"")

    def do_POST(self):
        self._send(404, b"")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18014
    ThreadingHTTPServer.allow_reuse_address = True
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
