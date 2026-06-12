"""Agent-loop runner: iterate up to `max_iters` turns with verifier diagnostics.

Each (task, language) attempt starts identically to the one-shot runner.
If the verifier fails and there are iterations left, the runner appends
the previous assistant turn plus a fresh user turn carrying the verifier
exit code, stderr tail, and — for Zero — the JSON output of `zero check`
and `zero fix --plan`. It then re-calls the model and re-verifies.

Only the final iteration's prompt, response, and verifier outcome land
in `task_attempts`. Iteration count and per-iteration exit codes are
encoded into the persisted response as a JSON header line followed by
`---SEP---\\n` and then the final assistant text, so the schema stays
at v1.
"""

from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .prompt import build_system_blocks, extract_fenced_code, render_user_prompt
from .runner import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    AnthropicClient,
    load_task_spec,
)
from .scratch import scratch_for_attempt
from .storage.sqlite import Storage
from .types import LANGUAGE_FILENAME, AttemptResult, Language, TaskSpec, VerifierOutcome
from .verify import run_verifier

DEFAULT_MAX_ITERS = 5
STDERR_TAIL_BYTES = 4096
ZERO_DIAG_TIMEOUT_S = 20.0
RESPONSE_HEADER_SEP = "---SEP---\n"


def _tail_bytes(text: str, limit: int = STDERR_TAIL_BYTES) -> str:
    """Return the last `limit` bytes of `text` (UTF-8 aware on best effort)."""
    if len(text) <= limit:
        return text
    return text[-limit:]


