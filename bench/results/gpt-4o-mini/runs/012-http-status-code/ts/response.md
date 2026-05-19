```ts
import { createServer } from 'http';
import { URL } from 'url';

const TIMEOUT = 5000;

async function fetchStatusCode(url: string): Promise<number | null> {
    return new Promise((resolve) => {
        const req = http.get(url, { timeout: TIMEOUT }, (res) => {
            resolve(res.statusCode ?? null);
        });

        req.on('error', () => {
            resolve(null);
        });

        req.setTimeout(TIMEOUT, () => {
            req.abort();
            resolve(null);
        });
    });
}

async function main() {
    let url = '';
    for await (const chunk of process.stdin) {
        url += chunk;
    }
    url = url.trim();

    const statusCode = await fetchStatusCode(url);
    if (statusCode === null) {
        process.stdout.write('error\n');
    } else {
        process.stdout.write(`${statusCode}\n`);
    }
}

main().catch(() => {
    process.stdout.write('error\n');
});
```