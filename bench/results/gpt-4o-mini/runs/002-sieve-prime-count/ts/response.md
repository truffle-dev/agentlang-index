```ts
for await (const chunk of process.stdin) {
    const N = parseInt(chunk.toString().trim());
    if (N < 0 || N > 10000) {
        process.stdout.write("error\n");
        process.exit(0);
    }

    if (N < 2) {
        process.stdout.write("0\n");
        process.exit(0);
    }

    const sieve = new Array(N + 1).fill(true);
    sieve[0] = sieve[1] = false; // 0 and 1 are not prime

    for (let i = 2; i * i <= N; i++) {
        if (sieve[i]) {
            for (let j = i * i; j <= N; j += i) {
                sieve[j] = false;
            }
        }
    }

    const primeCount = sieve.filter(isPrime => isPrime).length;
    process.stdout.write(`${primeCount}\n`);
}
```