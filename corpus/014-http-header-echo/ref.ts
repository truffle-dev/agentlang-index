#!/usr/bin/env -S tsx
// Reference implementation for 014-http-header-echo (TypeScript).
import { readFileSync } from "node:fs";

async function main(): Promise<void> {
  let raw: string;
  try {
    raw = readFileSync(0, "utf8");
  } catch {
    process.stdout.write("error\n");
    return;
  }
  const lines = raw.split("\n");
  if (lines.length < 2) {
    process.stdout.write("error\n");
    return;
  }
  const url = lines[0].trim();
  const name = lines[1].trim();
  if (!url || !name) {
    process.stdout.write("error\n");
    return;
  }
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 5000);
  try {
    const resp = await fetch(url, { method: "GET", signal: ctl.signal });
    clearTimeout(timer);
    if (resp.status !== 200) {
      process.stdout.write("error\n");
      return;
    }
    const value = resp.headers.get(name);
    if (value === null) {
      process.stdout.write("error\n");
      return;
    }
    process.stdout.write(value + "\n");
  } catch {
    clearTimeout(timer);
    process.stdout.write("error\n");
  }
}

main();
