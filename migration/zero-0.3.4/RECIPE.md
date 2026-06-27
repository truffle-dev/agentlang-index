# Zero 0.1.2 -> 0.3.4 corpus migration recipe

Status: **groundwork on branch `zero-0.3.4-refresh`, not merged.** The live
corpus and CI stay pinned to Zero 0.1.2 (`vendor/zero/0.1.2/version.txt`, the
`ZERO_PINNED_SHA` in `.github/workflows/verify-refs.yml`). This directory proves
the port recipe scales before the corpus is cut over wholesale.

Zero 0.3.4 (released 2026-06-13) is a major departure from 0.1.2. A binary swap
is not enough; the corpus sources, the per-task `verify.sh` invocation, the CI
build step, and `bench/runner.ts` all have to move together. This document is
the verified recipe for the source half of that move.

## What changes in a corpus `ref.zero`

1. **Keyword rename.** `pub fun` -> `pub fn`, `fun` -> `fn`. Mechanical.

2. **Mutable bindings.** `let mut x: T = ...` -> `var x: T = ...`. Immutable `let`
   is unchanged. `mut` is now a reserved word and is rejected as an identifier
   (`PAR100: reserved word cannot be used as an identifier`).

3. **Local bindings require a type annotation.** A bare `let x = expr` errors
   `PAR100: canonical local bindings require a type annotation`. Most corpus
   bindings were already annotated; only the ones whose type was previously
   inferred from a std return need a type added. The verified mapping:

   | inferred RHS              | 0.3.4 type     |
   | ------------------------- | -------------- |
   | `std.args.get(n)`         | `Maybe<String>`|
   | `std.args.len()`          | `usize`        |
   | `std.mem.span(...)`       | `Span<u8>`     |
   | `std.mem.len(...)`        | `usize`        |
   | `someMaybe.value`         | `String`       |
   | `someByteSpan[i]`         | `u8`           |

   `Maybe<T>` still exposes `.has` / `.value`; read `.value` only inside a
   visible `if x.has { ... }` guard (unchanged from 0.1.2).

`port_ref.py` applies all three transforms. It annotates only the RHS shapes
above and leaves any other inferred `let` untouched (printed to stderr as
`UNHANDLED`) so the compiler flags it loudly rather than the porter guessing.

## What changes in how a `ref` is compiled and run

0.1.2 ran a source file directly:

```
zero run ref.zero ARGS
```

0.3.4 is graph-based and rejects that with `BLD002: compiler command requires
graph input`. The two-step flow is:

```
zero import ref.0 --out ref.graph
zero run ref.graph ARGS
```

Two gotchas:

- **`zero import` requires a canonical `.0` extension.** Importing a file named
  `ref.zero` errors `BLD002: expected Zero source file or package`. The cutover
  will rename corpus `ref.zero` -> `ref.0` (and teach `bench/runner.ts` to emit
  `.0`).
- `if` is still statement-only, not an r-value (`let x: T = if c {..} else {..}`
  still errors PAR100). The 0.1.2 workarounds in the corpus already avoid this.

`zero-graph-shim.sh` bridges the old call into the new flow (copy to a `.0`
temp, import to a graph, run the graph), so the existing per-task `verify.sh`
runs unchanged against ported sources. It is a migration aid, not the final
harness.

## Proof

`verify-batch.sh` ports each single-file, non-HTTP corpus task through
`port_ref.py` and runs its unchanged `verify.sh --lang zero` through the shim
against the installed 0.3.4 binary. As of this commit all 15 pass byte-exact
across every public + hidden case:

```
000-hello-stdout 001-fibonacci-memoized 002-sieve-prime-count
003-levenshtein-distance 004-matrix-multiply 005-balanced-parens
006-substring-count 007-csv-line-tokenize 008-word-reverse 009-word-count
010-byte-frequency 011-rle-encode 015-checked-divide-u32 016-parse-list-sum
017-checked-add-overflow
---- PASS=15 FAIL=0
```

Run it yourself (needs zero 0.3.4 on PATH or `ZERO_REAL` set):

```
migration/zero-0.3.4/verify-batch.sh
```

## Out of scope here (later chapters of the cutover)

- **HTTP tasks 012-014** need a live fixture server plus `std.http` / `std.net`
  return-type annotations (`std.net.host`, `std.http.client`, `std.http.fetch`,
  `std.http.resultStatus`, ...). Not covered by the table above.
- **Multi-file tasks 018, 019** use a `zero/` package layout (`zero.json` +
  `src/`), not a single `ref.zero`. They import a package directory, not a file.
- Renaming `ref.zero` -> `ref.0`, rewriting every `verify.sh` Zero block to the
  import->run-graph flow, bumping the CI binary, and re-porting
  `bench/runner.ts`'s extraction + invocation are the cutover commit, done as
  one coordinated change so `verify-refs` never goes red mid-flight.
