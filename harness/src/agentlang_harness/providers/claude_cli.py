"""Shell out to the `claude` CLI in place of the Anthropic Python SDK.

`ClaudeCliClient` mirrors the bit of the SDK the runner uses: a
`.messages.create(model, max_tokens, system, messages, **kwargs)` call
returning an object with `.content` (list of `TextBlock`) and `.usage`
(token counts). The implementation flattens the SDK-style system+messages
input into a single prompt string and runs:

    claude --print --output-format json --model <model> --max-turns 1

The JSON shape returned by `claude --output-format json` in 2.1.x:

    {
      "type": "result",
      "result": "<assistant text>",
      "usage": {
        "input_tokens": int,
        "output_tokens": int,
        "cache_creation_input_tokens": int,
        "cache_read_input_tokens": int,
        ...
      },
      ...
    }

`max_tokens` is accepted but ignored — the CLI does not expose it as of
2.1.117. The runner already budgets prompt size separately.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_CLAUDE_BIN = Path.home() / ".local" / "bin" / "claude"
DEFAULT_TIMEOUT_S = 600.0


@dataclass
class TextBlock:
    type: str
    text: str


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


@dataclass
class ClaudeCliResponse:
    content: list[TextBlock]
    usage: Usage


def _resolve_claude_bin() -> str:
    """Pick the claude binary: env override, $PATH, then DEFAULT_CLAUDE_BIN."""
    override = os.environ.get("CLAUDE_BIN")
    if override:
        return override
    on_path = shutil.which("claude")
    if on_path:
        return on_path
    return str(DEFAULT_CLAUDE_BIN)


def _system_block_text(block: Any) -> str:
    """Read text out of a SDK-style system block (dict or text-attr object)."""
    if isinstance(block, dict):
        if block.get("type") == "text":
            return str(block.get("text", ""))
        return str(block.get("text", ""))
    text = getattr(block, "text", None)
    if text is not None:
        return str(text)
    return ""


def _message_text(message: dict[str, Any]) -> str:
    """Stitch the text from a SDK-style {role, content: [{type,text}]} turn."""
    content = message.get("content", [])
    if isinstance(content, str):
        return content
    parts: list[str] = []
    for block in content:
        if isinstance(block, dict):
            if block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        else:
            text = getattr(block, "text", None)
            if text is not None:
                parts.append(str(text))
    return "".join(parts)


def flatten_prompt(
    system: list[Any] | None, messages: list[dict[str, Any]]
) -> str:
    """Collapse SDK system+messages into a single CLI prompt string.

    System blocks (with cache_control stripped — the CLI does not expose
    it) are joined with blank lines and prefixed at the top. User and
    assistant turns are labeled `User:` / `Assistant:` so the model sees
    the conversation shape even though it lands as one prompt.
    """
    parts: list[str] = []
    if system:
        sys_chunks = [_system_block_text(b) for b in system]
        sys_chunks = [c for c in sys_chunks if c]
        if sys_chunks:
            parts.append("\n\n".join(sys_chunks))
    turns: list[str] = []
    for msg in messages:
        role = str(msg.get("role", "user"))
        label = "Assistant" if role == "assistant" else "User"
        text = _message_text(msg)
        turns.append(f"{label}:\n{text}")
    if turns:
        parts.append("\n\n".join(turns))
    return "\n\n".join(parts)


@dataclass
class ClaudeCliMessages:
    """Mirror of `anthropic.resources.Messages` shape used by the runner."""

    bin_path: str
    timeout_s: float = DEFAULT_TIMEOUT_S

    def create(
        self,
        *,
        model: str,
        max_tokens: int = 0,  # noqa: ARG002 — accepted for SDK parity, unused by CLI
        system: list[Any] | None = None,
        messages: list[dict[str, Any]] | None = None,
        **kwargs: Any,  # noqa: ARG002 — swallow any SDK-only kwargs callers pass
    ) -> ClaudeCliResponse:
        prompt = flatten_prompt(system or [], messages or [])
        argv = [
            self.bin_path,
            "--print",
            "--output-format",
            "json",
            "--model",
            model,
            "--max-turns",
            "1",
        ]
        try:
            completed = subprocess.run(
                argv,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(f"claude CLI invocation failed: {e}") from e
        if completed.returncode != 0:
            tail = (completed.stderr or completed.stdout or "").strip()[-2000:]
            raise RuntimeError(
                f"claude CLI exited {completed.returncode}: {tail}"
            )
        stdout = completed.stdout or ""
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as e:
            tail = stdout.strip()[-2000:]
            raise RuntimeError(
                f"claude CLI returned non-JSON output: {e}: {tail}"
            ) from e
        result_text = payload.get("result")
        if not isinstance(result_text, str):
            raise RuntimeError(
                f"claude CLI JSON missing string `result`: keys={sorted(payload)}"
            )
        usage_payload = payload.get("usage") or {}
        usage = Usage(
            input_tokens=int(usage_payload.get("input_tokens", 0) or 0),
            output_tokens=int(usage_payload.get("output_tokens", 0) or 0),
            cache_creation_input_tokens=int(
                usage_payload.get("cache_creation_input_tokens", 0) or 0
            ),
            cache_read_input_tokens=int(
                usage_payload.get("cache_read_input_tokens", 0) or 0
            ),
        )
        return ClaudeCliResponse(
            content=[TextBlock(type="text", text=result_text)],
            usage=usage,
        )


@dataclass
class ClaudeCliClient:
    """SDK-shaped client that drives the `claude` CLI via subprocess."""

    bin_path: str = field(default_factory=_resolve_claude_bin)
    timeout_s: float = DEFAULT_TIMEOUT_S
    messages: ClaudeCliMessages = field(init=False)

    def __post_init__(self) -> None:
        self.messages = ClaudeCliMessages(
            bin_path=self.bin_path, timeout_s=self.timeout_s
        )
