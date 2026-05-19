```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().trim();
    if (input.length === 0) {
        process.exit(0);
    }
    const words = input.split(/\s+/);
    const reversedWords = words.reverse().join(' ');
    process.stdout.write(reversedWords + '\n');
}
```