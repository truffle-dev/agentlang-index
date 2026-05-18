# Notes — 004-matrix-multiply

## Why this task

Fourth and last pure-computation task. Differs from 001-003 in two
shape changes:

1. **Multi-value input.** Tasks 001 and 002 took one integer; task 003
   took two strings. This one takes one integer and 2*N*N more
   integers. The model must read a variable amount of input,
   tokenize it, and dispatch into the right matrix slot. Off-by-ones
   in the read loop translate directly into wrong outputs.
2. **Multi-line, multi-column output.** Tasks 001-003 all emitted a
   single decimal followed by `\n`. This one emits an N x N table.
   The model must space-separate within a row, newline-terminate per
   row, and not append a trailing line. A model that pretty-prints
   with extra whitespace produces a byte-exact failure even with the
   right math.

Difficulty: easy as math, but the I/O matrix is broader than 001-003.
The triple-nested loop is canonical algorithm material.

## Input convention

Zero takes the flat sequence on argv: `argv[1]` = N, `argv[2..2+N*N-1]`
= A row-major, `argv[2+N*N..2+2*N*N-1]` = B row-major. With the spec
cap of N <= 5 the worst-case argv length is 1 + 50 + 1 (program name)
= 52 tokens, well inside the shell limit. The other four languages
read the user-friendly multi-line stdin schema.

## Edge cases probed

- `N = 1` (the trivial scalar case `[a] * [b] = [a*b]`).
- Identity-times-arbitrary (catches models that swap row/column
  indices in the inner loop, because the output then ceases to be B).
- Mixed positive and negative entries (catches models that try to use
  unsigned ints or skip the sign in the decimal renderer).
- `N = 5` at the spec cap (the largest matrix in the matrix exercises
  the full DP-flat indexing pattern; if the model used the wrong row
  stride it falls over here).

## Zero implementation notes

Two flat `[25]i32` buffers (5*5 = 25 = spec cap; using flat instead of
`[5][5]` keeps it inside the direct backend's single-element array
support). Element type i32 because entries are in [-99, 99] and
worst-case inner-product sum is `5 * 99 * 99 = 49005`, well inside
i32 range.

The integer parser handles a leading `-` and emits an i32. The
decimal renderer handles negative i32 by computing `(0 - s) as u32`
under guard `s < 0` and emitting a `-` byte before the digits. The
divisor in the renderer is 10 (u32), so it stays clear of the
2^32-divisor codegen SIGFPE.

The output buffer is `[512]u8`. For the worst case (N=5, every cell
6 chars including a leading `-`), the row length is `5 * 7 - 1 + 1`
(space-separated + newline) = 35 bytes; total = 175 bytes; 512 is a
comfortable cap.

## Future revisions

- Bigger N. The spec caps at 5 to make argv ergonomic and to keep
  the test fixtures readable. Lifting to N=20 (so 800 argv tokens
  for the two matrices) would still fit, but the test JSON files
  would balloon. Defer to v0.2 when the spec gains an alternative
  input convention.
- Floating point. A future variant could swap i32 for f64 and check
  that the model preserves precision in the sum. Catch: f64 printing
  conventions diverge across languages (Python's `repr` vs Rust's
  Display), so the spec would need a strict format string.
- Non-square. The current spec uses NxN matrices to halve the
  required input length. A non-square (MxK * KxN) variant would test
  whether the model truly understands the contraction dimension
  versus just copying a "do three nested loops" recipe.
