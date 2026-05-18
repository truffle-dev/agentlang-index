// HTTP POST + JSON sum reference for AgentLang Index.
//
// Reads three stdin lines: URL, a, b. POSTs `{"a":<a>,"b":<b>}` to URL
// with Content-Type: application/json and 5000 ms timeout. On HTTP 200
// with a JSON body containing an integer `sum`, writes the sum and
// newline. Otherwise writes `error\n`. Always exits 0.

async function readStdin(): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin as AsyncIterable<Buffer>) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf-8");
}

function fail(): void {
  process.stdout.write("error\n");
}

async function main(): Promise<void> {
  let url: string;
  let a: number;
  let b: number;
  try {
    const lines = (await readStdin()).split(/\r?\n/);
    url = (lines[0] ?? "").trim();
    a = parseInt((lines[1] ?? "").trim(), 10);
    b = parseInt((lines[2] ?? "").trim(), 10);
    if (!url || !Number.isInteger(a) || !Number.isInteger(b)) {
      fail();
      return;
    }
  } catch {
    fail();
    return;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  let resp: Response;
  try {
    resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: `{"a":${a},"b":${b}}`,
      signal: controller.signal,
      redirect: "manual",
    });
  } catch {
    clearTimeout(timeout);
    fail();
    return;
  }
  clearTimeout(timeout);

  if (resp.status !== 200) {
    fail();
    return;
  }

  let bodyText: string;
  try {
    bodyText = await resp.text();
  } catch {
    fail();
    return;
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(bodyText);
  } catch {
    fail();
    return;
  }

  if (
    typeof parsed !== "object" ||
    parsed === null ||
    !("sum" in parsed) ||
    typeof (parsed as { sum: unknown }).sum !== "number" ||
    !Number.isInteger((parsed as { sum: number }).sum)
  ) {
    fail();
    return;
  }
  const s = (parsed as { sum: number }).sum;
  process.stdout.write(`${s}\n`);
}

main();