def _zero_diagnostic(
    binary: Path, scratch_dir: Path, args: list[str]
) -> str:
    """Invoke a Zero diagnostic command in `scratch_dir`; return stdout or sentinel."""
    if not binary.exists():
        return "(not available)"
    try:
        completed = subprocess.run(
            [str(binary), *args],
            cwd=str(scratch_dir),
            capture_output=True,
            text=True,
            timeout=ZERO_DIAG_TIMEOUT_S,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return "(not available)"
    out = completed.stdout or ""
    return out if out.strip() else "(not available)"


@dataclass
class AgentLoopRunner:
    """Multi-turn harness: same first turn as one-shot, then iterate on failures."""

    storage: Storage
    client: AnthropicClient
    corpus_dir: Path
    zero_vendor_dir: Path | None = None
    zero_binary: Path | None = None
    model: str = DEFAULT_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS
    max_iters: int = DEFAULT_MAX_ITERS

    def build_messages(
        self, spec: TaskSpec, prompt_template: str, language: Language
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
        """Render system + initial messages — identical to the one-shot shape."""
        system_blocks = build_system_blocks(
            language=language, zero_vendor_dir=self.zero_vendor_dir
        )
        user_text = render_user_prompt(prompt_template, language, self.corpus_dir)
        messages = [{"role": "user", "content": [{"type": "text", "text": user_text}]}]
        return system_blocks, messages, user_text

    def call_model(
        self, system_blocks: list[dict[str, Any]], messages: list[dict[str, Any]]
    ) -> tuple[str, dict[str, Any]]:
        """One Messages API call. Mirrors OneShotRunner.call_model."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_blocks,
            messages=messages,
        )
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

    def build_followup_user_turn(
        self,
        language: Language,
        verifier: VerifierOutcome,
        zero_check_json: str | None,
        zero_fix_json: str | None,
    ) -> dict[str, Any]:
        """Render the user turn fed back to the model after a failed verifier."""
        ref_name = LANGUAGE_FILENAME[language]
        fence_tag = "zero" if language == "zero" else {
            "ts": "ts",
            "rust": "rust",
            "go": "go",
            "python": "python",
        }[language]
        stderr_tail = _tail_bytes(verifier.stderr or "")
        parts = [
            "Your code did not pass the verifier. Here are the diagnostics:",
            "",
            "### verifier exit code",
            str(verifier.exit_code),
            "",
            "### verifier stderr (last 4 KB)",
            stderr_tail if stderr_tail else "(empty)",
        ]
        if language == "zero":
            parts.extend([
                "",
                "### zero check --json",
                zero_check_json or "(not available)",
                "",
                "### zero fix --plan --json",
                zero_fix_json or "(not available)",
            ])
        parts.extend([
            "",
            f"Return a corrected {ref_name} in a single ```{fence_tag}``` fence. "
            "Do not include commentary.",
        ])
        text = "\n".join(parts)
        return {"role": "user", "content": [{"type": "text", "text": text}]}

    def _verify_and_diagnose(
        self,
        task_dir: Path,
        language: Language,
        source: str,
    ) -> tuple[VerifierOutcome, str | None, str | None]:
        """Run verify.sh and (for Zero) the JSON diagnostic commands."""
        with scratch_for_attempt(task_dir, language, source) as scratch:
            verifier = run_verifier(scratch, language)
            zero_check_json: str | None = None
            zero_fix_json: str | None = None
            if language == "zero":
                binary = self.zero_binary
                if binary is None:
                    zero_check_json = "(not available)"
                    zero_fix_json = "(not available)"
                else:
                    ref = LANGUAGE_FILENAME[language]
                    zero_check_json = _zero_diagnostic(
                        binary, scratch, ["check", "--json", ref]
                    )
                    zero_fix_json = _zero_diagnostic(
                        binary, scratch, ["fix", "--plan", "--json", ref]
                    )
        return verifier, zero_check_json, zero_fix_json

    def run_attempt(
        self, task_slug: str, language: Language, *, run_id: int | None = None
    ) -> AttemptResult:
        """Drive up to `max_iters` turns until the verifier passes or we exhaust."""
        spec, task_dir, template = load_task_spec(self.corpus_dir, task_slug)
        if language not in spec.languages:
            raise ValueError(
                f"task {task_slug!r} does not declare language {language!r}; "
                f"declared: {spec.languages}"
            )
        system_blocks, messages, user_prompt = self.build_messages(
            spec, template, language
        )
        per_iter_exit_codes: list[int] = []
        per_iter_passed: list[bool] = []
        last_response_text = ""
        last_verifier: VerifierOutcome | None = None
        total_call_ms = 0
        final_call_meta: dict[str, Any] = {"model": self.model}
        for iteration in range(1, self.max_iters + 1):
            call_started = time.monotonic()
            response_text, call_meta = self.call_model(system_blocks, messages)
            total_call_ms += int((time.monotonic() - call_started) * 1000)
            final_call_meta = call_meta
            source = extract_fenced_code(response_text, language)
            verifier, zero_check_json, zero_fix_json = self._verify_and_diagnose(
                task_dir, language, source
            )
            per_iter_exit_codes.append(verifier.exit_code)
            per_iter_passed.append(verifier.passed)
            last_response_text = response_text
            last_verifier = verifier
            if verifier.passed or iteration >= self.max_iters:
                break
            # Append the assistant turn that just failed, plus the followup.
            messages.append(
                {"role": "assistant", "content": [{"type": "text", "text": response_text}]}
            )
            messages.append(
                self.build_followup_user_turn(
                    language, verifier, zero_check_json, zero_fix_json
                )
            )
        assert last_verifier is not None  # loop runs at least once
        header = {
            "iterations": len(per_iter_exit_codes),
            "per_iter_passed": per_iter_passed,
            "per_iter_exit_codes": per_iter_exit_codes,
        }
        persisted_response = (
            json.dumps(header, sort_keys=True) + "\n" + RESPONSE_HEADER_SEP + last_response_text
        )
        metadata: dict[str, Any] = {
            "model_call_ms": total_call_ms,
            "iterations": len(per_iter_exit_codes),
            "per_iter_passed": per_iter_passed,
            "per_iter_exit_codes": per_iter_exit_codes,
            **final_call_meta,
        }
        if run_id is not None:
            self.storage.record_attempt(
                run_id=run_id,
                task_slug=task_slug,
                language=language,
                prompt=user_prompt,
                response=persisted_response,
                verifier_stdout=last_verifier.stdout,
                verifier_stderr=last_verifier.stderr,
                verifier_exit_code=last_verifier.exit_code,
                wall_time_ms=last_verifier.wall_time_ms,
                passed=last_verifier.passed,
            )
        return AttemptResult(
            task_slug=task_slug,
            language=language,
            prompt=user_prompt,
            response=last_response_text,
            verifier=last_verifier,
            metadata=metadata,
        )
