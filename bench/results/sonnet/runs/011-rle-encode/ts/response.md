```ts
import { Buffer } from "buffer";

const chunks: Buffer[] = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const data = Buffer.concat(chunks);

if (data.length === 0) process.exit(0);

let cur = data[0], count = 1;
for (let i = 1; i < data.length; i++) {
  if (data[i] === cur) { count++; }
  else { process.stdout.write(`${count} ${cur}\n`); cur = data[i]; count = 1; }
}
process.stdout.write(`${count} ${cur}\n`);
```