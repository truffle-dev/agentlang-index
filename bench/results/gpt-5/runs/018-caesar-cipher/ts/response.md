```ts
// ref.ts
async function main() {
  let input = '';
  try {
    for await (const chunk of (process.stdin as any)) {
      input += (chunk as any).toString('utf8');
    }

    // Extract two lines
    const firstNL = input.indexOf('\n');
    let line1: string;
    let remainder: string;
    if (firstNL === -1) {
      line1 = input;
      remainder = '';
    } else {
      line1 = input.slice(0, firstNL);
      remainder = input.slice(firstNL + 1);
    }
    const secondNL = remainder.indexOf('\n');
    const line2 = secondNL === -1 ? remainder : remainder.slice(0, secondNL);

    // Parse and validate shift (trim surrounding whitespace per spec tolerance)
    const s = line1.trim();
    if (s.length === 0) {
      process.stdout.write('error\n');
      return;
    }
    if (!/^\d+$/.test(s)) {
      process.stdout.write('error\n');
      return;
    }
    const shiftNum = Number(s);
    if (!Number.isFinite(shiftNum) || shiftNum > 25) {
      process.stdout.write('error\n');
      return;
    }
    const shift = shiftNum | 0;

    // Validate plaintext
    if (line2.length === 0) {
      process.stdout.write('error\n');
      return;
    }
    for (let i = 0; i < line2.length; i++) {
      const code = line2.charCodeAt(i);
      if (code < 97 || code > 122) {
        process.stdout.write('error\n');
        return;
      }
    }

    // Encrypt
    let out = '';
    if (shift === 0) {
      out = line2;
    } else {
      const a = 97;
      const z = 122;
      const mod = 26;
      const chars: string[] = new Array(line2.length);
      for (let i = 0; i < line2.length; i++) {
        const c = line2.charCodeAt(i);
        // c is guaranteed in [a..z]
        const rotated = ((c - a + shift) % mod) + a;
        chars[i] = String.fromCharCode(rotated);
      }
      out = chars.join('');
    }

    process.stdout.write(out + '\n');
  } catch {
    // On any unexpected error, still obey the contract.
    try {
      process.stdout.write('error\n');
    } catch {
      // ignore
    }
  }
}

main();
```