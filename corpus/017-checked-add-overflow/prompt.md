# 017-checked-add-overflow

Read two lines from standard input. Each line contains an unsigned
decimal integer that fits in u32 (range 0 through 4294967295
inclusive). Parse both. Compute the sum `a + b` and write the result
as decimal followed by a single newline.

If any of the following hold, write the literal string `error\n`
instead and exit:

1. Either line fails to parse as a u32 (empty input, non-digit
   characters in the body, leading `+` sign, value exceeds u32
   maximum).
2. The sum `a + b` would exceed 4294967295 (u32 overflow).

Trailing whitespace on either digit line is tolerated and trimmed
before parsing. Leading zeros are accepted (`007` parses as 7).

Output exactly one line followed by `\n`. Do not write to standard
error. Exit with status 0 in every case.

## Examples

Input (stdin):

```
2
3
```

Output: `5\n`

Input (stdin):

```
0
4294967295
```

Output: `4294967295\n` (boundary, sum equals u32 max)

Input (stdin):

```
4294967295
1
```

Output: `error\n` (smallest u32 overflow)

Input (stdin):

```
2147483648
2147483648
```

Output: `error\n` (2^31 + 2^31 = 2^32, exact wrap)

Input (stdin):

```
abc
5
```

Output: `error\n` (parse fails on first line)

## Zero input convention

Zero 0.1.2 has no exposed stdin capability. The Zero reference
reads `a` from `argv[1]` and `b` from `argv[2]`; values are
interpreted exactly as the two stdin lines for other languages.
