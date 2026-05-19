```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().trim();
    if (input.length === 0) {
        process.stdout.write('');
        process.exit(0);
    }
    const words = input.split(/\s+/).reverse();
    process.stdout.write(words.join(' ') + '\n');
}
```