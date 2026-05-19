```ts
// ref.ts
async function main() {
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    if (typeof chunk === "string") {
      chunks.push(Buffer.from(chunk));
    } else {
      chunks.push(Buffer.from(chunk));
    }
  }
  const buf = Buffer.concat(chunks);

  const nlIndex = buf.indexOf(0x0a); // '\n'
  if (nlIndex === -1) {
    process.stdout.write("error\n");
    return;
  }
  // Ensure exactly one trailing '\n' and nothing else afterward
  if (nlIndex !== buf.length - 1) {
    process.stdout.write("error\n");
    return;
  }

  const line = buf.subarray(0, nlIndex);
  if (line.length === 0) {
    process.stdout.write("error\n");
    return;
  }

  // Validate all bytes are 'a'..'z'
  for (let i = 0; i < line.length; i++) {
    const b = line[i];
    if (b < 0x61 || b > 0x7a) { // not 'a'..'z'
      process.stdout.write("error\n");
      return;
    }
  }

  let i = 0;
  let out = "";
  while (i < line.length) {
    const b = line[i];
    let j = i + 1;
    while (j < line.length && line[j] === b) j++;
    const runLen = j - i;
    out += String.fromCharCode(b) + runLen.toString(10);
    i = j;
  }
  out += "\n";
  process.stdout.write(out);
}

main();
```