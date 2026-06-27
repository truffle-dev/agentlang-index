#!/usr/bin/env bash
# Run each reference implementation against every test case and verify
# exact stdout / empty stderr / exit 0. Zero takes the input as argv[1]
# (no exposed stdin in Zero 0.1.2); the other languages read all bytes
# from stdin until EOF.
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

STDIN=()
ARGV=()
EXPECTED=()

# Public case 1: two-word line
STDIN+=($'hello world\n')
ARGV+=("hello world")
EXPECTED+=($'2\n')

# Public case 2: single word
STDIN+=($'hello\n')
ARGV+=("hello")
EXPECTED+=($'1\n')

# Public case 3: empty line -> zero words
STDIN+=($'\n')
ARGV+=("")
EXPECTED+=($'0\n')

# Hidden case 1: collapse + trim spaces
STDIN+=($'  the   quick brown   fox  \n')
ARGV+=("  the   quick brown   fox  ")
EXPECTED+=($'4\n')

# Hidden case 2: five-word line
STDIN+=($'alpha beta gamma delta epsilon\n')
ARGV+=("alpha beta gamma delta epsilon")
EXPECTED+=($'5\n')

# Hidden case 3: mixed whitespace (tab + space + newline + CR)
STDIN+=($'a\tb c\nd\re\n')
ARGV+=($'a\tb c\nd\re')
EXPECTED+=($'5\n')

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
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!ARGV[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    if ! "$zero_bin" run ref.graph "${ARGV[$i]}" >"$out_file" 2>"$err_file"; then
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
  if command -v rustc >/dev/null 2>&1; then
    tmp=$(mktemp -d)
    if rustc ref.rs -o "$tmp/word_count" 2>/dev/null; then
      check_stdin rust "$tmp/word_count"
    else
      echo "FAIL: rust (rustc compilation failed)"
      EXIT=1
    fi
    rm -rf "$tmp"
  else
    echo "SKIP: rust (rustc not found)"
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
