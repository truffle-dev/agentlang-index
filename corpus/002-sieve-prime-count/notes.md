# Notes — 002-sieve-prime-count

## Why this task

Second pure-computation task. Differs from 001-fibonacci-memoized in
shape: there is no recursion to memoize and no per-call subproblem to
cache; instead the solution exercises **array marking** and a nested
loop with the inner bound depending on the outer index. The model
must (a) allocate a flag buffer of size N+1, (b) iterate the right
range for the outer pointer, (c) stop the inner mark loop at the
right cap, (d) iterate again to count, all without off-by-ones.

Difficulty: easy. The sieve is canonical algorithm material, but it
catches models that confuse the count's upper bound (`<= N` vs `< N`)
or that overflow the inner-loop start (`i * i` rather than `2 * i` is
the optimization the spec rewards).

The acceptance criteria reduce to a byte-exact stdout match per test
case, same as 001. No subjective scoring.

## Edge cases probed

- `N = 0` and `N = 1` both yield `0`. A model that emits `0\n` or
  `\n` only on `N < 2` rather than always must still handle both.
- `N = 2` yields `1`. Catches models that initialize `i = 3` thinking
  they can hand-fold the only-even-prime case.
- `N = 10000` yields `1229`. A `is_prime(k)` trial-division fallback
  would still pass on this corpus (`O(N * sqrt(N))` = `O(10^6)` for
  the largest case), so the spec asks for a sieve specifically and
  `acceptance.requires_sieve` lifts that into a metadata flag that
  the harness will check against (we'll add a structural check on
  the model's output later — for v0.1 we trust the prompt).

## Zero implementation notes

Same input convention as 001: N is read from `argv[1]` because Zero
0.1.2 has no exposed stdin capability. All logic stays inside
`pub fun main`. The flag buffer is `[10001]u8` — a stack-allocated
fixed-size array of `u8`, which is one of the direct backend's
allowed element types. The size cap of 10001 doubles as the spec
upper bound (`N <= 10000`), so the program returns an error for
`N > 10000` rather than risking an out-of-bounds write.

The decimal renderer reuses the pattern from 001 (digits buffer,
walk the value, reverse into the output buffer) but with `count: u32`
as the source value, so the divmod stays on small u32 divisors and
does not trip the 2^32-divisor SIGFPE documented in
`~/repos/zero-bugs/u64-divmod-cast-sigfpe/`.

## Future revisions

- Property test: a structural check that the model's output uses a
  sieve, not trial division — possible candidates are time-budget
  shrinking (set `wall_time_max_ms` such that trial division would
  blow it on large `N`) or AST inspection of the generated code.
  Defer to v0.2.
- Higher `N`. The sieve allocation is `O(N)`; today's `[10001]u8`
  cap is easy to lift to `[100001]u8` once we confirm the direct
  backend handles ~100KB stack-local arrays without surprises.
