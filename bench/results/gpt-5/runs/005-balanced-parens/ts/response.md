```ts
// ref.ts
(async () => {
  let data = '';
  for await (const chunk of process.stdin) {
    data += typeof chunk === 'string' ? chunk : chunk.toString('utf8');
  }

  const nl = data.indexOf('\n');
  let line = nl === -1 ? data : data.slice(0, nl);
  // Tolerate a trailing CR before LF if present
  if (line.endsWith('\r')) line = line.slice(0, -1);

  const opening = new Set(['(', '[', '{']);
  const closingToOpening: Record<string, string> = {
    ')': '(',
    ']': '[',
    '}': '{',
  };

  const stack: string[] = [];
  let ok = true;

  for (const ch of line) {
    if (opening.has(ch)) {
      stack.push(ch);
    } else if (ch in closingToOpening) {
      const need = closingToOpening[ch];
      const got = stack.pop();
      if (got !== need) {
        ok = false;
        break;
      }
    }
    // ignore non-bracket characters
  }

  if (ok && stack.length === 0) {
    process.stdout.write('yes\n');
  } else {
    process.stdout.write('no\n');
  }
})();
```