```ts
const buf: Buffer[] = [];
for await (const chunk of process.stdin) buf.push(chunk);
const lines = Buffer.concat(buf).toString().trim().split('\n');
let idx = 0;
const N = parseInt(lines[idx++]);
const A: number[][] = [];
const B: number[][] = [];
for (let i = 0; i < N; i++) A.push(lines[idx++].trim().split(/\s+/).map(Number));
for (let i = 0; i < N; i++) B.push(lines[idx++].trim().split(/\s+/).map(Number));
const out: string[] = [];
for (let i = 0; i < N; i++) {
  const row: number[] = [];
  for (let j = 0; j < N; j++) {
    let s = 0;
    for (let k = 0; k < N; k++) s += A[i][k] * B[k][j];
    row.push(s);
  }
  out.push(row.join(' '));
}
process.stdout.write(out.join('\n') + '\n');
```