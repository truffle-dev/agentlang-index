```ts
const memo: { [key: number]: number } = {};

async function main() {
    for await (const chunk of process.stdin) {
        const N = parseInt(chunk.toString().trim(), 10);
        if (isNaN(N) || N < 0) {
            process.stdout.write("error\n");
            return;
        }
        const result = fib(N);
        process.stdout.write(`${result}\n`);
    }
}

function fib(n: number): number {
    if (n in memo) {
        return memo[n];
    }
    if (n === 0) {
        return 0;
    }
    if (n === 1) {
        return 1;
    }
    memo[n] = fib(n - 1) + fib(n - 2);
    return memo[n];
}

main().catch(err => {
    process.stdout.write("error\n");
});
```