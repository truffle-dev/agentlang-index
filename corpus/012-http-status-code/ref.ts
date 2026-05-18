async function main(): Promise<void> {
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk as Buffer);
  }
  const url = Buffer.concat(chunks).toString("utf-8").trim();

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5000);
  try {
    const response = await fetch(url, {
      method: "GET",
      signal: controller.signal,
      redirect: "manual",
    });
    process.stdout.write(`${response.status}\n`);
  } catch {
    process.stdout.write("error\n");
  } finally {
    clearTimeout(timer);
  }
}

main();
