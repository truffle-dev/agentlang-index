"""One-shot runner: call the model once per (task, language), score, persist."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from .prompt import build_system_blocks, extract_fenced_code, render_user_prompt
from .scratch import scratch_for_attempt
from .storage.sqlite import Storage
from .types import LANGUAGES, AttemptResult, Language, TaskSpec, VerifierOutcome
from .verify import run_verifier

DEFAULT_MODEL = "claude-opus-4-7"
DEFAULT_MAX_TOKENS = 8192


class AnthropicClient(Protocol):
    """Structural type for the bit of the Anthropic SDK the runner needs.

    Lets tests inject a fake without importing the real client.
    """

    messages: Any


def load_task_spec(corpus_dir: Path, task_slug: str) -> tuple[TaskSpec, Path, str]:
    """Load a task spec.json and prompt.md. Returns (spec, task_dir, prompt_template)."""
    task_dir = corpus_dir / task_slug
    spec_path = task_dir / "spec.json"
    prompt_path = task_dir / "prompt.md"
    if not spec_path.exists():
        raise FileNotFoundError(f"no spec.json at {spec_path}")
    if not prompt_path.exists():
        raise FileNotFoundError(f"no prompt.md at {prompt_path}")
    spec = TaskSpec.model_validate(json.loads(spec_path.read_text(encoding="utf-8")))
    template = prompt_path.read_text(encoding="utf-8")
    return spec, task_dir, template


def list_tasks(corpus_dir: Path) -> list[TaskSpec]:
    """List every task spec under `corpus_dir`, sorted by slug."""
    out: list[TaskSpec] = []
    if not corpus_dir.exists():
        return out
    for sub in sorted(corpus_dir.iterdir()):
        spec_path = sub / "spec.json"
        if spec_path.is_file():
            out.append(
                TaskSpec.model_validate(
                    json.loads(spec_path.read_text(encoding="utf-8"))
                )
            )
    return out


@dataclass
class OneShotRunner:
    """One-shot harness: prompt the model once per (task, language) and score it.

    The runner is intentionally stateless across invocations apart from
    the storage handle. Each `run_attempt` call is independent and can be
    parallelized externally once the SQLite layer is wrapped for it.
    """

    storage: Storage
    client: AnthropicClient
    corpus_dir: Path
    zero_vendor_dir: Path | None = None
    model: str = DEFAULT_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS

    def build_messages(
        self, spec: TaskSpec, prompt_template: str, language: Language
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
        """Render system + messages for one (task, language) attempt."""
        system_blocks = build_system_blocks(
            language=language, zero_vendor_dir=self.zero_vendor_dir
        )
        user_text = render_user_prompt(prompt_template, language, self.corpus_dir)
        messages = [{"role": "user", "content": [{"type": "text", "text": user_text}]}]
        return system_blocks, messages, user_text

    def call_model(
        self, system_blocks: list[dict[str, Any]], messages: list[dict[str, Any]]
    ) -> tuple[str, dict[str, Any]]:
        """Issue a single Messages API call and return (text, metadata)."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_blocks,
            messages=messages,
        )
        # Stitch every text block in the response in order.
        chunks: list[str] = []
        for block in getattr(response, "content", []) or []:
            block_type = getattr(block, "type", None) or (
                block.get("type") if isinstance(block, dict) else None
            )
            if block_type == "text":
                text = getattr(block, "text", None) or (
                    block.get("text") if isinstance(block, dict) else ""
                )
                chunks.append(text or "")
        text = "".join(chunks)
        usage = getattr(response, "usage", None)
        metadata: dict[str, Any] = {"model": self.model}
        if usage is not None:
            for field in (
                "input_tokens",
                "output_tokens",
                "cache_creation_input_tokens",
                "cache_read_input_tokens",
            ):
                value = getattr(usage, field, None)
                if value is None and isinstance(usage, dict):
                    value = usage.get(field)
                if value is not None:
                    metadata[field] = value
        return text, metadata

    def run_attempt(
        self, task_slug: str, language: Language, *, run_id: int | None = None
    ) -> AttemptResult:
        """Run one (task, language) attempt end to end.

        If `run_id` is given, the result is persisted as an attempt under
        that run. Callers driving a sweep keep one run_id across many
        attempts.
        """
        spec, task_dir, template = load_task_spec(self.corpus_dir, task_slug)
        if language not in spec.languages:
            raise ValueError(
                f"task {task_slug!r} does not declare language {language!r}; "
                f"declared: {spec.languages}"
            )
        system_blocks, messages, user_prompt = self.build_messages(spec, template, language)
        call_started = time.monotonic()
        response_text, call_meta = self.call_model(system_blocks, messages)
        call_ms = int((time.monotonic() - call_started) * 1000)
        source = extract_fenced_code(response_text, language)
        with scratch_for_attempt(task_dir, language, source) as scratch:
            verifier = run_verifier(scratch, language)
        metadata = {"model_call_ms": call_ms, **call_meta}
        if run_id is not None:
            self.storage.record_attempt(
                run_id=run_id,
                task_slug=task_slug,
                language=language,
                prompt=user_prompt,
                response=response_text,
                verifier_stdout=verifier.stdout,
                verifier_stderr=verifier.stderr,
                verifier_exit_code=verifier.exit_code,
                wall_time_ms=verifier.wall_time_ms,
                passed=verifier.passed,
            )
        return AttemptResult(
            task_slug=task_slug,
            language=language,
            prompt=user_prompt,
            response=response_text,
            verifier=verifier,
            metadata=metadata,
        )


def verify_local_source(
    corpus_dir: Path, task_slug: str, language: Language, source_path: Path
) -> VerifierOutcome:
    """Verify a hand-written file against a task without calling any model."""
    _, task_dir, _ = load_task_spec(corpus_dir, task_slug)
    source = source_path.read_text(encoding="utf-8")
    with scratch_for_attempt(task_dir, language, source) as scratch:
        return run_verifier(scratch, language)


def resolve_languages(spec: TaskSpec, requested: list[Language] | None) -> list[Language]:
    """Resolve a language filter against a task spec's supported list."""
    if requested is None:
        return list(spec.languages)
    out: list[Language] = []
    for lang in requested:
        if lang not in LANGUAGES:
            raise ValueError(f"unknown language {lang!r}; valid: {LANGUAGES}")
        if lang in spec.languages:
            out.append(lang)
    return out
