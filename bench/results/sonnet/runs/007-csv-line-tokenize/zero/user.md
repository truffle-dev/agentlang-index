## Spec

## Task: CSV line tokenizer (RFC 4180 subset)

Read one line of CSV input from standard input. Split it into fields per
a simplified RFC 4180 grammar and write each field on its own line of
stdout terminated by `\n`.

### Grammar

- Fields are separated by commas (`,`).
- A field may be **quoted** by enclosing the field in double quotes (`"`).
  Inside a quoted field, a literal `"` is represented by two consecutive
  double quotes (`""`), and commas are literal.
- An **unquoted** field contains no commas and no double quotes.
- The input is at most 1000 printable-ASCII characters and is terminated
  by `\n`. The input is well-formed; you do not need to handle malformed
  CSV.
- If the input line is empty, write nothing (zero fields, zero newlines).

### Output

Each field, in input order, followed by exactly one `\n`. Exit with status 0.

## Examples

| input             | output                |
| ----------------- | --------------------- |
| `a,b,c`           | `a\nb\nc\n`           |
| `"a,b",c`         | `a,b\nc\n`            |
| `,,`              | `\n\n\n`              |
| (empty)           | (empty)               |
| `"a""b","c"`      | `a"b\nc\n`            |
| `1,"hello, world",foo` | `1\nhello, world\nfoo\n` |

Two consecutive commas `,,` parse as three empty fields. A line with just
a single comma `,` parses as two empty fields. A pair of double quotes
`""` is one empty field.

## Single-file Zero layout

Write a single-file Zero program (ref.0). Read arguments from std.args (no stdin available). It is compiled with `zero import ref.0 --out ref.graph` and executed as: zero run ref.graph <argv...>
