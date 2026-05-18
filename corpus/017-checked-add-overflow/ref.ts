const U32_MAX = 4294967295n;

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
    if (lines.length < 2) {
        process.stdout.write("error\n");
        return;
    }
    const a = parseU32(lines[0]);
    const b = parseU32(lines[1]);
    if (a === null || b === null) {
        process.stdout.write("error\n");
        return;
    }
    const sum = a + b;
    if (sum > U32_MAX) {
        process.stdout.write("error\n");
        return;
    }
    process.stdout.write(`${sum}\n`);
}

main();
