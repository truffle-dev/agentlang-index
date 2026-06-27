## Spec

# 014-http-header-echo

Read two newline-terminated lines from standard input:

1. A URL — the endpoint to GET.
2. A header name to echo.

Issue an HTTP GET request to the URL with a 5000 millisecond
transport timeout.

On a transport-successful HTTP 200 response, locate the named
response header (case-insensitive on the name) and write its
value followed by a newline to standard output (e.g.
`application/json\n`).

On any failure — transport error (DNS, connect, TLS, timeout,
invalid URL, unsupported protocol, provider unavailable, I/O),
non-200 status, or the named header is not present — write the
literal string `error\n` to standard output instead. Do not
write to standard error. Exit with status 0 in every case.

Trailing whitespace on either input line should be trimmed
before use. Header name comparison is ASCII case-insensitive.
The echoed value bytes are exactly what the platform helper
returns; HTTP value trimming (leading/trailing whitespace inside
the value) is delegated to the helper.

## Examples

Input (stdin, two lines):

```
http://127.0.0.1:18014/headers
X-Echo
```

Output (stdout):

```
hello-world
```

Input (stdin):

```
http://127.0.0.1:18014/headers
content-type
```

Output (stdout):

```
application/json
```

Input (stdin):

```
http://127.0.0.1:18014/404
X-Echo
```

Output (stdout):

```
error
```

Input (stdin):

```
http://this-host-does-not-resolve.invalid/headers
X-Echo
```

Output (stdout):

```
error
```

## Acceptance

- stdout matches the expected bytes exactly per test case
- stderr is empty
- exit code is 0
- the run completes within 10 seconds wall time

## Input convention by language

- **TypeScript / Rust / Go / Python**: read two lines from stdin.
- **Zero**: take URL from `argv[1]`, header name from `argv[2]`
  because Zero 0.1.2 does not expose a standard-input
  capability. The byte semantics are the same.

## Verifier fixture

The verifier starts a local Python HTTP fixture server on port
18014 before running the references and tears it down after.

- `GET /headers` — returns HTTP 200 with headers
  `Content-Type: application/json`, `X-Echo: hello-world`, and
  `X-Custom-Name: first-value`. Body is `{}`.
- `GET /json` — returns HTTP 200 with `Content-Type: application/json`
  only. Body is `{}`.
- `GET /empty` — returns HTTP 200 with `Content-Type: text/plain`
  and no extra headers. Body is empty.
- `GET /404` — returns HTTP 404 with `X-Echo: shouldnotappear`.
  Body is empty.

References target `http://127.0.0.1:18014/<path>` for all
fixture-based cases. The transport-failure case points at a
name that does not resolve.

## Single-file Zero layout

Write a single-file Zero program (ref.0). Read arguments from std.args (no stdin available). It is compiled with `zero import ref.0 --out ref.graph` and executed as: zero run ref.graph <argv...>
