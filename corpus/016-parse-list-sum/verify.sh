#!/usr/bin/env bash
# Run each reference against six cases (three public + three hidden)
# verifying byte-exact stdout, empty stderr, and exit 0.
#
# Zero takes (N, v1, v2, ..., vN) as argv[1..N+1] (no exposed stdin in
# Zero 0.1.2); the other languages read N+1 newline-separated lines
# from stdin.
#
# Cases use a "|"-delimited string for the per-case argv list because
# Bash's parallel arrays don't support array-of-arrays cleanly.
#
# Usage:
#   verify.sh                  # check every language whose toolchain is present
#   verify.sh --lang <lang>    # check only one language
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

# Each ARGV[i] is a "|"-separated list of argv values starting with N.
# Each STDIN[i] is the corresponding newline-joined stdin text.
ARGV=()
EXPECTED=()

# Public 1: N=3, values [1,2,3] sum 6
ARGV+=("3|1|2|3"); EXPECTED+=($'6\n')

# Public 2: N=0, empty sum is 0
ARGV+=("0"); EXPECTED+=($'0\n')

# Public 3: N=5, values 10..50 sum 150
ARGV+=("5|10|20|30|40|50"); EXPECTED+=($'150\n')

# Hidden 1: N=2, second value non-digit
ARGV+=("2|1|abc"); EXPECTED+=($'error\n')

# Hidden 2: N=2, only 1 value provided
ARGV+=("2|1"); EXPECTED+=($'error\n')

# Hidden 3: N=2, running sum overflows u32 (2^32-1 + 1 = 2^32)
ARGV+=("2|4294967295|1"); EXPECTED+=($'error\n')

argv_to_stdin() {
  local argv_str="$1"
  local IFS='|'
  local arr=($argv_str)
  local out=""
  local x
  for x in "${arr[@]}"; do
    out+="${x}"$'\n'
  done
  printf '%s' "$out"
}

check_stdin() {
  local lang="$1" run_cmd="$2"
  local i out_file err_file expected_file stdin_text
  local lang_ok=1
  for i in "${!ARGV[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    stdin_text=$(argv_to_stdin "${ARGV[$i]}")
    if ! printf '%s' "$stdin_text" | bash -c "$run_cmd" >"$out_file" 2>"$err_file"; then
      echo "FAIL: $lang case $((i+1)) (nonzero exit)"
      lang_ok=0
    elif ! cmp -s "$expected_file" "$out_file"; then
      echo "FAIL: $lang case $((i+1)) (stdout mismatch)"
      diff <(printf '%s' "${EXPECTED[$i]}") "$out_file" | head -8
      lang_ok=0
    elif [[ -s "$err_file" ]]; then
      echo "FAIL: $lang case $((i+1)) (stderr non-empty: $(tr -d '\n' <"$err_file"))"
      lang_ok=0
    fi
    rm -f "$out_file" "$err_file" "$expected_file"
  done
  if (( lang_ok )); then
    echo "PASS: $lang (all ${#ARGV[@]} cases)"
  else
    EXIT=1
  fi
}

check_zero_argv() {
  local zero_bin="$1"
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!ARGV[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    local IFS='|'
    local arr=(${ARGV[$i]})
    if ! "$zero_bin" run ref.graph "${arr[@]}" >"$out_file" 2>"$err_file"; then
      echo "FAIL: zero case $((i+1)) (nonzero exit)"
      lang_ok=0
    elif ! cmp -s "$expected_file" "$out_file"; then
      echo "FAIL: zero case $((i+1)) (stdout mismatch)"
      diff <(printf '%s' "${EXPECTED[$i]}") "$out_file" | head -8
      lang_ok=0
    elif [[ -s "$err_file" ]]; then
      echo "FAIL: zero case $((i+1)) (stderr non-empty: $(tr -d '\n' <"$err_file"))"
      lang_ok=0
    fi
    rm -f "$out_file" "$err_file" "$expected_file"
  done
  if (( lang_ok )); then
    echo "PASS: zero (all ${#ARGV[@]} cases)"
  else
    EXIT=1
  fi
}

if want_lang zero; then
  ZERO="${ZERO:-/home/phantom/repos/zero/bin/zero}"
  if [[ -x "$ZERO" ]]; then
    "$ZERO" import ref.0 --out ref.graph >/dev/null 2>&1 || { echo "FAIL: zero (import ref.0)"; EXIT=1; }
    check_zero_argv "$ZERO"
  else
    echo "SKIP: zero (bin/zero not found)"
  fi
fi

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

if want_lang rust; then
  if command -v cargo >/dev/null 2>&1; then
    if cargo build --release --quiet 2>/dev/null; then
      check_stdin rust "./target/release/parse_list_sum"
    else
      echo "FAIL: rust (cargo build failed)"
      EXIT=1
    fi
  else
    echo "SKIP: rust (cargo not found)"
  fi
fi

if want_lang go; then
  if command -v go >/dev/null 2>&1; then
    check_stdin go "go run ref.go"
  else
    echo "SKIP: go (go not found)"
  fi
fi

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
