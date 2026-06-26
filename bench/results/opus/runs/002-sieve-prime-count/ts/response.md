```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const N = parseInt(Buffer.concat(buf).toString().trim(), 10);
if (N < 2) { process.stdout.write("0\n"); process.exit(0); }
const sieve = new Uint8Array(N + 1).fill(1);
sieve[0] = 0; sieve[1] = 0;
for (let i = 2; i * i <= N; i++) {
  if (sieve[i]) for (let j = i * i; j <= N; j += i) sieve[j] = 0;
}
let count = 0;
for (let i = 2; i <= N; i++) if (sieve[i]) count++;
process.stdout.write(count + "\n");
```