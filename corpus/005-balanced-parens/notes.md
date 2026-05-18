# Notes — 005-balanced-parens

## Algorithm

Single stack of openers. Walk the input character by character. Push on
`(` `[` `{`; on `)` `]` `}` pop and verify the popped opener matches the
closer kind. Anything else is ignored. Balanced iff no mismatch occurred
AND the stack is empty at the end.

## Zero-specific notes

- argv[1] is the input string. The 1000-char spec cap matches the
  `[1000]u8` flat stack buffer.
- Bracket bytes used directly: `(` 40, `)` 41, `[` 91, `]` 93, `{` 123,
  `}` 125. Encoded as `u8` literals (`40_u8`, etc).
- Zero 0.1.2 has no `break` keyword inside a `while`. To short-circuit on
  the first mismatch, the loop sets `i = n` instead of `i = i + 1`. The
  same exit shape worked in tasks 001-004.
- Empty argv[1] is allowed (operator may run `zero run ref.zero ""`) and
  Zero's `std.args.get` still returns a value with an empty span. We
  branch on `.has` for safety but the empty-span path falls through
  cleanly: `n = 0`, the while loop is skipped, balanced + empty stack
  prints `yes\n`.

## Edge cases checked

| input | expected |
|---|---|
| empty line | `yes` |
| `()` | `yes` |
| `([{}])` | `yes` |
| `([)]` | `no` |
| `)` | `no` |
| `(` | `no` |
| `if (x[0] == y) { a = 1 }` | `yes` |
| `{[()()]{[]}}([{}])` | `yes` |

## Cross-implementation parity

All five references produce byte-exact `yes\n` or `no\n` on every case in
both stdin (TS/Rust/Go/Python) and argv (Zero) input modes.
