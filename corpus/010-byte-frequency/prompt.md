# Task 010 — byte-frequency

## Problem

Read all bytes from standard input. Count how often each byte value
(0 through 255) appears. For every byte value with a non-zero count,
write one line of the form `<byte_decimal> <count>\n` to standard
output. The lines must be in ascending byte-value order. Exit with
status 0.

## Output format

- Each line is `<byte_decimal>` (the byte value 0..255 rendered in
  decimal, no padding), one ASCII space (0x20), `<count>` (the
  occurrence count in decimal, no padding), one newline (0x0A).
- No header, no trailing extra newline beyond the per-record one.

## Edge cases

- Empty input → empty output (no header, no `0\n`, nothing).
- Single byte input → one line.
- Repeated identical bytes → one line with the matching count.
- High-bit bytes (0x80..0xFF) appear with their decimal value
  (128..255) just like ASCII bytes.

## Acceptance

The stdout produced by your program must match the expected bytes
exactly for every test case. Stderr must be empty and the process
must exit 0.

## Input convention

- **stdin** (TypeScript, Rust, Go, Python): read all bytes until EOF.
- **argv[1]** (Zero 0.1.2 has no exposed stdin capability): read the
  bytes from the first command-line argument.

## Token budget

1600 tokens.
