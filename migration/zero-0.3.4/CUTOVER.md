# Zero 0.1.2 -> 0.3.4 cutover plan

`RECIPE.md` proves the source PORT recipe (every corpus task ports to 0.3.4 and
passes byte-exact, bridged through `zero-graph-shim.sh`). This file is the plan
for the **production cutover**: the live corpus and CI stop using 0.1.2 and the
shim, and start invoking the real 0.3.4 binary the documented way.

The cutover is one coordinated commit on `zero-0.3.4-refresh`, opened as a PR so
`verify-refs` validates the whole thing on 0.3.4 before it touches `main`. It has
three halves; all three must land together so CI never goes red mid-flight.

## Half 1 — corpus sources + verify.sh drivers (DONE as a tool)

`cutover.sh` performs the shimless migration on a corpus tree:

- single-file task: rename `ref.zero` -> `ref.0`, port it through `port_ref.py`,
  inject a one-time `zero import ref.0 --out ref.graph` after the
  `if [[ -x "$ZERO" ]]; then` anchor in `verify.sh`, and rewrite the run command
  `run ref.zero` -> `run ref.graph` (code lines only; comments left intact).
- package task: port every `zero/src/*.0` in place, inject a one-time
  `zero import zero` after the anchor; the `run zero -- ARGS` directory call is
  already correct for 0.3.4.

Proven: run with no argument it migrates a temp copy of `corpus/` and leaves the
live tree untouched. Every migrated `verify.sh --lang zero` was run against the
**real** 0.3.4 binary (no shim) and all 20 pass byte-exact:

```
migration/zero-0.3.4/cutover.sh                 # migrate a temp copy
for d in <temp>/0*/; do (cd "$d" && ZERO=~/.local/bin/zero bash verify.sh --lang zero); done
# -> PASS=20 FAIL=0
```

To execute Half 1 on the live tree: `cutover.sh corpus` (in-place).

## Half 2 — CI binary (`.github/workflows/verify-refs.yml`)

Today CI clones `vercel-labs/zero` at the 0.1.2-era pin
`ZERO_PINNED_SHA=2f182253d15c34335d70ab80aef6d7a794803fd6` and builds from
source. Switch it to download the tagged 0.3.4 release binary and verify its
checksum (matches how the repo vendors 0.3.4 in `vendor/zero/0.3.4/version.txt`):

```
gh release download v0.3.4 --repo vercel-labs/zero --pattern zero-linux-x64 -O bin/zero
echo "84a3c79d482260ee15660a49fc6b904afc927a230d05a4263039dd4dd1360e87  bin/zero" | sha256sum -c -
chmod +x bin/zero
```

The download is faster and more reproducible than a from-source build, and the
sha256 pin makes the toolchain version explicit. Drop the `ZERO_PINNED_SHA` env,
the `git clone`/`checkout`/build steps, and the stale comment that explains why
the pin is ahead of `vendor/.../version.txt` (no longer true after cutover).

## Half 3 — benchmark runner (`bench/runner.ts`)

The runner extracts each model's Zero output to a source file and invokes the
compiler. Re-port it to emit `ref.0` (not `ref.zero`) and to run the import->run
flow (single file: `import ref.0 --out ref.graph` then `run ref.graph`; package:
`import <dir>` then `run <dir> -- ARGS`), mirroring the verify.sh shape Half 1
writes. Keep the per-task arg plumbing unchanged.

## Build-artifact hygiene

`zero import` writes a graph next to the source: `ref.graph` for single files and
`zero/zero.graph` for packages. These are build outputs, not corpus inputs. Add
to `.gitignore` before the cutover so they are never committed:

```
corpus/**/ref.graph
corpus/**/zero/zero.graph
```

## What does NOT change

- The shim (`zero-graph-shim.sh`) and `verify-batch.sh` stay in `migration/` as
  the recipe proof; they are not part of the production path after cutover.
- The benchmark RUN against models (the paid OpenAI sweep) is separate from this
  cutover. Cutover only migrates the verification harness. A free Opus smoke runs
  first, and a paid sweep needs Cheema's go-ahead.
