"""`agentlang-run` CLI entrypoint with one-shot, verify-task, list-tasks verbs."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Sequence

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
DEFAULT_DB_PATH = REPO_ROOT_GUESS / "harness" / "runs.db"


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
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
