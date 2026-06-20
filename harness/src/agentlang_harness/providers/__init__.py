"""Model-call providers used by the runner.

The runner depends on the `AnthropicClient` Protocol in `runner.py`:
a `.messages.create(model, max_tokens, system, messages, ...)` callable
returning an object with `.content: list[TextBlock]` and `.usage`. Any
module here that satisfies that shape can drive the harness.

`PROVIDER_FACTORIES` is the single registry that maps a provider name to a
zero-argument factory returning such a client. The CLI's `--provider` flag
selects by name, so adding a second cloud or local provider is "write the
adapter module, register its factory here" with no change to the run verbs.
"""

from __future__ import annotations

from collections.abc import Callable

from .claude_cli import ClaudeCliClient
from .openai_compatible import OpenAICompatibleClient

DEFAULT_PROVIDER = "claude-cli"

# Provider name -> client factory. Each factory returns an object satisfying
# the AnthropicClient Protocol in runner.py. claude-cli is key-free (it shells
# out to the local `claude` CLI). openai-compatible drives any endpoint that
# speaks the OpenAI chat schema (hosted DeepSeek/Together/Fireworks/Groq, or a
# local Ollama server); it reads OPENAI_COMPAT_BASE_URL and an optional
# OPENAI_COMPAT_API_KEY from the environment at construction.
PROVIDER_FACTORIES: dict[str, Callable[[], object]] = {
    "claude-cli": ClaudeCliClient,
    "openai-compatible": OpenAICompatibleClient,
}


def available_providers() -> list[str]:
    """Return the registered provider names, sorted for stable help text."""
    return sorted(PROVIDER_FACTORIES)


def make_client(provider: str) -> object:
    """Construct the model client registered under `provider`.

    Raises ValueError naming the known providers when `provider` is not
    registered, so a caller can surface a clean message instead of a KeyError.
    """
    try:
        factory = PROVIDER_FACTORIES[provider]
    except KeyError:
        known = ", ".join(available_providers())
        raise ValueError(
            f"unknown provider {provider!r}; registered providers: {known}"
        ) from None
    return factory()
