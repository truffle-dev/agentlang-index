```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().split('\n');
    const pattern = input[0];
    const text = input[1] || '';
    
    let count = 0;
    let index = 0;

    while ((index = text.indexOf(pattern, index)) !== -1) {
        count++;
        index += pattern.length; // Move index forward to avoid overlap
    }

    process.stdout.write(count.toString() + '\n');
}
```