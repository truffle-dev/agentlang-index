```ts
// ref.ts
let input = '';
(async () => {
  for await (const chunk of process.stdin) {
    input += chunk.toString('utf8');
  }

  const lines = input.split('\n');
  const P = (lines[0] ?? '').replace(/\r$/, '');
  const T = (lines[1] ?? '').replace(/\r$/, '');

  let count = 0;
  if (P.length > 0 && T.length > 0) {
    let pos = 0;
    while (true) {
      const idx = T.indexOf(P, pos);
      if (idx === -1) break;
      count++;
      pos = idx + P.length;
    }
  }

  process.stdout.write(String(count) + '\n');
})();
```