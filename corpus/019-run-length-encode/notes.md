# Notes — 019-run-length-encode

## Algorithm

Read plaintext (lowercase a-z, non-empty, one line). Walk left to right
grouping consecutive identical bytes into maximal runs. For each run,
emit the byte followed by the decimal run length (no leading zeros,
no separator). Final trailing `\n`. If the line is empty or contains
any byte outside `a`..`z`, write `error\n`. Process exit is 0 in every
case.

## Multi-file arc closer

This task closes the multi-file arc that 018-caesar-cipher opened. The
Zero implementation lives under `zero/` as a proper Zero project:

```
zero/
  zero.json       # package metadata (cli exe target, linux-musl-x64)
  src/
    main.0        # parses argv, validates, walks runs, renders decimals
    lib.0         # is_lowercase_letter, digit_byte, decimal_length
```

The driver imports the library with `use lib`, then calls
`is_lowercase_letter(b)` for validation, `decimal_length(n)` to size
the digit emit, and `digit_byte(d)` to render each decimal digit. The
project is invoked as `zero run zero -- <plaintext>` — project
directory, double-dash, one argv value.

## Lib signature constraint (still scalar-only)

Lib signatures stay pure scalars to stay clear of the seventh quirk
(Span<u8>/MutSpan<u8>/shape values at the module boundary are
rejected on the direct ELF64 backend):

```zero
pub fun is_lowercase_letter(b: u8) -> Bool
pub fun digit_byte(d: u8) -> u8
pub fun decimal_length(n: u32) -> u32
```

Decimal length uses a hard-coded chain of `if n < 10/100/.../10^9`
returning 1..10 — covers any u32 with no log calls and no allocator.

## Tenth quirk — if-expressions in `let` bindings

A first draft of `main.0` ended an inner loop with:

```zero
let actual_end = if run_end > t_len { run_end - 1 } else { run_end }
```

This is rejected with PAR100 "expected ';' after expression". Zero
0.1.2 does not support if-expressions as r-value forms — `if` is
statement-only.

The workaround is the standard scanning-flag pattern: a `mut`
accumulator plus a `scanning: Bool` sentinel, with state mutated
inside the `if` arms instead of returned from them:

```zero
let mut run_len: usize = 1
let mut probe: usize = run_start + 1
let mut scanning: Bool = true
while scanning {
    if probe >= t_len {
        scanning = false
    } else {
        if text_in[probe] == run_byte {
            run_len = run_len + 1
            probe = probe + 1
        } else {
            scanning = false
        }
    }
}
```

This is a refinement of the existing PAR100 quirk surface but is
worth surfacing on its own line because it's a separate language
restriction with a different workaround. The known tally is now ten.

## Cross-implementation parity

All five share the same dispatch:

1. read input (stdin line 1 or argv[1])
2. validate non-empty
3. validate each byte in [a-z]
4. walk maximal runs: for each, emit byte + decimal run length
5. emit trailing `\n`

Byte-exact agreement on every case across zero/ts/rust/go/python.

## Zero-specific notes

- argv[1] carries plaintext (no exposed stdin in Zero 0.1.2).
- Output buffer is `[16384]u8 = [0_u8; 16384]` — generous fixed
  upper bound; each input byte expands to at most 1 + 10 bytes
  (letter + up to 10 decimal digits for u32 max). Real corpus
  inputs are far below this.
- Decimal digits are emitted left-to-right by dividing by 10^pos
  for each position from `digit_count - 1` down to 0, mod 10. This
  avoids any inline reversal or scratch buffer.
- `main` ends with explicit `return` to dodge the trailing-write
  byte-count-as-exit-code codegen quirk from task 012.

## v1.0 corpus closure

This is task 20 of 20. The corpus reaches v1.0 with all twenty tasks
shipping byte-exact across all five languages. Tag and release notes
land in the v1.0.0 commit.
