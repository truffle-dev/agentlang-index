```ts
import { createInterface } from "readline";

const rl = createInterface({ input: process.stdin, crlfDelay: Infinity });
rl.once("line", (line) => {
  const words = line.trim().split(/\s+/).filter(Boolean);
  if (words.length > 0) {
    process.stdout.write(words.reverse().join(" ") + "\n");
  }
  rl.close();
});
```