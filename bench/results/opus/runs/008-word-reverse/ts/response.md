```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const words = Buffer.concat(buf).toString().trim().split(/\s+/).filter(Boolean);
if (words.length) process.stdout.write(words.reverse().join(' ') + '\n');
```