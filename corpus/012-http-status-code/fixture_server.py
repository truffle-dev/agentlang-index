#!/usr/bin/env python3
# HTTP fixture for 012-http-status-code.
#
# Routes:
#   GET /status/<code>      -> returns HTTP <code> with an empty body
#   GET /                   -> 200 OK
#   GET anything else       -> 200 OK
#
# Listens on the port given as argv[1] (default 18012). Suppresses the
# stderr access log so verify.sh can assert stderr-empty on the parent
# shell. Prints "ready\n" to stdout once the listen socket is open.
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        code = 200
        if path.startswith("/status/"):
            tail = path[len("/status/"):]
            try:
                code = int(tail)
            except ValueError:
                code = 200
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, *args, **kwargs):
        pass


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18012
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("ready", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
