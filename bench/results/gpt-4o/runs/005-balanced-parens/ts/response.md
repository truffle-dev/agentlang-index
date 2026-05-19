```ts
async function isBalanced(input: string): Promise<string> {
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
                return 'no\n';
            }
        }
    }

    return stack.length === 0 ? 'yes\n' : 'no\n';
}

async function main() {
    let input = '';
    for await (const chunk of process.stdin) {
        input += chunk;
    }
    input = input.trim();
    const result = await isBalanced(input);
    process.stdout.write(result);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
```