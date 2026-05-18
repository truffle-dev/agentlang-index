# Notes — 007-csv-line-tokenize

## Algorithm

Explicit four-state machine over input bytes:

- `FIELD_START` (0): about to start a new field
- `IN_UNQUOTED` (1): inside an unquoted field
- `IN_QUOTED` (2): inside a quoted field
- `AFTER_CLOSING_QUOTE` (3): saw a `"` inside a quoted field; deciding
  whether it was an escape (`""`) or the close of the field

Transitions:

| state | `"` | `,` | other |
| --- | --- | --- | --- |
| `FIELD_START` | → `IN_QUOTED` | emit `\n` | emit char, → `IN_UNQUOTED` |
| `IN_UNQUOTED` | (does not occur per spec) | emit `\n`, → `FIELD_START` | emit char |
| `IN_QUOTED` | → `AFTER_CLOSING_QUOTE` | emit char | emit char |
| `AFTER_CLOSING_QUOTE` | emit `"`, → `IN_QUOTED` | emit `\n`, → `FIELD_START` | (malformed, ignored) |

After the loop ends, if any byte was processed, emit one final `\n` (the
last field's terminator).

## Why a state machine, not Python's `csv` module

The Python reference deliberately re-implements the state machine even
though `csv.reader` is available. The whole point of the AgentLang Index
is to make every reference do the same byte-level work so a model writing
each language has the same shape of code to discover. Hiding the
state machine behind a stdlib reader in Python would let TS/Rust/Go/Zero
diverge silently when a model misreads `""` as "escape" vs "close + new
quoted field."

## Edge cases the test set captures

- Empty input → zero fields → no output.
- `,,` → three empty fields → three newlines.
- `"a,b",c` → comma inside quoted field is literal.
- `"a""b","c"` → `""` is a literal `"` inside a quoted field.
- `1,"hello, world",foo` → mixed quoted/unquoted with embedded comma
  and space.

The single comma case (`,`) is not in the published set but is the
canonical trap: it produces **two** empty fields, not one. The state
machine handles it: FIELD_START sees `,`, emits `\n` and stays in
FIELD_START; loop ends; emit final `\n` → output is `\n\n`.

## Zero-specific notes

- argv[1] is the line.
- No `match`/`switch` in Zero 0.1.2 direct backend, so the state
  transitions are nested `if` blocks (state == 0 vs state == 1 etc.).
- Output buffer is `[1200]u8`. Worst-case is 501 newlines for `,` ×
  500 (the spec caps input at 1000 chars, so worst-case fields = 501).
- Output is built once and written with a single `world.out.write` call
  on a slice of the buffer; no per-field allocations.

## Cross-implementation parity

All five references produce byte-exact output on every case in both
stdin (TS/Rust/Go/Python) and argv (Zero) input modes.
