```ts
const chunks: Buffer[] = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const line = Buffer.concat(chunks).toString().replace(/\n$/, "");

const stack: string[] = [];
const match: Record<string, string> = { ")": "(", "]": "[", "}": "{" };
const openers = new Set(["(", "[", "{"]);
const closers = new Set([")", "]", "}"]);

let ok = true;
for (const ch of line) {
  if (openers.has(ch)) {
    stack.push(ch);
  } else if (closers.has(ch)) {
    if (stack.pop() !== match[ch]) { ok = false; break; }
  }
}

process.stdout.write(ok && stack.length === 0 ? "yes\n" : "no\n");
```