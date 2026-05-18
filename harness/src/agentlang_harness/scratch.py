"""Scratch directories for model-written source under test."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterator
from contextlib import contextmanager

from .types import LANGUAGE_FILENAME, Language


@contextmanager
def scratch_for_attempt(
    task_dir: Path, language: Language, source: str
) -> Iterator[Path]:
    """Materialize a task directory with model-written source for one language.

    Copies the task's auxiliary files (Cargo.toml, go.mod, etc.) into a
    fresh tempdir, drops the model's source as the canonical ref.<ext>
    filename, and yields the path. The directory is removed on exit.
    """
    scratch = Path(tempfile.mkdtemp(prefix=f"agentlang-{language}-"))
    try:
        # Copy aux files (Cargo.toml, go.mod, etc.) so language toolchains
        # that need a manifest still find one. Reference impls are
        # overwritten by the model output below.
        for entry in task_dir.iterdir():
            if entry.is_file() and entry.name not in {"verify.sh"}:
                shutil.copy2(entry, scratch / entry.name)
        target = scratch / LANGUAGE_FILENAME[language]
        target.write_text(source, encoding="utf-8")
        # Also drop verify.sh in, with exec bit, so the runner can invoke
        # it in-place.
        verifier = task_dir / "verify.sh"
        if verifier.exists():
            dest = scratch / "verify.sh"
            shutil.copy2(verifier, dest)
            dest.chmod(0o755)
        yield scratch
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
