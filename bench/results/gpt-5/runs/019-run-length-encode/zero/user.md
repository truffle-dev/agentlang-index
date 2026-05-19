## Spec

# 019-run-length-encode

Read one line from standard input. It is a non-empty string of
lowercase ASCII letters (bytes `a` through `z`), terminated by a
single `\n`.

Walk the input from left to right grouping consecutive identical
bytes into maximal runs. For each run, write the byte followed by
the decimal run length (no leading zeros, no separator). After all
runs are written, append a single trailing `\n`.

If the input line is empty, or if any byte is outside `a` through
`z` (uppercase, digits, punctuation, whitespace, or non-ASCII), write
the literal string `error\n` instead and exit.

Do not write to standard error. Exit with status 0 in every case.

## Examples

Input (stdin): `aaabbc\n`

Output: `a3b2c1\n`

Input (stdin): `abcdef\n`

Output: `a1b1c1d1e1f1\n` (every run has length one)

Input (stdin): `z\n`

Output: `z1\n` (single byte is a single run)

Input (stdin): `aaaaaaaaaaaaa\n` (thirteen `a`s)

Output: `a13\n` (multi-digit run length)

Input (stdin): `\n` (empty line)

Output: `error\n`

Input (stdin): `Hello\n`

Output: `error\n` (uppercase H rejects)

## Zero input convention

Zero 0.1.2 has no exposed stdin capability. The Zero reference is a
multi-file project under `zero/`: `zero.json` is the package manifest,
`src/main.0` is the driver, and `src/lib.0` exports
`is_lowercase_letter`, `digit_byte`, and `decimal_length`. The driver
reads the plaintext from `argv[1]`; the value is interpreted exactly
as the stdin line for other languages (taken verbatim). Invoked as
`zero run zero -- <plaintext>`.


## Multi-file Zero project layout

Write a multi-file Zero project. Emit at minimum:

=== zero.json ===
{
  "package": { "name": "t_019_run_length_encode", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/main.0 ===
(your driver, with `use lib` to pull in helpers)

=== src/lib.0 ===
(scalar-only exports, no Span<u8>/shape values)

Invoked as: zero run <projdir> -- <argv...>
