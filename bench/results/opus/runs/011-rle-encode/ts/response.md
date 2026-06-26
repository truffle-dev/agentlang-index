```ts
const chunks: Buffer[] = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const buf = Buffer.concat(chunks);
if (buf.length === 0) process.exit(0);
let i = 0;
while (i < buf.length) {
  const b = buf[i];
  let c = 1;
  while (i + c < buf.length && buf[i + c] === b) c++;
  process.stdout.write(`${c} ${b}\n`);
  i += c;
}
```