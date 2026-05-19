```ts
import * as http from 'http';
import * as https from 'https';

async function readStdin(): Promise<string> {
  let data = '';
  for await (const chunk of process.stdin) {
    data += chunk.toString();
  }
  // Trim only trailing CR/LF characters as per spec
  return data.replace(/[\r\n]+$/, '');
}

function getStatusCode(urlStr: string): Promise<number> {
  return new Promise((resolve, reject) => {
    let u: URL;
    try {
      u = new URL(urlStr);
    } catch {
      reject(new Error('invalid url'));
      return;
    }

    const proto = u.protocol;
    const lib = proto === 'http:' ? http : proto === 'https:' ? https : null;
    if (!lib) {
      reject(new Error('unsupported protocol'));
      return;
    }

    const ac = new AbortController();
    const timeout = setTimeout(() => {
      ac.abort();
    }, 5000);

    const options: any = {
      method: 'GET',
      signal: ac.signal,
    };

    // Prefer IPv4 for localhost to avoid IPv6 issues if the server isn't bound to ::1
    if (u.hostname === 'localhost') {
      options.family = 4;
    }

    const req = lib.request(u, options, (res) => {
      clearTimeout(timeout);
      if (typeof res.statusCode !== 'number') {
        // Shouldn't happen, but treat as error
        reject(new Error('no status code'));
        res.resume();
        return;
      }
      // Consume and discard any data to allow socket cleanup
      res.resume();
      resolve(res.statusCode);
    });

    req.on('error', (err) => {
      clearTimeout(timeout);
      reject(err);
    });

    req.end();
  });
}

(async () => {
  try {
    const input = await readStdin();
    const status = await getStatusCode(input);
    process.stdout.write(String(status) + '\n');
  } catch {
    process.stdout.write('error\n');
  }
})();
```