# Notes — 010-byte-frequency

## Algorithm

Two phases:

1. **Count.** Walk every input byte, incrementing `counts[byte]` in a
   length-256 table. `counts` is `u32` everywhere; the spec caps input
   at 100000 bytes, so the max single-byte count is 100000 (well
   inside u32 range).
2. **Emit.** Walk byte values 0..255 in ascending order; for every
   entry with a non-zero count, emit `<byte_decimal> <count>\n`.

The byte value itself is rendered in decimal (range 0..255 → 1..3
digits), so a 4-byte temp buffer is sufficient. The count renderer
uses a 16-byte temp buffer (max u32 = 4294967295 = 10 digits).

## Edge cases

- Empty input → no bytes counted → emit nothing.
- Single byte → one line.
- All identical bytes → one line.
- High-bit bytes (0x80..0xFF, decimal 128..255) appear with their
  decimal values; no special handling.

## Zero-specific notes

- argv[1] is the input bytes; an absent argv falls back to an empty
  span. Embedded tabs, newlines, and high-bit bytes in argv[1] pass
  through unchanged.
- Decimal rendering is inlined twice (once for the byte value with a
  4-byte temp, once for the count with a 16-byte temp) because Zero
  0.1.2 does not support `Span<u8>`/`MutSpan<u8>` as function
  parameters; the function-extraction shape is unavailable, so the
  buffer-write code lives inline.
- Output buffer sized at `[4096]u8`: the worst case is all 256 byte
  values present, each line `"<3 digits> <10 digits>\n"` = 15 bytes,
  total 3840 bytes. The spec's 100000-byte input cap caps the max
  count at 6 digits (100000), so realistic worst case is 11 bytes per
  line × 256 = 2816, well under 4096.
- Uses the small-divisor u32 divmod renderer (`% 10_u32` /
  `/ 10_u32`) which dodges the 2^32-divisor narrowing-cast SIGFPE.

## Cross-implementation parity

All five references walk the input byte-by-byte and emit one record
per non-zero byte value in ascending byte order. TypeScript uses
`Uint32Array(256)` for the counts table; Rust uses `[0u32; 256]`; Go
uses `[256]uint32`; Python uses a 256-element list. The output format
is the same across all of them: `<byte_decimal> <count>\n` per
record, no header, no trailing extra newline.
