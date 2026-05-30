# agentlang-index

[![verify-refs](https://github.com/truffle-dev/agentlang-index/actions/workflows/verify-refs.yml/badge.svg)](https://github.com/truffle-dev/agentlang-index/actions/workflows/verify-refs.yml)

Zero is Vercel Labs' agent-first programming language. The thesis is
that frontier models write Zero more accurately than they write
TypeScript, Rust, Go, or Python. AgentLang Index is the measurement.

## Status

v1.0 corpus shipped 2026-05-18, all 20 tasks byte-exact across five
languages. First public benchmark run published 2026-05-19 at
[truffleagent.com/agentlang](https://truffleagent.com/agentlang/)
covering three OpenAI frontier models. Per-model drill-downs:
[gpt-5](https://truffleagent.com/agentlang/models/gpt-5/),
[gpt-4o](https://truffleagent.com/agentlang/models/gpt-4o/),
[gpt-4o-mini](https://truffleagent.com/agentlang/models/gpt-4o-mini/).

Headline from the first run: every model scored **0%** on Zero and
70-95% on TypeScript, Rust, Go, and Python. The average language tax
is **-78%** — i.e. these models lose 78 percentage points of accuracy
when asked to write Zero instead of an established language. That is
the gap an agent-first language has to close before the agent-first
claim is real.

## What it tests

- Both one-shot and agent-loop modes per task per language. One-shot
  is the model. Agent-loop is the model plus structured diagnostics
  and up to five repair attempts.
- Five primary metrics: first-attempt pass rate, repair iterations to
  green, total token cost, wall-time, runtime correctness on hidden
  tests.
- A derived sixth metric, **language tax**: pass-rate-in-Zero minus
  pass-rate-in-each-other-language, per model. That is the chart the
  benchmark exists to produce.

## What it refuses to be

- **Not a Zero marketing instrument.** Tasks where Zero scores poorly
  ship in the dashboard with the same prominence as tasks where it
  scores well. The methodology page explains what went wrong, not
  how to phrase around it.
- **Not a closed dataset.** Every run is reproducible from
  [`truffle-dev/agentlang-index-data`](https://github.com/truffle-dev/agentlang-index-data),
  CC-BY-4.0, with the harness git SHA and Zero version pinned per
  export.
- **Not an opinion piece.** The thesis is testable. The artifact is
  the answer.

## Quickstart

Reproduce a single-model sweep from a clean clone:

```sh
git clone https://github.com/truffle-dev/agentlang-index
cd agentlang-index
export OPENAI_API_KEY=sk-...
bun run bench/runner.ts --model gpt-4o-mini
```

The runner depends only on `bun` (no `npm install` step; OpenAI is
called via raw `fetch`). Per-task language runners need `tsc`, `rustc`/
`cargo`, `go`, and `python` on PATH when the task uses them; missing
toolchains surface as `spawn ENOENT` in the per-task `stderr`.

Output lands under `bench/results/<model>/runs/<id>/` with per-task
`scratch/` (the materialized source the model wrote), `stdout`,
`stderr`, and `result.json`. Aggregate a finished sweep into the
landing-page JSON with `bun run bench/aggregate.ts --site`.

The Python harness at `harness/` is the longer-form runner with SQLite
storage and agent-loop mode; see [`harness/README.md`](harness/README.md).

## Layout

```
agentlang-index/
  bench/                   TypeScript single-attempt runner (bun)
    runner.ts              one-shot per-model entry point
    aggregate.ts           collate runs into models/results JSON
    results/               per-run stdout/stderr/scratch captures
  harness/                 Python agent-loop runner (uv + pytest)
  corpus/                  Task specs, prompts, reference impls, tests
    000-hello-stdout/
    ...
  vendor/
    zero/<version>/        Pinned zero --version + skill data
    ts/                    Pinned tsconfig.json
    rust/                  rust-toolchain.toml
    go/                    go.mod
    python/                .python-version
```

Companion repos:

- [`truffle-dev/agentlang-index-data`](https://github.com/truffle-dev/agentlang-index-data) — open dataset, CC-BY-4.0.
- [`truffle-dev/agentlang-spec`](https://github.com/truffle-dev/agentlang-spec) — Zero CLI used during corpus assembly.

## License

Apache-2.0. See [LICENSE](LICENSE).
