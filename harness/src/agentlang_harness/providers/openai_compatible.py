"""Drive any OpenAI-compatible `/chat/completions` endpoint over HTTP.

A single adapter covers every backend that speaks the OpenAI chat schema:
hosted DeepSeek, Together, Fireworks, and Groq, plus a local Ollama server
(`/v1/chat/completions`). It mirrors the slice of the Anthropic SDK the
runner uses: a `.messages.create(model, max_tokens, system, messages,
**kwargs)` call returning an object with `.content` (list of `TextBlock`)
and `.usage` (token counts).

Configuration is read from the environment at construction, so the
zero-argument factory in `providers/__init__.py` stays uniform:

    OPENAI_COMPAT_BASE_URL   required, e.g. https://api.deepseek.com/v1
                             or http://ollama:11434/v1 for a local server
    OPENAI_COMPAT_API_KEY    optional; sent as `Authorization: Bearer ...`
                             when present. Local servers (Ollama) need none.

Only stdlib `urllib` is used, so the harness gains no dependency and the
key is read at call time, never logged.

The OpenAI chat-completions response shape consumed here:

    {
      "choices": [{"message": {"role": "assistant", "content": "<text>"}}],
      "usage": {"prompt_tokens": int, "completion_tokens": int, ...}
    }
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

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
class OpenAICompatibleResponse:
    content: list[TextBlock]
    usage: Usage


def _system_block_text(block: Any) -> str:
    """Read text out of a SDK-style system block (dict or text-attr object)."""
    if isinstance(block, dict):
        return str(block.get("text", ""))
    text = getattr(block, "text", None)
    return str(text) if text is not None else ""


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


def to_chat_messages(
    system: list[Any] | None, messages: list[dict[str, Any]]
) -> list[dict[str, str]]:
    """Map SDK system+messages into the OpenAI chat `messages` array.

    System blocks collapse into a single leading `system` message; each
    SDK turn becomes one OpenAI turn with its text content flattened.
    """
    chat: list[dict[str, str]] = []
    if system:
        sys_chunks = [t for t in (_system_block_text(b) for b in system) if t]
        if sys_chunks:
            chat.append({"role": "system", "content": "\n\n".join(sys_chunks)})
    for msg in messages:
        role = str(msg.get("role", "user"))
        if role not in ("user", "assistant", "system"):
            role = "user"
        chat.append({"role": role, "content": _message_text(msg)})
    return chat


def _resolve_base_url(base_url: str | None) -> str:
    resolved = base_url or os.environ.get("OPENAI_COMPAT_BASE_URL")
    if not resolved:
        raise ValueError(
            "OpenAI-compatible provider needs a base URL; set "
            "OPENAI_COMPAT_BASE_URL (e.g. https://api.deepseek.com/v1 or "
            "http://ollama:11434/v1)"
        )
    return resolved.rstrip("/")


@dataclass
class OpenAICompatibleMessages:
    """Mirror of `anthropic.resources.Messages` over an HTTP chat endpoint."""

    base_url: str
    api_key: str | None = None
    timeout_s: float = DEFAULT_TIMEOUT_S

    def create(
        self,
        *,
        model: str,
        max_tokens: int = 0,
        system: list[Any] | None = None,
        messages: list[dict[str, Any]] | None = None,
        **kwargs: Any,  # noqa: ARG002 — swallow SDK-only kwargs callers pass
    ) -> OpenAICompatibleResponse:
        chat_messages = to_chat_messages(system or [], messages or [])
        body: dict[str, Any] = {"model": model, "messages": chat_messages}
        if max_tokens and max_tokens > 0:
            body["max_tokens"] = max_tokens
        data = json.dumps(body).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            tail = (e.read().decode("utf-8", "replace") or "").strip()[-2000:]
            raise RuntimeError(
                f"chat endpoint returned HTTP {e.code}: {tail}"
            ) from e
        except (urllib.error.URLError, OSError) as e:
            raise RuntimeError(f"chat endpoint request failed: {e}") from e
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"chat endpoint returned non-JSON output: {e}: "
                f"{raw.strip()[-2000:]}"
            ) from e
        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError(
                f"chat endpoint JSON missing `choices`: keys={sorted(payload)}"
            )
        message = choices[0].get("message") or {}
        text = message.get("content")
        if not isinstance(text, str):
            raise RuntimeError(
                "chat endpoint first choice missing string `message.content`"
            )
        usage_payload = payload.get("usage") or {}
        usage = Usage(
            input_tokens=int(usage_payload.get("prompt_tokens", 0) or 0),
            output_tokens=int(usage_payload.get("completion_tokens", 0) or 0),
        )
        return OpenAICompatibleResponse(
            content=[TextBlock(type="text", text=text)],
            usage=usage,
        )


@dataclass
class OpenAICompatibleClient:
    """SDK-shaped client for any OpenAI-compatible chat endpoint.

    Reads `OPENAI_COMPAT_BASE_URL` and optional `OPENAI_COMPAT_API_KEY` from
    the environment unless passed explicitly. Construction does not touch the
    network, so the zero-argument factory can register without a live server.
    """

    base_url: str | None = None
    api_key: str | None = None
    timeout_s: float = DEFAULT_TIMEOUT_S
    messages: OpenAICompatibleMessages = field(init=False)

    def __post_init__(self) -> None:
        resolved_url = _resolve_base_url(self.base_url)
        resolved_key = self.api_key or os.environ.get("OPENAI_COMPAT_API_KEY")
        self.messages = OpenAICompatibleMessages(
            base_url=resolved_url,
            api_key=resolved_key,
            timeout_s=self.timeout_s,
        )
