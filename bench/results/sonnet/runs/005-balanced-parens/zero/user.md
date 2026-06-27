## Spec

## Task: Balanced bracket checker

Read a single line of printable ASCII (at most 1000 characters) from standard
input. Decide whether the bracket characters `(`, `)`, `[`, `]`, `{`, `}` are
balanced:

- Every opener (`(`, `[`, `{`) has a matching closer (`)`, `]`, `}`).
- Every closer matches the most recent unmatched opener of the same kind.
- The opener/closer pairs nest without crossing.
- All non-bracket characters are ignored when judging balance.
- The empty input is balanced.

Write `yes` followed by a newline if the input is balanced, or `no` followed
by a newline if not. Exit with status 0.

## Acceptance

- Stdin: one line, at most 1000 printable-ASCII characters, terminated by `\n`.
- Stdout: exactly `yes\n` or exactly `no\n`.
- Stderr: empty.
- Exit code: 0.

## Examples

| input                      | output  |
| -------------------------- | ------- |
| (empty)                    | `yes`   |
| `()`                       | `yes`   |
| `([{}])`                   | `yes`   |
| `([)]`                     | `no`    |
| `(`                        | `no`    |
| `)`                        | `no`    |
| `abc(def[gh{ij}kl]mn)`     | `yes`   |
| `if (x[0] == y) { a = 1 }` | `yes`   |

## Single-file Zero layout

Write a single-file Zero program (ref.0). Read arguments from std.args (no stdin available). It is compiled with `zero import ref.0 --out ref.graph` and executed as: zero run ref.graph <argv...>
