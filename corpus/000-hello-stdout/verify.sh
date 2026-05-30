#!/usr/bin/env bash
# Run each reference implementation and verify it emits exactly the
# six bytes `hello\n` on stdout with empty stderr and exit code 0.
# Uses file-based comparison so trailing newlines survive (bash command
# substitution strips them).
#
# Usage:
#   verify.sh                  # check every language whose toolchain is present
#   verify.sh --lang <lang>    # check only one language (zero|ts|rust|go|python)
set -uo pipefail

cd "$(dirname "$0")"
EXIT=0

ONLY_LANG=""
while (( $# > 0 )); do
  case "$1" in
    --lang)
      ONLY_LANG="${2:-}"
      shift 2
      ;;
    --lang=*)
      ONLY_LANG="${1#*=}"
      shift
      ;;
    *)
      echo "verify.sh: unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

want_lang() {
  [[ -z "$ONLY_LANG" || "$ONLY_LANG" == "$1" ]]
}

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
if want_lang zero; then
  ZERO="${ZERO:-/home/phantom/repos/zero/bin/zero}"
  if [[ -x "$ZERO" ]]; then
    check zero "$ZERO run ref.zero"
  else
    echo "SKIP: zero (bin/zero not found)"
  fi
fi

# TypeScript via tsx or ts-node — fall back to node against a .mjs copy
if want_lang ts; then
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
fi

# Rust — use rustc directly to avoid Cargo overhead for a one-liner
if want_lang rust; then
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
fi

# Go
if want_lang go; then
  if command -v go >/dev/null 2>&1; then
    check go "go run ref.go"
  else
    echo "SKIP: go (go not found)"
  fi
fi

# Python
if want_lang python; then
  if command -v python3 >/dev/null 2>&1; then
    check python "python3 ref.py"
  elif command -v python >/dev/null 2>&1; then
    check python "python ref.py"
  else
    echo "SKIP: python (python3 not found)"
  fi
fi

exit $EXIT
