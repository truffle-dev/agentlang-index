```ts
const chunks: Buffer[] = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const lines = Buffer.concat(chunks).toString().split('\n');

const U32_MAX = 4294967295;

function parseU32(s: string): number | null {
  s = s.trimEnd();
  if (s.length === 0 || /[^0-9]/.test(s)) return null;
  const n = Number(s);
  if (n > U32_MAX) return null;
  return n;
}

const err = () => { process.stdout.write('error\n'); process.exit(0); };

const n = parseU32(lines[0] ?? '');
if (n === null || n > 1000) err();

if (lines.length - 1 < n!) err();

let sum = 0;
for (let i = 1; i <= n!; i++) {
  const v = parseU32(lines[i] ?? '');
  if (v === null) err();
  sum += v!;
  if (sum > U32_MAX) err();
}

process.stdout.write(sum + '\n');
```