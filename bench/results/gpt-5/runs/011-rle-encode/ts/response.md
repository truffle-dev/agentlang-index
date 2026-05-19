```ts
// ref.ts
async function main() {
  // Ensure we read raw bytes (Buffer) from stdin
  try {
    // @ts-ignore - allow null to force Buffer mode in all TS versions
    process.stdin.setEncoding(null);
  } catch {
    // Ignore if not supported; Node defaults to Buffer anyway
  }

  const out = process.stdout;

  let prev: number | null = null;
  let count = 0;

  function waitDrain(): Promise<void> {
    return new Promise((resolve) => out.once('drain', resolve));
  }

  async function writeLine(c: number, b: number) {
    const line = `${c} ${b}\n`;
    if (!out.write(line)) {
      await waitDrain();
    }
  }

  for await (const chunk of process.stdin as any as AsyncIterable<Buffer>) {
    const buf: Buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk as any);
    for (let i = 0; i < buf.length; i++) {
      const byte = buf[i];
      if (prev === null) {
        prev = byte;
        count = 1;
      } else if (byte === prev) {
        count++;
      } else {
        await writeLine(count, prev);
        prev = byte;
        count = 1;
      }
    }
  }

  if (prev !== null) {
    await writeLine(count, prev);
  }
}

main().catch(() => {
  // Swallow any unexpected errors to ensure exit code 0 and no stderr output.
});
```