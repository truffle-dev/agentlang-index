#!/usr/bin/env bash
# Run each reference against six cases (three public + three hidden)
# verifying byte-exact stdout, empty stderr, and exit 0.
#
# Zero takes (a, b) as argv[1..2] (no exposed stdin in Zero 0.1.2);
# the other languages read two newline-separated lines from stdin.
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

A=()
B=()
EXPECTED=()

# Public 1: small positive add (2 + 3 == 5)
A+=("2"); B+=("3"); EXPECTED+=($'5\n')

# Public 2: boundary just under wrap (0 + 4294967295 == 4294967295)
A+=("0"); B+=("4294967295"); EXPECTED+=($'4294967295\n')

# Public 3: small positive add (1000 + 2000 == 3000)
A+=("1000"); B+=("2000"); EXPECTED+=($'3000\n')

# Hidden 1: smallest u32 overflow (4294967295 + 1)
A+=("4294967295"); B+=("1"); EXPECTED+=($'error\n')

# Hidden 2: exact u32 wrap (2^31 + 2^31 == 2^32)
A+=("2147483648"); B+=("2147483648"); EXPECTED+=($'error\n')

# Hidden 3: parse fails on first addend
A+=("abc"); B+=("5"); EXPECTED+=($'error\n')

check_stdin() {
  local lang="$1" run_cmd="$2"
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!A[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    if ! printf '%s\n%s\n' "${A[$i]}" "${B[$i]}" | bash -c "$run_cmd" >"$out_file" 2>"$err_file"; then
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
    echo "PASS: $lang (all ${#A[@]} cases)"
  else
    EXIT=1
  fi
}

check_zero_argv() {
  local zero_bin="$1"
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!A[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    if ! "$zero_bin" run ref.zero "${A[$i]}" "${B[$i]}" >"$out_file" 2>"$err_file"; then
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
    echo "PASS: zero (all ${#A[@]} cases)"
  else
    EXIT=1
  fi
}

if want_lang zero; then
  ZERO=/home/phantom/repos/zero/bin/zero
  if [[ -x "$ZERO" ]]; then
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
      check_stdin rust "./target/release/checked_add_overflow"
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
