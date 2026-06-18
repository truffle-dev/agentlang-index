"""Unit tests for the one-shot runner that mock the Anthropic client."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from agentlang_harness.prompt import (
    build_system_blocks,
    extract_fenced_code,
    render_user_prompt,
    scaffold_for,
)
from agentlang_harness.runner import OneShotRunner, list_tasks, load_task_spec
from agentlang_harness.storage.sqlite import Storage
from agentlang_harness.types import LANGUAGES


REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = REPO_ROOT / "corpus"
VENDOR_ZERO = REPO_ROOT / "vendor" / "zero" / "0.1.2"


@dataclass
class _FakeUsage:
    input_tokens: int = 100
    output_tokens: int = 50
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


@dataclass
class _FakeBlock:
    type: str
    text: str


@dataclass
class _FakeResponse:
    content: list[_FakeBlock]
    usage: _FakeUsage


class _FakeMessages:
    """Records every call and replays canned responses keyed by language."""

    def __init__(self, payload_for_lang: dict[str, str]) -> None:
        self.payload_for_lang = payload_for_lang
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls.append(kwargs)
        user_text = kwargs["messages"][0]["content"][0]["text"]
        # Dispatch by matching the full scaffold text into the rendered prompt
        # — each language scaffold is unique enough on its leading clause.
        for lang, payload in self.payload_for_lang.items():
            head = scaffold_for(lang).split(".")[0]  # type: ignore[arg-type]
            if head in user_text:
                return _FakeResponse([_FakeBlock("text", payload)], _FakeUsage())
        first_lang = next(iter(self.payload_for_lang))
        return _FakeResponse(
            [_FakeBlock("text", self.payload_for_lang[first_lang])], _FakeUsage()
        )


class _FakeAnthropic:
    def __init__(self, payload_for_lang: dict[str, str]) -> None:
        self.messages = _FakeMessages(payload_for_lang)


@pytest.fixture
def corpus_dir() -> Path:
    return CORPUS_DIR


def test_list_tasks_discovers_corpus(corpus_dir: Path) -> None:
    """The corpus loader finds every task spec.json, sorted by slug."""
    specs = list_tasks(corpus_dir)
    slugs = [s.slug for s in specs]
    assert "000-hello-stdout" in slugs
    assert "001-fibonacci-memoized" in slugs
    assert slugs == sorted(slugs)


def test_render_user_prompt_substitutes_scaffold(corpus_dir: Path) -> None:
    """Each language scaffold replaces the {language_scaffold} placeholder."""
    spec, _, template = load_task_spec(corpus_dir, "000-hello-stdout")
    assert "{language_scaffold}" in template
    for lang in spec.languages:
        rendered = render_user_prompt(template, lang)
        assert "{language_scaffold}" not in rendered
        assert scaffold_for(lang) in rendered


def test_scaffolds_load_from_corpus_json(corpus_dir: Path, tmp_path: Path) -> None:
    """Scaffolds come from corpus/scaffolds.json and cover every language."""
    import json

    doc = json.loads((corpus_dir / "scaffolds.json").read_text(encoding="utf-8"))
    assert doc["placeholder"] == "{language_scaffold}"
    assert sorted(doc["scaffolds"]) == sorted(LANGUAGES)
    for lang in LANGUAGES:
        assert scaffold_for(lang, corpus_dir) == doc["scaffolds"][lang]
    # An explicit corpus_dir override reads that corpus's file.
    alt = {"version": 1, "scaffolds": {lang: f"ALT-{lang}" for lang in LANGUAGES}}
    (tmp_path / "scaffolds.json").write_text(json.dumps(alt), encoding="utf-8")
    assert scaffold_for("zero", tmp_path) == "ALT-zero"
    assert render_user_prompt("x {language_scaffold} y", "go", tmp_path) == "x ALT-go y"
    # A corpus without scaffolds.json fails with a pointed error.
    with pytest.raises(FileNotFoundError, match="scaffolds.json"):
        scaffold_for("zero", tmp_path / "missing")


def test_extract_fenced_code_prefers_language_tag() -> None:
    """A ```python fence beats a tag-less fence when extracting a Python answer."""
    response = (
        "Sure, here's the answer:\n\n"
        "```\nignore me\n```\n\n"
        "And the real one:\n\n"
        "```python\nimport sys\nsys.stdout.write('hello\\n')\n```\n"
    )
    extracted = extract_fenced_code(response, "python")
    assert "import sys" in extracted
    assert "ignore me" not in extracted
    assert extracted.endswith("\n")


def test_extract_fenced_code_falls_back_to_untagged() -> None:
    """Untagged fences are accepted when no language tag matches."""
    response = "Solution:\n```\nprint('x')\n```\n"
    extracted = extract_fenced_code(response, "python")
    assert "print('x')" in extracted


def test_extract_fenced_code_handles_no_fence() -> None:
    """No fences at all returns the response as-is (best-effort)."""
    response = "import sys\nsys.stdout.write('hello\\n')\n"
    extracted = extract_fenced_code(response, "python")
    assert "import sys" in extracted


def test_zero_skill_data_inlined_in_system_blocks() -> None:
    """Zero attempts inline the vendored Zero skill markdown as system blocks."""
    blocks = build_system_blocks(language="zero", zero_vendor_dir=VENDOR_ZERO)
    # Vendored Zero 0.1.2 ships 7 skill .md files plus the role primer.
    assert len(blocks) == 8
    # The final block carries cache_control to anchor the prompt-cache prefix.
    assert blocks[-1].get("cache_control") == {"type": "ephemeral"}
    # Earlier Zero skill blocks must NOT carry cache_control (single
    # breakpoint at the end of the prefix).
    for block in blocks[:-2]:
        assert "cache_control" not in block
    # Skill content actually got read off disk.
    big = "\n".join(b["text"] for b in blocks)
    assert "zero-language" in big or "zero-stdlib" in big


def test_non_zero_languages_skip_zero_skill_blocks() -> None:
    """Python/Rust/Go/TS attempts don't ship Zero skill data."""
    for lang in ("python", "rust", "go", "ts"):
        blocks = build_system_blocks(language=lang, zero_vendor_dir=VENDOR_ZERO)  # type: ignore[arg-type]
        assert len(blocks) == 1
        assert blocks[0]["cache_control"] == {"type": "ephemeral"}
        assert "zero-language" not in blocks[0]["text"]


def test_one_shot_run_attempt_persists_and_passes(
    corpus_dir: Path, tmp_path: Path
) -> None:
    """Runner end-to-end: fake API returns a known-good Python answer,
    verifier passes, attempt lands in SQLite."""
    payload = {
        "python": "Here:\n```python\nimport sys\nsys.stdout.write('hello\\n')\n```\n",
    }
    client = _FakeAnthropic(payload)
    db_path = tmp_path / "runs.db"
    with Storage(db_path) as store:
        run_id = store.start_run(model="fake", corpus_sha="t", mode="one_shot")
        runner = OneShotRunner(
            storage=store,
            client=client,  # type: ignore[arg-type]
            corpus_dir=corpus_dir,
            zero_vendor_dir=None,
        )
        result = runner.run_attempt("000-hello-stdout", "python", run_id=run_id)
        assert result.passed is True
        assert result.verifier.exit_code == 0
        attempts = store.attempts_for_run(run_id)
        assert len(attempts) == 1
        row = attempts[0]
        assert row["task_slug"] == "000-hello-stdout"
        assert row["language"] == "python"
        assert row["passed"] == 1
        # The model call kwargs include cache_control on system blocks.
        call = client.messages.calls[0]
        assert any("cache_control" in b for b in call["system"])


def test_one_shot_records_failure_when_source_is_wrong(
    corpus_dir: Path, tmp_path: Path
) -> None:
    """A model response that prints the wrong bytes is recorded as a failed
    attempt without raising."""
    payload = {
        "python": "```python\nimport sys\nsys.stdout.write('goodbye\\n')\n```\n",
    }
    client = _FakeAnthropic(payload)
    db_path = tmp_path / "runs.db"
    with Storage(db_path) as store:
        run_id = store.start_run(model="fake", corpus_sha="t", mode="one_shot")
        runner = OneShotRunner(
            storage=store,
            client=client,  # type: ignore[arg-type]
            corpus_dir=corpus_dir,
            zero_vendor_dir=None,
        )
        result = runner.run_attempt("000-hello-stdout", "python", run_id=run_id)
        assert result.passed is False
        attempts = store.attempts_for_run(run_id)
        assert attempts[0]["passed"] == 0


def test_languages_constant_matches_corpus_declarations(corpus_dir: Path) -> None:
    """Every task in the corpus declares only languages the harness knows."""
    for spec in list_tasks(corpus_dir):
        for lang in spec.languages:
            assert lang in LANGUAGES


def test_one_shot_dry_run_prints_prompts_without_calling_model(
    corpus_dir: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`one-shot --dry-run` prints the assembled prompt for each language and
    exits 0 without a model call, a database, or any leftover scaffold marker.

    Drives the real CLI entrypoint so the preview is exercised through the same
    OneShotRunner.build_messages path a live call uses. The --db default is never
    touched because the dry-run returns before storage is opened; pointing it at a
    fresh tmp path and asserting the file is absent proves that.
    """
    from agentlang_harness.cli import main

    db_path = tmp_path / "should-not-exist.db"
    ret = main(
        [
            "one-shot",
            "001-fibonacci-memoized",
            "--lang",
            "zero",
            "--lang",
            "python",
            "--corpus-dir",
            str(corpus_dir),
            "--db",
            str(db_path),
            "--dry-run",
        ]
    )
    assert ret == 0
    assert not db_path.exists()

    out = capsys.readouterr().out
    assert "===== 001-fibonacci-memoized :: zero =====" in out
    assert "===== 001-fibonacci-memoized :: python =====" in out
    # The placeholder must be substituted, never emitted literally.
    assert "{language_scaffold}" not in out
    # The canonical per-language scaffold text is what got substituted in.
    assert scaffold_for("zero", corpus_dir) in out
    assert scaffold_for("python", corpus_dir) in out
    # No run was finalized, so no run_id/db summary line is printed.
    assert "run_id=" not in out
