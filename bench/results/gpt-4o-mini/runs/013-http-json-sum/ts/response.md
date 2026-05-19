```ts
import { createServer } from 'http';
import { URL } from 'url';

async function readInput() {
    const input: string[] = [];
    for await (const chunk of process.stdin) {
        input.push(chunk.toString());
    }
    return input.map(line => line.trim());
}

async function postJson(url: string, data: object): Promise<number | null> {
    return new Promise((resolve) => {
        const json = JSON.stringify(data);
        const parsedUrl = new URL(url);
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(json),
            },
            timeout: 5000,
        };

        const req = createServer(parsedUrl, options, (res) => {
            let body = '';
            res.on('data', (chunk) => {
                body += chunk;
            });
            res.on('end', () => {
                try {
                    const jsonResponse = JSON.parse(body);
                    if (typeof jsonResponse.sum === 'number') {
                        resolve(jsonResponse.sum);
                    } else {
                        resolve(null);
                    }
                } catch {
                    resolve(null);
                }
            });
        });

        req.on('error', () => {
            resolve(null);
        });

        req.write(json);
        req.end();
    });
}

async function main() {
    const input = await readInput();
    if (input.length < 3) {
        process.stdout.write('error\n');
        return;
    }

    const [url, aStr, bStr] = input;
    const a = parseInt(aStr, 10);
    const b = parseInt(bStr, 10);

    if (isNaN(a) || isNaN(b)) {
        process.stdout.write('error\n');
        return;
    }

    const sum = await postJson(url, { a, b });
    if (sum !== null) {
        process.stdout.write(`${sum}\n`);
    } else {
        process.stdout.write('error\n');
    }
}

main().catch(() => {
    process.stdout.write('error\n');
});
```