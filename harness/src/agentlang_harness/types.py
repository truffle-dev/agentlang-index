"""Pydantic models for harness inputs, outputs, and persisted attempts."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Language = Literal["zero", "ts", "rust", "go", "python"]

LANGUAGES: tuple[Language, ...] = ("zero", "ts", "rust", "go", "python")

# Filename a model-written source lands on inside a scratch dir. Must match
# the verify.sh expectation for each language (the verifier looks for
# ref.<ext> by convention, and runs whatever it finds).
LANGUAGE_FILENAME: dict[Language, str] = {
    "zero": "ref.zero",
    "ts": "ref.ts",
    "rust": "ref.rs",
    "go": "ref.go",
    "python": "ref.py",
}

# Markdown fence tag a model is most likely to use per language.
LANGUAGE_FENCE: dict[Language, tuple[str, ...]] = {
    "zero": ("zero",),
    "ts": ("ts", "typescript", "javascript", "js"),
    "rust": ("rust", "rs"),
    "go": ("go", "golang"),
    "python": ("python", "py"),
}


class TaskSpec(BaseModel):
    """The on-disk corpus task spec (subset the runner needs)."""

    model_config = ConfigDict(extra="allow")

    slug: str
    title: str
    prompt: str
    languages: list[Language]
    token_budget: int = 8192


class VerifierOutcome(BaseModel):
    """Result of invoking verify.sh for a single language."""

    stdout: str
    stderr: str
    exit_code: int
    wall_time_ms: int

    @property
    def passed(self) -> bool:
        """A verifier exit of 0 means every test case for the language passed."""
        return self.exit_code == 0


class AttemptResult(BaseModel):
    """A single (task, language) one-shot attempt, persisted verbatim."""

    task_slug: str
    language: Language
    prompt: str
    response: str
    verifier: VerifierOutcome
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.verifier.passed
