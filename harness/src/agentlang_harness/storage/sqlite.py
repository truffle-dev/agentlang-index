"""SQLite-backed storage for AgentLang Index benchmark runs.

Schema v1: two tables.

    runs            — one row per harness invocation. Identifies the
                      model under test, the corpus snapshot, the mode
                      (one_shot or agent_loop), and the wall-clock
                      timeline of the run.

    task_attempts   — one row per (run, task, language) attempt. Stores
                      the prompt, the model response, the verifier
                      stdout/stderr/exit-code/wall-time, and whether
                      the attempt passed the hidden test cases.

The schema version is stored in SQLite's PRAGMA user_version. The
constructor compares it against SCHEMA_VERSION and upgrades by running
the diff between the recorded version and the current target. v1 is
the initial cut; future bumps will append to _MIGRATIONS.

All write paths use parameterized queries. Foreign keys are enabled
(PRAGMA foreign_keys = ON) so deleting a run cascades its attempts.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def _utcnow_iso() -> str:
    """ISO-8601 UTC timestamp with second precision, suffixed `Z`."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_MIGRATIONS: dict[int, list[str]] = {
    1: [
        """
        CREATE TABLE runs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            model           TEXT    NOT NULL,
            corpus_sha      TEXT    NOT NULL,
            mode            TEXT    NOT NULL CHECK (mode IN ('one_shot', 'agent_loop')),
            started_at      TEXT    NOT NULL,
            finished_at     TEXT,
            status          TEXT    NOT NULL DEFAULT 'in_progress'
                                    CHECK (status IN ('in_progress', 'completed', 'failed')),
            metadata_json   TEXT    NOT NULL DEFAULT '{}'
        )
        """,
        """
        CREATE TABLE task_attempts (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id              INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
            task_slug           TEXT    NOT NULL,
            language            TEXT    NOT NULL,
            prompt              TEXT    NOT NULL,
            response            TEXT    NOT NULL,
            verifier_stdout     TEXT    NOT NULL DEFAULT '',
            verifier_stderr     TEXT    NOT NULL DEFAULT '',
            verifier_exit_code  INTEGER NOT NULL,
            wall_time_ms        INTEGER NOT NULL,
            passed              INTEGER NOT NULL CHECK (passed IN (0, 1)),
            recorded_at         TEXT    NOT NULL,
            UNIQUE (run_id, task_slug, language)
        )
        """,
        "CREATE INDEX idx_task_attempts_run_id ON task_attempts(run_id)",
        "CREATE INDEX idx_runs_model ON runs(model)",
    ],
}


class Storage:
    """Thin SQLite wrapper for harness runs and per-task attempts.

    Usage:
        store = Storage("runs.db")
        run_id = store.start_run(model="claude-opus-4-7",
                                 corpus_sha="abc123",
                                 mode="one_shot")
        store.record_attempt(run_id=run_id,
                             task_slug="000-hello-stdout",
                             language="zero",
                             prompt="...",
                             response="...",
                             verifier_stdout="hello\\n",
                             verifier_stderr="",
                             verifier_exit_code=0,
                             wall_time_ms=42,
                             passed=True)
        store.finish_run(run_id, status="completed")
        store.close()
    """

    def __init__(self, db_path: str | Path) -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._path))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._migrate()

    # ------------------------------------------------------------------
    # schema management
    # ------------------------------------------------------------------

    def _migrate(self) -> None:
        current = self._conn.execute("PRAGMA user_version").fetchone()[0]
        if current > SCHEMA_VERSION:
            raise RuntimeError(
                f"database schema version {current} is newer than this "
                f"client (max {SCHEMA_VERSION}); upgrade agentlang-harness"
            )
        for version in range(current + 1, SCHEMA_VERSION + 1):
            statements = _MIGRATIONS.get(version)
            if statements is None:
                raise RuntimeError(f"missing migration for schema version {version}")
            with self._conn:
                for stmt in statements:
                    self._conn.execute(stmt)
                self._conn.execute(f"PRAGMA user_version = {version}")

    @property
    def schema_version(self) -> int:
        return self._conn.execute("PRAGMA user_version").fetchone()[0]

    # ------------------------------------------------------------------
    # runs
    # ------------------------------------------------------------------

    def start_run(
        self,
        *,
        model: str,
        corpus_sha: str,
        mode: str,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """Insert a new run row in `in_progress` status. Returns its id."""
        if mode not in {"one_shot", "agent_loop"}:
            raise ValueError(f"mode must be one_shot or agent_loop, got {mode!r}")
        meta_json = json.dumps(metadata or {}, sort_keys=True)
        with self._conn:
            cur = self._conn.execute(
                "INSERT INTO runs (model, corpus_sha, mode, started_at, metadata_json) "
                "VALUES (?, ?, ?, ?, ?)",
                (model, corpus_sha, mode, _utcnow_iso(), meta_json),
            )
        return int(cur.lastrowid)

    def finish_run(self, run_id: int, *, status: str = "completed") -> None:
        """Stamp the run as completed or failed."""
        if status not in {"completed", "failed"}:
            raise ValueError(f"status must be completed or failed, got {status!r}")
        with self._conn:
            cur = self._conn.execute(
                "UPDATE runs SET finished_at = ?, status = ? WHERE id = ?",
                (_utcnow_iso(), status, run_id),
            )
            if cur.rowcount == 0:
                raise KeyError(f"no run with id {run_id}")

    def get_run(self, run_id: int) -> dict[str, Any] | None:
        row = self._conn.execute(
            "SELECT * FROM runs WHERE id = ?", (run_id,)
        ).fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # attempts
    # ------------------------------------------------------------------

    def record_attempt(
        self,
        *,
        run_id: int,
        task_slug: str,
        language: str,
        prompt: str,
        response: str,
        verifier_stdout: str,
        verifier_stderr: str,
        verifier_exit_code: int,
        wall_time_ms: int,
        passed: bool,
    ) -> int:
        """Insert a per-task attempt row. Returns its id.

        Uniqueness is enforced on (run_id, task_slug, language); a second
        attempt for the same triple raises sqlite3.IntegrityError.
        """
        with self._conn:
            cur = self._conn.execute(
                "INSERT INTO task_attempts ("
                "run_id, task_slug, language, prompt, response, "
                "verifier_stdout, verifier_stderr, verifier_exit_code, "
                "wall_time_ms, passed, recorded_at"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    run_id,
                    task_slug,
                    language,
                    prompt,
                    response,
                    verifier_stdout,
                    verifier_stderr,
                    int(verifier_exit_code),
                    int(wall_time_ms),
                    1 if passed else 0,
                    _utcnow_iso(),
                ),
            )
        return int(cur.lastrowid)

    def attempts_for_run(self, run_id: int) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT * FROM task_attempts WHERE run_id = ? "
            "ORDER BY task_slug, language",
            (run_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def delete_run(self, run_id: int) -> None:
        """Delete a run and (via ON DELETE CASCADE) its attempts."""
        with self._conn:
            cur = self._conn.execute("DELETE FROM runs WHERE id = ?", (run_id,))
            if cur.rowcount == 0:
                raise KeyError(f"no run with id {run_id}")

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "Storage":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
