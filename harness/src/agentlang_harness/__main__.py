"""Entry point so `python -m agentlang_harness ...` works the same as `agentlang-run`."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
