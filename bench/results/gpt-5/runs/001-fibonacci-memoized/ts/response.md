```ts
// ref.ts
let input = '';
(async () => {
  for await (const chunk of process.stdin) {
    input += chunk.toString();
  }
  const s = input.trim();
  const N = BigInt(s);

  const memo = new Map<bigint, bigint>();
  memo.set(0n, 0n);
  memo.set(1n, 1n);

  const fib = (n: bigint): bigint => {
    const cached = memo.get(n);
    if (cached !== undefined) return cached;
    const val = fib(n - 1n) + fib(n - 2n);
    memo.set(n, val);
    return val;
    };
  
  const result = fib(N);
  process.stdout.write(result.toString() + '\n');
})().catch(() => {
  // Per spec, no stderr; ensure exit 0 even on unexpected issues
  // Not specified to handle errors; avoid extra output
  process.stdout.write('');
});
```