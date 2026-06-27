#!/usr/bin/env bash
# Spin up the local HTTP fixture on port 18014, then run each reference
# against six cases (three public + three hidden) verifying byte-exact
# stdout, empty stderr, and exit 0. Tear down the fixture on exit.
#
# Zero takes (URL, name) as argv[1..2] (no exposed stdin in Zero 0.1.2);
# the other languages read two newline-separated lines from stdin.
#
# Usage:
#   verify.sh                  # check every language whose toolchain is present
#   verify.sh --lang <lang>    # check only one language
set -uo pipefail

cd "$(dirname "$0")"
EXIT=0
PORT=18014

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

start_fixture() {
  local py
  if command -v python3 >/dev/null 2>&1; then
    py=python3
  elif command -v python >/dev/null 2>&1; then
    py=python
  else
    echo "verify.sh: python3 not found; cannot start fixture server" >&2
    return 2
  fi
  FIXTURE_LOG=$(mktemp)
  "$py" fixture_server.py "$PORT" >"$FIXTURE_LOG" 2>&1 &
  FIXTURE_PID=$!
  local waited=0
  while (( waited < 50 )); do
    if grep -q '^ready$' "$FIXTURE_LOG" 2>/dev/null; then
      return 0
    fi
    if ! kill -0 "$FIXTURE_PID" 2>/dev/null; then
      echo "verify.sh: fixture exited early; log:" >&2
      cat "$FIXTURE_LOG" >&2
      return 2
    fi
    sleep 0.1
    waited=$((waited + 1))
  done
  echo "verify.sh: fixture did not report ready within 5s" >&2
  cat "$FIXTURE_LOG" >&2
  return 2
}

stop_fixture() {
  if [[ -n "${FIXTURE_PID:-}" ]] && kill -0 "$FIXTURE_PID" 2>/dev/null; then
    kill "$FIXTURE_PID" 2>/dev/null
    wait "$FIXTURE_PID" 2>/dev/null
  fi
  if [[ -n "${FIXTURE_LOG:-}" ]]; then
    rm -f "$FIXTURE_LOG"
  fi
}

trap stop_fixture EXIT

if ! start_fixture; then
  exit 2
fi

URL=()
NAME=()
EXPECTED=()

# Public 1: X-Echo header on /headers route
URL+=("http://127.0.0.1:18014/headers"); NAME+=("X-Echo"); EXPECTED+=($'hello-world\n')

# Public 2: case-insensitive content-type lookup
URL+=("http://127.0.0.1:18014/headers"); NAME+=("content-type"); EXPECTED+=($'application/json\n')

# Public 3: X-Custom-Name header echo
URL+=("http://127.0.0.1:18014/headers"); NAME+=("X-Custom-Name"); EXPECTED+=($'first-value\n')

# Hidden 1: missing header on /empty route
URL+=("http://127.0.0.1:18014/empty"); NAME+=("X-Missing"); EXPECTED+=($'error\n')

# Hidden 2: non-200 status even with X-Echo present
URL+=("http://127.0.0.1:18014/404"); NAME+=("X-Echo"); EXPECTED+=($'error\n')

# Hidden 3: non-200 status on unknown route
URL+=("http://127.0.0.1:18014/no-such-route"); NAME+=("Content-Type"); EXPECTED+=($'error\n')

check_stdin() {
  local lang="$1" run_cmd="$2"
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!URL[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    if ! printf '%s\n%s\n' "${URL[$i]}" "${NAME[$i]}" | bash -c "$run_cmd" >"$out_file" 2>"$err_file"; then
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
    echo "PASS: $lang (all ${#URL[@]} cases)"
  else
    EXIT=1
  fi
}

check_zero_argv() {
  local zero_bin="$1"
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!URL[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    if ! "$zero_bin" run ref.graph "${URL[$i]}" "${NAME[$i]}" >"$out_file" 2>"$err_file"; then
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
    echo "PASS: zero (all ${#URL[@]} cases)"
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
      check_stdin rust "./target/release/http_header_echo"
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
