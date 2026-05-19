```ts
import * as http from 'node:http';
import * as https from 'node:https';

async function readStdin(): Promise<string> {
  let data = '';
  for await (const chunk of process.stdin) {
    data += chunk.toString();
  }
  return data;
}

function writeOut(s: string) {
  try {
    process.stdout.write(s);
  } catch { /* ignore */ }
}

function isInt32(n: number): boolean {
  return Number.isInteger(n) && n >= -2147483648 && n <= 2147483647;
}

function postJson(urlStr: string, body: string, timeoutMs: number): Promise<{ statusCode: number; body: string }> {
  return new Promise((resolve, reject) => {
    let u: URL;
    try {
      u = new URL(urlStr);
    } catch {
      reject(new Error('invalid url'));
      return;
    }
    const isHttp = u.protocol === 'http:';
    const isHttps = u.protocol === 'https:';
    if (!isHttp && !isHttps) {
      reject(new Error('unsupported protocol'));
      return;
    }
    const lib = isHttp ? http : https;

    const options: http.RequestOptions = {
      protocol: u.protocol,
      hostname: u.hostname,
      port: u.port ? Number(u.port) : undefined,
      path: u.pathname + (u.search || ''),
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    let finished = false;
    const req = lib.request(options, (res) => {
      if (finished) return;
      const statusCode = res.statusCode ?? 0;
      if (statusCode !== 200) {
        finished = true;
        // Drain response to allow socket reuse before rejecting
        res.resume();
        clearTimeout(to);
        reject(new Error('non-200'));
        return;
      }
      let respData = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        respData += chunk;
      });
      res.on('end', () => {
        if (finished) return;
        finished = true;
        clearTimeout(to);
        resolve({ statusCode, body: respData });
      });
      res.on('error', (err) => {
        if (finished) return;
        finished = true;
        clearTimeout(to);
        reject(err);
      });
    });

    const to = setTimeout(() => {
      if (finished) return;
      finished = true;
      req.destroy(new Error('timeout'));
      // reject will be triggered by 'error' from destroy in most cases,
      // but ensure rejection even if not
      reject(new Error('timeout'));
    }, timeoutMs);

    req.on('error', (err) => {
      if (finished) return;
      finished = true;
      clearTimeout(to);
      reject(err);
    });

    req.write(body);
    req.end();
  });
}

async function main() {
  try {
    const input = await readStdin();
    const lines = input.split(/\r?\n/);
    if (lines.length < 3 || lines[0] === undefined || lines[1] === undefined || lines[2] === undefined) {
      writeOut('error\n');
      return;
    }

    const urlLine = lines[0];
    const aStr = lines[1].replace(/\s+$/g, '');
    const bStr = lines[2].replace(/\s+$/g, '');

    const aNum = Number(aStr);
    const bNum = Number(bStr);

    if (!isInt32(aNum) || !isInt32(bNum)) {
      writeOut('error\n');
      return;
    }

    const body = JSON.stringify({ a: aNum, b: bNum });

    let resp;
    try {
      resp = await postJson(urlLine, body, 5000);
    } catch {
      writeOut('error\n');
      return;
    }

    try {
      const parsed = JSON.parse(resp.body);
      if (parsed && typeof parsed === 'object' && Number.isInteger(parsed.sum) && isInt32(parsed.sum)) {
        writeOut(String(parsed.sum) + '\n');
      } else {
        writeOut('error\n');
      }
    } catch {
      writeOut('error\n');
    }
  } catch {
    writeOut('error\n');
  }
}

main();
```