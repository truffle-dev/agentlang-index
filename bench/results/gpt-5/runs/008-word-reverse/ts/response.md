```ts
// ref.ts
async function main() {
  let data = '';
  for await (const chunk of process.stdin) {
    data += typeof chunk === 'string' ? chunk : chunk.toString('utf8');
  }

  const nl = data.indexOf('\n');
  let line = nl >= 0 ? data.slice(0, nl) : data;
  if (line.endsWith('\r')) line = line.slice(0, -1);

  const words = line.split(' ').filter(w => w.length > 0);
  if (words.length === 0) {
    return;
  }
  const out = words.reverse().join(' ') + '\n';
  process.stdout.write(out);
}

main().catch(() => {
  // Swallow any errors to ensure exit code 0 and no stderr output.
});
```