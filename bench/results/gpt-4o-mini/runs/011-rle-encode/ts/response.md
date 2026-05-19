```ts
for await (const chunk of process.stdin) {
    let count = 0;
    let lastByte: number | null = null;

    for (const byte of chunk) {
        if (lastByte === null || byte !== lastByte) {
            if (lastByte !== null) {
                process.stdout.write(`${count} ${lastByte}\n`);
            }
            lastByte = byte;
            count = 1;
        } else {
            count++;
        }
    }

    if (lastByte !== null) {
        process.stdout.write(`${count} ${lastByte}\n`);
    }
}
```