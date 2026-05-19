```ts
import { request } from 'http';
import { URL } from 'url';

async function readStdin(): Promise<string> {
  let input = '';
  for await (const chunk of process.stdin) {
    input += chunk;
  }
  return input.trim();
}

async function main() {
  const urlString = await readStdin();
  let url: URL;

  try {
    url = new URL(urlString);
  } catch {
    process.stdout.write('error\n');
    return;
  }

  const options = {
    method: 'GET',
    timeout: 5000,
  };

  const req = request(url, options, (res) => {
    process.stdout.write(`${res.statusCode}\n`);
  });

  req.on('error', () => {
    process.stdout.write('error\n');
  });

  req.on('timeout', () => {
    req.abort();
    process.stdout.write('error\n');
  });

  req.end();
}

main().catch(() => {
  process.stdout.write('error\n');
});
```