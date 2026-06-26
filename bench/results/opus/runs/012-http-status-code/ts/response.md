```ts
(async () => {
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  const url = input.trim();
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(url, { signal: controller.signal, redirect: "follow" });
    clearTimeout(timer);
    process.stdout.write(res.status + "\n");
  } catch {
    process.stdout.write("error\n");
  }
})();
```