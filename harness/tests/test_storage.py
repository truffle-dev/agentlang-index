"""Unit tests for agentlang_harness.storage.sqlite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from agentlang_harness.storage.sqlite import SCHEMA_VERSION, Storage


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "runs.db"


def test_schema_initializes_at_current_version(db_path: Path) -> None:
    """A fresh database is migrated to SCHEMA_VERSION on first open and
    holds the two expected tables."""
    with Storage(db_path) as store:
        assert store.schema_version == SCHEMA_VERSION
        # Both tables exist and parameterized inserts work end-to-end.
        run_id = store.start_run(model="m", corpus_sha="abc", mode="one_shot")
        attempt_id = store.record_attempt(
            run_id=run_id,
            task_slug="000-hello-stdout",
            language="zero",
            prompt="p",
            response="r",
            verifier_stdout="hello\n",
            verifier_stderr="",
            verifier_exit_code=0,
            wall_time_ms=12,
            passed=True,
        )
        assert run_id == 1
        assert attempt_id == 1

    # Re-opening the same file leaves the version stable (idempotent
    # migration) — exercises the upper-bound branch in _migrate.
    with Storage(db_path) as store:
        assert store.schema_version == SCHEMA_VERSION


def test_run_roundtrip_records_start_and_finish(db_path: Path) -> None:
    """start_run → record_attempt → finish_run preserves the data and
    flips status from in_progress to completed."""
    with Storage(db_path) as store:
        run_id = store.start_run(
            model="claude-opus-4-7",
            corpus_sha="deadbeef",
            mode="agent_loop",
            metadata={"seed": 42, "iterations": 3},
        )
        row = store.get_run(run_id)
        assert row is not None
        assert row["model"] == "claude-opus-4-7"
        assert row["corpus_sha"] == "deadbeef"
        assert row["mode"] == "agent_loop"
        assert row["status"] == "in_progress"
        assert row["finished_at"] is None
        # metadata_json is sorted-key JSON; recover via json.loads.
        import json
        assert json.loads(row["metadata_json"]) == {"seed": 42, "iterations": 3}

        store.record_attempt(
            run_id=run_id,
            task_slug="001-fibonacci-memoized",
            language="python",
            prompt="...",
            response="...",
            verifier_stdout="55\n",
            verifier_stderr="",
            verifier_exit_code=0,
            wall_time_ms=80,
            passed=True,
        )
        attempts = store.attempts_for_run(run_id)
        assert len(attempts) == 1
        assert attempts[0]["task_slug"] == "001-fibonacci-memoized"
        assert attempts[0]["language"] == "python"
        assert attempts[0]["passed"] == 1

        store.finish_run(run_id, status="completed")
        row = store.get_run(run_id)
        assert row["status"] == "completed"
        assert row["finished_at"] is not None


def test_duplicate_attempt_rejected_by_unique_constraint(db_path: Path) -> None:
    """A second attempt for the same (run, task, language) triple raises
    IntegrityError — the schema-level guard against double-recording."""
    with Storage(db_path) as store:
        run_id = store.start_run(model="m", corpus_sha="abc", mode="one_shot")
        store.record_attempt(
            run_id=run_id,
            task_slug="000-hello-stdout",
            language="ts",
            prompt="p",
            response="r",
            verifier_stdout="hello\n",
            verifier_stderr="",
            verifier_exit_code=0,
            wall_time_ms=20,
            passed=True,
        )
        with pytest.raises(sqlite3.IntegrityError):
            store.record_attempt(
                run_id=run_id,
                task_slug="000-hello-stdout",
                language="ts",
                prompt="p2",
                response="r2",
                verifier_stdout="hello\n",
                verifier_stderr="",
                verifier_exit_code=0,
                wall_time_ms=21,
                passed=True,
            )


def test_delete_run_cascades_to_attempts(db_path: Path) -> None:
    """Deleting a run removes its attempts via ON DELETE CASCADE,
    confirming foreign_keys = ON is in force."""
    with Storage(db_path) as store:
        run_id = store.start_run(model="m", corpus_sha="abc", mode="one_shot")
        for lang in ("zero", "ts", "rust"):
            store.record_attempt(
                run_id=run_id,
                task_slug="000-hello-stdout",
                language=lang,
                prompt="p",
                response="r",
                verifier_stdout="hello\n",
                verifier_stderr="",
                verifier_exit_code=0,
                wall_time_ms=10,
                passed=True,
            )
        assert len(store.attempts_for_run(run_id)) == 3
        store.delete_run(run_id)
        assert store.get_run(run_id) is None
        assert store.attempts_for_run(run_id) == []
