#!/usr/bin/env bash
# Reproducible proof that the 0.1.2 -> 0.3.4 port recipe scales.
#
# For each single-file, non-HTTP corpus task it:
#   1. ports corpus/<task>/ref.zero through port_ref.py
#   2. drops the ported source + the unchanged corpus verify.sh into a temp dir
#   3. runs that verify.sh --lang zero through zero-graph-shim.sh, which bridges
#      the 0.1.2 `zero run ref.zero` call into the 0.3.4 import->run-graph flow
#   4. asserts the task PASSes byte-exact across every public + hidden case
#
# The live corpus is never mutated; this only reads it. HTTP tasks (012-014)
# need a fixture server + std.http type annotations and are out of scope here;
# the multi-file tasks (018, 019) use a zero/ package layout, also out of scope
# for this single-file batch proof.
#
# Requires: zero 0.3.4 on PATH (or ZERO_REAL pointing at it), python3.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PORT="$HERE/port_ref.py"
SHIM="$HERE/zero-graph-shim.sh"
export ZERO_REAL="${ZERO_REAL:-$HOME/.local/bin/zero}"

BATCH="000-hello-stdout 001-fibonacci-memoized 002-sieve-prime-count \
003-levenshtein-distance 004-matrix-multiply 005-balanced-parens \
006-substring-count 007-csv-line-tokenize 008-word-reverse 009-word-count \
010-byte-frequency 011-rle-encode 015-checked-divide-u32 016-parse-list-sum \
017-checked-add-overflow"

PASS=0; FAIL=0
for t in $BATCH; do
  src="$REPO/corpus/$t/ref.zero"
  ver="$REPO/corpus/$t/verify.sh"
  if [[ ! -f "$src" || ! -f "$ver" ]]; then
    echo "MISSING $t"; FAIL=$((FAIL+1)); continue
  fi
  td="$(mktemp -d)"
  if ! python3 "$PORT" < "$src" > "$td/ref.zero" 2>"$td/unhandled"; then
    echo "FAIL $t (port_ref.py error)"; cat "$td/unhandled"; FAIL=$((FAIL+1)); rm -rf "$td"; continue
  fi
  if [[ -s "$td/unhandled" ]]; then
    echo "WARN $t has unhandled inferred lets:"; sed 's/^/    /' "$td/unhandled"
  fi
  cp "$ver" "$td/verify.sh"
  out="$(cd "$td" && ZERO="$SHIM" bash verify.sh --lang zero 2>&1)"
  if grep -q "^PASS: zero" <<<"$out"; then
    echo "PASS $t"; PASS=$((PASS+1))
  else
    echo "FAIL $t:"; sed 's/^/    /' <<<"$out"; FAIL=$((FAIL+1))
  fi
  rm -rf "$td"
done

echo "---- PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" -eq 0 ]]
