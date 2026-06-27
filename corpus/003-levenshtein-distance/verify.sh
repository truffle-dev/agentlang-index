#!/usr/bin/env bash
# Run each reference implementation against every test case and verify
# exact stdout / empty stderr / exit 0. Zero takes A as argv[1] and B as
# argv[2] because Zero 0.1.2 has no exposed stdin capability; the rest
# read two lines from stdin.
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

# Test matrix: cover the public cases plus the hidden cases so this
# script is the canonical reference-impl sanity check for the task.
A_LIST=(
  "kitten"
  ""
  ""
  "saturday"
  "intention"
  "the quick brown fox jumps over the lazy dog"
)
B_LIST=(
  "sitting"
  ""
  "abc"
  "sunday"
  "execution"
  "the quick brown dog jumps over the lazy fox"
)
EXPECTED=("3" "0" "3" "3" "5" "4")

# check_stdin <lang_label> <run_cmd>
# Runs each (A, B, expected) triple by piping "A\nB\n" into bash -c "$run_cmd".
check_stdin() {
  local lang="$1" run_cmd="$2"
  local i a b expected out_file err_file expected_file
  local lang_ok=1
  for i in "${!A_LIST[@]}"; do
    a="${A_LIST[$i]}"
    b="${B_LIST[$i]}"
    expected="${EXPECTED[$i]}"
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s\n' "$expected" > "$expected_file"
    if ! printf '%s\n%s\n' "$a" "$b" | bash -c "$run_cmd" >"$out_file" 2>"$err_file"; then
      echo "FAIL: $lang A=$(printf %q "$a") B=$(printf %q "$b") (nonzero exit)"
      lang_ok=0
    elif ! cmp -s "$expected_file" "$out_file"; then
      echo "FAIL: $lang A=$(printf %q "$a") B=$(printf %q "$b") (stdout mismatch: got $(tr -d '\n' <"$out_file"), want $expected)"
      lang_ok=0
    elif [[ -s "$err_file" ]]; then
      echo "FAIL: $lang A=$(printf %q "$a") B=$(printf %q "$b") (stderr non-empty: $(tr -d '\n' <"$err_file"))"
      lang_ok=0
    fi
    rm -f "$out_file" "$err_file" "$expected_file"
  done
  if (( lang_ok )); then
    echo "PASS: $lang (all ${#A_LIST[@]} cases)"
  else
    EXIT=1
  fi
}

# check_zero_argv <zero_bin>
# Calls `<zero_bin> run ref.zero <A> <B>` so A and B reach the program as
# argv[1] and argv[2] without shell-quoting gymnastics on the strings.
check_zero_argv() {
  local zero_bin="$1"
  local i a b expected out_file err_file expected_file
  local lang_ok=1
  for i in "${!A_LIST[@]}"; do
    a="${A_LIST[$i]}"
    b="${B_LIST[$i]}"
    expected="${EXPECTED[$i]}"
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s\n' "$expected" > "$expected_file"
    if ! "$zero_bin" run ref.graph "$a" "$b" >"$out_file" 2>"$err_file"; then
      echo "FAIL: zero A=$(printf %q "$a") B=$(printf %q "$b") (nonzero exit)"
      lang_ok=0
    elif ! cmp -s "$expected_file" "$out_file"; then
      echo "FAIL: zero A=$(printf %q "$a") B=$(printf %q "$b") (stdout mismatch: got $(tr -d '\n' <"$out_file"), want $expected)"
      lang_ok=0
    elif [[ -s "$err_file" ]]; then
      echo "FAIL: zero A=$(printf %q "$a") B=$(printf %q "$b") (stderr non-empty: $(tr -d '\n' <"$err_file"))"
      lang_ok=0
    fi
    rm -f "$out_file" "$err_file" "$expected_file"
  done
  if (( lang_ok )); then
    echo "PASS: zero (all ${#A_LIST[@]} cases)"
  else
    EXIT=1
  fi
}

# Zero - argv[1] + argv[2]
if want_lang zero; then
  ZERO="${ZERO:-/home/phantom/repos/zero/bin/zero}"
  if [[ -x "$ZERO" ]]; then
    "$ZERO" import ref.0 --out ref.graph >/dev/null 2>&1 || { echo "FAIL: zero (import ref.0)"; EXIT=1; }
    check_zero_argv "$ZERO"
  else
    echo "SKIP: zero (bin/zero not found)"
  fi
fi

# TypeScript: prefer tsx, then bun, then node on a .mjs copy.
if want_lang ts; then
  if command -v tsx >/dev/null 2>&1; then
    check_stdin ts "tsx ref.ts"
  elif command -v bun >/dev/null 2>&1; then
    check_stdin ts "bun run ref.ts"
  elif command -v node >/dev/null 2>&1; then
    tmp_ts=$(mktemp --suffix=.mjs)
    cp ref.ts "$tmp_ts"
    check_stdin ts "node $tmp_ts"
    rm -f "$tmp_ts"
  else
    echo "SKIP: ts (no tsx, bun, or node)"
  fi
fi

# Rust - rustc directly, drop the binary into a tmp dir
if want_lang rust; then
  if command -v rustc >/dev/null 2>&1; then
    tmp=$(mktemp -d)
    if rustc ref.rs -o "$tmp/levenshtein" 2>/dev/null; then
      check_stdin rust "$tmp/levenshtein"
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
    check_stdin go "go run ref.go"
  else
    echo "SKIP: go (go not found)"
  fi
fi

# Python
if want_lang python; then
  if command -v python3 >/dev/null 2>&1; then
    check_stdin python "python3 ref.py"
  elif command -v python >/dev/null 2>&1; then
    check_stdin python "python ref.py"
  else
    echo "SKIP: python (python3 not found)"
  fi
fi

exit $EXIT
