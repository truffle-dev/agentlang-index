"""Unit tests for the provider registry and the CLI's --provider seam."""

from __future__ import annotations

import pytest

from agentlang_harness.cli import build_parser
from agentlang_harness.providers import (
    DEFAULT_PROVIDER,
    PROVIDER_FACTORIES,
    available_providers,
    make_client,
)
from agentlang_harness.providers.claude_cli import ClaudeCliClient


def test_default_provider_is_registered() -> None:
    assert DEFAULT_PROVIDER in PROVIDER_FACTORIES
    assert DEFAULT_PROVIDER in available_providers()


def test_available_providers_is_sorted() -> None:
    names = available_providers()
    assert names == sorted(names)
    assert names == sorted(PROVIDER_FACTORIES)


def test_make_client_builds_the_registered_client() -> None:
    client = make_client("claude-cli")
    assert isinstance(client, ClaudeCliClient)


def test_make_client_unknown_names_the_known_providers() -> None:
    with pytest.raises(ValueError) as excinfo:
        make_client("gemini")
    message = str(excinfo.value)
    assert "gemini" in message
    # The error lists what is registered so a caller can correct the name.
    assert "claude-cli" in message


@pytest.mark.parametrize("verb", ["one-shot", "agent-loop"])
def test_provider_flag_defaults_to_claude_cli(verb: str) -> None:
    parser = build_parser()
    args = parser.parse_args([verb, "001-fibonacci-memoized"])
    assert args.provider == DEFAULT_PROVIDER


@pytest.mark.parametrize("verb", ["one-shot", "agent-loop"])
def test_provider_flag_rejects_unregistered_choice(verb: str) -> None:
    parser = build_parser()
    # argparse `choices` rejects an unknown provider at parse time with exit 2,
    # before any client is constructed.
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args([verb, "001-fibonacci-memoized", "--provider", "gemini"])
    assert excinfo.value.code == 2
