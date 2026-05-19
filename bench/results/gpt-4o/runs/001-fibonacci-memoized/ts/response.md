```ts
const memo: Map<number, number> = new Map();

function fib(n: number): number {
    if (memo.has(n)) {
        return memo.get(n)!;
    }
    if (n === 0) {
        return 0;
    }
    if (n === 1) {
        return 1;
    }
    const result = fib(n - 1) + fib(n - 2);
    memo.set(n, result);
    return result;
}

async function main() {
    let input = '';
    for await (const chunk of process.stdin) {
        input += chunk;
    }
    const N = parseInt(input.trim(), 10);
    const result = fib(N);
    process.stdout.write(result.toString() + '\n');
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
```