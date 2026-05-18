# 000-hello-stdout — notes

Smoke-test task. Probes the multi-language toolchain plumbing, not model
capability. All five reference implementations must pass on day one or
the harness cannot be trusted.

## Why this exists

If a frontier model fails this task, something is wrong with the prompt
template, the sandbox, or the scoring grader. Use it as a canary on
every harness change.

## Calibration

- Zero: `bin/zero run ref.zero` from a Zero checkout. Output is exactly
  `hello\n`.
- TS: `node` or `tsx` against `ref.ts`. Pure stdio API, no async surprises.
- Rust: `rustc ref.rs -o hello && ./hello`. No `println!` because the
  spec is exact-byte; `print!` is the right call.
- Go: `go run ref.go`. `fmt.Print` (not `fmt.Println`) because the trailing
  newline is part of the byte sequence we're matching exactly.
- Python: `sys.stdout.write` instead of `print()` to avoid Python's
  print-end behavior; the spec wants exactly seven bytes.
