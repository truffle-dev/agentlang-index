// Levenshtein edit distance, TypeScript reference.
// Reads A and B from stdin (one per line), runs a two-row DP.
import { readFileSync } from "node:fs";

const raw = readFileSync(0, "utf8");
const lines = raw.split("\n");
const a = lines[0] ?? "";
const b = lines[1] ?? "";
if (a.length > 50 || b.length > 50) {
  process.stderr.write("each string must be at most 50 characters\n");
  process.exit(1);
}

const m = a.length;
const n = b.length;
let prev = new Array<number>(n + 1);
let curr = new Array<number>(n + 1);
for (let j = 0; j <= n; j++) prev[j] = j;
for (let i = 0; i < m; i++) {
  curr[0] = i + 1;
  const ai = a.charCodeAt(i);
  for (let k = 0; k < n; k++) {
    const delCost = prev[k + 1] + 1;
    const insCost = curr[k] + 1;
    const subCost = prev[k] + (ai === b.charCodeAt(k) ? 0 : 1);
    curr[k + 1] = Math.min(delCost, insCost, subCost);
  }
  [prev, curr] = [curr, prev];
}
process.stdout.write(`${prev[n]}\n`);
