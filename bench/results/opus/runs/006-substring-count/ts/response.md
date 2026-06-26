```ts
const chunks: Buffer[] = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const [P, T] = Buffer.concat(chunks).toString().split('\n');
let count = 0;
let i = 0;
while (i <= T.length - P.length) {
  if (T.startsWith(P, i)) { count++; i += P.length; } else { i++; }
}
process.stdout.write(count + '\n');
```