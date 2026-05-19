## Spec

# Task 009 — word-count

## Problem

Read all bytes from standard input. A **word** is a maximal run of
non-whitespace bytes. The whitespace bytes are:

- space (0x20)
- tab (0x09)
- newline (0x0A)
- carriage return (0x0D)

Write the total word count as a decimal integer to standard output,
followed by exactly one newline. Exit with status 0.

## Edge cases

- Empty input → write `0\n`.
- All-whitespace input → write `0\n`.
- Single word with no trailing whitespace → write `1\n`.
- Words separated by any mix of whitespace bytes count by maximal
  non-whitespace runs only; consecutive whitespace bytes never produce
  an empty word.

## Acceptance

The stdout produced by your program must match the expected bytes
exactly for every test case (public and hidden). Stderr must be empty
and the process must exit 0.

## Input convention

- **stdin** (TypeScript, Rust, Go, Python): read all bytes until EOF.
- **argv[1]** (Zero 0.1.2 has no exposed stdin capability): read the
  bytes from the first command-line argument.

## Token budget

1200 tokens.
