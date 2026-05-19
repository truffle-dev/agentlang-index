```ts
// ref.ts
(async () => {
  let count = 0;
  let inWord = false;

  for await (const chunk of process.stdin) {
    const buf: Buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk as any);
    for (let i = 0; i < buf.length; i++) {
      const b = buf[i];
      if (b === 0x20 || b === 0x09 || b === 0x0A || b === 0x0D) {
        inWord = false;
      } else {
        if (!inWord) {
          count++;
          inWord = true;
        }
      }
    }
  }

  process.stdout.write(String(count) + "\n");
})().catch(() => {
  try {
    process.stdout.write("0\n");
  } catch {}
});
```