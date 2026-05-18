function isLowercaseLetter(b: number): boolean {
    return b >= 97 && b <= 122;
}

function shiftLetter(b: number, shift: number): number {
    const zeroBased = b - 97;
    return 97 + ((zeroBased + shift) % 26);
}

function parseShift(s: string): number | null {
    const t = s.trim();
    if (t.length === 0) return null;
    for (let i = 0; i < t.length; i++) {
        const c = t.charCodeAt(i);
        if (c < 48 || c > 57) return null;
    }
    const v = Number(t);
    if (!Number.isInteger(v) || v < 0 || v > 25) return null;
    return v;
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
    const shift = parseShift(lines[0]);
    if (shift === null) {
        process.stdout.write("error\n");
        return;
    }
    const text = lines[1];
    if (text.length === 0) {
        process.stdout.write("error\n");
        return;
    }
    const out: number[] = [];
    for (let i = 0; i < text.length; i++) {
        const c = text.charCodeAt(i);
        if (!isLowercaseLetter(c)) {
            process.stdout.write("error\n");
            return;
        }
        out.push(shiftLetter(c, shift));
    }
    process.stdout.write(Buffer.from(out).toString("ascii") + "\n");
}

main();
