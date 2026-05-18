# Notes — 017-checked-add-overflow

## Algorithm

Read two unsigned decimal integers (each in u32 range). Parse both,
reject leading sign and non-digit bodies. If either parse fails or
`a + b` would exceed `u32::MAX = 4294967295`, write `error\n`.
Otherwise write the sum as decimal followed by `\n`. Process exit is
0 in every case.

## Failure modes

Three independent paths collapse to the same `error\n`:

1. argv/stdin shape missing (under two lines or two argv values).
2. Either integer fails to parse (empty body, non-digit byte, leading
   `+`/`-`, or value exceeds u32::MAX = 4294967295).
3. The sum `a + b` would exceed u32::MAX (u32 add wrap).

Leading zeros are accepted (`007` parses to 7). Trailing whitespace
on the stdin lines is tolerated and trimmed before parsing; for the
Zero argv path the values are taken exactly as the OS passes them
(no embedded whitespace).

## Overflow-check shape per language

- Python / TypeScript: arithmetic is unbounded (BigInt in TS, native
  int in Python). Sum then compare `> U32_MAX`. No wraparound trap.
- Rust: `u32::checked_add` returns `Option<u32>` — `None` on
  overflow. The match arm pattern threads it cleanly with the parse
  failures (`Some(av).checked_add(bv)` then match).
- Go: cast both addends to `uint64`, sum, compare against
  `math.MaxUint32`. (Could also use `bits.Add32` to read the carry
  bit; the u64 widen is simpler and equivalent.)
- Zero: accumulate both parsed values in `u64` directly, sum in u64,
  compare `> 4294967295_u64`. Identical pattern to the per-value
  bounds check on the parse path — u64 is already the working type.

## Arc closure (third structural distinct shape)

This task closes the error-handling arc at 3/3:

- 015 (`checked-divide-u32`): three flat failure paths that
  short-circuit at gate checks BEFORE the work (missing argv, parse
  failure, divisor zero). The work is a single divide; no
  arithmetic-side failure surface.
- 016 (`parse-list-sum`): a counted loop where ANY iteration can
  fail (parse failure OR running-sum overflow). Failure is mid-work
  and must terminate the loop cleanly.
- 017 (`checked-add-overflow`): the work itself is the failure
  surface. Both inputs parse cleanly yet the operation can still
  fail — overflow is detected by computing in a wider type and
  bounds-checking, OR by using a checked-arithmetic primitive that
  signals overflow as a sum-time return value.

Across the three: pre-work gate, in-loop failure with state,
post-parse arithmetic failure. The error-output collapse is uniform
(`error\n` + exit 0), but the where-it-fails dimension is structurally
distinct each time.

## Cross-implementation parity

All five share the same dispatch:

1. parse a (u32)
2. parse b (u32)
3. check `a + b <= u32::MAX`
4. emit sum + `\n`

Byte-exact agreement on every case.

## Zero-specific notes

- argv[1..2] carry a and b (no exposed stdin in Zero 0.1.2).
- `std.args.get(i)` returns `Maybe<String>`. The `.value` is a
  String, which `std.mem.span(.)` converts to a `Span<u8>` for the
  manual digit scan.
- `std.parse.parseU32` is still unusable for runtime data per the
  eighth quirk surfaced on task 015 (CGEN004 on direct ELF64 for
  non-literal input).
- Parse helpers are inlined twice (once for a, once for b) per the
  seventh quirk forbidding `Span<u8>`-taking user functions on
  direct ELF64. The two parse blocks are byte-identical apart from
  the local-variable prefix.
- main ends with an explicit `return` to dodge the trailing-write
  byte-count-as-exit-code codegen quirk surfaced on task 012.
- The overflow check is `if sum > 4294967295_u64 { error }` where
  `sum` is `a_acc + b_acc` both already validated <= 4294967295_u64.
  Worst-case sum is 2 * (2^32 - 1) = 2^33 - 2, comfortably within
  u64 range (no second-order wrap).
- The render loop uses a small-divisor (10) decimal split, dodging
  the 2^32-divisor SIGFPE quirk noted for direct ELF64 in the
  AgentLang Index notes.

No new codegen quirks surfaced during 017 — the eight quirks from
tasks 012-015 were already in scope, and this task follows the
patterns established in 015/016.
