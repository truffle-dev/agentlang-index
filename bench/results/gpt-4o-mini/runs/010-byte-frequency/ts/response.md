```ts
for await (const chunk of process.stdin) {
    const counts = new Uint32Array(256);
    for (const byte of chunk) {
        counts[byte]++;
    }
    for (let i = 0; i < 256; i++) {
        if (counts[i] > 0) {
            process.stdout.write(`${i} ${counts[i]}\n`);
        }
    }
}
```