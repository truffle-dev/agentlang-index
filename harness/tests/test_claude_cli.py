"""Unit tests for the claude-CLI subprocess provider."""

from __future__ import annotations

import json
import subprocess
from typing import Any

import pytest

from agentlang_harness.providers.claude_cli import (
    ClaudeCliClient,
    ClaudeCliMessages,
    Usage,
    flatten_prompt,
)


def test_flatten_prompt_joins_system_then_messages() -> None:
    """System blocks land first; user/assistant turns get labeled and concatenated."""
    system = [
        {"type": "text", "text": "primer one"},
        {"type": "text", "text": "primer two", "cache_control": {"type": "ephemeral"}},
    ]
    messages = [
        {"role": "user", "content": [{"type": "text", "text": "hello"}]},
        {"role": "assistant", "content": [{"type": "text", "text": "hi there"}]},
        {"role": "user", "content": [{"type": "text", "text": "fix this"}]},
    ]
    prompt = flatten_prompt(system, messages)
    assert "primer one" in prompt
    assert "primer two" in prompt
    # Cache-control marker is metadata, not body text — only `text` makes it in.
    assert "ephemeral" not in prompt
    # The system prefix comes before the first labeled turn.
    assert prompt.index("primer one") < prompt.index("User:")
    # Each turn is labeled and ordered.
    assert "User:\nhello" in prompt
    assert "Assistant:\nhi there" in prompt
    assert "User:\nfix this" in prompt
    assert prompt.index("User:\nhello") < prompt.index("Assistant:\nhi there")
    assert prompt.index("Assistant:\nhi there") < prompt.index("User:\nfix this")


def test_flatten_prompt_handles_empty_system() -> None:
    """No system blocks means the prompt starts with the first labeled turn."""
    messages = [{"role": "user", "content": [{"type": "text", "text": "lone"}]}]
    assert flatten_prompt(None, messages) == "User:\nlone"
    assert flatten_prompt([], messages) == "User:\nlone"


def test_flatten_prompt_accepts_str_content() -> None:
    """If a turn carries a bare string content, it's used as-is."""
    messages = [{"role": "user", "content": "raw"}]
    assert flatten_prompt(None, messages) == "User:\nraw"


def test_messages_create_parses_canned_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    """A successful subprocess returning the documented JSON shape parses cleanly."""
    payload = {
        "type": "result",
        "result": "```python\nprint('hi')\n```\n",
        "usage": {
            "input_tokens": 12,
            "output_tokens": 7,
            "cache_creation_input_tokens": 3,
            "cache_read_input_tokens": 5,
        },
    }
    captured: dict[str, Any] = {}

    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        captured["argv"] = argv
        captured["input"] = kwargs.get("input")
        return subprocess.CompletedProcess(
            args=argv, returncode=0, stdout=json.dumps(payload), stderr=""
        )

    monkeypatch.setattr(
        "agentlang_harness.providers.claude_cli.subprocess.run", fake_run
    )
    msgs = ClaudeCliMessages(bin_path="/fake/claude")
    response = msgs.create(
        model="opus",
        max_tokens=8192,
        system=[{"type": "text", "text": "primer"}],
        messages=[{"role": "user", "content": [{"type": "text", "text": "do x"}]}],
    )
    assert response.content[0].type == "text"
    assert response.content[0].text == "```python\nprint('hi')\n```\n"
    assert isinstance(response.usage, Usage)
    assert response.usage.input_tokens == 12
    assert response.usage.output_tokens == 7
    assert response.usage.cache_creation_input_tokens == 3
    assert response.usage.cache_read_input_tokens == 5
    # The argv carries the documented flags.
    assert captured["argv"][0] == "/fake/claude"
    assert "--print" in captured["argv"]
    assert "--output-format" in captured["argv"]
    assert "json" in captured["argv"]
    assert "--model" in captured["argv"]
    assert "opus" in captured["argv"]
    assert "--max-turns" in captured["argv"]
    # The prompt fed on stdin contains both the system primer and the user turn.
    assert "primer" in captured["input"]
    assert "do x" in captured["input"]


def test_messages_create_nonzero_exit_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """A subprocess failure becomes a RuntimeError carrying the stderr tail."""
    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=argv, returncode=2, stdout="", stderr="auth: not logged in\n"
        )

    monkeypatch.setattr(
        "agentlang_harness.providers.claude_cli.subprocess.run", fake_run
    )
    msgs = ClaudeCliMessages(bin_path="/fake/claude")
    with pytest.raises(RuntimeError) as excinfo:
        msgs.create(
            model="opus",
            max_tokens=0,
            system=None,
            messages=[{"role": "user", "content": [{"type": "text", "text": "x"}]}],
        )
    assert "auth: not logged in" in str(excinfo.value)
    assert "exited 2" in str(excinfo.value)


def test_messages_create_bad_json_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Garbage stdout becomes a RuntimeError, not a JSONDecodeError leak."""
    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=argv, returncode=0, stdout="not json at all", stderr=""
        )

    monkeypatch.setattr(
        "agentlang_harness.providers.claude_cli.subprocess.run", fake_run
    )
    msgs = ClaudeCliMessages(bin_path="/fake/claude")
    with pytest.raises(RuntimeError) as excinfo:
        msgs.create(
            model="opus",
            max_tokens=0,
            system=None,
            messages=[{"role": "user", "content": [{"type": "text", "text": "x"}]}],
        )
    assert "non-JSON" in str(excinfo.value)


def test_messages_create_missing_result_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """JSON that parses but lacks `result` is still a RuntimeError."""
    payload = {"type": "result", "usage": {"input_tokens": 1}}

    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=argv, returncode=0, stdout=json.dumps(payload), stderr=""
        )

    monkeypatch.setattr(
        "agentlang_harness.providers.claude_cli.subprocess.run", fake_run
    )
    msgs = ClaudeCliMessages(bin_path="/fake/claude")
    with pytest.raises(RuntimeError) as excinfo:
        msgs.create(
            model="opus",
            max_tokens=0,
            system=None,
            messages=[{"role": "user", "content": [{"type": "text", "text": "x"}]}],
        )
    assert "missing string `result`" in str(excinfo.value)


def test_client_messages_attribute_shape() -> None:
    """ClaudeCliClient exposes a `.messages.create` callable like the SDK."""
    client = ClaudeCliClient(bin_path="/fake/claude")
    assert isinstance(client.messages, ClaudeCliMessages)
    assert client.messages.bin_path == "/fake/claude"
    assert callable(client.messages.create)
