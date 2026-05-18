// Balanced bracket checker, TypeScript reference.
// Reads one line of printable ASCII (up to 1000 chars), prints `yes` or `no`.

import { readFileSync } from "node:fs";

function main(): void {
  let line = readFileSync(0, "utf8");
  if (line.endsWith("\n")) line = line.slice(0, -1);
  const stack: string[] = [];
  const pairs: Record<string, string> = { ")": "(", "]": "[", "}": "{" };
  let balanced = true;
  for (const ch of line) {
    if (ch === "(" || ch === "[" || ch === "{") {
      stack.push(ch);
    } else if (ch === ")" || ch === "]" || ch === "}") {
      if (stack.length === 0 || stack[stack.length - 1] !== pairs[ch]) {
        balanced = false;
        break;
      }
      stack.pop();
    }
  }
  if (balanced && stack.length === 0) {
    process.stdout.write("yes\n");
  } else {
    process.stdout.write("no\n");
  }
}

main();
