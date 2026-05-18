"""Tests that exercise verify.sh end-to-end through the verify module."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentlang_harness.runner import verify_local_source

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = REPO_ROOT / "corpus"


def test_verify_python_reference_for_hello_stdout() -> None:
    """The corpus's own Python reference passes its own verifier."""
    ref = CORPUS_DIR / "000-hello-stdout" / "ref.py"
    outcome = verify_local_source(CORPUS_DIR, "000-hello-stdout", "python", ref)
    assert outcome.exit_code == 0, outcome.stdout + outcome.stderr
    assert "PASS: python" in outcome.stdout


def test_verify_python_with_wrong_output_fails(tmp_path: Path) -> None:
    """A wrong-output Python source is correctly flagged FAIL."""
    bad = tmp_path / "bad.py"
    bad.write_text("import sys\nsys.stdout.write('goodbye\\n')\n", encoding="utf-8")
    outcome = verify_local_source(CORPUS_DIR, "000-hello-stdout", "python", bad)
    assert outcome.exit_code != 0
    assert "FAIL: python" in outcome.stdout


def test_verify_fibonacci_python_reference_runs_all_cases() -> None:
    """Task 001's Python reference clears all five test cases (incl. N=50)."""
    ref = CORPUS_DIR / "001-fibonacci-memoized" / "ref.py"
    outcome = verify_local_source(CORPUS_DIR, "001-fibonacci-memoized", "python", ref)
    assert outcome.exit_code == 0, outcome.stdout + outcome.stderr
    assert "PASS: python" in outcome.stdout


def test_verify_only_runs_target_language(tmp_path: Path) -> None:
    """`--lang python` does not invoke the Zero, Rust, Go, or TS sub-blocks."""
    ref = CORPUS_DIR / "000-hello-stdout" / "ref.py"
    outcome = verify_local_source(CORPUS_DIR, "000-hello-stdout", "python", ref)
    # Only the python lane reports.
    assert "PASS: python" in outcome.stdout
    for other in ("zero", "ts", "rust", "go"):
        assert f"PASS: {other}" not in outcome.stdout
        assert f"SKIP: {other}" not in outcome.stdout
        assert f"FAIL: {other}" not in outcome.stdout
