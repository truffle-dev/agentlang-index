## Spec

## Task: Square integer matrix multiply

Read two `N x N` integer matrices `A` and `B` from standard input, compute the
matrix product `C = A * B`, and write `C` to standard output.

**Input format** (stdin):

```
N
a_11 a_12 ... a_1N
a_21 a_22 ... a_2N
...
a_N1 a_N2 ... a_NN
b_11 b_12 ... b_1N
b_21 b_22 ... b_2N
...
b_N1 b_N2 ... b_NN
```

- `1 <= N <= 5`.
- Each matrix entry is an integer in `[-99, 99]`.
- Each row is on its own line; entries on a row are separated by single spaces.

**Output format** (stdout): `N` lines. Each line is one row of `C`, written as
`N` decimal integers separated by single spaces, terminated by a single newline.
The output ends with a newline after the last row.

## Acceptance

- Stdout: byte-exact match per test case.
- Stderr: empty.
- Exit code: 0.
- The program must complete each test case within 5 seconds.

## Examples

### Example 1

Input:
```
1
2
3
```

Output:
```
6
```

### Example 2

Input:
```
2
1 2
3 4
5 6
7 8
```

Output:
```
19 22
43 50
```

## Language scaffold

{language_scaffold}
