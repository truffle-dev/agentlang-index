```ts
import { createInterface } from "readline";

async function main() {
  const lines: string[] = [];
  const rl = createInterface({ input: process.stdin });
  for await (const line of rl) {
    lines.push(line);
    if (lines.length === 2) break;
  }

  const U32_MAX = 4294967295n;

  function parseU32(s: string): bigint | null {
    const trimmed = s.trimEnd();
    if (!/^\d+$/.test(trimmed)) return null;
    const n = BigInt(trimmed);
    if (n > U32_MAX) return null;
    return n;
  }

  const a = parseU32(lines[0] ?? "");
  const b = parseU32(lines[1] ?? "");

  if (a === null || b === null || b === 0n) {
    process.stdout.write("error\n");
    process.exit(0);
  }

  process.stdout.write((a / b).toString() + "\n");
}

main();
```