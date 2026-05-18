// Reverse the order of words on a line, TypeScript reference.

import { readFileSync } from "node:fs";

function main(): void {
  let line = readFileSync(0, "utf8");
  if (line.endsWith("\n")) line = line.slice(0, -1);
  const words = line.split(" ").filter((w) => w.length > 0);
  if (words.length === 0) return;
  words.reverse();
  process.stdout.write(words.join(" ") + "\n");
}

main();
