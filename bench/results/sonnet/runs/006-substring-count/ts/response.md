```ts
import * as readline from "readline";

const rl = readline.createInterface({ input: process.stdin });
const lines: string[] = [];
rl.on("line", (line) => lines.push(line));
rl.on("close", () => {
  const P = lines[0] ?? "";
  const T = lines[1] ?? "";
  let count = 0;
  let i = 0;
  while (i <= T.length - P.length) {
    if (T.substring(i, i + P.length) === P) {
      count++;
      i += P.length;
    } else {
      i++;
    }
  }
  process.stdout.write(count + "\n");
});
```