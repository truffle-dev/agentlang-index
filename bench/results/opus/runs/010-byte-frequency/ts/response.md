```ts
const counts = new Uint32Array(256);
const chunks: Buffer[] = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const buf = Buffer.concat(chunks);
for (let i = 0; i < buf.length; i++) counts[buf[i]]++;
let out = '';
for (let b = 0; b < 256; b++) if (counts[b]) out += `${b} ${counts[b]}\n`;
process.stdout.write(out);
```