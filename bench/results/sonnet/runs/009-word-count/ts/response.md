```ts
import { createInterface } from "readline";

let inWord = false;
let count = 0;

const rl = createInterface({ input: process.stdin, terminal: false });

for await (const line of rl) {
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    const ws = c === " " || c === "\t" || c === "\r";
    if (!ws) {
      if (!inWord) { count++; inWord = true; }
    } else {
      inWord = false;
    }
  }
  inWord = false; // newline resets word
}

process.stdout.write(count + "\n");
```