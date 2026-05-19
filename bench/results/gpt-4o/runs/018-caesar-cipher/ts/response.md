```ts
for await (const chunk of process.stdin) {
  const input = chunk.toString().split('\n');
  const shiftStr = input[0].trim();
  const plaintext = input[1];

  if (!/^\d+$/.test(shiftStr)) {
    process.stdout.write('error\n');
    continue;
  }

  const shift = parseInt(shiftStr, 10);

  if (shift < 0 || shift > 25 || !plaintext || /[^a-z]/.test(plaintext)) {
    process.stdout.write('error\n');
    continue;
  }

  const ciphertext = plaintext.split('').map(char => {
    const shiftedCharCode = ((char.charCodeAt(0) - 97 + shift) % 26) + 97;
    return String.fromCharCode(shiftedCharCode);
  }).join('');

  process.stdout.write(ciphertext + '\n');
}
```