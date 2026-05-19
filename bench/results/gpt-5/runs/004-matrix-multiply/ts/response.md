```ts
// ref.ts
(async () => {
  let input = '';
  for await (const chunk of process.stdin) {
    input += chunk;
  }

  input = input.replace(/^\uFEFF/, '');
  const tokens = input.trim().split(/\s+/).filter(t => t.length > 0);

  if (tokens.length === 0) {
    process.stdout.write('');
    return;
  }

  let idx = 0;
  const N = parseInt(tokens[idx++] || '0', 10);

  const A: number[][] = Array.from({ length: N }, () => Array<number>(N).fill(0));
  const B: number[][] = Array.from({ length: N }, () => Array<number>(N).fill(0));

  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      A[i][j] = parseInt(tokens[idx++] || '0', 10);
    }
  }

  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      B[i][j] = parseInt(tokens[idx++] || '0', 10);
    }
  }

  const C: number[][] = Array.from({ length: N }, () => Array<number>(N).fill(0));

  for (let i = 0; i < N; i++) {
    for (let k = 0; k < N; k++) {
      const aik = A[i][k];
      for (let j = 0; j < N; j++) {
        C[i][j] += aik * B[k][j];
      }
    }
  }

  const lines: string[] = [];
  for (let i = 0; i < N; i++) {
    lines.push(C[i].join(' '));
  }
  process.stdout.write(lines.join('\n') + '\n');
})();
```