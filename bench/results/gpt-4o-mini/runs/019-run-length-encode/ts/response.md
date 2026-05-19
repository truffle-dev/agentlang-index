```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString();
    if (input.length === 0 || !/^[a-z\n]+$/.test(input)) {
        process.stdout.write("error\n");
        process.exit(0);
    }

    let result = '';
    let count = 1;

    for (let i = 1; i < input.length; i++) {
        if (input[i] === input[i - 1]) {
            count++;
        } else {
            result += input[i - 1] + count;
            count = 1;
        }
    }
    result += input[input.length - 1] + count; // Add the last run

    process.stdout.write(result + '\n');
    process.exit(0);
}
```