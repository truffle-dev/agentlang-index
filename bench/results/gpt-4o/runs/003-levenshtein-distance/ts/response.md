```ts
async function main() {
    const input: string[] = [];
    for await (const chunk of process.stdin) {
        input.push(chunk);
    }
    const lines = input.join('').split('\n');
    const A = lines[0] || '';
    const B = lines[1] || '';

    const m = A.length;
    const n = B.length;

    // Create a 2D array to store distances
    const dp: number[][] = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

    // Initialize the first row and column
    for (let i = 0; i <= m; i++) {
        dp[i][0] = i;
    }
    for (let j = 0; j <= n; j++) {
        dp[0][j] = j;
    }

    // Fill the dp array
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (A[i - 1] === B[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1,    // Deletion
                    dp[i][j - 1] + 1,    // Insertion
                    dp[i - 1][j - 1] + 1 // Substitution
                );
            }
        }
    }

    // The answer is in the bottom-right corner of the matrix
    process.stdout.write(dp[m][n] + '\n');
}

main();
```