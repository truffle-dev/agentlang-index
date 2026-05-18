const U32_MAX = 4294967295n;
const N_MAX = 1000n;

function parseU32(s: string): bigint | null {
    const t = s.trim();
    if (t.length === 0) return null;
    for (let i = 0; i < t.length; i++) {
        const c = t.charCodeAt(i);
        if (c < 48 || c > 57) return null;
    }
    try {
        const v = BigInt(t);
        if (v > U32_MAX) return null;
        return v;
    } catch {
        return null;
    }
}

async function readAll(): Promise<string> {
    const chunks: Buffer[] = [];
    for await (const chunk of process.stdin) {
        chunks.push(chunk as Buffer);
    }
    return Buffer.concat(chunks).toString("utf8");
}

async function main(): Promise<void> {
    const data = await readAll();
    const lines = data.split("\n");
    if (lines.length < 1) {
        process.stdout.write("error\n");
        return;
    }
    const n = parseU32(lines[0]);
    if (n === null || n > N_MAX) {
        process.stdout.write("error\n");
        return;
    }
    const count = Number(n);
    if (lines.length < count + 1) {
        process.stdout.write("error\n");
        return;
    }
    let total = 0n;
    for (let i = 1; i <= count; i++) {
        const v = parseU32(lines[i]);
        if (v === null) {
            process.stdout.write("error\n");
            return;
        }
        total += v;
        if (total > U32_MAX) {
            process.stdout.write("error\n");
            return;
        }
    }
    process.stdout.write(`${total}\n`);
}

main();
