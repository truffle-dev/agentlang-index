# 013-http-json-sum

Read three newline-terminated lines from standard input:

1. A URL — the endpoint to POST to.
2. An integer `a`.
3. An integer `b`.

Issue an HTTP POST request to the URL with:

- A 5000 millisecond transport timeout.
- Header `Content-Type: application/json`.
- Body `{"a":<a>,"b":<b>}` (no whitespace inside the JSON).

On a transport-successful HTTP 200 response whose body parses as a
JSON object containing an integer `sum` field, write that integer
as decimal followed by a newline to standard output (e.g. `7\n`).

On any failure — transport error (DNS, connect, TLS, timeout,
invalid URL, unsupported protocol, provider unavailable, I/O),
non-200 status, JSON parse error, or `sum` field missing /
non-integer — write the literal string `error\n` to standard
output instead. Do not write to standard error. Exit with status 0
in every case.

All integers (a, b, sum) fit in `i32`. Trailing whitespace on the
two digit lines should be trimmed before use.

## Examples

Input (stdin, three lines):

```
http://localhost:18013/sum
3
4
```

Output (stdout):

```
7
```

Input (stdin):

```
http://localhost:18013/sum
100
200
```

Output (stdout):

```
300
```

Input (stdin):

```
http://localhost:18013/404
1
1
```

Output (stdout):

```
error
```

Input (stdin):

```
http://this-host-does-not-resolve.invalid/sum
1
1
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

- **TypeScript / Rust / Go / Python**: read three lines from stdin.
- **Zero**: take URL from `argv[1]`, a from `argv[2]`, b from
  `argv[3]` because Zero 0.1.2 does not expose a standard-input
  capability. The byte semantics are the same — Zero callers
  should treat the three argv strings identically to three stdin
  reads.

## Verifier fixture

The verifier starts a local Python HTTP fixture server on port
18013 before running the references and tears it down after.

- `POST /sum` — parses JSON body `{"a":n,"b":m}`, returns
  `{"sum":n+m}` with HTTP 200 and `Content-Type: application/json`.
- `POST /missing` — returns `{"other":99}` (no `sum` field) with
  HTTP 200.
- `POST /badjson` — returns the literal body `not-json` with
  HTTP 200.
- `POST /404` — returns HTTP 404 with an empty body.

References target `http://127.0.0.1:18013/<path>` for the
happy-path and structured-failure cases. The transport-failure
case points at a name that does not resolve.

## Language scaffold

{language_scaffold}
