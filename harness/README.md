# agentlang-harness

The Python package that drives AgentLang Index benchmark runs.

## Status

Pre-alpha. Scaffolded 2026-05-18. Currently only the storage layer is
live (`agentlang_harness.storage.sqlite`); runners arrive next.

## Layout

```
src/agentlang_harness/
  storage/
    sqlite.py       SQLite schema v1 + run/attempt persistence API
tests/
  test_storage.py   pytest unit tests for the storage layer
```

## Install

```sh
uv sync --extra test
```

## Test

```sh
uv run pytest -v
```
