```ts
// ref.ts
(async () => {
  try {
    let input = '';
    for await (const chunk of process.stdin) {
      input += chunk.toString('utf8');
    }

    const lines = input.split('\n');

    const parseU32 = (line: string | undefined): bigint | null => {
      if (line === undefined) return null;
      const s = line.trimEnd();
      if (s.length === 0) return null;
      if (!/^[0-9]+$/.test(s)) return null;
      try {
        const v = BigInt(s);
        if (v > 4294967295n) return null;
        return v;
      } catch {
        return null;
      }
    };

    const a = parseU32(lines[0]);
    const b = parseU32(lines[1]);

    let out: string;
    if (a === null || b === null || b === 0n) {
      out = 'error\n';
    } else {
      const q = a / b;
      out = q.toString() + '\n';
    }

    process.stdout.write(out);
  } catch {
    try {
      process.stdout.write('error\n');
    } catch {}
  }
})();
```