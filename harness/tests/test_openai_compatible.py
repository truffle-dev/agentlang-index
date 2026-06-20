"""Tests for the OpenAI-compatible provider adapter.

The unit tests are hermetic: they stub `urllib.request.urlopen` so no
network is touched. One opt-in smoke test runs against a real local Ollama
server when `AGENTLANG_LIVE_OPENAI_COMPAT_URL` points at one; it is skipped
otherwise, so CI stays offline.
"""

from __future__ import annotations

import io
import json
import os
import urllib.error
import urllib.request

import pytest

from agentlang_harness.providers import make_client
from agentlang_harness.providers.openai_compatible import (
    OpenAICompatibleClient,
    TextBlock,
    to_chat_messages,
)


def _system_blocks(*texts: str) -> list[dict[str, str]]:
    return [{"type": "text", "text": t} for t in texts]


def _user_turn(text: str) -> dict[str, object]:
    return {"role": "user", "content": [{"type": "text", "text": text}]}


def test_to_chat_messages_leads_with_one_system_message() -> None:
    chat = to_chat_messages(
        _system_blocks("be terse", "use python"), [_user_turn("solve it")]
    )
    assert chat[0] == {"role": "system", "content": "be terse\n\nuse python"}
    assert chat[1] == {"role": "user", "content": "solve it"}


def test_to_chat_messages_omits_system_when_no_blocks() -> None:
    chat = to_chat_messages([], [_user_turn("hi")])
    assert chat == [{"role": "user", "content": "hi"}]


def test_to_chat_messages_normalizes_unknown_roles_to_user() -> None:
    chat = to_chat_messages([], [{"role": "tool", "content": "x"}])
    assert chat == [{"role": "user", "content": "x"}]


def test_client_requires_a_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_COMPAT_BASE_URL", raising=False)
    with pytest.raises(ValueError) as excinfo:
        OpenAICompatibleClient()
    assert "OPENAI_COMPAT_BASE_URL" in str(excinfo.value)


def test_client_reads_base_url_and_key_from_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_COMPAT_BASE_URL", "https://api.example.com/v1/")
    monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "secret-token")
    client = OpenAICompatibleClient()
    # The trailing slash is stripped so request URLs join cleanly.
    assert client.messages.base_url == "https://api.example.com/v1"
    assert client.messages.api_key == "secret-token"


def _stub_urlopen(captured: dict[str, object], response_payload: dict[str, object]):
    def fake_urlopen(request, timeout=None):  # noqa: ANN001, ANN202
        captured["url"] = request.full_url
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        body = json.dumps(response_payload).encode("utf-8")

        class _Resp(io.BytesIO):
            def __enter__(self):  # noqa: ANN204
                return self

            def __exit__(self, *exc):  # noqa: ANN002, ANN204
                self.close()
                return False

        return _Resp(body)

    return fake_urlopen


def test_create_posts_chat_and_maps_usage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    payload = {
        "choices": [{"message": {"role": "assistant", "content": "def f(): ..."}}],
        "usage": {"prompt_tokens": 24, "completion_tokens": 7},
    }
    monkeypatch.setattr(
        urllib.request, "urlopen", _stub_urlopen(captured, payload)
    )
    client = OpenAICompatibleClient(
        base_url="https://api.example.com/v1", api_key="k"
    )
    response = client.messages.create(
        model="some-model",
        max_tokens=128,
        system=_system_blocks("sys"),
        messages=[_user_turn("write f")],
    )
    assert captured["url"] == "https://api.example.com/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer k"
    body = captured["body"]
    assert body["model"] == "some-model"
    assert body["max_tokens"] == 128
    assert body["messages"][0] == {"role": "system", "content": "sys"}
    assert response.content == [TextBlock(type="text", text="def f(): ...")]
    assert response.usage.input_tokens == 24
    assert response.usage.output_tokens == 7


def test_create_omits_authorization_without_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    payload = {
        "choices": [{"message": {"role": "assistant", "content": "ok"}}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1},
    }
    monkeypatch.setattr(
        urllib.request, "urlopen", _stub_urlopen(captured, payload)
    )
    client = OpenAICompatibleClient(base_url="http://ollama:11434/v1")
    client.messages.create(model="m", messages=[_user_turn("hi")])
    assert "Authorization" not in captured["headers"]


def test_create_raises_on_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request, timeout=None):  # noqa: ANN001, ANN202
        raise urllib.error.HTTPError(
            request.full_url, 401, "Unauthorized", {}, io.BytesIO(b"bad key")
        )

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    client = OpenAICompatibleClient(base_url="https://api.example.com/v1")
    with pytest.raises(RuntimeError) as excinfo:
        client.messages.create(model="m", messages=[_user_turn("hi")])
    assert "HTTP 401" in str(excinfo.value)


def test_create_raises_when_choices_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setattr(
        urllib.request, "urlopen", _stub_urlopen(captured, {"error": "nope"})
    )
    client = OpenAICompatibleClient(base_url="https://api.example.com/v1")
    with pytest.raises(RuntimeError) as excinfo:
        client.messages.create(model="m", messages=[_user_turn("hi")])
    assert "choices" in str(excinfo.value)


def test_make_client_builds_openai_compatible(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_COMPAT_BASE_URL", "http://ollama:11434/v1")
    monkeypatch.delenv("OPENAI_COMPAT_API_KEY", raising=False)
    client = make_client("openai-compatible")
    assert isinstance(client, OpenAICompatibleClient)


@pytest.mark.skipif(
    not os.environ.get("AGENTLANG_LIVE_OPENAI_COMPAT_URL"),
    reason="set AGENTLANG_LIVE_OPENAI_COMPAT_URL to run the live smoke test",
)
def test_live_smoke_against_real_endpoint() -> None:
    """Round-trip a real request when a live endpoint is configured.

    Reads the base URL from AGENTLANG_LIVE_OPENAI_COMPAT_URL, the model from
    AGENTLANG_LIVE_OPENAI_COMPAT_MODEL, and an optional key from
    OPENAI_COMPAT_API_KEY. Kept out of CI by the skipif guard.
    """
    base_url = os.environ["AGENTLANG_LIVE_OPENAI_COMPAT_URL"]
    model = os.environ.get(
        "AGENTLANG_LIVE_OPENAI_COMPAT_MODEL", "qwen2.5-coder:0.5b"
    )
    client = OpenAICompatibleClient(base_url=base_url)
    response = client.messages.create(
        model=model,
        max_tokens=16,
        system=_system_blocks("You are terse."),
        messages=[_user_turn("Reply with the single word: ready")],
    )
    assert response.content
    assert response.content[0].text.strip()
    assert response.usage.input_tokens > 0
