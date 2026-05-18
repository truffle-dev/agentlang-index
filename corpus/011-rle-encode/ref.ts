// Run-length encode the input, TypeScript reference.

import { readFileSync } from "node:fs";

function main(): void {
  const data = readFileSync(0);
  if (data.length === 0) return;
  const out: string[] = [];
  let curByte = data[0];
  let curCount = 1;
  for (let i = 1; i < data.length; i++) {
    const b = data[i];
    if (b === curByte) {
      curCount++;
    } else {
      out.push(`${curCount} ${curByte}\n`);
      curByte = b;
      curCount = 1;
    }
  }
  out.push(`${curCount} ${curByte}\n`);
  process.stdout.write(out.join(""));
}

main();
