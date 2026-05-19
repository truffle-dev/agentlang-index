```ts
for await (const chunk of process.stdin) {
    const line = chunk.toString().trim();
    if (line === "") {
        process.stdout.write("");
        continue;
    }

    const fields: string[] = [];
    let currentField = "";
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
        const char = line[i];

        if (inQuotes) {
            if (char === '"') {
                if (i + 1 < line.length && line[i + 1] === '"') {
                    currentField += '"';
                    i++; // Skip the next quote
                } else {
                    inQuotes = false; // End of quoted field
                }
            } else {
                currentField += char; // Regular character inside quotes
            }
        } else {
            if (char === '"') {
                inQuotes = true; // Start of quoted field
            } else if (char === ',') {
                fields.push(currentField);
                currentField = ""; // Reset for the next field
            } else {
                currentField += char; // Regular character
            }
        }
    }

    // Push the last field
    fields.push(currentField);

    // Write each field to stdout
    for (const field of fields) {
        process.stdout.write(field + "\n");
    }
}
```