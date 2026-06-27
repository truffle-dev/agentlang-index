```ts
import { createInterface } from "readline";

const rl = createInterface({ input: process.stdin });
rl.once("line", (line) => {
  const n = parseInt(line.trim(), 10);
  if (n < 2) {
    process.stdout.write("0\n");
    return;
  }
  const sieve = new Uint8Array(n + 1).fill(1);
  sieve[0] = 0;
  sieve[1] = 0;
  for (let i = 2; i * i <= n; i++) {
    if (sieve[i]) {
      for (let j = i * i; j <= n; j += i) {
        sieve[j] = 0;
      }
    }
  }
  let count = 0;
  for (let i = 2; i <= n; i++) {
    if (sieve[i]) count++;
  }
  process.stdout.write(count + "\n");
  rl.close();
});
```