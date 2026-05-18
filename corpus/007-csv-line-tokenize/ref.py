"""CSV line tokenizer (RFC 4180 subset), Python reference.

Reads one line of CSV from stdin and writes each field on its own line.
Uses an explicit state machine rather than the csv module to keep parity
with the other language references (and to make the trap shape - empty
input vs ",," vs '""' - explicit).
"""
import sys

FIELD_START = 0
IN_UNQUOTED = 1
IN_QUOTED = 2
AFTER_CLOSING_QUOTE = 3


def main() -> None:
    line = sys.stdin.readline()
    if line.endswith("\n"):
        line = line[:-1]
    out = []
    state = FIELD_START
    if line:
        for ch in line:
            if state == FIELD_START:
                if ch == '"':
                    state = IN_QUOTED
                elif ch == ",":
                    out.append("\n")
                else:
                    out.append(ch)
                    state = IN_UNQUOTED
            elif state == IN_UNQUOTED:
                if ch == ",":
                    out.append("\n")
                    state = FIELD_START
                else:
                    out.append(ch)
            elif state == IN_QUOTED:
                if ch == '"':
                    state = AFTER_CLOSING_QUOTE
                else:
                    out.append(ch)
            elif state == AFTER_CLOSING_QUOTE:
                if ch == '"':
                    out.append('"')
                    state = IN_QUOTED
                elif ch == ",":
                    out.append("\n")
                    state = FIELD_START
        out.append("\n")
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
