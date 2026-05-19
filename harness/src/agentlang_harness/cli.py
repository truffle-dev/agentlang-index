"""`agentlang-run` CLI: one-shot, agent-loop, verify-task, list-tasks verbs."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from .agent_loop import DEFAULT_MAX_ITERS, AgentLoopRunner
from .runner import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    OneShotRunner,
    list_tasks,
    load_task_spec,
    resolve_languages,
    verify_local_source,
)
from .storage.sqlite import Storage
from .types import LANGUAGES, Language

REPO_ROOT_GUESS = Path(__file__).resolve().parents[3]
DEFAULT_CORPUS_DIR = REPO_ROOT_GUESS / "corpus"
DEFAULT_VENDOR_ZERO_DIR = REPO_ROOT_GUESS / "vendor" / "zero" / "0.1.2"
DEFAULT_ZERO_BINARY = Path("/home/phantom/repos/zero/bin/zero")
DEFAULT_DB_PATH = REPO_ROOT_GUESS / "harness" / "runs.db"
DEFAULT_MOCK_FIXTURE_DIR = (
    REPO_ROOT_GUESS / "harness" / "tests" / "fixtures" / "agent_loop_mock"
)


def _add_corpus_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--corpus-dir",
        type=Path,
        default=DEFAULT_CORPUS_DIR,
        help=f"path to the corpus root (default: {DEFAULT_CORPUS_DIR})",
    )


def _corpus_sha(corpus_dir: Path) -> str:
    """Stable identifier for the corpus snapshot: SHA-256 of slug list + spec sizes."""
    h = hashlib.sha256()
    for sub in sorted(corpus_dir.iterdir()):
        spec = sub / "spec.json"
        if spec.is_file():
            h.update(sub.name.encode())
            h.update(b":")
            h.update(str(spec.stat().st_size).encode())
            h.update(b"\n")
    return h.hexdigest()[:16]


def _cmd_list_tasks(args: argparse.Namespace) -> int:
    tasks = list_tasks(args.corpus_dir)
    if not tasks:
        print(f"no tasks under {args.corpus_dir}", file=sys.stderr)
        return 1
    for spec in tasks:
        langs = ",".join(spec.languages)
        print(f"{spec.slug:32s} {spec.title}  [{langs}]")
    return 0


def _cmd_verify_task(args: argparse.Namespace) -> int:
    spec, task_dir, _ = load_task_spec(args.corpus_dir, args.task)
    languages = resolve_languages(spec, args.languages)
    if not languages:
        print(f"no matching languages for task {args.task!r}", file=sys.stderr)
        return 2
    all_passed = True
    for lang in languages:
        ref_name = {
            "zero": "ref.zero",
            "ts": "ref.ts",
            "rust": "ref.rs",
            "go": "ref.go",
            "python": "ref.py",
        }[lang]
        ref_path = task_dir / ref_name
        if not ref_path.exists():
            print(f"SKIP: {lang} (no {ref_name})")
            continue
        outcome = verify_local_source(args.corpus_dir, args.task, lang, ref_path)
        status = "PASS" if outcome.passed else "FAIL"
        print(f"{status}: {lang} (exit={outcome.exit_code}, wall={outcome.wall_time_ms}ms)")
        if not outcome.passed:
            all_passed = False
            if outcome.stdout:
                sys.stdout.write(outcome.stdout)
            if outcome.stderr:
                sys.stderr.write(outcome.stderr)
    return 0 if all_passed else 1


def _make_anthropic_client() -> object:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit(
            "ANTHROPIC_API_KEY is not set. Export it before running one-shot."
        )
    from anthropic import Anthropic

    return Anthropic(api_key=api_key)


@dataclass
class _MockBlock:
    type: str
    text: str


@dataclass
class _MockResponse:
    content: list[_MockBlock]
    usage: Any = None


class _MockMessages:
    """Replay canned fixture files per language; loop on the last fixture."""

    def __init__(self, fixtures: dict[str, list[str]]) -> None:
        self._fixtures = fixtures
        self._cursor: dict[str, int] = {lang: 0 for lang in fixtures}

    def create(self, **kwargs: Any) -> _MockResponse:
        user_text = kwargs["messages"][0]["content"][0]["text"]
        from .prompt import scaffold_for

        match: str | None = None
        for lang in self._fixtures:
            head = scaffold_for(lang).split(".")[0]  # type: ignore[arg-type]
            if head in user_text:
                match = lang
                break
        if match is None:
            match = next(iter(self._fixtures))
        payloads = self._fixtures[match]
        idx = min(self._cursor[match], len(payloads) - 1)
        self._cursor[match] += 1
        return _MockResponse([_MockBlock("text", payloads[idx])])


@dataclass
class _MockClient:
    fixtures: dict[str, list[str]]
    messages: _MockMessages = field(init=False)

    def __post_init__(self) -> None:
        self.messages = _MockMessages(self.fixtures)


def _load_mock_fixtures(
    fixture_dir: Path, task_slug: str, languages: list[Language]
) -> dict[str, list[str]]:
    """Read `<task>/<lang>.txt` fixture files; missing files raise SystemExit(2)."""
    task_dir = fixture_dir / task_slug
    fixtures: dict[str, list[str]] = {}
    for lang in languages:
        path = task_dir / f"{lang}.txt"
        if not path.is_file():
            print(
                f"agent-loop --mock: missing fixture {path} for "
                f"task={task_slug!r} lang={lang!r}",
                file=sys.stderr,
            )
            raise SystemExit(2)
        text = path.read_text(encoding="utf-8")
        # Multi-turn fixtures separate canned responses with a `---` line on its own.
        payloads = [chunk.strip("\n") + "\n" for chunk in text.split("\n---\n") if chunk.strip()]
        if not payloads:
            payloads = [text]
        fixtures[lang] = payloads
    return fixtures


def _cmd_one_shot(args: argparse.Namespace) -> int:
    spec, _, _ = load_task_spec(args.corpus_dir, args.task)
    languages = resolve_languages(spec, args.languages)
    if not languages:
        print(f"no matching languages for task {args.task!r}", file=sys.stderr)
        return 2
    client = _make_anthropic_client()
    with Storage(args.db) as store:
        run_id = store.start_run(
            model=args.model,
            corpus_sha=_corpus_sha(args.corpus_dir),
            mode="one_shot",
            metadata={"task": args.task, "languages": languages},
        )
        runner = OneShotRunner(
            storage=store,
            client=client,  # type: ignore[arg-type]
            corpus_dir=args.corpus_dir,
            zero_vendor_dir=args.vendor_zero_dir,
            model=args.model,
            max_tokens=args.max_tokens,
        )
        all_passed = True
        for lang in languages:
            try:
                result = runner.run_attempt(args.task, lang, run_id=run_id)
            except Exception as e:  # noqa: BLE001 — surface every failure mode
                print(f"ERROR: {lang}: {e}", file=sys.stderr)
                all_passed = False
                continue
            status = "PASS" if result.passed else "FAIL"
            print(
                f"{status}: {lang} (exit={result.verifier.exit_code}, "
                f"verify={result.verifier.wall_time_ms}ms, "
                f"run_id={run_id})"
            )
            if not result.passed:
                all_passed = False
        store.finish_run(run_id, status="completed" if all_passed else "failed")
        print(f"run_id={run_id} db={args.db}")
    return 0 if all_passed else 1


def _cmd_agent_loop(args: argparse.Namespace) -> int:
    spec, _, _ = load_task_spec(args.corpus_dir, args.task)
    languages = resolve_languages(spec, args.languages)
    if not languages:
        print(f"no matching languages for task {args.task!r}", file=sys.stderr)
        return 2
    if args.mock:
        fixtures = _load_mock_fixtures(args.mock_fixture_dir, args.task, languages)
        client: Any = _MockClient(fixtures=fixtures)
    else:
        client = _make_anthropic_client()
    zero_binary = args.zero_binary if args.zero_binary.exists() else None
    with Storage(args.db) as store:
        run_id = store.start_run(
            model=args.model,
            corpus_sha=_corpus_sha(args.corpus_dir),
            mode="agent_loop",
            metadata={
                "task": args.task,
                "languages": languages,
                "max_iters": args.max_iters,
                "mock": bool(args.mock),
            },
        )
        runner = AgentLoopRunner(
            storage=store,
            client=client,
            corpus_dir=args.corpus_dir,
            zero_vendor_dir=args.vendor_zero_dir,
            zero_binary=zero_binary,
            model=args.model,
            max_tokens=args.max_tokens,
            max_iters=args.max_iters,
        )
        all_passed = True
        for lang in languages:
            try:
                result = runner.run_attempt(args.task, lang, run_id=run_id)
            except Exception as e:  # noqa: BLE001 — surface every failure mode
                print(f"ERROR: {lang}: {e}", file=sys.stderr)
                all_passed = False
                continue
            status = "PASS" if result.passed else "FAIL"
            iters = result.metadata.get("iterations", 1)
            print(
                f"{status}: {lang} (iterations={iters}, "
                f"exit={result.verifier.exit_code}, "
                f"verify={result.verifier.wall_time_ms}ms, "
                f"run_id={run_id})"
            )
            if not result.passed:
                all_passed = False
        store.finish_run(run_id, status="completed" if all_passed else "failed")
        print(f"run_id={run_id} db={args.db}")
    return 0 if all_passed else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agentlang-run",
        description="AgentLang Index harness: one-shot, verify-task, list-tasks.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list-tasks", help="list every task in the corpus")
    _add_corpus_arg(p_list)
    p_list.set_defaults(func=_cmd_list_tasks)

    p_verify = sub.add_parser(
        "verify-task",
        help="run a task's reference impls through its verifier (no model call)",
    )
    _add_corpus_arg(p_verify)
    p_verify.add_argument("task", help="task slug, e.g. 000-hello-stdout")
    p_verify.add_argument(
        "--lang",
        dest="languages",
        action="append",
        choices=LANGUAGES,
        help="restrict to one or more languages (repeatable; default: all in spec)",
    )
    p_verify.set_defaults(func=_cmd_verify_task)

    p_one = sub.add_parser(
        "one-shot", help="prompt the model once per (task, language) and score it"
    )
    _add_corpus_arg(p_one)
    p_one.add_argument("task", help="task slug, e.g. 000-hello-stdout")
    p_one.add_argument(
        "--lang",
        dest="languages",
        action="append",
        choices=LANGUAGES,
        help="restrict to one or more languages (repeatable; default: all in spec)",
    )
    p_one.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Anthropic model id (default: {DEFAULT_MODEL})",
    )
    p_one.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"max output tokens per call (default: {DEFAULT_MAX_TOKENS})",
    )
    p_one.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"SQLite path for run/attempt persistence (default: {DEFAULT_DB_PATH})",
    )
    p_one.add_argument(
        "--vendor-zero-dir",
        type=Path,
        default=DEFAULT_VENDOR_ZERO_DIR,
        help=(
            "directory of vendored Zero skill markdown files; "
            f"default: {DEFAULT_VENDOR_ZERO_DIR}"
        ),
    )
    p_one.set_defaults(func=_cmd_one_shot)

    p_loop = sub.add_parser(
        "agent-loop",
        help="iterate the model with verifier diagnostics until pass or max-iters",
    )
    _add_corpus_arg(p_loop)
    p_loop.add_argument("task", help="task slug, e.g. 000-hello-stdout")
    p_loop.add_argument(
        "--lang",
        dest="languages",
        action="append",
        choices=LANGUAGES,
        help="restrict to one or more languages (repeatable; default: all in spec)",
    )
    p_loop.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Anthropic model id (default: {DEFAULT_MODEL})",
    )
    p_loop.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"max output tokens per call (default: {DEFAULT_MAX_TOKENS})",
    )
    p_loop.add_argument(
        "--max-iters",
        type=int,
        default=DEFAULT_MAX_ITERS,
        help=f"total turns including the first attempt (default: {DEFAULT_MAX_ITERS})",
    )
    p_loop.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"SQLite path for run/attempt persistence (default: {DEFAULT_DB_PATH})",
    )
    p_loop.add_argument(
        "--vendor-zero-dir",
        type=Path,
        default=DEFAULT_VENDOR_ZERO_DIR,
        help=(
            "directory of vendored Zero skill markdown files; "
            f"default: {DEFAULT_VENDOR_ZERO_DIR}"
        ),
    )
    p_loop.add_argument(
        "--zero-binary",
        type=Path,
        default=DEFAULT_ZERO_BINARY,
        help=(
            "path to the zero binary used for check/fix JSON diagnostics; "
            f"default: {DEFAULT_ZERO_BINARY}"
        ),
    )
    p_loop.add_argument(
        "--mock",
        action="store_true",
        help="replay canned responses from --mock-fixture-dir instead of calling the API",
    )
    p_loop.add_argument(
        "--mock-fixture-dir",
        type=Path,
        default=DEFAULT_MOCK_FIXTURE_DIR,
        help=(
            "directory with <task>/<lang>.txt fixtures used by --mock; "
            f"default: {DEFAULT_MOCK_FIXTURE_DIR}"
        ),
    )
    p_loop.set_defaults(func=_cmd_agent_loop)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
