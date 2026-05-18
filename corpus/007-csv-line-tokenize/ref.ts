// CSV line tokenizer (RFC 4180 subset), TypeScript reference.
// Reads one line of CSV from stdin and writes each field on its own line.

import { readFileSync } from "node:fs";

const FIELD_START = 0;
const IN_UNQUOTED = 1;
const IN_QUOTED = 2;
const AFTER_CLOSING_QUOTE = 3;

function main(): void {
  let line = readFileSync(0, "utf8");
  if (line.endsWith("\n")) line = line.slice(0, -1);
  const out: string[] = [];
  let state = FIELD_START;
  if (line.length > 0) {
    for (const ch of line) {
      if (state === FIELD_START) {
        if (ch === '"') {
          state = IN_QUOTED;
        } else if (ch === ",") {
          out.push("\n");
        } else {
          out.push(ch);
          state = IN_UNQUOTED;
        }
      } else if (state === IN_UNQUOTED) {
        if (ch === ",") {
          out.push("\n");
          state = FIELD_START;
        } else {
          out.push(ch);
        }
      } else if (state === IN_QUOTED) {
        if (ch === '"') {
          state = AFTER_CLOSING_QUOTE;
        } else {
          out.push(ch);
        }
      } else if (state === AFTER_CLOSING_QUOTE) {
        if (ch === '"') {
          out.push('"');
          state = IN_QUOTED;
        } else if (ch === ",") {
          out.push("\n");
          state = FIELD_START;
        }
      }
    }
    out.push("\n");
  }
  process.stdout.write(out.join(""));
}

main();
