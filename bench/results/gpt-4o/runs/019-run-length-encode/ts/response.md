```ts
import { createInterface } from 'readline';

async function main() {
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
  });

  let input = '';
  for await (const chunk of rl) {
    input += chunk;
  }

  if (input.length === 0 || input[input.length - 1] !== '\n') {
    process.stdout.write('error\n');
    return;
  }

  input = input.slice(0, -1); // Remove the trailing newline

  if (input.length === 0 || /[^a-z]/.test(input)) {
    process.stdout.write('error\n');
    return;
  }

  let result = '';
  let currentChar = input[0];
  let count = 1;

  for (let i = 1; i < input.length; i++) {
    if (input[i] === currentChar) {
      count++;
    } else {
      result += currentChar + count.toString();
      currentChar = input[i];
      count = 1;
    }
  }

  result += currentChar + count.toString();
  process.stdout.write(result + '\n');
}

main();
```