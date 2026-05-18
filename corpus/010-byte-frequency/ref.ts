// Per-byte frequency table, TypeScript reference.

import { readFileSync } from "node:fs";

function main(): void {
  const data = readFileSync(0);
  const counts = new Uint32Array(256);
  for (let i = 0; i < data.length; i++) {
    counts[data[i]]++;
  }
  const out: string[] = [];
  for (let b = 0; b < 256; b++) {
    const c = counts[b];
    if (c > 0) {
      out.push(`${b} ${c}\n`);
    }
  }
  process.stdout.write(out.join(""));
}

main();
