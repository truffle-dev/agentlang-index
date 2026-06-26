```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const input = Buffer.concat(buf).toString();
const lines = input.split('\n');
const line1 = (lines[0] ?? '').replace(/\s+$/,'');
const line2 = lines[1] ?? '';

if (!line1 || !/^\d+$/.test(line1)) { process.stdout.write('error\n'); process.exit(0); }
const shift = parseInt(line1, 10);
if (shift > 25) { process.stdout.write('error\n'); process.exit(0); }
if (!line2.length || !/^[a-z]+$/.test(line2)) { process.stdout.write('error\n'); process.exit(0); }

let out = '';
for (const ch of line2) out += String.fromCharCode(((ch.charCodeAt(0) - 97 + shift) % 26) + 97);
process.stdout.write(out + '\n');
```