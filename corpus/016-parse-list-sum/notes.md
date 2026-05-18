# Notes — 016-parse-list-sum

## Algorithm

Read a count `N` (u32, capped at 1000) from line 1. Then read `N`
more lines, each a u32. Sum them and write the sum as decimal + `\n`.
Three failure-mode classes collapse to `error\n`:

1. Line 1 fails to parse, exceeds 1000, or is missing.
2. Fewer than `N` value lines are available.
3. Any value line fails to parse, OR the running sum overflows u32.

The running sum is accumulated in u64 so the overflow check is a
single `> 4294967295_u64` comparison after each addition.

## Loop-with-mid-iteration-failure shape

This is the structural distinction from task 015. Where 015 had
three independent flat failure modes that short-circuit at gate
checks before the work, 016 has a counted loop where ANY iteration
can fail and must terminate the loop cleanly with an error signal.
Each language threads this differently:

- Python / TypeScript: early `return` from `main` inside the loop.
- Rust: `?` on `Option<u32>` inside a helper `run` that returns
  `Option<u64>`; `main` matches once at the end.
- Go: explicit `(uint64, bool)` return from a helper; loop checks
  `!ok` and short-circuits.
- Zero: `loop_ok: Bool` flag plus `idx = n_val` to break the outer
  loop (no `break` in 0.1.2). The post-loop branch reads the flag.

The Zero pattern is the same flag-then-set-counter-to-end trick used
in tasks 008, 011 for inner scans — the loop-with-mid-iteration
shape isn't new but this is the first task where it gates the whole
output decision rather than just an inner-loop short-circuit.

## Cross-implementation parity

All five share the same dispatch:

1. parse N
2. validate N <= 1000
3. validate enough lines/argv remain
4. loop N times: parse value, check value <= u32::MAX, add to u64
   running sum, check sum <= u32::MAX
5. emit sum + `\n`

Byte-exact agreement on every case.

## Zero-specific notes

- argv[1] is N; argv[2..N+1] are the values. `std.args.len()`
  includes the program name at index 0, so `argc >= N + 2` checks
  that enough argv slots exist.
- The parse helper is inlined twice (once for N, once per value
  iteration) per the seventh quirk forbidding Span<u8>-taking user
  functions on direct ELF64. The two parse blocks are byte-identical
  apart from the local-variable prefix (`n_*` vs `v_*`).
- `std.parse.parseU32` is still unusable for runtime data per the
  eighth quirk (CGEN004 on direct ELF64 for non-literal input).
- main ends with an explicit `return` to dodge the trailing-write
  byte-count-as-exit-code codegen quirk.
- Sum is rendered from u64 (after the u32::MAX bounds check), not
  u32, because the rendering loop reuses the same u64 path that was
  used in the accumulator. The final value is always <= u32::MAX.

No new codegen quirks surfaced during 016 — the eighth quirk from
015 was already in scope, and the rest of the program follows
patterns established in 013-015.
