```ts
async function main() {
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  const lines = input.split("\n");
  const url = lines[0]?.trim() ?? "";
  const a = parseInt((lines[1] ?? "").trim(), 10);
  const b = parseInt((lines[2] ?? "").trim(), 10);

  if (!url || isNaN(a) || isNaN(b)) {
    process.stdout.write("error\n");
    return;
  }

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: `{"a":${a},"b":${b}}`,
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (res.status !== 200) {
      process.stdout.write("error\n");
      return;
    }
    const json = JSON.parse(await res.text());
    if (json == null || typeof json.sum !== "number" || !Number.isInteger(json.sum)) {
      process.stdout.write("error\n");
      return;
    }
    process.stdout.write(json.sum + "\n");
  } catch {
    process.stdout.write("error\n");
  }
}

main();
```