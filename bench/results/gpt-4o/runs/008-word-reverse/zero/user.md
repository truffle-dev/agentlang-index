## Spec

## Task: Reverse the order of words on a line

Read one line of printable ASCII (at most 1000 characters) from standard
input. A **word** is a maximal run of non-space characters; the only
delimiter is the ASCII space (0x20). Multiple consecutive spaces, leading
spaces, and trailing spaces are allowed in the input but produce no
empty words.

Write the words in reverse order, separated by single spaces, followed by
exactly one newline. If the input contains no words at all (empty input or
all-space input), write nothing — no output and no newline. Exit with
status 0.

## Acceptance

- Stdin: one line, at most 1000 printable-ASCII characters, terminated by
  `\n`.
- Stdout: reversed words single-space separated and `\n`-terminated, OR
  empty if no words were present.
- Stderr: empty.
- Exit code: 0.

## Examples

| input                  | output             |
| ---------------------- | ------------------ |
| `hello world`          | `world hello\n`    |
| `the quick brown fox`  | `fox brown quick the\n` |
| `single`               | `single\n`         |
| (empty)                | (empty)            |
| `   `                  | (empty)            |
| `  multi   spaces  `   | `spaces multi\n`   |
| `a b c`                | `c b a\n`          |

Note: all runs of consecutive spaces collapse, and leading/trailing
spaces are stripped. The output always uses exactly one space between
adjacent words.

## Language scaffold

{language_scaffold}


## Single-file Zero layout

Write a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>
