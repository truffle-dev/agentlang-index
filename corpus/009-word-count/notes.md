# Notes — 009-word-count

## Algorithm

One-pass state machine over the input bytes:

- `in_word` starts `false`, `count` starts `0`.
- For each byte `b`: if `b` is whitespace, set `in_word = false`;
  otherwise if `in_word` is false, increment `count` and set
  `in_word = true`.
- Whitespace bytes: space (0x20), tab (0x09), newline (0x0A), CR (0x0D).
- After the loop, emit `count` as decimal followed by one newline.

## Edge cases

- Empty input → `count` stays 0 → output `0\n`.
- All-whitespace input → no non-whitespace bytes → output `0\n`.
- Trailing whitespace (including a trailing newline from stdin) does
  not create a phantom word; the state machine simply stays at
  `in_word = false` past the end.
- Single word with no trailing newline → output `1\n`.
- Tab, newline, and CR all act as separators identically to space.

## Zero-specific notes

- argv[1] is the input bytes; an absent argv falls back to an empty
  span. Embedded tabs and newlines inside argv[1] (passed as
  `$'a\tb\nc'` from bash) are preserved literally.
- The whitespace classification is written as four independent `if`
  branches that each set `is_ws = true`. This avoids assuming `||`
  short-circuits in the Zero 0.1.2 direct backend; even though none of
  the byte comparisons here would trap, the explicit-flag pattern
  matches the safety shape used elsewhere in the corpus.
- **Zero 0.1.2 does not have a `!` prefix operator for booleans.** The
  natural shape `if !in_word { ... }` trips PAR100 at the `!`. Use the
  explicit comparison `if in_word == false { ... }` instead. This is
  the fourth Zero direct-backend quirk surfaced by the corpus; it
  joins the 2^32-divisor SIGFPE (task 002), the i32-vs-usize and
  bool-vs-Bool TYP002 quirks (task 004), and the `&&` non-short-circuit
  trap (task 008) as silent-under-`zero check` codegen gaps.
- The decimal renderer uses small-divisor u32 divmod (`% 10_u32` /
  `/ 10_u32`). This dodges the 2^32-divisor narrowing-cast SIGFPE
  documented in task 002 notes; 10 fits in u32 so the cast pattern
  is never triggered.

## Cross-implementation parity

All five references treat the four whitespace bytes identically and
walk the input byte-by-byte (no Unicode-aware tokenization). TypeScript
and Python read raw byte buffers (`readFileSync(0)` and
`sys.stdin.buffer`); Rust uses `read_to_end` for the same reason. Go
uses `io.ReadAll` and ranges over the byte slice with `_, b := range`
which yields bytes from a `[]byte`. Byte-exact agreement holds on
every case.
