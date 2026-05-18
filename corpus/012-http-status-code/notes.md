# Notes — 012-http-status-code

## Algorithm

There is no algorithm. The task is direct: read a URL, GET it, write
the HTTP status code as decimal, write `error` on transport failure.
All references converge on the same shape: read input → call the
language's HTTP client → branch on transport-success-vs-error →
write the decimal status code or the literal `error\n`.

## Fixture

A local Python HTTP server listens on `127.0.0.1:18012` while
`verify.sh` runs the references. Routes:

- `/status/<code>` returns HTTP `<code>` with an empty body
- `/` and any other path return 200 OK

`verify.sh` starts the fixture in the background, waits for it to
print `ready` on stdout, runs all references against six cases, and
kills the fixture on exit. The unresolvable-host case
(`http://this-host-does-not-resolve.invalid/`) does not touch the
fixture; it exercises every reference's transport-error path.

## Edge cases

- Trailing newline on the URL must be trimmed before use.
- The `/status/<code>` route is the contract; the references must
  treat the status code as a number, not as text from a body.
- Transport-failure path covers DNS failure, connect-refused, TLS
  error, timeout, invalid URL, unsupported protocol, provider
  unavailable, and I/O failure. All collapse to `error\n`.

## Zero-specific notes

- argv[1] carries the URL because Zero 0.1.2 has no exposed stdin.
- The HTTP request envelope for `std.http.fetch` is `GET <url>\n\n`
  in a `[320]u8` buffer; the URL is bounded by the 256-byte spec
  cap so the envelope fits with overhead.
- Response buffer is `[8192]u8`. The references use only the status
  field via `std.http.resultStatus`, so body and header parsing is
  not exercised here.
- Decimal renderer reuses the small-divisor u32 divmod pattern from
  prior tasks (avoids the 2^32-divisor SIGFPE).
- The Zero `std.http.fetch` provider is implemented in libcurl and
  is link-time. On a VM without `libcurl4-openssl-dev`, the Zero
  build fails at link time with `BLD003: host runtime link failed`.
  Userland fix: extract the deb into `~/.local/include` and symlink
  `~/.local/lib/libcurl.so` → `/usr/lib/x86_64-linux-gnu/libcurl.so.4`,
  then `export C_INCLUDE_PATH=~/.local/include` and
  `export LIBRARY_PATH=~/.local/lib`. These are wired into
  `~/.config/truffle/env.sh` for this machine.
- Zero 0.1.2 codegen leaks the trailing `world.out.write(...)`
  return value (bytes written) as the process exit code unless main
  has an explicit `return` at the end. Symptom: stdout shows `200`
  but exit is `4`. Fix: end main with `return`.

## Cross-implementation parity

All five references issue a GET, observe one HTTP transaction, and
write `<status>\n` on success or `error\n` on failure. No retries,
no redirects (each reference explicitly opts out of redirect
following), no body inspection. Byte-exact agreement on every case.
