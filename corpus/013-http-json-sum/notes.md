# Notes — 013-http-json-sum

## Algorithm

Read three inputs (URL, integer `a`, integer `b`). POST a JSON body
`{"a":a,"b":b}` to the URL with `Content-Type: application/json`. On
HTTP 200, parse the response body as JSON, extract integer field
`"sum"`, and write that integer followed by `\n`. On any transport
error, non-200 status, body parse failure, or missing `sum` field,
write `error\n`. Process exit is `0` either way.

## Fixture

A local Python HTTP server listens on `127.0.0.1:18013` while
`verify.sh` runs the references. Routes are all POST:

- `/sum`     → parses request body as JSON, returns `{"sum":a+b}` 200
- `/missing` → returns `{"other":99}` 200 (no `sum` field)
- `/badjson` → returns the literal body `not-json` with status 200
- `/404`     → returns HTTP 404 with empty body

`verify.sh` starts the fixture in the background, waits for `ready`
on stdout, runs all references against six cases (three public,
three hidden) covering the four routes, and kills the fixture on
exit.

## Edge cases

- Inputs are trimmed for leading/trailing whitespace before integer
  parsing.
- `a` and `b` are parsed as i32 with optional leading `-`. Values
  outside i32 range are rejected (write `error\n`).
- The `"sum":` byte literal is matched in the response body; the
  digits that follow are parsed with optional leading `-` and i32
  range validation.
- The byte after the digits must be a JSON terminator (`,`, `}`,
  `]`, whitespace, or end-of-buffer); a trailing non-terminator
  byte rejects the parse.
- Redirects are not followed in any reference.
- Five second wall-clock timeout on every fetch.

## Zero-specific notes

- argv[1..3] carry URL, a, b because Zero 0.1.2 has no exposed stdin.
- The POST envelope shape for `std.http.fetch` is
  `POST <url>\nContent-Type: application/json\n\n{"a":<a>,"b":<b>}`
  in a `[1024]u8` buffer.
- Zero 0.1.2's direct backend ELF64 MVP forbids user functions that
  take or return shape values, `Span<u8>`, or `MutSpan<u8>`. The
  only fully supported user-function signatures are primitive
  integer + Bool parameters and primitive integer + Bool returns.
  Member access on shape values is supported only for
  `Maybe<MutSpan<u8>>.has` and `.value`. Every other shape access
  routes through `CGEN004`. The ref therefore inlines the integer
  parse (twice, once for `a` and once for `b`), the envelope
  decimal renderer (twice), the response body scan, and the output
  renderer all directly into `main`. The same code in a
  helper-function shape is fine for `zero check` but fails at
  `zero build` time.
- `std.json` in Zero 0.1.2 exposes `validate`, `parse`, and
  `streamTokens` but no field accessors. The ref scans for the byte
  literal `"sum":` and parses the integer that follows, validating
  the following byte is a JSON terminator.
- The `(c - 48_u8) as u32` cast must be parenthesized AND bound to
  a typed local (`let digit: u32 = ...`) before being added to a
  `u32` accumulator; the inline form `acc * 10_u32 + (c - 48_u8) as u32`
  trips TYP002 because `as` does not lift the resulting u8 cleanly
  in mixed-type expressions.
- `0_i32 - 2147483648_i64 as i32` is rejected as type-mismatched.
  The ref drops INT_MIN special-casing: any |value| > 2147483647
  is an `error\n`, matching the i32-range contract of the other
  references.
- `std.http.fetch` is provided by libcurl at link time. The userland
  install from task 012 (`~/.local/include/curl/`, `~/.local/lib/libcurl.so`
  symlink, `C_INCLUDE_PATH` and `LIBRARY_PATH` exports in
  `~/.config/truffle/env.sh`) carries over unchanged.
- main ends with an explicit `return` to dodge the trailing-write
  byte-count-as-exit-code codegen quirk surfaced in task 012.

## Cross-implementation parity

All five references issue exactly one POST with body
`{"a":<a>,"b":<b>}`, observe one HTTP transaction (no redirects),
and surface either the integer `sum` field of the response object
or the literal `error\n` for any failure. Byte-exact agreement on
every case.
