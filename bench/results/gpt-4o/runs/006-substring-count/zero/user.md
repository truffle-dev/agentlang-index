## Spec

## Task: Non-overlapping substring count

Read two lines from standard input:

1. A pattern `P` (1 to 100 printable-ASCII characters).
2. A text `T` (0 to 1000 printable-ASCII characters).

Count the number of **non-overlapping** occurrences of `P` inside `T`, using
a greedy left-to-right scan: once a match starts at index `i`, the next
candidate match starts at `i + len(P)`. Write the decimal count followed by
a newline. Exit with status 0.

## Acceptance

- Stdin: `P\nT\n`. Both lines printable-ASCII; `P` length in `[1, 100]`,
  `T` length in `[0, 1000]`.
- Stdout: the count as a decimal integer (no leading zeros, no sign) followed
  by exactly one `\n`.
- Stderr: empty.
- Exit code: 0.

## Examples

| pattern (P) | text (T)            | output |
| ----------- | ------------------- | ------ |
| `ab`        | `abababab`          | `4`    |
| `aa`        | `aaaa`              | `2`    |
| `xyz`       | `aaa`               | `0`    |
| `a`         | `bbbbb`             | `0`    |
| `na`        | `banana`            | `2`    |
| `hello`     | `hello`             | `1`    |
| `x`         | (empty)             | `0`    |

In `aa` over `aaaa`, the greedy non-overlapping rule yields 2 matches at
positions 0 and 2, not 3 matches. In `na` over `banana`, the matches are at
positions 2 and 4 (no overlap).

## Language scaffold

{language_scaffold}


## Single-file Zero layout

Write a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>
