```ts
import { get } from "http";
import { get as httpsGet } from "https";

async function main() {
  let url = "";
  for await (const chunk of process.stdin) {
    url += chunk.toString();
  }
  url = url.trimEnd();

  await new Promise<void>((resolve) => {
    try {
      const parsed = new URL(url);
      const getter = parsed.protocol === "https:" ? httpsGet : get;

      const req = getter(url, { timeout: 5000 }, (res) => {
        process.stdout.write(`${res.statusCode}\n`);
        res.resume();
        res.on("end", resolve);
      });

      req.on("timeout", () => {
        req.destroy();
        process.stdout.write("error\n");
        resolve();
      });

      req.on("error", () => {
        process.stdout.write("error\n");
        resolve();
      });
    } catch {
      process.stdout.write("error\n");
      resolve();
    }
  });
}

main();
```