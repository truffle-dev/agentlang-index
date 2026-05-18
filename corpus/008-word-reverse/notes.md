# Notes — 008-word-reverse

## Algorithm

Two-pass over the input bytes:

1. **Scan.** Walk left to right. Skip runs of spaces, then record each
   non-space run as a `(start, length)` pair. After this pass, `nw` is
   the word count.
2. **Emit.** If `nw == 0`, write nothing and exit. Otherwise walk from
   `nw - 1` down to 0, copying each word's bytes to the output buffer
   and inserting a single space between adjacent words. Append a single
   `\n`.

## Edge cases

- Empty input (`n == 0`) → no words → no output.
- All spaces (e.g. `"   "`) → no words → no output.
- Single word (`"single"`) → one word → output is the word plus `\n`.
- Multiple internal/leading/trailing spaces (`"  multi   spaces  "`) →
  two words → output is `spaces multi\n`.

The "no output for zero words" rule is the trap. Models often emit a
bare `\n` for empty input, which fails the byte-exact check.

## Zero-specific notes

- argv[1] is the line; an absent argv falls back to an empty span.
- **`&&` is NOT short-circuit in the Zero 0.1.2 direct backend.** The
  natural shape `while i < n && bytes[i] == 32_u8` traps with SIGILL
  (exit 132) because the index expression is evaluated even when the
  guard is false. The fix is to split the loop into a `while flag {
  if i >= n { flag = false } else { ... } }` shape so the index is
  only evaluated under an explicit guard.
- Word position arrays `[500]u32 starts` and `[500]u32 lens` (500 is
  the upper bound on words for a 1000-char input of alternating
  single-char + space).
- Output buffer `[1024]u8`. Worst case: same total length as input plus
  one trailing newline; the per-word write loop never overflows because
  the words' total byte count is `<= n`.

## Cross-implementation parity

All five references produce byte-exact output on every case in both
stdin (TS/Rust/Go/Python) and argv (Zero) input modes.
