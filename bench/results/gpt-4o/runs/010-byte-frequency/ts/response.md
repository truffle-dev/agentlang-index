```ts
async function main() {
    const byteCounts = new Array(256).fill(0);

    for await (const chunk of process.stdin) {
        for (const byte of chunk) {
            byteCounts[byte]++;
        }
    }

    let output = '';
    for (let i = 0; i < 256; i++) {
        if (byteCounts[i] > 0) {
            output += `${i} ${byteCounts[i]}\n`;
        }
    }

    process.stdout.write(output);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
```