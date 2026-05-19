#!/usr/bin/env bun
// Synthesize summary.json from existing per-attempt result.json files.
// Lets us resume a partial sweep via --skip-existing.

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from "fs";
import { join } from "path";

const REPO_ROOT = "/home/phantom/repos/agentlang-index";
const RESULTS_DIR = join(REPO_ROOT, "bench", "results");

const model = process.argv[2];
if (!model) {
  console.error("usage: bun run bench/synth-summary.ts <model>");
  process.exit(2);
}

const runsDir = join(RESULTS_DIR, model, "runs");
if (!existsSync(runsDir)) {
  console.error("no runs dir at", runsDir);
  process.exit(1);
}

const attempts: any[] = [];
const tasks = readdirSync(runsDir).filter((d) => /^\d{3}-/.test(d)).sort();
for (const t of tasks) {
  const taskDir = join(runsDir, t);
  if (!statSync(taskDir).isDirectory()) continue;
  const langs = readdirSync(taskDir);
  for (const l of langs) {
    const rp = join(taskDir, l, "result.json");
    if (!existsSync(rp)) continue;
    try {
      const r = JSON.parse(readFileSync(rp, "utf8"));
      attempts.push(r);
    } catch (e) {
      console.error("bad result.json:", rp);
    }
  }
}

const perLang: Record<string, { passed: number; total: number; rate: number }> = {};
let totalPassed = 0;
let totalAttempts = 0;
let totalPromptTokens = 0;
let totalCompletionTokens = 0;
for (const a of attempts) {
  if (!perLang[a.lang]) perLang[a.lang] = { passed: 0, total: 0, rate: 0 };
  perLang[a.lang].total += 1;
  if (a.passed) perLang[a.lang].passed += 1;
  totalAttempts += 1;
  if (a.passed) totalPassed += 1;
  totalPromptTokens += a.prompt_tokens ?? 0;
  totalCompletionTokens += a.completion_tokens ?? 0;
}
for (const l of Object.keys(perLang)) {
  perLang[l].rate = perLang[l].total === 0 ? 0 : perLang[l].passed / perLang[l].total;
}
const passRate = totalAttempts === 0 ? 0 : totalPassed / totalAttempts;
const zeroRate = perLang.zero?.rate ?? 0;
const langTax: Record<string, number> = {};
for (const l of Object.keys(perLang)) {
  if (l === "zero") continue;
  langTax[l] = perLang[l].rate - zeroRate;
}

const summary = {
  model,
  perLang,
  totalPassed,
  totalAttempts,
  passRate,
  totalPromptTokens,
  totalCompletionTokens,
  langTax,
  timestamp: new Date().toISOString(),
  attempts,
};

const out = join(RESULTS_DIR, model, "summary.json");
writeFileSync(out, JSON.stringify(summary, null, 2));
console.log(`Wrote ${out}`);
console.log(`Attempts: ${totalAttempts}, passed: ${totalPassed} (${(passRate * 100).toFixed(1)}%)`);
console.log(perLang);
