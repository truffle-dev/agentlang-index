```ts
import * as readline from "readline";

const rl = readline.createInterface({ input: process.stdin });
const lines: string[] = [];

rl.on("line", (line) => lines.push(line));
rl.on("close", () => {
  const a = lines[0] ?? "";
  const b = lines[1] ?? "";
  const m = a.length, n = b.length;
  const dp: number[] = Array.from({ length: n + 1 }, (_, i) => i);
  for (let i = 1; i <= m; i++) {
    let prev = dp[0];
    dp[0] = i;
    for (let j = 1; j <= n; j++) {
      const temp = dp[j];
      dp[j] = a[i-1] === b[j-1] ? prev : 1 + Math.min(prev, dp[j], dp[j-1]);
      prev = temp;
    }
  }
  process.stdout.write(dp[n] + "\n");
});
```