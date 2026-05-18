// Count whitespace-separated tokens in input, TypeScript reference.

import { readFileSync } from "node:fs";

function main(): void {
  const data = readFileSync(0);
  let count = 0;
  let inWord = false;
  for (let i = 0; i < data.length; i++) {
    const b = data[i];
    const isWS = b === 32 || b === 9 || b === 10 || b === 13;
    if (isWS) {
      inWord = false;
    } else if (!inWord) {
      count++;
      inWord = true;
    }
  }
  process.stdout.write(`${count}\n`);
}

main();
