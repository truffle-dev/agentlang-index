```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().trim().split('\n');
    const N = parseInt(input[0].trim(), 10);

    if (isNaN(N) || N < 0 || N > 1000) {
        process.stdout.write("error\n");
        process.exit(0);
    }

    if (input.length - 1 < N) {
        process.stdout.write("error\n");
        process.exit(0);
    }

    let sum = 0;

    for (let i = 1; i <= N; i++) {
        const value = input[i].trim();
        const num = parseInt(value, 10);

        if (value === "" || isNaN(num) || num < 0 || num > 4294967295) {
            process.stdout.write("error\n");
            process.exit(0);
        }

        if (sum > 4294967295 - num) {
            process.stdout.write("error\n");
            process.exit(0);
        }

        sum += num;
    }

    process.stdout.write(`${sum}\n`);
}
```