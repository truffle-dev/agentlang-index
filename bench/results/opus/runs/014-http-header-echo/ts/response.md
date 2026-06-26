```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const lines = Buffer.concat(buf).toString().split('\n');
const url = (lines[0] ?? '').trimEnd();
const headerName = (lines[1] ?? '').trimEnd();

try {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5000);
  const res = await fetch(url, { signal: controller.signal });
  clearTimeout(timer);
  if (res.status !== 200) {
    process.stdout.write('error\n');
  } else {
    const val = res.headers.get(headerName);
    if (val === null) {
      process.stdout.write('error\n');
    } else {
      process.stdout.write(val + '\n');
    }
  }
} catch {
  process.stdout.write('error\n');
}
```