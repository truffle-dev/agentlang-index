#!/usr/bin/env python3
"""Port a Zero 0.1.2 ref.zero to 0.3.4 syntax.

Transforms (in order):
  1. `pub fun ` -> `pub fn `, `fun ` -> `fn ` (keyword rename)
  2. `let mut <name>` -> `var <name>` (mutable bindings now use `var`)
  3. annotate inferred `let <name> = <rhs>` whose RHS type is known:
       std.args.get(...)   -> Maybe<String>
       std.args.len()      -> usize
       std.mem.span(...)    -> Span<u8>
       std.mem.len(...)     -> usize
       <ident>.value        -> String      (Maybe<String>.value)
       <span_ident>[<idx>]  -> u8          (Span<u8> / [N]u8 element)
Annotation only fires for lets that are NOT already type-annotated and whose
RHS matches one of the patterns above. Anything else is left untouched so the
compiler flags it loudly (better than guessing).
"""
import re
import sys

SPAN_ELEM_TYPE = "u8"  # all indexed lets in the non-HTTP corpus are byte spans

def annotate_type(rhs: str) -> str | None:
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
    return None

def port(text: str) -> tuple[str, list[str]]:
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
            t = annotate_type(rhs)
            if t is not None:
                line = f"{indent}let {name}: {t} = {rhs}"
            else:
                unhandled.append(line.strip())
        out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else ""), unhandled

if __name__ == "__main__":
    src = sys.stdin.read()
    ported, unhandled = port(src)
    sys.stdout.write(ported)
    if unhandled:
        sys.stderr.write("UNHANDLED inferred lets:\n")
        for u in unhandled:
            sys.stderr.write("  " + u + "\n")
