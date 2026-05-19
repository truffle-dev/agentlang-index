```ts
async function main() {
    const inputChunks: string[] = [];
    for await (const chunk of process.stdin) {
        inputChunks.push(chunk);
    }
    const input = inputChunks.join('');
    const lines = input.trim().split('\n');
    
    const N = parseInt(lines[0].trim());
    const A: number[][] = [];
    const B: number[][] = [];
    
    for (let i = 0; i < N; i++) {
        A.push(lines[i + 1].trim().split(' ').map(Number));
    }
    
    for (let i = 0; i < N; i++) {
        B.push(lines[i + 1 + N].trim().split(' ').map(Number));
    }
    
    const C: number[][] = Array.from({ length: N }, () => Array(N).fill(0));
    
    for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
            for (let k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    
    const output = C.map(row => row.join(' ')).join('\n') + '\n';
    process.stdout.write(output);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
```