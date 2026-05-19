```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString();
    const words = input.split(/[\s]+/).filter(word => word.length > 0);
    process.stdout.write(`${words.length}\n`);
}
```