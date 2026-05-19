```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().trim().split('\n');
    const N = parseInt(input[0]);
    const A: number[][] = [];
    const B: number[][] = [];
    
    for (let i = 1; i <= N; i++) {
        A.push(input[i].split(' ').map(Number));
    }
    
    for (let i = N + 1; i <= 2 * N; i++) {
        B.push(input[i].split(' ').map(Number));
    }
    
    const C: number[][] = Array.from({ length: N }, () => Array(N).fill(0));
    
    for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
            for (let k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    
    for (let i = 0; i < N; i++) {
        process.stdout.write(C[i].join(' ') + '\n');
    }
}
```