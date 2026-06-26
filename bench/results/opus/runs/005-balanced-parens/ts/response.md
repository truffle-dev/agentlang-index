```ts
let buf = '';
for await (const chunk of process.stdin) buf += chunk;
const line = buf.split('\n')[0] ?? '';
const stack: string[] = [];
const match: Record<string, string> = { ')': '(', ']': '[', '}': '{' };
let ok = true;
for (const c of line) {
  if (c === '(' || c === '[' || c === '{') stack.push(c);
  else if (c in match) {
    if (stack.pop() !== match[c]) { ok = false; break; }
  }
}
if (stack.length) ok = false;
process.stdout.write(ok ? 'yes\n' : 'no\n');
```