```ts
// ref.ts
async function main(): Promise<void> {
  let input = '';
  try {
    for await (const chunk of process.stdin) {
      input += chunk.toString('utf8');
    }
  } catch {
    process.stdout.write('error\n');
    return;
  }

  const nlIndex = input.indexOf('\n');
  let line = nlIndex === -1 ? input : input.slice(0, nlIndex);
  if (line.endsWith('\r')) {
    line = line.slice(0, -1);
  }

  if (line.length === 0) {
    return;
  }

  const fields = parseCSVLine(line);
  if (fields.length > 0) {
    process.stdout.write(fields.join('\n') + '\n');
  }
}

function parseCSVLine(line: string): string[] {
  const fields: string[] = [];
  let curr: string[] = [];
  let i = 0;
  const len = line.length;
  let inQuotes = false;

  while (i < len) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"') {
        if (i + 1 < len && line[i + 1] === '"') {
          curr.push('"');
          i += 2;
        } else {
          inQuotes = false;
          i += 1;
        }
      } else {
        curr.push(ch);
        i += 1;
      }
    } else {
      if (ch === ',') {
        fields.push(curr.join(''));
        curr = [];
        i += 1;
      } else if (ch === '"') {
        inQuotes = true;
        i += 1;
      } else {
        curr.push(ch);
        i += 1;
      }
    }
  }

  fields.push(curr.join(''));
  return fields;
}

main().catch(() => {
  process.stdout.write('error\n');
});
```