# Notes — 003-levenshtein-distance

## Why this task

Third pure-computation task. The first two corpus tasks exercised
single-integer arithmetic (recursion + memoization for 001, array
marking for 002). This one is the first that takes **two inputs**
and produces a number that depends on a two-dimensional dynamic
programming relation. The model must (a) read two strings, not one
integer, (b) materialize the standard Levenshtein recurrence (insert,
delete, substitute, each cost 1, take the minimum), (c) keep the
table small enough to run cheaply on the 50-char cap, (d) emit a
single decimal followed by `\n`.

Difficulty: easy. The recurrence is canonical algorithm material but
catches models that get the row/column indexing wrong, that forget
to seed the first row and first column with the lengths, or that
forget the equal-character zero-cost short circuit.

## Input shape changes

Tasks 001 and 002 read a single integer N from stdin (or argv[1] for
Zero). This task reads **two strings**, one per line. For Zero that
means `argv[1]` is A and `argv[2]` is B, mirroring the per-line
convention of the other four languages.

The 50-character cap on each string keeps the DP table inside Zero's
stack-allocated `[51]u32` rolling buffers (the prior tasks used `[N]u8`
because the spec's data fit in bytes; here we need u32 because the
distance for a 50/50 string pair could theoretically reach 50 and a
u8 would still cover that, but I'd rather keep the cell type the same
as the conventional textbook value).

## Edge cases probed

- Both strings empty: distance 0. Catches off-by-one initialization.
- One empty, one non-empty: distance equals the length of the other.
  Catches models that skip the boundary seeding entirely.
- Equal strings (not tested in the matrix here but covered transitively
  by case-002 with empty/empty == "abc"/"abc" == 0 logic).
- Classic `kitten` -> `sitting` (distance 3) and `saturday` -> `sunday`
  (distance 3) cover the substitution + insertion + deletion mix that
  shows up in every algorithms textbook.
- `intention` -> `execution` (distance 5) tests a deeper DP path with
  no obvious shared prefix to short-circuit.
- The long pair `the quick brown fox jumps over the lazy dog` vs
  `the quick brown dog jumps over the lazy fox` is interesting because
  the naive intuition is "6 substitutions, 3 per word" but the right
  answer is **4**: `o` is shared between `fox` and `dog` at the middle
  position, so only `f<->d` and `x<->g` substitute. Easy hand-error.

## Zero implementation notes

Same input convention as 001 and 002: argv-based because Zero 0.1.2
has no exposed stdin capability. All logic stays inside `pub fun main`.

The DP uses two rolling `[51]u32` buffers (current row and previous
row) rather than a full `[51][51]u32` table. Two reasons:
1. The direct backend's array-element-type matrix doesn't include
   nested arrays as cleanly as a single flat allocation.
2. Two rolling buffers are the textbook memory optimization and cut
   the stack footprint from ~10KB to ~408 bytes.

The decimal renderer reuses the pattern from 001/002 (digits buffer,
walk the value, reverse into the output buffer) with `distance: u32`
as the source value. Same small-divisor (10) divmod, so it stays
clear of the 2^32-divisor SIGFPE documented in
`~/repos/zero-bugs/u64-divmod-cast-sigfpe/`.

## Future revisions

- Higher per-string cap. The current `[51]u32` allocation tracks the
  spec's 50-char limit. A 256-char cap would push the rolling buffer
  to about 2KB still, well inside the stack budget.
- Unicode. Today's spec is ASCII-only to keep the byte indexing
  trivial. A future revision could ask for Unicode-codepoint-level
  edit distance, which would surface whether the model knows the
  difference between `len(bytes)` and `len(codepoints)`.
- Damerau-Levenshtein (add a transposition rule). Same recurrence
  with one extra case for adjacent swap. Defer to v0.2 if a model
  consistently confuses the two variants.
