```ts
import * as readline from 'readline';

async function main() {
  const lines: string[] = [];
  const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
  for await (const line of rl) {
    lines.push(line);
  }

  const U32_MAX = 4294967295n;

  function parseU32(s: string): bigint | null {
    const trimmed = s.trimEnd();
    if (!/^\d+$/.test(trimmed)) return null;
    const val = BigInt(trimmed);
    if (val > U32_MAX) return null;
    return val;
  }

  if (lines.length === 0) {
    process.stdout.write('error\n');
    return;
  }

  const nVal = parseU32(lines[0].trimEnd());
  if (nVal === null || nVal > 1000n) {
    process.stdout.write('error\n');
    return;
  }

  const n = Number(nVal);
  if (lines.length - 1 < n) {
    process.stdout.write('error\n');
    return;
  }

  let sum = 0n;
  for (let i = 1; i <= n; i++) {
    const val = parseU32(lines[i].trimEnd());
    if (val === null) {
      process.stdout.write('error\n');
      return;
    }
    sum += val;
    if (sum > U32_MAX) {
      process.stdout.write('error\n');
      return;
    }
  }

  process.stdout.write(sum.toString() + '\n');
}

main();
```