# Notes — 015-checked-divide-u32

## Algorithm

Read two unsigned decimal integers (each in u32 range). Parse both,
reject leading sign and non-digit bodies. If either parse fails or
the second value is 0, write `error\n`. Otherwise write the integer
floor quotient as decimal followed by `\n`. Process exit is 0 in
every case.

## Failure modes

Three independent paths collapse to the same `error\n`:

1. argv/stdin shape missing (under two lines or two argv values).
2. Either integer fails to parse (empty body, non-digit byte, leading
   `+`/`-`, or value exceeds u32::MAX = 4294967295).
3. Divisor parses to 0.

Leading zeros are accepted (`007` parses to 7). Trailing whitespace
on the stdin lines is tolerated and trimmed before parsing; for the
Zero argv path the values are taken exactly as the OS passes them
(no embedded whitespace).

## Cross-implementation parity

- Python: hand-rolled `parse_u32` that trims, validates ASCII digits,
  delegates to `int()`, bounds-checks against `U32_MAX`.
- TypeScript: same shape using `BigInt` and a charCode digit check.
- Rust: `parse_u32` that trims, byte-validates `b'0'..=b'9'`, calls
  `str::parse::<u32>` (the bounds check is built into the parse).
- Go: `parseU32` that trims, byte-validates, calls
  `strconv.ParseUint(t, 10, 32)`. The `bitSize=32` arg enforces the
  u32 cap.
- Zero: inline u64 accumulator with an upper-bound check against
  `4294967295_u64` (see "Zero-specific notes" below).

All five share the same dispatch: parse a, parse b, divide-by-zero
check, render decimal. Byte-exact agreement on every case.

## Zero-specific notes

- argv[1..2] carry a and b (no exposed stdin in Zero 0.1.2).
- `std.args.get(i)` returns `Maybe<String>`. The `.value` is a
  String, which `std.mem.span(.)` converts to a `Span<u8>` for the
  manual digit scan.
- The natural API for this task would be
  `std.parse.parseU32(maybe_a.value)` — `parseU32` takes a `String`
  and returns `Maybe<u32>` with built-in overflow rejection. **But
  the direct ELF64 backend rejects runtime-String inputs to
  `std.parse.*` with `CGEN004`:**
  ```
  CGEN004: direct backend std.parse helpers currently require literal text
  ```
  So the parse is implemented inline: u64 accumulator (i.e.
  `0_u64..=18446744073709551615_u64`), digit-by-digit ASCII check,
  followed by `if a_acc > 4294967295_u64 { error }`.
- The direct backend ELF64 MVP forbids user functions taking
  `Span<u8>` / `MutSpan<u8>` / shape values (seventh quirk surfaced
  in task 013), so the parse loop and the output rendering loop are
  both inline in `main`.
- main ends with an explicit `return` to dodge the trailing-write
  byte-count-as-exit-code codegen quirk surfaced in task 012.

## Eighth direct-backend codegen quirk (CGEN004)

`std.parse.parseU8`, `parseU16`, `parseU32` accept any `String` per
their type signatures, but on the direct ELF64 backend they only
codegen for **compile-time string literals**. Passing a runtime
String (e.g. `std.args.get(1).value`) raises `CGEN004` with the
message "direct backend std.parse helpers currently require literal
text". This means the natural use case of "parse a numeric argv
value" is impossible via the standard library helper on native
targets; programs must either target WASM (untested by this task)
or implement parsing manually.

This is the eighth quirk in the running list against the direct
ELF64 backend that the AgentLang Index has surfaced so far:

1. (task 012) trailing-write byte-count returned as exit code unless
   `main` ends with explicit `return`.
2. (task 013) `responseBodyOffset` returns the offset within the
   shared response buffer, not into the body slice itself.
3. (task 013) `std.http.fetch` accepts `[N]u8` arrays directly as
   the request envelope rather than requiring `std.mem.span(.)`.
4. (task 014) `headerValue/headerFound/headerOffset/headerLen` is
   the only documented way to scan a response header; no
   higher-level helper.
5. (task 013) user functions taking `Span<u8>` / `MutSpan<u8>` /
   shape locals are forbidden on direct ELF64 — entire body of
   `main` must be one inline pass.
6. (task 013) JSON literals must be assembled byte-by-byte; no
   `std.json.write(.)` equivalent for emitting JSON.
7. (task 013) member access on shape values only supported for
   `Maybe<MutSpan<u8>>.has` and `.value` on direct ELF64.
8. (task 015 — THIS TASK) `std.parse.parseU*` rejects runtime
   `String` inputs with `CGEN004`. Only compile-time string literals
   compile through the direct backend.

These will go into a single upstream issue once the AgentLang Index
v0.1 ships.
