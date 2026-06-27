#!/usr/bin/env python3
"""Port a Zero 0.1.2 ref.zero to 0.3.4 syntax.

Transforms (in order):
  1. `pub fun ` -> `pub fn `, `fun ` -> `fn ` (keyword rename)
  2. `let mut <name>` -> `var <name>` (mutable bindings now use `var`)
  3. annotate inferred `let <name> = <rhs>` whose RHS type is known:
       std.args.get(...)        -> Maybe<String>
       std.args.len()           -> usize
       std.mem.span(...)         -> Span<u8>
       std.mem.len(...)          -> usize
       <ident>.value             -> String   (Maybe<String>.value)
       <span_ident>[<idx>]       -> u8        (Span<u8> / [N]u8 element)
       <userfn>(...)             -> declared return type of <userfn>
       <typed-literal arithmetic> -> the literal's suffix type (e.g. 1_u32 -> u32)

The user-fn return types are read, not guessed: the porter scans the source it
is porting plus any sibling .0 files passed as argv for `pub fn NAME(..) -> RET`
(and bare `fn`) signatures and uses the declared RET. For package tasks, pass
every src/*.0 file so cross-file calls (e.g. main.0 calling lib.0) resolve.

Annotation only fires for lets that are NOT already type-annotated and whose
RHS matches one of the patterns above. Anything else is left untouched so the
compiler flags it loudly (better than guessing).

Usage:
  port_ref.py [sibling1.0 sibling2.0 ...] < ref.zero > ported.0
"""
import re
import sys

SPAN_ELEM_TYPE = "u8"  # all indexed lets in the non-HTTP corpus are byte spans

# `pub fn NAME(...) -> RET` / `fn NAME(...) -> RET`; RET may be generic
# (Maybe<String>) and may be followed by `raises` / `{`.
_FN_SIG = re.compile(
    r"\b(?:pub\s+)?(?:fun|fn)\s+([A-Za-z_]\w*)\s*\([^)]*\)\s*->\s*([A-Za-z_][\w<>]*)"
)


def scan_fn_returns(texts: list[str]) -> dict[str, str]:
    """Build {fn_name: declared_return_type} from the given source texts."""
    returns: dict[str, str] = {}
    for text in texts:
        for m in _FN_SIG.finditer(text):
            returns.setdefault(m.group(1), m.group(2))
    return returns


def arith_literal_type(rhs: str) -> str | None:
    """Infer the type of a pure typed-literal arithmetic expression.

    Fires only when the RHS has no field access, no indexing, and no call,
    contains an arithmetic operator, and carries a typed numeric literal
    (e.g. `emit_i - 1_u32` -> u32). Returns None otherwise.
    """
    if "[" in rhs or "." in rhs:
        return None
    if re.search(r"[A-Za-z_]\w*\s*\(", rhs):  # function call
        return None
    if not re.search(r"[-+*/%]", rhs):
        return None
    m = re.search(r"\b\d+_([a-z]\w*)\b", rhs)
    return m.group(1) if m else None


def annotate_type(rhs: str, fn_returns: dict[str, str]) -> str | None:
    rhs = rhs.strip()
    if re.match(r"std\.args\.get\(", rhs):
        return "Maybe<String>"
    if re.match(r"std\.args\.len\(\)", rhs):
        return "usize"
    if re.match(r"std\.mem\.span\(", rhs):
        return "Span<u8>"
    if re.match(r"std\.mem\.len\(", rhs):
        return "usize"
    if re.match(r"[A-Za-z_][A-Za-z0-9_]*\.value\s*$", rhs):
        return "String"
    if re.match(r"[A-Za-z_][A-Za-z0-9_]*\[[^\]]+\]\s*$", rhs):
        return SPAN_ELEM_TYPE
    # user-fn call: NAME(args) with a known declared return type
    m = re.match(r"([A-Za-z_]\w*)\s*\(", rhs)
    if m and m.group(1) in fn_returns and rhs.endswith(")"):
        return fn_returns[m.group(1)]
    # typed-literal arithmetic
    return arith_literal_type(rhs)


def port(text: str, fn_returns: dict[str, str]) -> tuple[str, list[str]]:
    unhandled: list[str] = []
    out_lines = []
    for line in text.splitlines():
        # 1. keyword rename
        line = re.sub(r"\bpub fun\b", "pub fn", line)
        line = re.sub(r"\bfun\b", "fn", line)
        # 2. let mut -> var
        line = re.sub(r"\blet mut\b", "var", line)
        # 3. annotate inferred lets (only un-annotated `let name = rhs`)
        m = re.match(r"^(\s*)let ([A-Za-z_][A-Za-z0-9_]*) = (.+)$", line)
        if m:
            indent, name, rhs = m.group(1), m.group(2), m.group(3)
            t = annotate_type(rhs, fn_returns)
            if t is not None:
                line = f"{indent}let {name}: {t} = {rhs}"
            else:
                unhandled.append(line.strip())
        out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else ""), unhandled


if __name__ == "__main__":
    src = sys.stdin.read()
    sibling_texts = []
    for path in sys.argv[1:]:
        try:
            with open(path, encoding="utf-8") as fh:
                sibling_texts.append(fh.read())
        except OSError as exc:
            sys.stderr.write(f"warning: could not read sibling {path}: {exc}\n")
    fn_returns = scan_fn_returns([src, *sibling_texts])
    ported, unhandled = port(src, fn_returns)
    sys.stdout.write(ported)
    if unhandled:
        sys.stderr.write("UNHANDLED inferred lets:\n")
        for u in unhandled:
            sys.stderr.write("  " + u + "\n")
