```ts
const chunks: Buffer[] = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const n = parseInt(Buffer.concat(chunks).toString().trim(), 10);
const memo = new Map<number, bigint>();
function fib(n: number): bigint {
  if (n === 0) return 0n;
  if (n === 1) return 1n;
  if (memo.has(n)) return memo.get(n)!;
  const result = fib(n - 1) + fib(n - 2);
  memo.set(n, result);
  return result;
}
process.stdout.write(fib(n).toString() + "\n");
```