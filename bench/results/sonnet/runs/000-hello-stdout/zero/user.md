## Spec

# Task: Hello, stdout

Write a complete program that prints the six bytes `hello\n` (lowercase,
no quotes, single trailing newline) to standard output and exits with
status code 0. Read no input.

## Acceptance

- Stdout must contain exactly the six bytes `hello\n`.
- Stderr must be empty.
- Exit code must be 0.
- Program must complete within 5 seconds.

## Single-file Zero layout

Write a single-file Zero program (ref.0). Read arguments from std.args (no stdin available). It is compiled with `zero import ref.0 --out ref.graph` and executed as: zero run ref.graph <argv...>
