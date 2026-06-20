# agentlang-harness

The Python package that drives AgentLang Index benchmark runs.

## Status

Pre-alpha. Scaffolded 2026-05-18. Both one-shot and agent-loop runners
live; agent-loop landed 2026-05-19 with `--mock` fixture replay for
reproducible test runs.

## Layout

```
src/agentlang_harness/
  cli.py            agentlang-run entrypoint (one-shot, agent-loop, verify-task, list-tasks)
  runner.py         one-shot per-language attempt orchestration
  agent_loop.py     iterative model + verifier-diagnostic loop (default max 5 iters)
  prompt.py         prompt assembly + Zero skill inlining + fence extraction
  scratch.py        per-attempt scratch dir management
  verify.py         verify.sh invocation and outcome capture
  types.py          pydantic models (TaskSpec, AttemptResult, VerifierOutcome)
  storage/
    sqlite.py       SQLite schema v1 + run/attempt persistence API
tests/
  test_storage.py       storage layer
  test_runner_dry.py    one-shot runner with a mocked Anthropic client
  test_agent_loop.py    agent-loop with --mock fixture replay
  test_verify.py        verify.sh invocation against reference impls
  fixtures/
    agent_loop_mock/    canned multi-turn responses keyed by task/lang
```

## Install

```sh
uv sync --extra test
```

## Test

```sh
uv run pytest -v
```

## Usage

```sh
# List every task in the corpus.
uv run agentlang-run list-tasks

# Run a task's reference impls through its verifier (no model call).
uv run agentlang-run verify-task 000-hello-stdout
uv run agentlang-run verify-task 000-hello-stdout --lang python

# One-shot a model against a task. Requires the `claude` CLI on PATH
# (defaults to ~/.local/bin/claude; override with CLAUDE_BIN=).
uv run agentlang-run one-shot 000-hello-stdout --lang python
uv run agentlang-run one-shot 001-fibonacci-memoized  # all 5 langs

# --dry-run prints the exact system + user prompt for each (task, language)
# and exits, with no model call, no database, and no network.
uv run agentlang-run one-shot 001-fibonacci-memoized --lang zero --dry-run

# Agent-loop: model writes, verifier reports, model fixes, up to --max-iters times.
uv run agentlang-run agent-loop 000-hello-stdout --lang python
uv run agentlang-run agent-loop 005-balanced-parens --max-iters 8

# --mock replays canned fixtures instead of calling the API (used by tests).
uv run agentlang-run agent-loop 000-hello-stdout --lang python --mock

# --provider selects the model-call backend (default: claude-cli). The
# registry lives in providers/__init__.py; cloud providers register there
# once their keys are provisioned.
uv run agentlang-run one-shot 001-fibonacci-memoized --provider claude-cli

# openai-compatible drives any endpoint that speaks the OpenAI chat schema
# (hosted DeepSeek/Together/Fireworks/Groq, or a local Ollama server). It
# reads OPENAI_COMPAT_BASE_URL and an optional OPENAI_COMPAT_API_KEY from the
# environment; local servers like Ollama need no key.
OPENAI_COMPAT_BASE_URL=http://ollama:11434/v1 \
  uv run agentlang-run one-shot 001-fibonacci-memoized \
  --provider openai-compatible --model qwen2.5-coder:0.5b
```

The one-shot verb prompts `claude-opus-4-7` once per (task, language),
extracts the fenced source from the response, writes it into a per-attempt
scratch directory, invokes the task's `verify.sh --lang <lang>`, and
persists everything (prompt, response, verifier stdout/stderr/exit, wall
time, pass/fail) through the SQLite storage layer. Model calls shell out
to the `claude` CLI (`claude --print --output-format json --model <id>`);
no `ANTHROPIC_API_KEY` is needed — the CLI uses its own login. Zero
attempts ship the vendored Zero 0.1.2 skill data as a cacheable prefix;
non-Zero attempts ship only a short role primer.

The agent-loop verb runs the same first call as one-shot, then on a
verifier failure feeds the structured diagnostic back to the model and
re-extracts source. It iterates until the verifier passes or `--max-iters`
(default 5) is exhausted. Every iteration's prompt, response, scratch
dir, and verifier outcome are persisted; the `--mock` mode replays canned
responses from `tests/fixtures/agent_loop_mock/<task>/<lang>.txt` (multi-
turn fixtures split on a literal `---` line) so the loop is exercisable
without API access.
