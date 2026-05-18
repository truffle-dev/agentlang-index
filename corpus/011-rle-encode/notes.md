# Notes — 011-rle-encode

## Algorithm

Single forward walk with one open run at a time:

1. Open the first run at byte 0; `cur_byte = bytes[0]`, `cur_count = 1`.
2. For each subsequent byte: if it equals `cur_byte`, increment
   `cur_count`; otherwise emit the open run, then start a new one
   anchored on this byte.
3. After the loop, emit the last open run.

The four reference implementations in TS/Rust/Go/Python all use the
emit-on-change-plus-final-flush shape directly. The Zero ref uses a
slightly different shape — an outer loop that picks up one run per
iteration via an inner-flag scan — because the emit-on-change shape
needs the "scan past the matching run" step to live somewhere, and
the explicit-flag inner-scan pattern from task 008 reuses cleanly
here.

## Edge cases

- Empty input → emit nothing.
- Single byte → one line with `count=1`.
- Two-byte input with identical bytes → one line with `count=2`.
- Two-byte input with different bytes → two lines, each `count=1`.
- Recurring byte after a gap (`aabbaa`) forms a new run — the third
  run is still `2 97\n` even though byte 97 already appeared.

## Zero-specific notes

- argv[1] is the input bytes; an absent argv falls back to an empty
  span.
- Inner-loop scan uses the explicit-flag pattern (no `&&` short-circuit
  available in Zero 0.1.2 direct backend).
- Decimal renderer is inlined twice per emit site (once for the
  count, once for the byte value) because Zero 0.1.2 does not support
  `Span<u8>`/`MutSpan<u8>` as function parameters; the function
  extraction shape is unavailable. The count renderer assumes
  positive (`cur_count >= 1`), so it omits the `v == 0` branch; the
  byte renderer keeps the `v == 0` branch because byte value 0 is
  valid input.
- Output buffer at `[8192]u8`: worst case is the 1000-byte input cap
  with every byte different, producing 1000 lines of `"1 NNN\n"` =
  7 bytes max each, total 7000 bytes. Comfortably under 8192.

## Cross-implementation parity

All five references walk the input byte-by-byte and emit one record
per maximal run in input order. Byte-exact agreement on every case.
