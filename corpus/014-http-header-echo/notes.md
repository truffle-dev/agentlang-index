# Notes — 014-http-header-echo

## Algorithm

Read two inputs (URL, header name). GET the URL with a 5-second
transport timeout. On HTTP 200, look up the named header
(case-insensitive on the name) and write its value followed by
`\n`. On any transport error, non-200 status, or missing header,
write `error\n`. Process exit is `0` either way.

## Fixture

A local Python HTTP server listens on `127.0.0.1:18014` while
`verify.sh` runs the references. Routes are all GET:

- `/headers` → returns 200 with `Content-Type: application/json`,
  `X-Echo: hello-world`, `X-Custom-Name: first-value`. Body `{}`.
- `/json`    → returns 200 with `Content-Type: application/json`
  only. Body `{}`.
- `/empty`   → returns 200 with `Content-Type: text/plain` and
  no extras. Body empty.
- `/404`     → returns HTTP 404 with `X-Echo: shouldnotappear`
  (proves that non-200 results suppress header echoing).

`verify.sh` starts the fixture in the background, waits for `ready`
on stdout, runs all references against six cases (three public,
three hidden) covering the four routes, and kills the fixture on
exit.

## Edge cases

- Header name comparison is ASCII case-insensitive on the name;
  matches whatever the underlying HTTP library does.
- Value bytes are echoed exactly as the platform helper returns
  them (no extra trimming beyond what the HTTP layer already
  performs on header value whitespace).
- Inputs are trimmed for leading/trailing whitespace on the
  stdin path (and trusted clean on the Zero argv path).
- Redirects are not followed in any reference.
- Five second wall-clock timeout on every fetch.
- A header that is found but has an empty value writes `\n`
  (the value bytes plus newline). This is a structural choice
  — the spec defines failure as "missing header", not
  "empty-value header".

## Zero-specific notes

- argv[1..2] carry URL and header name because Zero 0.1.2 has
  no exposed stdin.
- The GET envelope shape is `GET <url>\n\n` in a `[1024]u8`
  buffer (method-line, URL, blank line, no body).
- `std.http.headerValue(response, name_span)` returns an
  `HttpHeaderValue` metadata pack. The accessors are
  `std.http.headerFound(value)` (Bool), `std.http.headerOffset(value)`
  (usize byte offset into the response buffer), and
  `std.http.headerLen(value)` (usize byte length). Slice the
  bytes with `response[offset..offset + len]`.
- Header name matching is case-insensitive at the helper level,
  so a stdin name of "content-type" matches a `Content-Type`
  response header without any manual normalization.
- The direct backend ELF64 MVP forbids user functions that take
  or return `Span<u8>` / `MutSpan<u8>` / shape values (the
  "seventh codegen quirk" surfaced in task 013). The body of
  `main` is therefore one inline pass with no helper functions.
- Output is rendered into a `[4096]u8` `out` buffer rather than
  written directly with `response[h_off..h_off + h_len]`. This
  keeps the slice + newline as a single contiguous `world.out.write`,
  which is byte-exact equivalent to two writes but reads cleaner
  and avoids any chance of buffering quirks across the boundary.
- The 5-second timeout is `std.time.ms(5000)` on the `fetch` call;
  on timeout, `resultOk` returns false and the reference falls
  through to the `error\n` path.
- main ends with an explicit `return` to dodge the trailing-write
  byte-count-as-exit-code codegen quirk surfaced in task 012.

## Cross-implementation parity

All five references issue exactly one GET, observe one HTTP
transaction (no redirects), and surface either the named
response header's value bytes (case-insensitive on the name) or
the literal `error\n` for any failure. Byte-exact agreement on
every case.

The Go reference disambiguates "header present with empty value"
from "header missing" via `Header.Values(name)` (since `Get`
returns `""` for both). Rust uses `headers().get(name)`; Python
uses `resp.headers.get(name)` (which returns `None` for missing);
TypeScript uses `headers.get(name)` (which returns `null` for
missing). Zero uses `std.http.headerFound(value)`.
