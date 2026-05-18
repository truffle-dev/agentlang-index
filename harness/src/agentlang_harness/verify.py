"""Invoke a corpus task's verify.sh and capture the result."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from .types import Language, VerifierOutcome

# Generous default: a verifier may compile rustc, run go, spin up zero, etc.
DEFAULT_TIMEOUT_S = 60.0


def run_verifier(
    scratch_dir: Path, language: Language, *, timeout_s: float = DEFAULT_TIMEOUT_S
) -> VerifierOutcome:
    """Run `bash verify.sh --lang <language>` in `scratch_dir`."""
    verifier = scratch_dir / "verify.sh"
    if not verifier.exists():
        raise FileNotFoundError(f"verify.sh missing in scratch dir {scratch_dir}")
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["bash", str(verifier), "--lang", language],
            cwd=str(scratch_dir),
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        wall_ms = int((time.monotonic() - started) * 1000)
        return VerifierOutcome(
            stdout=completed.stdout,
            stderr=completed.stderr,
            exit_code=completed.returncode,
            wall_time_ms=wall_ms,
        )
    except subprocess.TimeoutExpired as e:
        wall_ms = int((time.monotonic() - started) * 1000)
        return VerifierOutcome(
            stdout=e.stdout.decode("utf-8", errors="replace") if e.stdout else "",
            stderr=(e.stderr.decode("utf-8", errors="replace") if e.stderr else "")
            + f"\n[harness: verifier timeout after {timeout_s}s]\n",
            exit_code=124,
            wall_time_ms=wall_ms,
        )
