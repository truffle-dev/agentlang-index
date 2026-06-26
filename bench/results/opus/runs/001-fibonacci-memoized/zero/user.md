## Spec

## Task: Fibonacci with memoization

Read a single non-negative integer `N` from standard input. Compute
`fib(N)` using **memoization** (cache previously computed values so
repeated subproblems are O(1)). Write `fib(N)` followed by a single
newline to standard output. Exit with status 0.

Definition:

- `fib(0) = 0`
- `fib(1) = 1`
- `fib(n) = fib(n-1) + fib(n-2)` for `n >= 2`

## Acceptance

- Stdin: one line containing the integer `N`.
- Stdout: the decimal digits of `fib(N)` followed by `\n`.
- Stderr: empty.
- Exit code: 0.
- The program must complete `fib(50)` within 5 seconds. (A non-memoized
  recursive solution will not meet this budget.)

## Examples

| N  | stdout            |
| -- | ----------------- |
| 0  | `0\n`             |
| 1  | `1\n`             |
| 10 | `55\n`            |
| 50 | `12586269025\n`   |

## Single-file Zero layout

Write a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>
