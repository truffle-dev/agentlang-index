# agentlang-harness

The Python package that drives AgentLang Index benchmark runs.

## Status

Pre-alpha. Scaffolded 2026-05-18. One-shot runner live; agent-loop arrives next.

## Layout

```
src/agentlang_harness/
  cli.py            agentlang-run entrypoint (one-shot, verify-task, list-tasks)
  runner.py         one-shot per-language attempt orchestration
  prompt.py         prompt assembly + Zero skill inlining + fence extraction
  scratch.py        per-attempt scratch dir management
  verify.py         verify.sh invocation and outcome capture
  types.py          pydantic models (TaskSpec, AttemptResult, VerifierOutcome)
  storage/
    sqlite.py       SQLite schema v1 + run/attempt persistence API
tests/
  test_storage.py     storage layer
  test_runner_dry.py  one-shot runner with a mocked Anthropic client
  test_verify.py      verify.sh invocation against reference impls
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

# One-shot a model against a task (requires ANTHROPIC_API_KEY).
export ANTHROPIC_API_KEY=sk-ant-...
uv run agentlang-run one-shot 000-hello-stdout --lang python
uv run agentlang-run one-shot 001-fibonacci-memoized  # all 5 langs
```

The one-shot verb prompts `claude-opus-4-7` once per (task, language),
extracts the fenced source from the response, writes it into a per-attempt
scratch directory, invokes the task's `verify.sh --lang <lang>`, and
persists everything (prompt, response, verifier stdout/stderr/exit, wall
time, pass/fail) through the SQLite storage layer. Zero attempts ship the
vendored Zero 0.1.2 skill data as a cacheable prefix; non-Zero attempts
ship only a short role primer.
