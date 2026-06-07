"""Model-call providers used by the runner.

The runner depends on the `AnthropicClient` Protocol in `runner.py`:
a `.messages.create(model, max_tokens, system, messages, ...)` callable
returning an object with `.content: list[TextBlock]` and `.usage`. Any
module here that satisfies that shape can drive the harness.
"""
