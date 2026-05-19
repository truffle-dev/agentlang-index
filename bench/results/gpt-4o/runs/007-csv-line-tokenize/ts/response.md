```ts
async function main() {
    let input = '';
    for await (const chunk of process.stdin) {
        input += chunk;
    }
    input = input.trimEnd(); // Remove the trailing newline

    if (input === '') {
        return; // If the input is empty, do nothing
    }

    const fields: string[] = [];
    let currentField = '';
    let inQuotes = false;
    let i = 0;

    while (i < input.length) {
        const char = input[i];

        if (inQuotes) {
            if (char === '"') {
                if (i + 1 < input.length && input[i + 1] === '"') {
                    currentField += '"';
                    i++; // Skip the next quote
                } else {
                    inQuotes = false;
                }
            } else {
                currentField += char;
            }
        } else {
            if (char === ',') {
                fields.push(currentField);
                currentField = '';
            } else if (char === '"') {
                inQuotes = true;
            } else {
                currentField += char;
            }
        }
        i++;
    }
    fields.push(currentField); // Add the last field

    for (const field of fields) {
        process.stdout.write(field + '\n');
    }
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
```