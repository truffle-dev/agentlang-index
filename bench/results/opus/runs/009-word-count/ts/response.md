```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const s = Buffer.concat(buf).toString();
const words = s.split(/[\x20\x09\x0A\x0D]+/).filter(w => w.length > 0);
process.stdout.write(words.length + "\n");
```