```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().trim();
    const stack: string[] = [];
    const matchingBrackets: { [key: string]: string } = {
        ')': '(',
        ']': '[',
        '}': '{'
    };

    for (const char of input) {
        if (char === '(' || char === '[' || char === '{') {
            stack.push(char);
        } else if (char === ')' || char === ']' || char === '}') {
            if (stack.length === 0 || stack.pop() !== matchingBrackets[char]) {
                process.stdout.write('no\n');
                process.exit(0);
            }
        }
    }

    process.stdout.write(stack.length === 0 ? 'yes\n' : 'no\n');
}
```