# Notes — 018-caesar-cipher

## Algorithm

Read shift (0..=25) and plaintext (lowercase a-z, non-empty). For each
plaintext byte `b`, output `'a' + ((b - 'a' + shift) % 26)`. Trailing
newline on output. If shift fails to parse or exceeds 25, or plaintext
is empty, or any plaintext byte is outside `a`..`z`, write `error\n`.
Process exit is 0 in every case.

## Multi-file arc opener

This task opens the multi-file arc. The Zero implementation lives
under `zero/` as a proper Zero project:

```
zero/
  zero.json       # package metadata (cli exe target, linux-musl-x64)
  src/
    main.0        # parses argv, validates, composes lib calls
    lib.0         # is_lowercase_letter, shift_letter helpers
```

The driver imports the library with `use lib`, then calls
`is_lowercase_letter(b)` on each plaintext byte for validation and
`shift_letter(b, shift_val)` to produce each ciphertext byte. The
project is invoked as `zero run zero -- <shift> <plaintext>` —
project directory, double-dash, two argv values.

## Lib signature constraint

Zero 0.1.2's direct ELF64 backend forbids user functions that take
or return `Span<u8>`, `MutSpan<u8>`, or shape values (the seventh
quirk surfaced on task 014). Lib signatures are pinned to pure
scalars to stay below that line:

```zero
pub fun is_lowercase_letter(b: u8) -> Bool
pub fun shift_letter(b: u8, shift: u8) -> u8
```

The plaintext bytes are walked one at a time in `main.0`, calling
into `lib.0` for each byte. This keeps the module boundary purely
scalar and produces a clean compile across both modules.

## Maybe<T> construction constraint (discovery)

I briefly tried to have lib expose a `parse_shift(s: Span<u8>) ->
Maybe<u8>` helper. Two problems compounded:

1. `Span<u8>` at the module boundary trips the seventh quirk.
2. Even with scalar inputs, constructing a `Maybe<u8>` for the
   success case fails: user code cannot construct `Some(value)`.
   The shape-literal form `Maybe<u8>{ has: true, value: x }` is
   rejected with PAR100 "expected '}' after block". User code can
   only `return null` for None; Some values come back from stdlib
   calls returning `Maybe<T>` directly.

The workaround keeps parse logic inline in `main.0` (parses argv[1]
as a u64 accumulator, bounds-checks against 25, casts down to u8)
and exports only the per-byte scalar helpers from lib. This shape
both avoids the boundary quirk AND avoids the Maybe<T> construction
limitation, while still demonstrating a real lib/main split.

This is recorded as Zero 0.1.2 quirk #9 in the running tally
(user-code Maybe<T>::Some construction not supported), but it does
not block any task in the corpus — every error path can collapse
through `error\n` without needing to thread Some values across
module boundaries.

## Cross-implementation parity

All five share the same dispatch:

1. parse shift (0..=25 inclusive)
2. validate plaintext non-empty
3. validate each plaintext byte in [a-z]
4. emit `'a' + ((byte - 'a' + shift) % 26)` for each, then `\n`

Byte-exact agreement on every case across zero/ts/rust/go/python.

## Zero-specific notes

- argv[1..2] carry shift and plaintext (no exposed stdin in Zero 0.1.2).
- The output buffer is `[1100]u8 = [0_u8; 1100]` — generous fixed
  upper bound for the test corpus; no dynamic allocation needed.
- `main` ends with an explicit `return` to dodge the trailing-write
  byte-count-as-exit-code codegen quirk surfaced on task 012.
- `std.parse.parseU32` would in principle work for shift parsing
  but it's still unusable for runtime data per the eighth quirk
  (CGEN004 on direct ELF64 for non-literal input from task 015).
- The shift accumulator uses u64 to keep overflow-free across the
  digit loop, then bounds-checks against 25 before casting to u8.

No new codegen quirks surfaced during 018 — the nine quirks now
known were all visible from prior tasks or from the Maybe<T>
construction probe done here. The multi-file build worked
end-to-end on first compile of both modules.
