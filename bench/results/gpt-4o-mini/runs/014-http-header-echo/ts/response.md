```ts
import { createServer } from 'http';
import { URL } from 'url';
import { promisify } from 'util';
import { setTimeout as delay } from 'timers/promises';

const TIMEOUT = 5000;

async function fetchHeader(url: string, headerName: string): Promise<string | null> {
    return new Promise((resolve) => {
        const req = createServer().request(url, (res) => {
            const headers = res.headers;
            const headerValue = Object.keys(headers).find(key => key.toLowerCase() === headerName.toLowerCase());
            resolve(headerValue ? headers[headerValue] : null);
        });

        req.on('error', () => resolve(null));
        req.setTimeout(TIMEOUT, () => {
            req.abort();
            resolve(null);
        });
        req.end();
    });
}

async function main() {
    const input: string[] = [];
    for await (const chunk of process.stdin) {
        input.push(chunk.toString());
        if (input.length === 2) break;
    }

    const url = input[0].trim();
    const headerName = input[1].trim();

    try {
        const headerValue = await fetchHeader(url, headerName);
        if (headerValue) {
            process.stdout.write(`${headerValue}\n`);
        } else {
            process.stdout.write('error\n');
        }
    } catch {
        process.stdout.write('error\n');
    }
}

main();
```