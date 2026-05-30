#!/usr/bin/env bash
# Spin up the local HTTP fixture on port 18012, then run each reference
# against six cases (three public + three hidden) verifying byte-exact
# stdout, empty stderr, and exit 0. Tear down the fixture on exit.
#
# Zero takes the URL as argv[1] (no exposed stdin in Zero 0.1.2); the
# other languages read the URL from stdin until newline/EOF.
#
# Usage:
#   verify.sh                  # check every language whose toolchain is present
#   verify.sh --lang <lang>    # check only one language
set -uo pipefail

cd "$(dirname "$0")"
EXIT=0
PORT=18012

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
  # Wait up to 5s for "ready" line.
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

STDIN=()
ARGV=()
EXPECTED=()

# Public 1: 200 OK
STDIN+=("http://127.0.0.1:18012/status/200")
ARGV+=("http://127.0.0.1:18012/status/200")
EXPECTED+=($'200\n')

# Public 2: 404 Not Found
STDIN+=("http://127.0.0.1:18012/status/404")
ARGV+=("http://127.0.0.1:18012/status/404")
EXPECTED+=($'404\n')

# Public 3: 500 Internal Server Error
STDIN+=("http://127.0.0.1:18012/status/500")
ARGV+=("http://127.0.0.1:18012/status/500")
EXPECTED+=($'500\n')

# Hidden 1: 503 Service Unavailable
STDIN+=("http://127.0.0.1:18012/status/503")
ARGV+=("http://127.0.0.1:18012/status/503")
EXPECTED+=($'503\n')

# Hidden 2: root path defaults to 200
STDIN+=("http://127.0.0.1:18012/")
ARGV+=("http://127.0.0.1:18012/")
EXPECTED+=($'200\n')

# Hidden 3: unresolvable host surfaces as error
STDIN+=("http://this-host-does-not-resolve.invalid/")
ARGV+=("http://this-host-does-not-resolve.invalid/")
EXPECTED+=($'error\n')

check_stdin() {
  local lang="$1" run_cmd="$2"
  local i out_file err_file expected_file
  local lang_ok=1
  for i in "${!STDIN[@]}"; do
    out_file=$(mktemp)
    err_file=$(mktemp)
    expected_file=$(mktemp)
    printf '%s' "${EXPECTED[$i]}" > "$expected_file"
    if ! printf '%s\n' "${STDIN[$i]}" | bash -c "$run_cmd" >"$out_file" 2>"$err_file"; then
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
    if ! "$zero_bin" run ref.zero "${ARGV[$i]}" >"$out_file" 2>"$err_file"; then
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
      check_stdin rust "./target/release/http_status_code"
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
