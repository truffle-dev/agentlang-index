#!/usr/bin/env bash
# Zero 0.3.4 compat shim for the AgentLang Index 0.1.2 verify.sh harness.
# 0.1.2 compiled+ran a source file directly: `zero run ref.zero ARGS`.
# 0.3.4 is graph-based: you must `zero import file.0 --out f.graph` first,
# then `zero run f.graph ARGS`. This shim transparently bridges that so the
# existing per-task verify.sh files run unchanged against ported refs.
set -uo pipefail
REAL="${ZERO_REAL:-$HOME/.local/bin/zero}"

if [[ "${1:-}" == "run" && "${2:-}" == *.zero ]]; then
  src="$2"; shift 2
  # 0.3.4 requires a canonical .0 extension for import; the corpus uses .zero.
  zsrc="$(mktemp --suffix=.0)"
  cp "$src" "$zsrc"
  g="$(mktemp --suffix=.graph)"
  ierr="$(mktemp)"
  if ! "$REAL" import "$zsrc" --out "$g" >/dev/null 2>"$ierr"; then
    cat "$ierr" >&2          # surface import diagnostics on failure
    rm -f "$g" "$ierr" "$zsrc"
    exit 1
  fi
  rm -f "$ierr"              # import succeeded: discard any benign stderr
  "$REAL" run "$g" "$@"
  rc=$?
  rm -f "$g" "$zsrc"
  exit $rc
fi

if [[ "${1:-}" == "run" && -d "${2:-}" ]]; then
  dir="$2"; shift 2
  # Package flow (zero.json + src/main.0 + src/lib.0). 0.3.4 import for a
  # package writes a fixed zero.graph inside the package dir; --out is rejected
  # (RGP002), so we import in place, then run the directory.
  ierr="$(mktemp)"
  if ! "$REAL" import "$dir" >/dev/null 2>"$ierr"; then
    cat "$ierr" >&2          # surface import diagnostics on failure
    rm -f "$ierr"
    exit 1
  fi
  rm -f "$ierr"              # import succeeded: discard any benign stderr
  "$REAL" run "$dir" "$@"
  exit $?
fi

exec "$REAL" "$@"
