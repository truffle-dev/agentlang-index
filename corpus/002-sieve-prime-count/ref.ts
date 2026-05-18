// Prime count via Sieve of Eratosthenes, TypeScript reference.
// Reads N from stdin, runs a byte-flag sieve, counts unmarked [2, N].
import { readFileSync } from "node:fs";

const input = readFileSync(0, "utf8").trim();
const n = Number.parseInt(input, 10);
if (!Number.isInteger(n) || n < 0) {
  process.stderr.write("N must be a non-negative integer\n");
  process.exit(1);
}

if (n < 2) {
  process.stdout.write("0\n");
} else {
  const composite = new Uint8Array(n + 1);
  for (let i = 2; i * i <= n; i++) {
    if (composite[i] === 0) {
      for (let j = i * i; j <= n; j += i) {
        composite[j] = 1;
      }
    }
  }
  let count = 0;
  for (let k = 2; k <= n; k++) {
    if (composite[k] === 0) count++;
  }
  process.stdout.write(`${count}\n`);
}
