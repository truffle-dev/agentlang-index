```ts
async function main() {
  let input = Buffer.alloc(0);
  for await (const chunk of process.stdin) {
    input = Buffer.concat([input, chunk]);
  }

  if (input.length === 0) {
    return;
  }

  let currentByte = input[0];
  let count = 1;

  for (let i = 1; i < input.length; i++) {
    if (input[i] === currentByte) {
      count++;
    } else {
      process.stdout.write(`${count} ${currentByte}\n`);
      currentByte = input[i];
      count = 1;
    }
  }

  process.stdout.write(`${count} ${currentByte}\n`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
```