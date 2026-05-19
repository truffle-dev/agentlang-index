```ts
// ref.ts
async function main() {
  process.stdin.setEncoding('utf8');
  let input = '';
  for await (const chunk of process.stdin) {
    input += chunk as string;
  }

  const lines = input.split('\n');
  let A = (lines[0] ?? '').replace(/\r$/, '');
  let B = (lines[1] ?? '').replace(/\r$/, '');

  function levenshtein(a: string, b: string): number {
    const m = a.length;
    const n = b.length;
    if (m === 0) return n;
    if (n === 0) return m;

    // Use smaller string for columns to reduce memory
    if (n < m) {
      // swap to keep n >= m for slightly better cache/memory
      return levenshtein(b, a);
    }

    const row = new Array(n + 1);
    for (let j = 0; j <= n; j++) row[j] = j;

    for (let i = 1; i <= m; i++) {
      let prevDiag = row[0]; // value from previous row, previous column
      row[0] = i;
      const ai = a.charCodeAt(i - 1);
      for (let j = 1; j <= n; j++) {
        const temp = row[j];
        const cost = ai === b.charCodeAt(j - 1) ? 0 : 1;
        // deletion: row[j] + 1
        // insertion: row[j - 1] + 1
        // substitution: prevDiag + cost
        let v = row[j] + 1;
        const ins = row[j - 1] + 1;
        if (ins < v) v = ins;
        const sub = prevDiag + cost;
        if (sub < v) v = sub;
        row[j] = v;
        prevDiag = temp;
      }
    }
    return row[n];
  }

  const dist = levenshtein(A, B);
  process.stdout.write(String(dist) + '\n');
}

main().catch(() => {
  // Ensure silent failure without writing to stderr; still exit 0 per spec.
  process.stdout.write('error\n');
});
```