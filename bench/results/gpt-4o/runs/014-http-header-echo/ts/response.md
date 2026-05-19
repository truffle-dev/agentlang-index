```ts
import http from 'http';
import https from 'https';
import { URL } from 'url';

async function readInput(): Promise<string[]> {
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString().trim().split('\n').map(line => line.trim());
}

function getHeaderValue(url: string, headerName: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const options = {
      method: 'GET',
      timeout: 5000,
    };

    const request = (parsedUrl.protocol === 'https:' ? https : http).request(parsedUrl, options, (response) => {
      if (response.statusCode !== 200) {
        resolve('error\n');
        return;
      }

      const headers = response.headers;
      const headerValue = headers[headerName.toLowerCase()];

      if (headerValue) {
        resolve(`${headerValue}\n`);
      } else {
        resolve('error\n');
      }
    });

    request.on('error', () => resolve('error\n'));
    request.on('timeout', () => {
      request.destroy();
      resolve('error\n');
    });

    request.end();
  });
}

async function main() {
  const [url, headerName] = await readInput();

  if (!url || !headerName) {
    process.stdout.write('error\n');
    return;
  }

  try {
    const result = await getHeaderValue(url, headerName);
    process.stdout.write(result);
  } catch {
    process.stdout.write('error\n');
  }
}

main();
```