// Square integer matrix multiply, TypeScript reference.
// Reads N, then N rows of A, then N rows of B, prints rows of C = A * B.
import { readFileSync } from "node:fs";

const raw = readFileSync(0, "utf8");
const tokens = raw.split(/\s+/).filter((t) => t.length > 0);
let pos = 0;
const n = Number.parseInt(tokens[pos++], 10);
if (!Number.isInteger(n) || n < 1 || n > 5) {
  process.stderr.write("N must be in [1, 5]\n");
  process.exit(1);
}

const a: number[][] = [];
const b: number[][] = [];
for (let i = 0; i < n; i++) {
  const row: number[] = [];
  for (let j = 0; j < n; j++) row.push(Number.parseInt(tokens[pos++], 10));
  a.push(row);
}
for (let i = 0; i < n; i++) {
  const row: number[] = [];
  for (let j = 0; j < n; j++) row.push(Number.parseInt(tokens[pos++], 10));
  b.push(row);
}

const rows: string[] = [];
for (let i = 0; i < n; i++) {
  const cells: string[] = [];
  for (let j = 0; j < n; j++) {
    let s = 0;
    for (let k = 0; k < n; k++) s += a[i][k] * b[k][j];
    cells.push(String(s));
  }
  rows.push(cells.join(" "));
}
process.stdout.write(rows.join("\n") + "\n");
