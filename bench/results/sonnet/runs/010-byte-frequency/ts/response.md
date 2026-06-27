```ts
import { Buffer } from "buffer";

const counts = new Uint32Array(256);
for await (const chunk of process.stdin) {
  const buf = Buffer.from(chunk);
  for (let i = 0; i < buf.length; i++) counts[buf[i]]++;
}
const out: string[] = [];
for (let b = 0; b < 256; b++) {
  if (counts[b] > 0) out.push(`${b} ${counts[b]}\n`);
}
process.stdout.write(out.join(""));
```