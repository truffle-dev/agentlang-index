```ts
import * as readline from "readline";

const rl = readline.createInterface({ input: process.stdin });
const lines: string[] = [];

rl.on("line", (line) => lines.push(line.trim()));
rl.on("close", () => {
  let idx = 0;
  const N = parseInt(lines[idx++]);
  const A: number[][] = [];
  const B: number[][] = [];
  for (let i = 0; i < N; i++) {
    A.push(lines[idx++].split(" ").map(Number));
  }
  for (let i = 0; i < N; i++) {
    B.push(lines[idx++].split(" ").map(Number));
  }
  const C: number[][] = Array.from({ length: N }, () => new Array(N).fill(0));
  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      for (let k = 0; k < N; k++) {
        C[i][j] += A[i][k] * B[k][j];
      }
    }
  }
  const out = C.map((row) => row.join(" ")).join("\n") + "\n";
  process.stdout.write(out);
});
```