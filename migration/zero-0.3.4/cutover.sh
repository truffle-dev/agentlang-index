#!/usr/bin/env bash
# Perform the shimless 0.1.2 -> 0.3.4 corpus cutover on a target corpus tree.
#
# Unlike verify-batch.sh (which proves the source PORT recipe by bridging the
# old `zero run ref.zero` call through zero-graph-shim.sh), this script writes
# the production end-state: the corpus invokes the real 0.3.4 binary the way the
# 0.3.4 docs say to, with NO shim in the loop.
#
# For each task it:
#   single-file (has ref.zero):
#     1. rename ref.zero -> ref.0 and port it through port_ref.py
#     2. inject a one-time `zero import ref.0 --out ref.graph` after the
#        `if [[ -x "$ZERO" ]]; then` anchor in verify.sh
#     3. rewrite the run command `run ref.zero` -> `run ref.graph` (code only,
#        comments left intact)
#   package (has zero/ dir, verify.sh uses `run zero --`):
#     1. port every zero/src/*.0 in place (passing all siblings)
#     2. inject a one-time `zero import zero` after the anchor; the
#        `run zero -- ARGS` directory call is already correct for 0.3.4
#
# It does NOT touch CI (.github/workflows/verify-refs.yml) or bench/runner.ts;
# those are the other two halves of the cutover commit. It only migrates the
# corpus sources + their verify.sh drivers.
#
# Usage:
#   cutover.sh [TARGET_CORPUS_DIR]
# With no argument it copies the repo's live corpus/ into a temp dir, migrates
# the copy, and leaves the live tree untouched (the safe default for proving the
# cutover). Pass an explicit dir (e.g. the live corpus/) to migrate in place.
#
# Requires: python3, the port_ref.py next to this script.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PORT="$HERE/port_ref.py"

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  TARGET="$(mktemp -d)/corpus"
  cp -r "$REPO/corpus" "$TARGET"
  echo "no target given; migrating a temp copy at: $TARGET"
fi

if [[ ! -d "$TARGET" ]]; then
  echo "cutover.sh: target corpus dir not found: $TARGET" >&2
  exit 2
fi

# Inject a guarded one-time import immediately after the anchor line.
inject_import() {
  local verify="$1" import_cmd="$2"
  awk -v cmd="$import_cmd" '
    { print }
    /^[[:space:]]*if \[\[ -x "\$ZERO" \]\]; then$/ && !done {
      print "    " cmd
      done = 1
    }
  ' "$verify" > "$verify.tmp" && mv "$verify.tmp" "$verify"
}

# Swap the run command on code lines only (leave comments untouched).
swap_run() {
  local verify="$1"
  awk '
    /^[[:space:]]*#/ { print; next }       # comment line: leave as-is
    { gsub(/run ref\.zero/, "run ref.graph"); print }
  ' "$verify" > "$verify.tmp" && mv "$verify.tmp" "$verify"
}

migrate_single() {
  local dir="$1" verify="$dir/verify.sh"
  python3 "$PORT" < "$dir/ref.zero" > "$dir/ref.0" 2>"$dir/.unhandled"
  if [[ -s "$dir/.unhandled" ]]; then
    echo "  WARN unhandled inferred lets:"; sed 's/^/    /' "$dir/.unhandled"
  fi
  rm -f "$dir/.unhandled" "$dir/ref.zero"
  inject_import "$verify" '"$ZERO" import ref.0 --out ref.graph >/dev/null 2>&1 || { echo "FAIL: zero (import ref.0)"; EXIT=1; }'
  swap_run "$verify"
}

migrate_package() {
  local dir="$1" verify="$dir/verify.sh"
  local siblings=("$dir"/zero/src/*.0)
  local f
  for f in "${siblings[@]}"; do
    [[ -f "$f" ]] || continue
    python3 "$PORT" "${siblings[@]}" < "$f" > "$f.ported" 2>"$dir/.unhandled"
    if [[ -s "$dir/.unhandled" ]]; then
      echo "  WARN $(basename "$f") unhandled inferred lets:"; sed 's/^/    /' "$dir/.unhandled"
    fi
    mv "$f.ported" "$f"
  done
  rm -f "$dir/.unhandled"
  inject_import "$verify" '"$ZERO" import zero >/dev/null 2>&1 || { echo "FAIL: zero (import zero)"; EXIT=1; }'
}

for dir in "$TARGET"/0*/; do
  t="$(basename "$dir")"
  [[ -f "$dir/verify.sh" ]] || { echo "SKIP $t (no verify.sh)"; continue; }
  if [[ -f "$dir/ref.zero" ]]; then
    echo "single  $t"
    migrate_single "$dir"
  elif [[ -d "$dir/zero" ]]; then
    echo "package $t"
    migrate_package "$dir"
  else
    echo "SKIP $t (no ref.zero, no zero/ package)"
  fi
done

echo "cutover written to: $TARGET"
