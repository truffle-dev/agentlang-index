"""Prompt assembly: task prompt + per-language scaffold + Zero skill data."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from .types import Language

# Per-language scaffold blocks are injected at the `{language_scaffold}`
# site in each task's prompt.md. They tell the model what file to produce,
# what the runtime contract is, and the language-specific gotchas the
# harness expects the model to respect (e.g. Zero 0.1.2 has no stdin).
#
# The canonical strings live in `corpus/scaffolds.json` so the corpus is
# self-describing and external consumers (e.g. the agentlang-spec CLI's
# `emit` verb) read the same file instead of carrying a copy.
DEFAULT_SCAFFOLDS_PATH = (
    Path(__file__).resolve().parents[3] / "corpus" / "scaffolds.json"
)


@lru_cache(maxsize=None)
def _load_scaffolds(scaffolds_path: Path) -> dict[str, str]:
    try:
        doc = json.loads(scaffolds_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FileNotFoundError(
            f"scaffolds file not found: {scaffolds_path} — the corpus must "
            "ship a scaffolds.json (see corpus/scaffolds.json on main)"
        ) from None
    scaffolds = doc.get("scaffolds")
    if not isinstance(scaffolds, dict):
        raise ValueError(f"malformed scaffolds file (no 'scaffolds' map): {scaffolds_path}")
    return scaffolds


def _scaffolds_path_for(corpus_dir: Path | None) -> Path:
    if corpus_dir is None:
        return DEFAULT_SCAFFOLDS_PATH
    return corpus_dir / "scaffolds.json"


def scaffold_for(language: Language, corpus_dir: Path | None = None) -> str:
    """Return the per-language scaffold string injected into the prompt.

    Reads `<corpus_dir>/scaffolds.json` (default: this repo's corpus).
    """
    return _load_scaffolds(_scaffolds_path_for(corpus_dir))[language]


def render_user_prompt(
    prompt_template: str, language: Language, corpus_dir: Path | None = None
) -> str:
    """Substitute the `{language_scaffold}` placeholder in a task prompt."""
    return prompt_template.replace(
        "{language_scaffold}", scaffold_for(language, corpus_dir)
    )


def zero_skill_blocks(vendor_dir: Path) -> list[dict[str, Any]]:
    """Load Zero skill markdown files as cacheable system blocks.

    Returns Anthropic-message-format content blocks ready to drop into the
    request `system` field. The final block carries `cache_control:
    ephemeral` so the entire skill prefix sticks in the prompt cache for
    the 5-minute window.
    """
    if not vendor_dir.exists():
        return []
    md_files = sorted(p for p in vendor_dir.glob("*.md"))
    if not md_files:
        return []
    blocks: list[dict[str, Any]] = []
    for path in md_files:
        blocks.append({"type": "text", "text": path.read_text(encoding="utf-8")})
    blocks[-1]["cache_control"] = {"type": "ephemeral"}
    return blocks


def build_system_blocks(
    *, language: Language, zero_vendor_dir: Path | None
) -> list[dict[str, Any]]:
    """Assemble the system content blocks for a one-shot call.

    For Zero, prepends the vendored Zero 0.1.2 skill data (cached). For
    other languages, the system block is a brief role primer (also cached
    so it amortizes across attempts).
    """
    primer = (
        "You are participating in the AgentLang Index benchmark. Each task "
        "asks for a complete, compilable program in a specific language. "
        "Return only the source code inside a single fenced code block — "
        "no commentary, no explanation, no surrounding prose."
    )
    blocks: list[dict[str, Any]] = []
    if language == "zero" and zero_vendor_dir is not None:
        blocks.extend(zero_skill_blocks(zero_vendor_dir))
    blocks.append({"type": "text", "text": primer, "cache_control": {"type": "ephemeral"}})
    return blocks


def extract_fenced_code(response: str, language: Language) -> str:
    """Extract source from the first fenced code block in a model response.

    Prefers a fence tagged with one of the language's expected tags
    (e.g. ```zero``` for Zero); falls back to the first untagged fence;
    finally returns the trimmed response if no fence is found at all.
    """
    from .types import LANGUAGE_FENCE

    preferred = LANGUAGE_FENCE[language]
    lines = response.splitlines()
    fences: list[tuple[str, str]] = []  # (tag, body)
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith("```"):
            tag = stripped[3:].strip().lower()
            body_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                body_lines.append(lines[i])
                i += 1
            # Consume the closing fence (or EOF).
            i += 1
            fences.append((tag, "\n".join(body_lines)))
        else:
            i += 1
    for tag, body in fences:
        if tag in preferred:
            return body if body.endswith("\n") else body + "\n"
    for tag, body in fences:
        if not tag:
            return body if body.endswith("\n") else body + "\n"
    if fences:
        body = fences[0][1]
        return body if body.endswith("\n") else body + "\n"
    return response.strip() + "\n"
