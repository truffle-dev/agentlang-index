## Spec

# 016-parse-list-sum

Read line 1 as `N`, a decimal integer count in the range 0 to 1000
inclusive. Then read `N` more lines, each a decimal unsigned integer
that fits in u32 (range 0 through 4294967295 inclusive). Sum all
`N` values. Write the sum as decimal followed by a single newline.

If any of the following hold, write `error\n` instead and exit:

1. Line 1 fails to parse as a u32 or exceeds 1000.
2. Fewer than `N` additional value lines are available.
3. Any value line fails to parse as a u32 (empty body, non-digit
   characters, leading `+`/`-` sign, or value exceeds u32 max).
4. The running sum overflows u32 (would exceed 4294967295).

Trailing whitespace on each line is tolerated and trimmed before
parsing. Leading zeros are accepted (`007` parses as 7). The empty
sum (`N=0`) writes `0\n`.

Output exactly one line followed by `\n`. Do not write to standard
error. Exit with status 0 in every case.

## Examples

Input (stdin):

```
3
1
2
3
```

Output: `6\n`

Input (stdin):

```
0
```

Output: `0\n`

Input (stdin):

```
2
1
abc
```

Output: `error\n` (non-digit mid-list)

Input (stdin):

```
2
4294967295
1
```

Output: `error\n` (running sum overflows u32)

## Zero input convention

Zero 0.1.2 has no exposed stdin capability. The Zero reference reads
`N` from `argv[1]` and the `N` values from `argv[2]`, `argv[3]`, etc.;
values are interpreted exactly as the corresponding stdin lines for
other languages.

## Single-file Zero layout

Write a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>
