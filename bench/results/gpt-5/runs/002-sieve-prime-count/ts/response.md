```ts
// ref.ts
(async () => {
  let input = '';
  for await (const chunk of process.stdin) {
    input += chunk;
  }
  const s = input.trim();
  let N = parseInt(s, 10);
  if (!Number.isFinite(N) || isNaN(N)) N = 0;
  if (N < 2) {
    process.stdout.write('0\n');
    return;
  }

  const isPrime = new Uint8Array(N + 1);
  isPrime.fill(1, 2); // mark 2..N as prime initially

  for (let p = 2; p * p <= N; p++) {
    if (isPrime[p]) {
      for (let m = p * p; m <= N; m += p) {
        isPrime[m] = 0;
      }
    }
  }

  let count = 0;
  for (let i = 2; i <= N; i++) {
    if (isPrime[i]) count++;
  }

  process.stdout.write(String(count) + '\n');
})();
```