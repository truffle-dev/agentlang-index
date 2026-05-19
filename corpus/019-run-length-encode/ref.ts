function isLowercaseLetter(b: number): boolean {
    return b >= 97 && b <= 122;
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
    const text = lines[0];
    if (text.length === 0) {
        process.stdout.write("error\n");
        return;
    }
    const bytes = Buffer.from(text, "utf8");
    for (let i = 0; i < bytes.length; i++) {
        if (!isLowercaseLetter(bytes[i])) {
            process.stdout.write("error\n");
            return;
        }
    }
    const out: string[] = [];
    let i = 0;
    while (i < bytes.length) {
        const runByte = bytes[i];
        let runLen = 1;
        let j = i + 1;
        while (j < bytes.length && bytes[j] === runByte) {
            runLen++;
            j++;
        }
        out.push(String.fromCharCode(runByte));
        out.push(String(runLen));
        i = j;
    }
    process.stdout.write(out.join("") + "\n");
}

main();
