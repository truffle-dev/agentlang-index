```ts
import * as http from "http";
import * as https from "https";

async function main() {
  let raw = "";
  for await (const chunk of process.stdin) {
    raw += chunk.toString();
  }
  const lines = raw.split("\n");
  const url = lines[0]?.trimEnd() ?? "";
  const headerName = lines[1]?.trimEnd().toLowerCase() ?? "";

  try {
    const value = await fetchHeader(url, headerName);
    if (value === null) {
      process.stdout.write("error\n");
    } else {
      process.stdout.write(value + "\n");
    }
  } catch {
    process.stdout.write("error\n");
  }
}

function fetchHeader(url: string, headerName: string): Promise<string | null> {
  return new Promise((resolve) => {
    let parsed: URL;
    try {
      parsed = new URL(url);
    } catch {
      resolve(null);
      return;
    }

    const lib = parsed.protocol === "https:" ? https : parsed.protocol === "http:" ? http : null;
    if (!lib) {
      resolve(null);
      return;
    }

    const req = lib.get(url, { timeout: 5000 }, (res) => {
      res.resume();
      if (res.statusCode !== 200) {
        resolve(null);
        return;
      }
      const headers = res.headers;
      const val = headers[headerName];
      if (val === undefined || val === null) {
        resolve(null);
      } else if (Array.isArray(val)) {
        resolve(val[0] ?? null);
      } else {
        resolve(val);
      }
    });

    req.on("timeout", () => {
      req.destroy();
      resolve(null);
    });

    req.on("error", () => {
      resolve(null);
    });
  });
}

main();
```