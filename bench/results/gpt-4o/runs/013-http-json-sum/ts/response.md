```ts
import fetch from 'node-fetch';

async function main() {
    const input = [];
    for await (const chunk of process.stdin) {
        input.push(chunk);
    }
    const lines = Buffer.concat(input).toString().split('\n').map(line => line.trim());
    const url = lines[0];
    const a = parseInt(lines[1], 10);
    const b = parseInt(lines[2], 10);

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ a, b }),
            timeout: 5000
        });

        if (response.ok) {
            const json = await response.json();
            if (typeof json.sum === 'number') {
                process.stdout.write(`${json.sum}\n`);
                return;
            }
        }
    } catch (error) {
        // Handle any errors silently
    }

    process.stdout.write('error\n');
}

main();
```