```ts
// ref.ts
async function main(): Promise<void> {
  const counts: number[] = new Array(256).fill(0);

  for await (const chunk of process.stdin) {
    const buf: Buffer = chunk as Buffer;
    for (let i = 0; i < buf.length; i++) {
      counts[buf[i]]++;
    }
  }

  const outParts: string[] = [];
  for (let i = 0; i < 256; i++) {
    const c = counts[i];
    if (c !== 0) {
      outParts.push(String(i), " ", String(c), "\n");
    }
  }

  if (outParts.length > 0) {
    process.stdout.write(outParts.join(""));
  }
}

main().catch(() => {});
```