```ts
import * as http from "http";
import * as https from "https";

async function main() {
  let raw = "";
  for await (const chunk of process.stdin) {
    raw += chunk;
  }
  const lines = raw.split("\n");
  const url = lines[0]?.trim() ?? "";
  const a = parseInt((lines[1] ?? "").trim(), 10);
  const b = parseInt((lines[2] ?? "").trim(), 10);

  const body = JSON.stringify({ a, b });

  try {
    const result = await new Promise<string>((resolve, reject) => {
      const parsed = new URL(url);
      const lib = parsed.protocol === "https:" ? https : http;
      if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
        reject(new Error("unsupported protocol"));
        return;
      }

      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
      };

      const req = lib.request(url, options, (res) => {
        if (res.statusCode !== 200) {
          res.resume();
          reject(new Error(`non-200: ${res.statusCode}`));
          return;
        }
        let data = "";
        res.on("data", (chunk) => { data += chunk; });
        res.on("end", () => resolve(data));
        res.on("error", reject);
      });

      req.setTimeout(5000, () => {
        req.destroy(new Error("timeout"));
      });

      req.on("error", reject);
      req.write(body);
      req.end();
    });

    const parsed = JSON.parse(result);
    if (typeof parsed !== "object" || parsed === null || !("sum" in parsed)) {
      process.stdout.write("error\n");
      return;
    }
    const sum = parsed.sum;
    if (typeof sum !== "number" || !Number.isInteger(sum)) {
      process.stdout.write("error\n");
      return;
    }
    process.stdout.write(`${sum}\n`);
  } catch {
    process.stdout.write("error\n");
  }
}

main();
```