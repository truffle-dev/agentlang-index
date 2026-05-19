```ts
import * as http from 'node:http';
import * as https from 'node:https';

async function readStdin(): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin as any) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString('utf8');
}

function writeOut(s: string) {
  try {
    process.stdout.write(s);
  } catch {
    // Ignore write errors per spec (still exit 0)
  }
}

function printError() {
  writeOut('error\n');
}

function httpGet(urlObj: URL, timeoutMs: number): Promise<http.IncomingMessage> {
  return new Promise((resolve, reject) => {
    const lib = urlObj.protocol === 'http:' ? http : urlObj.protocol === 'https:' ? https : null;
    if (!lib) {
      reject(new Error('unsupported protocol'));
      return;
    }
    let timer: NodeJS.Timeout | undefined;
    const req = lib.request(urlObj, { method: 'GET' }, (res) => {
      if (timer) clearTimeout(timer);
      resolve(res);
    });
    req.on('error', (err) => {
      if (timer) clearTimeout(timer);
      reject(err);
    });
    timer = setTimeout(() => {
      // Destroy triggers 'error' and rejects the promise.
      req.destroy(new Error('timeout'));
    }, timeoutMs);
    req.end();
  });
}

(async () => {
  const input = await readStdin();
  const parts = input.split('\n');
  const urlStr = (parts[0] ?? '').trimEnd();
  const headerNameRaw = (parts[1] ?? '').trimEnd();

  if (!urlStr || !headerNameRaw) {
    printError();
    return;
  }

  let urlObj: URL;
  try {
    urlObj = new URL(urlStr);
  } catch {
    printError();
    return;
  }

  try {
    const res = await httpGet(urlObj, 5000);
    const status = res.statusCode || 0;
    if (status !== 200) {
      res.resume();
      printError();
      return;
    }

    const headerKey = headerNameRaw.toLowerCase();
    const val = (res.headers as http.IncomingHttpHeaders)[headerKey];
    res.resume();

    if (val === undefined) {
      printError();
      return;
    }

    const out = Array.isArray(val) ? (val[0] ?? '') : String(val);
    if (out === '') {
      printError();
      return;
    }

    writeOut(out + '\n');
  } catch {
    printError();
  }
})();
```