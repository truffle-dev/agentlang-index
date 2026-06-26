```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const n = parseInt(Buffer.concat(buf).toString().trim(), 10);
const memo = new Map<number, bigint>();
function fib(k: number): bigint {
  if (k <= 0) return 0n;
  if (k === 1) return 1n;
  if (memo.has(k)) return memo.get(k)!;
  const v = fib(k - 1) + fib(k - 2);
  memo.set(k, v);
  return v;
}
process.stdout.write(fib(n).toString() + "\n");
```