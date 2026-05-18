"""Prompt assembly: task prompt + per-language scaffold + Zero skill data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .types import Language

# Per-language scaffold blocks injected at the `{language_scaffold}` site
# in each task's prompt.md. They tell the model what file to produce, what
# the runtime contract is, and the language-specific gotchas the harness
# expects the model to respect (e.g. Zero 0.1.2 has no stdin).
_SCAFFOLDS: dict[Language, str] = {
    "zero": (
        "Write a single Zero 0.1.2 source file named `ref.zero`. Define "
        "`pub fun main(world: World) -> Void raises`. Use `world.out.write` "
        "for stdout and `world.err.write` for stderr. Zero 0.1.2's direct "
        "ELF64 backend exposes no stdin capability; if the task requires "
        "input, read it from `std.args.get(1)` instead. Fixed-array element "
        "types are restricted to i32, u32, and u8; emulate larger integer "
        "memos with parallel u32 arrays. Return only the source inside a "
        "single ```zero fenced code block."
    ),
    "ts": (
        "Write a single TypeScript source file named `ref.ts`. Read from "
        "`process.stdin` if the task requires input and write the answer "
        "to `process.stdout`. Keep type annotations minimal so the same "
        "source runs under tsx, bun, or plain node. Return only the source "
        "inside a single ```ts fenced code block."
    ),
    "rust": (
        "Write a single Rust source file named `ref.rs` that compiles with "
        "`rustc ref.rs -o prog` (no Cargo manifest used at runtime). Read "
        "from `std::io::stdin` if input is required and write to "
        "`std::io::stdout`. Prefer `print!` over `println!` when the spec "
        "is byte-exact. Return only the source inside a single ```rust "
        "fenced code block."
    ),
    "go": (
        "Write a single Go source file named `ref.go` in `package main`. "
        "Read stdin via `bufio.NewReader(os.Stdin)` if input is required. "
        "Use `fmt.Print` (not `fmt.Println`) when the spec is byte-exact. "
        "The harness runs `go run ref.go`. Return only the source inside "
        "a single ```go fenced code block."
    ),
    "python": (
        "Write a single Python 3.12 source file named `ref.py`. Use "
        "`sys.stdin.read()` or `input()` for input and `sys.stdout.write` "
        "for output (not `print`) when the spec is byte-exact. The harness "
        "runs `python3 ref.py`. Return only the source inside a single "
        "```python fenced code block."
    ),
}


def scaffold_for(language: Language) -> str:
    """Return the per-language scaffold string injected into the prompt."""
    return _SCAFFOLDS[language]


def render_user_prompt(prompt_template: str, language: Language) -> str:
    """Substitute the `{language_scaffold}` placeholder in a task prompt."""
    return prompt_template.replace("{language_scaffold}", scaffold_for(language))


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
