```ts
import * as readline from "readline";

const rl = readline.createInterface({ input: process.stdin, terminal: false });
const lines: string[] = [];

rl.on("line", (line) => lines.push(line));
rl.on("close", () => {
  if (lines.length < 2) {
    process.stdout.write("error\n");
    return;
  }

  const shiftStr = lines[0].trimEnd();
  const plaintext = lines[1];

  if (!/^\d+$/.test(shiftStr)) {
    process.stdout.write("error\n");
    return;
  }

  const shift = parseInt(shiftStr, 10);
  if (shift > 25) {
    process.stdout.write("error\n");
    return;
  }

  if (plaintext.length === 0) {
    process.stdout.write("error\n");
    return;
  }

  for (let i = 0; i < plaintext.length; i++) {
    const c = plaintext.charCodeAt(i);
    if (c < 97 || c > 122) {
      process.stdout.write("error\n");
      return;
    }
  }

  let result = "";
  for (let i = 0; i < plaintext.length; i++) {
    const c = plaintext.charCodeAt(i) - 97;
    result += String.fromCharCode(((c + shift) % 26) + 97);
  }

  process.stdout.write(result + "\n");
});
```