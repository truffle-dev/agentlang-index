```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().split('\n').map(line => line.trim());
    if (input.length < 2) {
        process.stdout.write('error\n');
        process.exit(0);
    }

    const shiftStr = input[0];
    const plaintext = input[1];

    const shift = parseInt(shiftStr, 10);
    if (isNaN(shift) || shift < 0 || shift > 25 || shiftStr.trim() === '') {
        process.stdout.write('error\n');
        process.exit(0);
    }

    if (plaintext.length === 0 || !/^[a-z]+$/.test(plaintext)) {
        process.stdout.write('error\n');
        process.exit(0);
    }

    const ciphertext = Array.from(plaintext).map(char => {
        const newCharCode = ((char.charCodeAt(0) - 97 + shift) % 26) + 97;
        return String.fromCharCode(newCharCode);
    }).join('');

    process.stdout.write(ciphertext + '\n');
}
```