# Notes — 006-substring-count

## Algorithm

Greedy left-to-right scan. For each position `i` in `0..=n-m`, test
`T[i..i+m] == P`. On match, `count++` and `i += m`. On miss, `i += 1`.
Empty `T` or `m > n` short-circuits to 0.

## Why greedy non-overlap (not overlapping count)

The two reasonable count semantics are:

1. **Greedy non-overlapping** (what we use): `aa` in `aaaa` = 2.
2. **Overlapping**: `aa` in `aaaa` = 3.

We chose the greedy non-overlapping shape because (a) it is the more common
default across `str.count` implementations (Python `"aaaa".count("aa")` = 2,
Rust `str::matches` does non-overlapping when used naively), and (b) it is
the deterministic shape that a model can derive without ambiguity from the
spec wording "once a match starts at index i, the next candidate match
starts at i + len(P)."

Models that conflate the two semantics will fail case 2 (the canonical
trap) and case 1 (which would yield 5, not 4, under the overlapping rule
applied to `ab` over `abababab`).

## Zero-specific notes

- argv[1] = P, argv[2] = T. Both defaulted to empty `Span<u8>` when the
  caller omits them (we branch on `.has`).
- Inner equality check is a manual byte-loop (no `==` on `Span<u8>` in
  Zero 0.1.2 direct backend). Early-exit on mismatch by setting the loop
  index to `m` (Zero has no `break`).
- The count fits in `u32` (max is `n/m` and `n <= 1000`). The decimal
  renderer reuses the small-divisor pattern from tasks 001-004.

## Cross-implementation parity

All five references produce byte-exact decimal-count followed by `\n` on
every case in both stdin (TS/Rust/Go/Python) and argv (Zero) input modes.
