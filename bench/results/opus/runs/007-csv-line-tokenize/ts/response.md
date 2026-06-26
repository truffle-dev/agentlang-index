```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const line = Buffer.concat(buf).toString().replace(/\n$/, '');
if (line.length === 0) process.exit(0);

const fields: string[] = [];
let i = 0;
while (i <= line.length) {
  if (i < line.length && line[i] === '"') {
    i++;
    let f = '';
    while (i < line.length) {
      if (line[i] === '"' && i + 1 < line.length && line[i + 1] === '"') {
        f += '"';
        i += 2;
      } else if (line[i] === '"') {
        i++;
        break;
      } else {
        f += line[i++];
      }
    }
    fields.push(f);
    if (i < line.length && line[i] === ',') i++;
  } else {
    const comma = line.indexOf(',', i);
    if (comma === -1) {
      fields.push(line.slice(i));
      break;
    } else {
      fields.push(line.slice(i, comma));
      i = comma + 1;
      if (i === line.length) { fields.push(''); break; }
    }
  }
}

for (const f of fields) process.stdout.write(f + '\n');
```