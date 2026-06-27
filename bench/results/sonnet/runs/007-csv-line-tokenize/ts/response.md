```ts
import * as readline from "readline";

const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });

rl.once("line", (line) => {
  if (line.length === 0) {
    process.exit(0);
  }

  const fields: string[] = [];
  let i = 0;

  while (i <= line.length) {
    if (i === line.length) {
      // trailing comma case - shouldn't happen as we break below, but safety
      break;
    }
    if (line[i] === '"') {
      // quoted field
      i++; // skip opening quote
      let field = "";
      while (i < line.length) {
        if (line[i] === '"') {
          if (i + 1 < line.length && line[i + 1] === '"') {
            field += '"';
            i += 2;
          } else {
            i++; // skip closing quote
            break;
          }
        } else {
          field += line[i];
          i++;
        }
      }
      fields.push(field);
      // skip comma
      if (i < line.length && line[i] === ',') i++;
    } else {
      // unquoted field
      let field = "";
      while (i < line.length && line[i] !== ',') {
        field += line[i];
        i++;
      }
      fields.push(field);
      if (i < line.length && line[i] === ',') {
        i++;
        // if comma was last char, we need one more empty field
        if (i === line.length) {
          fields.push("");
          break;
        }
      } else {
        break;
      }
    }
  }

  for (const f of fields) {
    process.stdout.write(f + "\n");
  }
  process.exit(0);
});
```