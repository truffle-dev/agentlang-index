```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().split('\n');
    const P = input[0];
    const T = input[1];

    let count = 0;
    let index = 0;
    const patternLength = P.length;

    while (index <= T.length - patternLength) {
        if (T.substring(index, index + patternLength) === P) {
            count++;
            index += patternLength;
        } else {
            index++;
        }
    }

    process.stdout.write(count.toString() + '\n');
}
```