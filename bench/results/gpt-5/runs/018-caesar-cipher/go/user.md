## Spec

# 018-caesar-cipher

Read two lines from standard input.

Line 1 is a non-negative decimal integer `shift` in the range 0 through
25 inclusive.

Line 2 is the plaintext: a non-empty string of lowercase ASCII letters
(bytes `a` through `z`).

Rotate each plaintext byte forward by `shift` positions within the
lowercase alphabet, wrapping `z + 1` back to `a`. Write the
resulting ciphertext followed by a single newline.

If any of the following hold, write the literal string `error\n`
instead and exit:

1. Line 1 fails to parse: empty after trimming whitespace, contains
   non-digit bytes, or evaluates to a value greater than 25.
2. Line 2 is empty.
3. Line 2 contains any byte outside `a` through `z` (uppercase,
   digits, punctuation, whitespace, non-ASCII all reject).

Trailing whitespace on line 1 is tolerated and trimmed before parsing.
Line 2 is taken verbatim (no trimming, no normalization).

Output exactly one line followed by `\n`. Do not write to standard
error. Exit with status 0 in every case.

## Examples

Input (stdin):

```
3
abc
```

Output: `def\n`

Input (stdin):

```
0
hello
```

Output: `hello\n` (shift of zero is the identity)

Input (stdin):

```
25
abc
```

Output: `zab\n` (each byte shifted back one position, with wrap)

Input (stdin):

```
13
xyz
```

Output: `klm\n` (rot13 on the lowercase alphabet)

Input (stdin):

```
26
abc
```

Output: `error\n` (shift > 25 rejects)

Input (stdin):

```
5
Hello
```

Output: `error\n` (uppercase H rejects)

## Zero input convention

Zero 0.1.2 has no exposed stdin capability. The Zero reference is a
multi-file project under `zero/`: `zero.json` is the package manifest,
`src/main.0` is the driver, and `src/lib.0` exports
`is_lowercase_letter` and `shift_letter`. The driver reads `shift`
from `argv[1]` and the plaintext from `argv[2]`; values are
interpreted exactly as the two stdin lines for other languages
(line 1 trimmed, line 2 verbatim). Invoked as
`zero run zero -- <shift> <plaintext>`.
