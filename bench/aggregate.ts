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

function firstNonEmptyLine(s: string | undefined): string {
  if (!s) return "";
  for (const line of s.split("\n")) {
    const t = line.trim();
    if (t.length > 0) return t;
  }
  return "";
}

function cleanExcerpt(s: string): string {
  return s
    .replace(/\/home\/phantom\/repos\/agentlang-index\/bench\/results\/[^\/]+\/runs\/[^\/]+\/[^\/]+\/scratch\//g, "")
    .replace(/\/tmp\/[^ :]*\//g, "");
}

function classifyFailure(stderr: string, exitCode: number, stdoutMatch: boolean): string {
  if (stderr.match(/PAR\d{3}|TYP\d{3}|CGEN\d{3}|BLD\d{3}/)) return "compile";
  if (stderr.match(/SyntaxError|SyntaxError:|panic\.go:|error\[E\d{4}\]|cannot find|expected|unexpected/)) return "compile";
  if (stderr.match(/SIGFPE|SIGSEGV|SIGILL|panic:|RuntimeError|TypeError|ValueError|IndexError|KeyError|ZeroDivisionError|stack overflow/)) return "runtime";
  if (exitCode === 0 && !stdoutMatch) return "wrong-output";
  if (exitCode !== 0 && stderr.length === 0) return "wrong-output";
  return "other";
}

const LANG_EXT: Record<string, string> = {
  zero: "zero",
  ts: "ts",
  rust: "rs",
  go: "go",
  python: "py",
};

const HARDEST_TIEBREAK: Record<string, number> = {
  zero: 0,
  rust: 1,
  go: 2,
  ts: 3,
  python: 4,
};

function readRefForLang(slug: string, lang: string): string {
  if (lang === "zero") {
    const refZero = join(CORPUS_DIR, slug, "ref.zero");
    if (existsSync(refZero)) return readFileSync(refZero, "utf8");
    const zeroDir = join(CORPUS_DIR, slug, "zero", "src");
    if (existsSync(zeroDir)) {
      const main = join(zeroDir, "main.0");
      const lib = join(zeroDir, "lib.0");
      const parts: string[] = [];
      if (existsSync(main)) parts.push(`// src/main.0\n${readFileSync(main, "utf8")}`);
      if (existsSync(lib)) parts.push(`// src/lib.0\n${readFileSync(lib, "utf8")}`);
      return parts.join("\n\n");
    }
    return "";
  }
  const ext = LANG_EXT[lang];
  if (!ext) return "";
  const p = join(CORPUS_DIR, slug, `ref.${ext}`);
  if (!existsSync(p)) return "";
  return readFileSync(p, "utf8");
}

function readPromptForTask(slug: string): string {
  const p = join(CORPUS_DIR, slug, "prompt.md");
  if (!existsSync(p)) return "";
  return readFileSync(p, "utf8");
}

function readNotesForTask(slug: string): string {
  const p = join(CORPUS_DIR, slug, "notes.md");
  if (!existsSync(p)) return "";
  return readFileSync(p, "utf8");
}

function readSpecForTask(slug: string): any {
  const p = join(CORPUS_DIR, slug, "spec.json");
  if (!existsSync(p)) return {};
  return JSON.parse(readFileSync(p, "utf8"));
}

function buildTasksPayload(
  modelDirs: string[],
  tasks: { slug: string; title: string; tags: string[]; difficulty: string }[],
) {
  // Pivot per-model attempts into per-task attempts.
  const perTaskAttempts: Record<string, any[]> = {};
  for (const t of tasks) perTaskAttempts[t.slug] = [];

  for (const model of modelDirs) {
    const sum = loadModelSummary(model);
    if (!sum) continue;
    for (const a of sum.attempts as any[]) {
      const cr0 = (a.case_results ?? [])[0] ?? {};
      const stderr = cr0.stderr ?? "";
      const exitCode = cr0.exit_code ?? 0;
      const stdoutMatch = cr0.stdout_match ?? false;
      const mode = a.passed ? "pass" : classifyFailure(stderr, exitCode, stdoutMatch);

      if (!perTaskAttempts[a.task]) perTaskAttempts[a.task] = [];
      perTaskAttempts[a.task].push({
        model,
        lang: a.lang,
        passed: a.passed,
        numCases: a.num_cases,
        numPassed: a.num_passed,
        failureMode: mode,
        failureExcerpt: a.passed ? "" : cleanExcerpt(firstNonEmptyLine(stderr)).slice(0, 240),
        apiMs: a.api_ms,
        execMs: a.exec_ms,
        promptTokens: a.prompt_tokens,
        completionTokens: a.completion_tokens,
      });
    }
  }

  const out: any = { generatedAt: new Date().toISOString(), tasks: [] };

  for (const t of tasks) {
    const attempts = perTaskAttempts[t.slug] ?? [];
    const spec = readSpecForTask(t.slug);
    const prompt = readPromptForTask(t.slug);
    const notes = readNotesForTask(t.slug);
    const refs: Record<string, string> = {};
    for (const lang of LANGS) {
      refs[lang] = readRefForLang(t.slug, lang);
    }

    // Hardest lang: lowest pass rate across models for this task. Ties: zero > rust > go > ts > python.
    const langPass: Record<string, { passed: number; total: number }> = {};
    for (const lang of LANGS) langPass[lang] = { passed: 0, total: 0 };
    for (const a of attempts) {
      if (!langPass[a.lang]) langPass[a.lang] = { passed: 0, total: 0 };
      langPass[a.lang].total += 1;
      if (a.passed) langPass[a.lang].passed += 1;
    }
    let hardestLang = "";
    let hardestRate = Infinity;
    for (const lang of LANGS) {
      const lp = langPass[lang];
      if (lp.total === 0) continue;
      const rate = lp.passed / lp.total;
      if (
        rate < hardestRate ||
        (rate === hardestRate && HARDEST_TIEBREAK[lang] < (HARDEST_TIEBREAK[hardestLang] ?? Infinity))
      ) {
        hardestRate = rate;
        hardestLang = lang;
      }
    }

    // Most common failure mode across failing attempts.
    const failureCounts: Record<string, number> = {};
    for (const a of attempts) {
      if (a.passed) continue;
      failureCounts[a.failureMode] = (failureCounts[a.failureMode] ?? 0) + 1;
    }
    let mostCommonFailureMode = "";
    let mostCommonCount = 0;
    for (const [mode, count] of Object.entries(failureCounts)) {
      if (count > mostCommonCount) {
        mostCommonCount = count;
        mostCommonFailureMode = mode;
      }
    }

    out.tasks.push({
      slug: t.slug,
      title: t.title,
      tags: t.tags,
      difficulty: t.difficulty,
      prompt,
      notes,
      acceptance: spec.acceptance ?? {},
      refs,
      attempts,
      hardestLang,
      mostCommonFailureMode,
    });
  }

  out.tasks.sort((a: any, b: any) => a.slug.localeCompare(b.slug));
  return out;
}

function buildModelsPayload(modelDirs: string[], tasks: { slug: string; title: string; tags: string[]; difficulty: string }[]) {
  const taskBySlug = new Map(tasks.map((t) => [t.slug, t]));
  const out: any = { generatedAt: new Date().toISOString(), models: [] };

  for (const model of modelDirs) {
    const sum = loadModelSummary(model);
    if (!sum) continue;

    const failureCountsByLang: Record<string, Record<string, number>> = {};
    for (const lang of LANGS) failureCountsByLang[lang] = { compile: 0, runtime: 0, "wrong-output": 0, other: 0, pass: 0 };

    const attempts: any[] = [];
    for (const a of sum.attempts as any[]) {
      const cr0 = (a.case_results ?? [])[0] ?? {};
      const stderr = cr0.stderr ?? "";
      const exitCode = cr0.exit_code ?? 0;
      const stdoutMatch = cr0.stdout_match ?? false;
      const mode = a.passed ? "pass" : classifyFailure(stderr, exitCode, stdoutMatch);
      failureCountsByLang[a.lang][mode] = (failureCountsByLang[a.lang][mode] ?? 0) + 1;

      const taskMeta = taskBySlug.get(a.task);
      attempts.push({
        task: a.task,
        taskTitle: taskMeta?.title ?? a.task,
        lang: a.lang,
        passed: a.passed,
        numCases: a.num_cases,
        numPassed: a.num_passed,
        failureMode: mode,
        failureExcerpt: a.passed ? "" : cleanExcerpt(firstNonEmptyLine(stderr)).slice(0, 240),
        apiMs: a.api_ms,
        execMs: a.exec_ms,
        promptTokens: a.prompt_tokens,
        completionTokens: a.completion_tokens,
      });
    }

    out.models.push({
      model,
      timestamp: sum.timestamp,
      perLang: sum.perLang,
      passRate: sum.passRate,
      totalPassed: sum.totalPassed,
      totalAttempts: sum.totalAttempts,
      totalPromptTokens: sum.totalPromptTokens,
      totalCompletionTokens: sum.totalCompletionTokens,
      langTax: sum.langTax,
      failureCountsByLang,
      attempts,
    });
  }

  out.models.sort((a: any, b: any) => b.passRate - a.passRate);
  return out;
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

    const modelsOut = join(SITE_DATA_DIR, "agentlang-models.json");
    const modelsPayload = buildModelsPayload(models, tasks);
    writeFileSync(modelsOut, JSON.stringify(modelsPayload, null, 2));
    console.log(`Wrote ${modelsOut}`);

    const tasksOut = join(SITE_DATA_DIR, "agentlang-tasks.json");
    const tasksPayload = buildTasksPayload(models, tasks);
    writeFileSync(tasksOut, JSON.stringify(tasksPayload, null, 2));
    console.log(`Wrote ${tasksOut}`);
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
