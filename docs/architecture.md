# architecture decision record

Written 2026-05-18, day one of the project. The scout repo backfilled
its architecture doc weeks after the commits started landing; this one
lands first.

## the insight, in one sentence

Zero claims to be agent-first, and nobody has measured it. An identical
task corpus, run across five languages and a row of frontier models in
both one-shot and agent-loop modes, is the measurement.

## what agentlang-index is

A Python harness that takes a corpus of small programming tasks, asks
each frontier model to solve each task in Zero, TypeScript, Rust, Go,
and Python, scores the result, and emits an open dataset of runs. The
benchmark runs in two modes per (task, model, language): one-shot (one
completion, no tool calls) and agent-loop (up to five attempts with
structured diagnostics between attempts). The output is a per-model,
per-language pass rate plus four secondary metrics.

## what agentlang-index refuses to be

- **Not a Zero marketing instrument.** The harness is open, the
  corpus is open, the dataset is open. Tasks where Zero scores below
  Python ship in the same dashboard as tasks where Zero wins. The
  thesis is testable and the artifact answers it honestly.
- **Not a whole-language evaluation.** The corpus probes specific
  shapes (pure computation, parsing, I/O, networking, error handling,
  multi-file). It does not score "how good is this language for
  building a webserver" because that question is unscorable.
- **Not a one-shot leaderboard.** The agent-loop column is the
  headline column. One-shot is the baseline against which the
  iteration delta is computed. A benchmark that only reports
  one-shot pass rates elides the whole question Zero is asking.
- **Not a closed dataset.** Every dashboard cell links to a run
  identifier resolvable against
  [`truffle-dev/agentlang-index-data`](https://github.com/truffle-dev/agentlang-index-data).
  CC-BY-4.0 on the data, Apache-2.0 on the harness.

## the data flow

```
corpus/<task>/spec.json ─┐
                         ├─► render prompt ─► provider ─► sandbox ─► grader ─► storage
vendor/zero/<v>/skill ───┤                                                       │
                         │                                                       ├─► sqlite
models.toml ─────────────┘                                                       └─► parquet ─► JSON export
```

- **corpus**: each task is a directory containing `spec.json`, a
  prompt template, five hand-written reference implementations, a
  set of test cases split into public and hidden buckets, and
  `notes.md` with the task's design rationale.
- **vendor/zero/\<version\>**: pinned snapshot of `zero --version`
  and bundled skill data. The harness reads `vendor/zero/CURRENT`
  at runtime. Re-snapshotted per Zero release; old snapshots stay
  so old runs remain reproducible.
- **render prompt**: the harness shells out to `agentlang-spec
  emit --task <slug> --lang <lang>` (the companion Zero CLI) to
  produce the language-specific framing. Zero is load-bearing
  inside the harness, not optional.
- **provider**: a small protocol (`name`, `model_id`, `complete`,
  `cost`). Anthropic, OpenAI, Google, Together, Fireworks each
  implement it. Anthropic uses prompt caching aggressively: the
  task scaffold plus language skill data is cached, the model
  suffix is not. Target cache hit ratio is 80%.
- **sandbox**: per-language subprocess wrapper. Zero shells out to
  `zero run`. TypeScript runs through `tsc --noEmit` then `node`.
  Rust does `cargo check && cargo run`. Go does `go vet && go run`.
  Python does `mypy --strict && python`.
- **grader**: per-test-case pass/fail plus failure-mode
  classification (`syntax_error`, `type_error`, `runtime_panic`,
  `wrong_output`, `timeout`, `token_budget_exceeded`,
  `hallucinated_api`, `incomplete`). The `hallucinated_api`
  classification is the diagnostic of interest for the Zero
  thesis.
- **storage**: SQLite for metadata, Parquet for bulk run records
  (model outputs, conversation logs), JSON export for the public
  dataset.

## the scoring shape

Five primary metrics per (task, model, language, mode):

- **First-attempt pass rate.** Did attempt 1 pass all hidden test cases?
- **Repair iterations to green.** 1-5 or "never."
- **Total token cost.** Prompt + completion tokens across all
  attempts. Reported in tokens and USD because token prices change.
- **Wall-time.** Median seconds from task start to test-pass or
  final failure.
- **Runtime correctness.** Percentage of hidden test cases that
  passed on the final attempt.

A sixth derived metric, **language tax**, is pass-rate-in-Zero minus
pass-rate-in-each-other-language per model. Positive means the model
writes Zero better. That is the chart that gets quoted.

## decisions worth naming

- **Polyrepo, not monorepo.** Three repos: harness (Apache-2.0),
  dataset (CC-BY-4.0), Zero CLI (Apache-2.0). The dataset will
  accumulate gigabytes; pollulating `git clone` time for the
  harness contributor is the wrong trade. Three top-level LICENSE
  files in one repo also invite mistakes.
- **Both one-shot and agent-loop.** Reporting only one would
  hide the question Zero is asking. The dashboard surfaces them
  as side-by-side columns.
- **Hand-written reference implementations.** Not model-generated.
  If the reference is model-written the benchmark is circular.
- **Token budget per task.** A model cannot game
  repair-iterations-to-green by writing 5,000-line attempt-one
  submissions. Budget is 4x the longest reference, rounded up to
  the next 500 tokens.
- **No third-party-library tasks.** Zero's stdlib is the baseline.
  Tasks that need `tokio` or `requests` would force per-language
  sandbox provisioning and blow up the operations cost.
- **Pinned Zero per run.** `vendor/zero/<version>/` snapshots
  capture both `zero --version` and the bundled skill data. The
  harness reads `vendor/zero/CURRENT` at runtime. Old snapshots
  stay so old benchmark runs reproduce byte-for-byte.

## what comes next

Week 1: three repos, README + architecture doc per repo, task
000-hello-stdout with five reference implementations and verifier.

Weeks 2-4: tasks 001-005, Anthropic + OpenAI providers, one-shot
mode end-to-end, SQLite storage, first private benchmark run.

Month 2: tasks 006-015, agent-loop mode, Gemini + Together +
Fireworks providers, dashboard wired to real data, first public
preview run.

Month 3: 20-task v1.0 corpus, all providers wired, dashboard
polished, methodology page, v1.0 announce.
