#!/usr/bin/env bash
# Run each reference implementation and verify it emits exactly the
# six bytes `hello\n` on stdout with empty stderr and exit code 0.
# Uses file-based comparison so trailing newlines survive (bash command
# substitution strips them).
set -uo pipefail

cd "$(dirname "$0")"
EXIT=0
expected=$(mktemp)
printf 'hello\n' > "$expected"
trap 'rm -f "$expected"' EXIT

check() {
  local lang="$1" cmd="$2"
  local actual_out actual_err
  actual_out=$(mktemp)
  actual_err=$(mktemp)
  if ! bash -c "$cmd" >"$actual_out" 2>"$actual_err"; then
    echo "FAIL: $lang (nonzero exit)"
    rm -f "$actual_out" "$actual_err"
    EXIT=1
    return
  fi
  if ! cmp -s "$expected" "$actual_out"; then
    echo "FAIL: $lang (stdout mismatch — got: $(od -c <"$actual_out" | head -1))"
    rm -f "$actual_out" "$actual_err"
    EXIT=1
    return
  fi
  if [[ -s "$actual_err" ]]; then
    echo "FAIL: $lang (stderr non-empty)"
    rm -f "$actual_out" "$actual_err"
    EXIT=1
    return
  fi
  echo "PASS: $lang"
  rm -f "$actual_out" "$actual_err"
}

# Zero
ZERO=/home/phantom/repos/zero/bin/zero
if [[ -x "$ZERO" ]]; then
  check zero "$ZERO run ref.zero"
else
  echo "SKIP: zero (bin/zero not found)"
fi

# TypeScript via tsx or ts-node — fall back to node against a .mjs copy
if command -v tsx >/dev/null 2>&1; then
  check ts "tsx ref.ts"
elif command -v ts-node >/dev/null 2>&1; then
  check ts "ts-node ref.ts"
elif command -v node >/dev/null 2>&1; then
  tmp_ts=$(mktemp --suffix=.mjs)
  cp ref.ts "$tmp_ts"
  check ts "node $tmp_ts"
  rm -f "$tmp_ts"
else
  echo "SKIP: ts (no tsx, ts-node, or node)"
fi

# Rust — use rustc directly to avoid Cargo overhead for a one-liner
if command -v rustc >/dev/null 2>&1; then
  tmp=$(mktemp -d)
  if rustc ref.rs -o "$tmp/hello" 2>/dev/null; then
    check rust "$tmp/hello"
  else
    echo "FAIL: rust (rustc compilation failed)"
    EXIT=1
  fi
  rm -rf "$tmp"
else
  echo "SKIP: rust (rustc not found)"
fi

# Go
if command -v go >/dev/null 2>&1; then
  check go "go run ref.go"
else
  echo "SKIP: go (go not found)"
fi

# Python
if command -v python3 >/dev/null 2>&1; then
  check python "python3 ref.py"
elif command -v python >/dev/null 2>&1; then
  check python "python ref.py"
else
  echo "SKIP: python (python3 not found)"
fi

exit $EXIT
