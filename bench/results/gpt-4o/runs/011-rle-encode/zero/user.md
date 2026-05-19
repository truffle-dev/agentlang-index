## Spec

# Task 011 — rle-encode

## Problem

Read all bytes from standard input. Walk left to right; for every
maximal run of identical consecutive bytes, write one line of the
form `<count> <byte_decimal>\n` to standard output where `<count>`
is the run length in decimal and `<byte_decimal>` is the byte value
(0..255) in decimal. The lines must appear in input order. Exit with
status 0.

## Output format

- Each line is `<count>` (decimal, no padding), one ASCII space
  (0x20), `<byte_decimal>` (0..255, no padding), one newline (0x0A).
- No header. No trailing extra newline beyond the per-record one.

## Edge cases

- Empty input → empty output.
- Single byte → one line, count 1.
- All identical bytes → one line with the full count.
- Each maximal run is emitted exactly once; a byte that recurs after
  a gap forms a new run with its own line.

## Examples

- Input `aaa` → `3 97\n`
- Input `abc` → `1 97\n1 98\n1 99\n`
- Input `aaabbc` → `3 97\n2 98\n1 99\n`
- Input `aabbaa` → `2 97\n2 98\n2 97\n` (the second `aa` is a
  separate run because there is a different byte between them).

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


## Single-file Zero layout

Write a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>
