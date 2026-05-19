```ts
for await (const chunk of process.stdin) {
    const input = chunk.toString().trim().split('\n');
    const A = input[0];
    const B = input[1];

    const distance = (a: string, b: string): number => {
        const m = a.length;
        const n = b.length;
        const dp: number[][] = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

        for (let i = 0; i <= m; i++) {
            for (let j = 0; j <= n; j++) {
                if (i === 0) {
                    dp[i][j] = j; // If A is empty
                } else if (j === 0) {
                    dp[i][j] = i; // If B is empty
                } else if (a[i - 1] === b[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1]; // No operation needed
                } else {
                    dp[i][j] = Math.min(
                        dp[i - 1][j] + 1, // Deletion
                        dp[i][j - 1] + 1, // Insertion
                        dp[i - 1][j - 1] + 1 // Substitution
                    );
                }
            }
        }
        return dp[m][n];
    };

    const result = distance(A, B);
    process.stdout.write(result.toString() + '\n');
}
```