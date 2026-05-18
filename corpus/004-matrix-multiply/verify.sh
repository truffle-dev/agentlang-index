#!/usr/bin/env bash
# Run each reference implementation against every test case and verify
# exact stdout / empty stderr / exit 0. Zero takes argv-flat: argv[1] is N,
# the next N*N args are A row-major, the next N*N args are B row-major.
# The other languages read the stdin schema described in the task spec.
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

# Test matrix: encoded as parallel arrays. STDIN holds the multi-line
# stdin payload (with \n inserted via $'...'); ARGV is a single string
# of whitespace-separated tokens that we expand into argv for Zero.
STDIN=()
ARGV=()
EXPECTED=()

# case 1: N=1, [2] * [3] = 6
STDIN+=($'1\n2\n3\n')
ARGV+=("1 2 3")
EXPECTED+=($'6\n')

# case 2: N=2, [[1,2],[3,4]] * [[5,6],[7,8]] = [[19,22],[43,50]]
STDIN+=($'2\n1 2\n3 4\n5 6\n7 8\n')
ARGV+=("2 1 2 3 4 5 6 7 8")
EXPECTED+=($'19 22\n43 50\n')

# case 3: N=3, identity * arbitrary = arbitrary
STDIN+=($'3\n1 0 0\n0 1 0\n0 0 1\n4 -3 2\n0 5 -1\n7 8 9\n')
ARGV+=("3 1 0 0 0 1 0 0 0 1 4 -3 2 0 5 -1 7 8 9")
EXPECTED+=($'4 -3 2\n0 5 -1\n7 8 9\n')

# case 4: N=3, larger product
STDIN+=($'3\n1 2 3\n4 5 6\n7 8 9\n9 8 7\n6 5 4\n3 2 1\n')
ARGV+=("3 1 2 3 4 5 6 7 8 9 9 8 7 6 5 4 3 2 1")
EXPECTED+=($'30 24 18\n84 69 54\n138 114 90\n')

# case 5: N=4 with mixed signs
STDIN+=($'4\n1 -1 2 0\n3 4 -5 6\n0 2 1 -3\n8 -7 0 5\n2 0 1 -1\n0 3 -2 4\n5 -1 0 2\n7 6 -3 0\n')
ARGV+=("4 1 -1 2 0 3 4 -5 6 0 2 1 -3 8 -7 0 5 2 0 1 -1 0 3 -2 4 5 -1 0 2 7 6 -3 0")
EXPECTED+=($'12 -5 3 -1\n23 53 -23 3\n-16 -13 5 10\n51 9 7 -36\n')

# case 6: N=5 with mixed signs
STDIN+=($'5\n1 2 3 4 5\n6 7 8 9 -1\n-2 -3 -4 -5 -6\n0 1 0 -1 0\n9 -9 1 -1 0\n1 -1 1 -1 1\n0 2 0 -2 0\n3 0 -3 0 3\n0 4 0 -4 0\n-5 5 -5 5 -5\n')
ARGV+=("5 1 2 3 4 5 6 7 8 9 -1 -2 -3 -4 -5 -6 0 1 0 -1 0 9 -9 1 -1 0 1 -1 1 -1 1 0 2 0 -2 0 3 0 -3 0 3 0 4 0 -4 0 -5 5 -5 5 -5")
EXPECTED+=($'-15 44 -33 4 -15\n35 39 -13 -61 35\n16 -54 40 -2 16\n0 -2 0 2 0\n12 -31 6 13 12\n')

# check_stdin <lang_label> <run_cmd>
check_stdin() {
  local lang="$1" run_cmd="$2"
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!STDIN[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    if ! printf '%s' "${STDIN[$i]}" | bash -c "$run_cmd" >"$out_file" 2>"$err_file"; then
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
    echo "PASS: $lang (all ${#STDIN[@]} cases)"
  else
    EXIT=1
  fi
}

check_zero_argv() {
  local zero_bin="$1"
  local i out_file err_file expected_file argv_str argv_arr
  local lang_ok=1
  for i in "${!ARGV[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    argv_str="${ARGV[$i]}"
    # shellcheck disable=SC2206
    argv_arr=($argv_str)
    if ! "$zero_bin" run ref.zero "${argv_arr[@]}" >"$out_file" 2>"$err_file"; then
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

# Zero - flat argv
if want_lang zero; then
  ZERO=/home/phantom/repos/zero/bin/zero
  if [[ -x "$ZERO" ]]; then
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
    if rustc ref.rs -o "$tmp/matmul" 2>/dev/null; then
      check_stdin rust "$tmp/matmul"
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
