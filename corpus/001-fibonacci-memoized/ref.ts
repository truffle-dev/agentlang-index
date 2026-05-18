// Fibonacci with memoization, TypeScript reference.
// Reads N from stdin, caches fib(i) in a Map, writes fib(N) + newline.
// BigInt sidesteps the 2^53 precision limit of JS number for large N.
// Annotations are kept minimal so the same source also runs under plain
// `node` (TS type stripping varies by runner — tsx/bun handle it, older
// nodes don't). The Map's value type is documented in the comment instead.

const chunks = [];
process.stdin.on("data", (c) => chunks.push(c));
process.stdin.on("end", () => {
  const input = Buffer.concat(chunks).toString("utf8").trim();
  const n = Number.parseInt(input, 10);
  if (!Number.isFinite(n) || n < 0) {
    process.stderr.write("N must be a non-negative integer\n");
    process.exit(1);
  }
  // memo: Map<number, bigint>
  const memo = new Map();
  memo.set(0, 0n);
  memo.set(1, 1n);
  const fib = (k) => {
    const cached = memo.get(k);
    if (cached !== undefined) return cached;
    const v = fib(k - 1) + fib(k - 2);
    memo.set(k, v);
    return v;
  };
  process.stdout.write(fib(n).toString() + "\n");
});
