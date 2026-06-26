```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const lines = Buffer.concat(buf).toString().split('\n');
const a = lines[0] ?? '';
const b = lines[1] ?? '';
const m = a.length, n = b.length;
const dp = new Uint16Array(n + 1);
for (let j = 0; j <= n; j++) dp[j] = j;
for (let i = 1; i <= m; i++) {
  let prev = dp[0];
  dp[0] = i;
  for (let j = 1; j <= n; j++) {
    const tmp = dp[j];
    dp[j] = a[i - 1] === b[j - 1] ? prev : 1 + Math.min(prev, dp[j], dp[j - 1]);
    prev = tmp;
  }
}
process.stdout.write(dp[n] + '\n');
```