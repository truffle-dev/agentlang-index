"""Unit tests for the agent-loop runner with a mock Anthropic client."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from agentlang_harness.agent_loop import AgentLoopRunner
from agentlang_harness.prompt import scaffold_for
from agentlang_harness.storage.sqlite import Storage
from agentlang_harness.types import VerifierOutcome

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = REPO_ROOT / "corpus"

GOOD_PYTHON = "```python\nimport sys\nsys.stdout.write('hello\\n')\n```\n"
BAD_PYTHON = "```python\nimport sys\nsys.stdout.write('goodbye\\n')\n```\n"


@dataclass
class _FakeUsage:
    input_tokens: int = 100
    output_tokens: int = 50


@dataclass
class _FakeBlock:
    type: str
    text: str


@dataclass
class _FakeResponse:
    content: list[_FakeBlock]
    usage: _FakeUsage


class _ScriptedMessages:
    """Returns a sequence of canned responses for the matching language."""

    def __init__(self, payloads_for_lang: dict[str, list[str]]) -> None:
        self._payloads = payloads_for_lang
        self._cursor: dict[str, int] = {lang: 0 for lang in payloads_for_lang}
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls.append(kwargs)
        user_text = kwargs["messages"][0]["content"][0]["text"]
        match: str | None = None
        for lang in self._payloads:
            head = scaffold_for(lang).split(".")[0]  # type: ignore[arg-type]
            if head in user_text:
                match = lang
                break
        if match is None:
            match = next(iter(self._payloads))
        payloads = self._payloads[match]
        idx = min(self._cursor[match], len(payloads) - 1)
        self._cursor[match] += 1
        return _FakeResponse([_FakeBlock("text", payloads[idx])], _FakeUsage())


class _ScriptedAnthropic:
    def __init__(self, payloads_for_lang: dict[str, list[str]]) -> None:
        self.messages = _ScriptedMessages(payloads_for_lang)


def _make_runner(client: Any, store: Storage, *, max_iters: int) -> AgentLoopRunner:
    return AgentLoopRunner(
        storage=store,
        client=client,
        corpus_dir=CORPUS_DIR,
        zero_vendor_dir=None,
        zero_binary=None,
        max_iters=max_iters,
    )


def test_agent_loop_passes_first_try_records_one_iteration(tmp_path: Path) -> None:
    client = _ScriptedAnthropic({"python": [GOOD_PYTHON]})
    with Storage(tmp_path / "runs.db") as store:
        run_id = store.start_run(model="fake", corpus_sha="t", mode="agent_loop")
        runner = _make_runner(client, store, max_iters=5)
        result = runner.run_attempt("000-hello-stdout", "python", run_id=run_id)
        assert result.passed is True
        assert result.metadata["iterations"] == 1
        assert result.metadata["per_iter_passed"] == [True]
        assert result.metadata["per_iter_exit_codes"] == [0]
        # Mock client got exactly one call.
        assert len(client.messages.calls) == 1
        rows = store.attempts_for_run(run_id)
        assert len(rows) == 1
        assert rows[0]["passed"] == 1
        assert "---SEP---" in rows[0]["response"]


def test_agent_loop_recovers_on_second_iteration(tmp_path: Path) -> None:
    client = _ScriptedAnthropic({"python": [BAD_PYTHON, GOOD_PYTHON]})
    with Storage(tmp_path / "runs.db") as store:
        run_id = store.start_run(model="fake", corpus_sha="t", mode="agent_loop")
        runner = _make_runner(client, store, max_iters=5)
        result = runner.run_attempt("000-hello-stdout", "python", run_id=run_id)
        assert result.passed is True
        assert result.metadata["iterations"] == 2
        assert result.metadata["per_iter_passed"] == [False, True]
        assert result.metadata["per_iter_exit_codes"][-1] == 0
        assert len(client.messages.calls) == 2
        # Second call must carry assistant + followup-user turns appended.
        second_messages = client.messages.calls[1]["messages"]
        assert len(second_messages) == 3
        assert second_messages[1]["role"] == "assistant"
        assert second_messages[2]["role"] == "user"
        followup_text = second_messages[2]["content"][0]["text"]
        assert "verifier exit code" in followup_text
        assert "verifier stderr" in followup_text


def test_agent_loop_exhausts_max_iters_and_fails(tmp_path: Path) -> None:
    client = _ScriptedAnthropic({"python": [BAD_PYTHON]})
    with Storage(tmp_path / "runs.db") as store:
        run_id = store.start_run(model="fake", corpus_sha="t", mode="agent_loop")
        runner = _make_runner(client, store, max_iters=3)
        result = runner.run_attempt("000-hello-stdout", "python", run_id=run_id)
        assert result.passed is False
        assert result.metadata["iterations"] == 3
        assert result.metadata["per_iter_passed"] == [False, False, False]
        assert len(client.messages.calls) == 3
        # Persisted: one row, the FINAL iteration's verifier outcome.
        rows = store.attempts_for_run(run_id)
        assert len(rows) == 1
        assert rows[0]["passed"] == 0


def test_build_followup_user_turn_zero_includes_json_sections() -> None:
    runner = AgentLoopRunner(
        storage=None,  # type: ignore[arg-type]
        client=None,  # type: ignore[arg-type]
        corpus_dir=CORPUS_DIR,
    )
    verifier = VerifierOutcome(stdout="", stderr="boom", exit_code=1, wall_time_ms=10)
    turn = runner.build_followup_user_turn(
        "zero", verifier, '{"ok": false}', '{"plan": []}'
    )
    assert turn["role"] == "user"
    text = turn["content"][0]["text"]
    assert "zero check --json" in text
    assert "zero fix --plan --json" in text
    assert "ref.zero" in text
    assert "```zero```" in text
    assert "verifier exit code" in text
    assert "1" in text


def test_build_followup_user_turn_non_zero_omits_zero_sections() -> None:
    runner = AgentLoopRunner(
        storage=None,  # type: ignore[arg-type]
        client=None,  # type: ignore[arg-type]
        corpus_dir=CORPUS_DIR,
    )
    verifier = VerifierOutcome(stdout="", stderr="boom", exit_code=1, wall_time_ms=10)
    turn = runner.build_followup_user_turn("python", verifier, None, None)
    text = turn["content"][0]["text"]
    assert "zero check --json" not in text
    assert "zero fix --plan --json" not in text
    assert "ref.py" in text
    assert "```python```" in text
