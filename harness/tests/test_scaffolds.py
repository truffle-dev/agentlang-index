"""Corpus-wide guard on the single source of truth for per-language scaffolds.

`corpus/scaffolds.json` became the only home for the scaffold strings on
2026-06-12 (both the Python harness and the agentlang-spec `emit` verb read
it). Two invariants keep that consolidation honest, and both are easy to
break silently:

  1. Every task prompt.md must contain the `{language_scaffold}` placeholder.
     `render_user_prompt` substitutes via `str.replace`, which is a no-op when
     the placeholder is absent, so a task that drops the section ships a prompt
     with no scaffold and no error. Tasks 009-019 hit exactly this.

  2. scaffolds.json must carry an entry for every language any task declares,
     and must not carry orphans. A missing entry raises a bare KeyError deep in
     the runner; an orphan signals a language that left the corpus.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentlang_harness.prompt import DEFAULT_SCAFFOLDS_PATH

CORPUS_DIR = Path(__file__).resolve().parents[2] / "corpus"
PLACEHOLDER = "{language_scaffold}"


def _task_dirs() -> list[Path]:
    return sorted(p for p in CORPUS_DIR.iterdir() if p.is_dir() and (p / "spec.json").exists())


def _scaffold_keys() -> set[str]:
    doc = json.loads(DEFAULT_SCAFFOLDS_PATH.read_text(encoding="utf-8"))
    return set(doc["scaffolds"].keys())


def test_corpus_has_tasks() -> None:
    """Guard against a path typo silently turning every parametrized test into
    a no-op."""
    assert len(_task_dirs()) >= 20


@pytest.mark.parametrize("task_dir", _task_dirs(), ids=lambda p: p.name)
def test_prompt_contains_scaffold_placeholder(task_dir: Path) -> None:
    text = (task_dir / "prompt.md").read_text(encoding="utf-8")
    assert PLACEHOLDER in text, (
        f"{task_dir.name}/prompt.md is missing the {PLACEHOLDER} marker; the "
        "runner would ship this task's prompt with no per-language scaffold"
    )


@pytest.mark.parametrize("task_dir", _task_dirs(), ids=lambda p: p.name)
def test_every_declared_language_has_a_scaffold(task_dir: Path) -> None:
    spec = json.loads((task_dir / "spec.json").read_text(encoding="utf-8"))
    keys = _scaffold_keys()
    missing = [lang for lang in spec["languages"] if lang not in keys]
    assert not missing, f"{task_dir.name} declares languages with no scaffold: {missing}"


def test_scaffolds_have_no_orphan_languages() -> None:
    declared: set[str] = set()
    for task_dir in _task_dirs():
        spec = json.loads((task_dir / "spec.json").read_text(encoding="utf-8"))
        declared.update(spec["languages"])
    orphans = _scaffold_keys() - declared
    assert not orphans, f"scaffolds.json carries languages no task declares: {sorted(orphans)}"


def test_scaffolds_placeholder_field_matches_runner_marker() -> None:
    """scaffolds.json advertises the placeholder string; it must equal the
    marker the runner actually substitutes, or external consumers (emit) and
    the harness disagree about what to replace."""
    doc = json.loads(DEFAULT_SCAFFOLDS_PATH.read_text(encoding="utf-8"))
    assert doc["placeholder"] == PLACEHOLDER
