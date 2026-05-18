// Non-overlapping substring count, TypeScript reference.
// Reads pattern P from line 1 of stdin and text T from line 2.

import { readFileSync } from "node:fs";

function main(): void {
  const raw = readFileSync(0, "utf8");
  const lines = raw.split("\n");
  const p = lines[0] ?? "";
  const t = lines[1] ?? "";
  let count = 0;
  if (p.length > 0) {
    let i = 0;
    const n = t.length;
    const m = p.length;
    while (i + m <= n) {
      if (t.substring(i, i + m) === p) {
        count++;
        i += m;
      } else {
        i++;
      }
    }
  }
  process.stdout.write(`${count}\n`);
}

main();
