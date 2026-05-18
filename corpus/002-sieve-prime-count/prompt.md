## Task: Prime count via Sieve of Eratosthenes

Read a single non-negative integer `N` from standard input (`0 <= N <= 10000`).
Compute the count of prime numbers in the closed interval `[2, N]` using a
**Sieve of Eratosthenes** (a brute-force `is_prime(k)` per candidate is
considered out of band; the task is about the sieve algorithm). Write the
count to standard output followed by a single newline. Exit with status 0.

Edge cases:

- `N = 0` and `N = 1` both yield `0` (no primes in the interval).
- `N = 2` yields `1` (just `2`).

## Acceptance

- Stdin: one line containing the integer `N`.
- Stdout: the decimal digits of the count, followed by `\n`.
- Stderr: empty.
- Exit code: 0.
- The program must complete `N = 10000` within 5 seconds.

## Examples

| N     | stdout    |
| ----- | --------- |
| 0     | `0\n`     |
| 2     | `1\n`     |
| 10    | `4\n`     |
| 100   | `25\n`    |
| 1000  | `168\n`   |
| 10000 | `1229\n`  |

## Language scaffold

{language_scaffold}
