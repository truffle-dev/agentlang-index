# 001-fibonacci-memoized — notes

First non-trivial corpus task. Probes whether a model picks a memoized
strategy when the spec mandates it (the 5-second budget kills naive
double-recursion at N=50). Every reference is explicitly memoized.

## Memo representations across the references

- TS: `Map<number, bigint>`, recursive
- Rust: `HashMap<u32, u64>`, recursive
- Go: `map[int]uint64`, recursive
- Python: `dict[int, int]`, recursive (Python ints are bignum)
- Zero: two parallel `[64]u32` arrays (memo_hi / memo_lo) treated as a
  u64 memo, iterative bottom-up

All five fit comfortably within the 5-second wall budget at N=50.

## Zero 0.1.2 direct-backend adaptations

The Zero reference takes notable liberties from the cross-language norm,
all forced by what the direct ELF64 MVP backend (`zero-c`) supports today:

1. **N comes from `argv[1]`, not stdin.** The 0.1.2 `World` capability
   exposes `World.out` and `World.err` but no `World.in`, so stdin is
   unreachable from a hosted-world program. Every other language reads
   stdin. `verify.sh` routes input accordingly.

2. **u64 memo is two `[N]u32` arrays.** The direct backend restricts
   fixed-array local element types to `i32`, `u32`, and `u8`, so a
   `[N]u64` is rejected. The references store the high and low 32 bits
   of each fib(i) in parallel arrays and reconstruct u64 values for the
   recurrence.

3. **All logic stays inside `pub fun main`.** The direct backend rejects
   `Span<u8>` and `MutSpan<u8>` as function parameter types in the
   single-file `zero run` path, so the digit parser and decimal renderer
   could not be factored out as helper functions.

4. **`std.parse.parseU32` not used.** It is gated behind a literal-text
   requirement on the direct backend; the Zero reference walks the
   digits manually.

5. **u64 division + cast is split across statements.** The expression
   `(sum / 4294967296_u64) as u32` triggers a compiler crash on this
   backend revision. Binding intermediate variables for the divmod
   results before casting works around it. Worth filing upstream once
   the corpus stabilises and we have a minimal repro.

## Public vs hidden test split

- Public (`tests/public/case-00{1..4}.json`): N=0, 1, 10, 50. Mirrors
  the four examples in `prompt.md` so a model can self-check.
- Hidden (`tests/hidden/case-001.json`): N=15 → 610. Not in the prompt;
  used by the harness to confirm the solution generalises and isn't
  table-lookup hardcoded.

Each case carries both `stdin` and `argv` because the harness needs to
adapt per language (Zero uses `argv`, others use `stdin`).
