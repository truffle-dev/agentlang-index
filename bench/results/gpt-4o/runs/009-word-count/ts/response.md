```ts
async function main() {
    let input = '';
    for await (const chunk of process.stdin) {
        input += chunk;
    }

    const words = input.split(/[\x20\x09\x0A\x0D]+/).filter(word => word.length > 0);
    process.stdout.write(words.length + '\n');
}

main();
```