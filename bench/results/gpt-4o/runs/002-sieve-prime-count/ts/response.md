```ts
import { createInterface } from 'readline';

async function main() {
    const rl = createInterface({
        input: process.stdin,
        output: process.stdout
    });

    for await (const line of rl) {
        const N = parseInt(line.trim(), 10);
        if (N < 2) {
            process.stdout.write('0\n');
            return;
        }

        const isPrime = new Array(N + 1).fill(true);
        isPrime[0] = isPrime[1] = false;

        for (let i = 2; i * i <= N; i++) {
            if (isPrime[i]) {
                for (let j = i * i; j <= N; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        const primeCount = isPrime.reduce((count, prime) => count + (prime ? 1 : 0), 0);
        process.stdout.write(primeCount + '\n');
    }
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
```