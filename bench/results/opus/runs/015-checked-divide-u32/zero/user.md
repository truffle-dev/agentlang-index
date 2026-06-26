## Spec

# 015-checked-divide-u32

Read two lines from standard input. Each line contains an unsigned
decimal integer that fits in u32 (range 0 through 4294967295
inclusive). Parse both. Compute the integer floor quotient `a / b`
and write the result as decimal followed by a single newline.

If any of the following hold, write the literal string `error\n`
instead and exit:

1. Either line fails to parse as a u32 (empty input, non-digit
   characters in the body, leading `+` sign, value exceeds u32
   maximum).
2. The second value (`b`) is 0.

Trailing whitespace on either digit line is tolerated and trimmed
before parsing. Leading zeros are accepted (`007` parses as 7).

Output exactly one line followed by `\n`. Do not write to standard
error. Exit with status 0 in every case.

## Examples

Input (stdin):

```
20
4
```

Output: `5\n`

Input (stdin):

```
42
0
```

Output: `error\n`

Input (stdin):

```
abc
9
```

Output: `error\n`

Input (stdin):

```
4294967296
1
```

Output: `error\n` (exceeds u32 max)

Input (stdin):

```
0
7
```

Output: `0\n` (0 / 7 == 0)

## Zero input convention

Zero 0.1.2 has no exposed stdin capability. The Zero reference
reads `a` from `argv[1]` and `b` from `argv[2]`; values are
interpreted exactly as the two stdin lines for other languages.

## Single-file Zero layout

Write a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>
