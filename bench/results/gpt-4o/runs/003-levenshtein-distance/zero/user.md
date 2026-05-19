## Spec

## Task: Levenshtein edit distance

Read two short ASCII strings `A` and `B` from standard input (one per line),
each at most 50 characters and using only printable ASCII (`0x20..=0x7E`).
Compute the **Levenshtein edit distance** between them: the minimum number
of single-character insertions, deletions, or substitutions to transform
`A` into `B`. Each edit has cost 1. Write the distance to standard output
followed by a single newline. Exit with status 0.

Edge cases:

- If `A == B` the distance is `0`.
- If either string is empty the distance is the length of the other.

## Acceptance

- Stdin: two lines. Line 1 is `A`, line 2 is `B`. Either may be empty.
- Stdout: the decimal digits of the distance, followed by `\n`.
- Stderr: empty.
- Exit code: 0.
- The program must complete each test case within 5 seconds.

## Examples

| A          | B          | distance |
| ---------- | ---------- | -------- |
| `kitten`   | `sitting`  | `3`      |
| `saturday` | `sunday`   | `3`      |
| `flaw`     | `lawn`     | `2`      |
| `intention`| `execution`| `5`      |
| empty      | `abc`      | `3`      |
| empty      | empty      | `0`      |

## Language scaffold

{language_scaffold}


## Single-file Zero layout

Write a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>
