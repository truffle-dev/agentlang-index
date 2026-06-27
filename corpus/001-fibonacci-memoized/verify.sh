#!/usr/bin/env bash
# Run each reference implementation against every test case and verify
# exact stdout / empty stderr / exit 0. Zero takes N as argv[1] because
# Zero 0.1.2 has no exposed stdin capability; the rest read stdin.
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

# Test matrix: (label, N, expected). Includes the hidden N=15 case so
# this script is the canonical reference-impl sanity check.
CASES=(
  "N=0  expected=0\n"
  "N=1  expected=1\n"
  "N=10 expected=55\n"
  "N=15 expected=610\n"
  "N=50 expected=12586269025\n"
)
NS=(0 1 10 15 50)
EXPECTED=("0" "1" "55" "610" "12586269025")

# $1 = lang label, $2 = input-mode (stdin|argv), $3 = command template
# with %N% placeholder.
check_lang() {
  local lang="$1" mode="$2" tmpl="$3"
  local i n expected cmd out_file err_file expected_file
  local lang_ok=1
  for i in "${!NS[@]}"; do
    n="${NS[$i]}"
    expected="${EXPECTED[$i]}"
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s\n' "$expected" > "$expected_file"
    cmd="${tmpl//%N%/$n}"
    if [[ "$mode" == "stdin" ]]; then
      if ! printf '%s\n' "$n" | bash -c "$cmd" >"$out_file" 2>"$err_file"; then
        echo "FAIL: $lang N=$n (nonzero exit)"
        lang_ok=0
      elif ! cmp -s "$expected_file" "$out_file"; then
        echo "FAIL: $lang N=$n (stdout mismatch: got $(tr -d '\n' <"$out_file"), want $expected)"
        lang_ok=0
      elif [[ -s "$err_file" ]]; then
        echo "FAIL: $lang N=$n (stderr non-empty: $(tr -d '\n' <"$err_file"))"
        lang_ok=0
      fi
    else
      if ! bash -c "$cmd" >"$out_file" 2>"$err_file"; then
        echo "FAIL: $lang N=$n (nonzero exit)"
        lang_ok=0
      elif ! cmp -s "$expected_file" "$out_file"; then
        echo "FAIL: $lang N=$n (stdout mismatch: got $(tr -d '\n' <"$out_file"), want $expected)"
        lang_ok=0
      elif [[ -s "$err_file" ]]; then
        echo "FAIL: $lang N=$n (stderr non-empty: $(tr -d '\n' <"$err_file"))"
        lang_ok=0
      fi
    fi
    rm -f "$out_file" "$err_file" "$expected_file"
  done
  if (( lang_ok )); then
    echo "PASS: $lang (all ${#NS[@]} cases)"
  else
    EXIT=1
  fi
}

# Zero — argv[1]
if want_lang zero; then
  ZERO="${ZERO:-/home/phantom/repos/zero/bin/zero}"
  if [[ -x "$ZERO" ]]; then
    "$ZERO" import ref.0 --out ref.graph >/dev/null 2>&1 || { echo "FAIL: zero (import ref.0)"; EXIT=1; }
    check_lang zero argv "$ZERO run ref.graph %N%"
  else
    echo "SKIP: zero (bin/zero not found)"
  fi
fi

# TypeScript: prefer tsx, then bun (native TS), then node on a .mjs copy.
# ref.ts is written so plain node accepts it after a .ts -> .mjs rename.
if want_lang ts; then
  if command -v tsx >/dev/null 2>&1; then
    check_lang ts stdin "tsx ref.ts"
  elif command -v bun >/dev/null 2>&1; then
    check_lang ts stdin "bun run ref.ts"
  elif command -v node >/dev/null 2>&1; then
    tmp_ts=$(mktemp --suffix=.mjs)
    cp ref.ts "$tmp_ts"
    check_lang ts stdin "node $tmp_ts"
    rm -f "$tmp_ts"
  else
    echo "SKIP: ts (no tsx, bun, or node)"
  fi
fi

# Rust — rustc directly, drop the binary into a tmp dir
if want_lang rust; then
  if command -v rustc >/dev/null 2>&1; then
    tmp=$(mktemp -d)
    if rustc ref.rs -o "$tmp/fib" 2>/dev/null; then
      check_lang rust stdin "$tmp/fib"
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
    check_lang go stdin "go run ref.go"
  else
    echo "SKIP: go (go not found)"
  fi
fi

# Python
if want_lang python; then
  if command -v python3 >/dev/null 2>&1; then
    check_lang python stdin "python3 ref.py"
  elif command -v python >/dev/null 2>&1; then
    check_lang python stdin "python ref.py"
  else
    echo "SKIP: python (python3 not found)"
  fi
fi

exit $EXIT
