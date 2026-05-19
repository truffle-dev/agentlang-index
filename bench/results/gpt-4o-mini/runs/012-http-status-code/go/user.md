## Spec

# 012-http-status-code

Read a single URL from standard input. Issue an HTTP GET request to
that URL with a 5000 millisecond transport timeout. Write the HTTP
response status code as decimal followed by a newline to standard
output (e.g. `200\n`).

If the transport fails for any reason — DNS lookup failure, connect
refused, TLS error, request timed out, invalid URL, unsupported
protocol, the HTTP provider being unavailable, or any I/O error —
write the literal string `error\n` to standard output instead of a
status code. Do not write to standard error in either case. Exit
with status 0 in every case.

The URL on stdin may have a trailing newline; trim it before use.

## Examples

Input (stdin):

```
http://localhost:18012/status/200
```

Output (stdout):

```
200
```

Input (stdin):

```
http://localhost:18012/status/404
```

Output (stdout):

```
404
```

Input (stdin):

```
http://this-host-does-not-resolve.invalid/
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

- **TypeScript / Rust / Go / Python**: read the URL from stdin until
  newline or EOF; trim trailing newline.
- **Zero**: take the URL from `argv[1]` because Zero 0.1.2 does not
  expose a standard-input capability. The byte semantics are the
  same — Zero callers should treat the argv string identically to a
  stdin read.

## Verifier fixture

The verifier starts a local Python HTTP fixture server on port 18012
before running the references and tears it down after. The server
responds to `/status/<code>` with status `<code>` and an empty body,
to `/` with 200 OK, and to any other path with 200 OK. References
target `http://localhost:18012/...` for the happy-path cases. For
the transport-failure cases the URL points at a name that does not
resolve, so the reference must surface the failure as `error\n`.
