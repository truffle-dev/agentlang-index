```ts
let buf = '';
for await (const chunk of process.stdin) buf += chunk;
const line = buf.endsWith('\n') ? buf.slice(0, -1) : buf;
if (line.length === 0 || !/^[a-z]+$/.test(line)) {
  process.stdout.write('error\n');
} else {
  let out = '';
  let i = 0;
  while (i < line.length) {
    const ch = line[i];
    let count = 1;
    while (i + count < line.length && line[i + count] === ch) count++;
    out += ch + count;
    i += count;
  }
  process.stdout.write(out + '\n');
}
```