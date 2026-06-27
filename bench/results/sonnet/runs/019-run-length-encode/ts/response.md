```ts
import { Buffer } from "buffer";

let input = "";
for await (const chunk of process.stdin) {
  input += Buffer.isBuffer(chunk) ? chunk.toString("binary") : chunk;
}

// Must end with \n and have at least one char before it
if (!input.endsWith("\n")) {
  process.stdout.write("error\n");
  process.exit(0);
}

const line = input.slice(0, -1);

if (line.length === 0) {
  process.stdout.write("error\n");
  process.exit(0);
}

for (let i = 0; i < line.length; i++) {
  const c = line.charCodeAt(i);
  if (c < 97 || c > 122) {
    process.stdout.write("error\n");
    process.exit(0);
  }
}

let out = "";
let i = 0;
while (i < line.length) {
  const ch = line[i];
  let count = 1;
  while (i + count < line.length && line[i + count] === ch) {
    count++;
  }
  out += ch + count.toString();
  i += count;
}
out += "\n";
process.stdout.write(out);
```