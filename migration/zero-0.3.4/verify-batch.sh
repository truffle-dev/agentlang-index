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
# The multi-file tasks (018, 019) use a zero/ package layout (zero.json +
# src/main.0 + src/lib.0); they are ported the same way (every src/*.0 through
# port_ref.py, zero.json untouched) and driven through the shim's package
# branch, which bridges `zero run zero -- args` into the 0.3.4 import->run flow.
#
# The HTTP tasks (012, 013, 014) are single-file ref.zero drivers that talk to
# a per-task fixture_server.py over std.http. They are ported the same way as
# the other single-file tasks (the porter now carries the 0.3.4 std.http /
# std.net return types plus a local symbol table for identifier-RHS bindings)
# and additionally copy fixture_server.py into the temp dir so the corpus
# verify.sh can spin the fixture up itself.
#
# The live corpus is never mutated; this only reads it.
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

PKG_BATCH="018-caesar-cipher 019-run-length-encode"
for t in $PKG_BATCH; do
  pkg="$REPO/corpus/$t/zero"
  ver="$REPO/corpus/$t/verify.sh"
  if [[ ! -d "$pkg" || ! -f "$ver" ]]; then
    echo "MISSING $t"; FAIL=$((FAIL+1)); continue
  fi
  td="$(mktemp -d)"
  cp -r "$pkg" "$td/zero"
  # Port every package source (zero.json is left untouched). Every src/*.0 file
  # is passed as a sibling to each port invocation so cross-file user-fn calls
  # (e.g. main.0 calling a lib.0 export) resolve their declared return type.
  siblings=("$td"/zero/src/*.0)
  port_err=0
  for f in "${siblings[@]}"; do
    [[ -f "$f" ]] || continue
    if ! python3 "$PORT" "${siblings[@]}" < "$f" > "$f.ported" 2>"$td/unhandled"; then
      echo "FAIL $t (port_ref.py error on $(basename "$f"))"; cat "$td/unhandled"; port_err=1; break
    fi
    mv "$f.ported" "$f"
    if [[ -s "$td/unhandled" ]]; then
      echo "WARN $t/$(basename "$f") has unhandled inferred lets:"; sed 's/^/    /' "$td/unhandled"
    fi
  done
  if (( port_err )); then FAIL=$((FAIL+1)); rm -rf "$td"; continue; fi
  cp "$ver" "$td/verify.sh"
  out="$(cd "$td" && ZERO="$SHIM" bash verify.sh --lang zero 2>&1)"
  if grep -q "^PASS: zero" <<<"$out"; then
    echo "PASS $t"; PASS=$((PASS+1))
  else
    echo "FAIL $t:"; sed 's/^/    /' <<<"$out"; FAIL=$((FAIL+1))
  fi
  rm -rf "$td"
done

HTTP_BATCH="012-http-status-code 013-http-json-sum 014-http-header-echo"
for t in $HTTP_BATCH; do
  src="$REPO/corpus/$t/ref.zero"
  ver="$REPO/corpus/$t/verify.sh"
  fix="$REPO/corpus/$t/fixture_server.py"
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
  [[ -f "$fix" ]] && cp "$fix" "$td/fixture_server.py"
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
