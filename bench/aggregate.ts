#!/usr/bin/env bun
/**
 * Aggregate per-model bench/results/<model>/summary.json files into a
 * single bench/results/dashboard.json and an optional site-ready JSON
 * file for truffleagent-site.
 *
 * Usage:
 *   bun run bench/aggregate.ts                 # writes bench/results/dashboard.json
 *   bun run bench/aggregate.ts --site          # also writes site/src/data/agentlang-results.json
 */

import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from "fs";
import { join } from "path";

const REPO_ROOT = "/home/phantom/repos/agentlang-index";
const RESULTS_DIR = join(REPO_ROOT, "bench", "results");
const CORPUS_DIR = join(REPO_ROOT, "corpus");
const SITE_DATA_DIR = "/home/phantom/repos/truffleagent-site/src/data";

const LANGS = ["zero", "ts", "rust", "go", "python"];

type Attempt = {
  model: string;
  task: string;
  lang: string;
  passed: boolean;
  extracted: boolean;
  num_cases: number;
  num_passed: number;
  pass_rate: number;
  api_ms: number;
  build_ms: number;
  exec_ms: number;
  prompt_tokens: number;
  completion_tokens: number;
  error?: string;
};

type ModelSummary = {
  model: string;
  perLang: Record<string, { passed: number; total: number; rate: number }>;
  totalPassed: number;
  totalAttempts: number;
  passRate: number;
  totalPromptTokens: number;
  totalCompletionTokens: number;
  langTax: Record<string, number>;
  timestamp: string;
  attempts: Attempt[];
};

function listTasks(): { slug: string; title: string; tags: string[]; difficulty: string }[] {
  return readdirSync(CORPUS_DIR)
    .filter((d) => /^\d{3}-/.test(d))
    .sort()
    .map((slug) => {
      const spec = JSON.parse(readFileSync(join(CORPUS_DIR, slug, "spec.json"), "utf8"));
      return {
        slug,
        title: spec.title,
        tags: spec.tags ?? [],
        difficulty: spec.difficulty ?? "easy",
      };
    });
}

function loadModelSummary(model: string): ModelSummary | null {
  const p = join(RESULTS_DIR, model, "summary.json");
  if (!existsSync(p)) return null;
  return JSON.parse(readFileSync(p, "utf8"));
}

function main() {
  const args = process.argv.slice(2);
  const toSite = args.includes("--site");

  const models = readdirSync(RESULTS_DIR)
    .filter((d) => {
      const p = join(RESULTS_DIR, d, "summary.json");
      return existsSync(p);
    })
    .sort();

  if (models.length === 0) {
    console.error("No per-model summaries found in", RESULTS_DIR);
    process.exit(1);
  }

  const tasks = listTasks();
  const dashboard = {
    generatedAt: new Date().toISOString(),
    models: [] as any[],
    tasks,
    perTaskPerModel: {} as Record<string, Record<string, Record<string, number>>>,
  };

  for (const model of models) {
    const sum = loadModelSummary(model);
    if (!sum) continue;

    // Model-level row.
    dashboard.models.push({
      model,
      perLang: sum.perLang,
      totalPassed: sum.totalPassed,
      totalAttempts: sum.totalAttempts,
      passRate: sum.passRate,
      langTax: sum.langTax,
      timestamp: sum.timestamp,
      totalPromptTokens: sum.totalPromptTokens,
      totalCompletionTokens: sum.totalCompletionTokens,
    });

    // Per-task per-language matrix.
    for (const a of sum.attempts) {
      if (!dashboard.perTaskPerModel[a.task]) dashboard.perTaskPerModel[a.task] = {};
      if (!dashboard.perTaskPerModel[a.task][model]) dashboard.perTaskPerModel[a.task][model] = {};
      dashboard.perTaskPerModel[a.task][model][a.lang] = a.passed ? 1 : 0;
    }
  }

  // Sort models by overall pass rate desc.
  dashboard.models.sort((a, b) => b.passRate - a.passRate);

  const out = join(RESULTS_DIR, "dashboard.json");
  writeFileSync(out, JSON.stringify(dashboard, null, 2));
  console.log(`Wrote ${out}`);
  console.log(`Models: ${dashboard.models.length}`);
  console.log(`Tasks:  ${dashboard.tasks.length}`);

  if (toSite) {
    if (!existsSync(SITE_DATA_DIR)) mkdirSync(SITE_DATA_DIR, { recursive: true });
    const siteOut = join(SITE_DATA_DIR, "agentlang-results.json");
    writeFileSync(siteOut, JSON.stringify(dashboard, null, 2));
    console.log(`Wrote ${siteOut}`);
  }

  // Print a quick table.
  console.log("");
  console.log("Model summary:");
  for (const m of dashboard.models) {
    const langCols = LANGS.map((l) => {
      const pl = (m.perLang as any)[l];
      if (!pl) return `${l}=--`;
      return `${l}=${Math.round(pl.rate * 100)}%`;
    }).join("  ");
    console.log(
      `  ${m.model.padEnd(20)}  overall=${Math.round(m.passRate * 100)}%  ${langCols}`
    );
  }
}

main();
