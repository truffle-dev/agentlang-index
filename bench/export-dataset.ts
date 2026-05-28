#!/usr/bin/env bun
/**
 * Export a benchmark run as a CC-BY-4.0 open dataset under
 * <dest>/exports/<YYYY-MM-DD>/. Pairs with truffle-dev/agentlang-index-data.
 *
 * What lands on disk:
 *   manifest.json   one object pinning harness SHA, Zero version, model
 *                   list, task list, language list, and per-run totals.
 *   dashboard.json  verbatim copy of bench/results/dashboard.json.
 *   runs.json       flat array of 300 attempt records, one per
 *                   (model, task, lang). Each record carries timing,
 *                   tokens, pass/fail, and a derived failure mode.
 *   attempts/<model>/<task>/<lang>/{response.md, system.md, user.md,
 *                                   result.json}   raw artifacts. The
 *   scratch/ trees under bench/results are excluded — they're
 *   reproducible and add hundreds of KB per attempt.
 *
 * Usage:
 *   bun bench/export-dataset.ts --dest /path/to/agentlang-index-data
 */

import {
  readFileSync,
  writeFileSync,
  readdirSync,
  existsSync,
  mkdirSync,
  copyFileSync,
  statSync,
} from "fs";
import { execSync } from "child_process";
import { dirname, join } from "path";

const REPO_ROOT = "/home/phantom/repos/agentlang-index";
const RESULTS_DIR = join(REPO_ROOT, "bench", "results");
const CORPUS_DIR = join(REPO_ROOT, "corpus");
const ZERO_VERSION_FILE = join(REPO_ROOT, "vendor", "zero", "CURRENT", "version.txt");

const MODELS = ["gpt-5", "gpt-4o", "gpt-4o-mini"];
const LANGS = ["zero", "ts", "rust", "go", "python"];

type CaseResult = {
  hidden: boolean;
  passed: boolean;
  stdout_match: boolean;
  stderr_empty: boolean;
  exit_zero: boolean;
  stdout: string;
  stderr: string;
  exit_code: number;
  ms: number;
};

type AttemptRaw = {
  model: string;
  task: string;
  lang: string;
  passed: boolean;
  extracted: boolean;
  case_results: CaseResult[];
  pass_rate: number;
  num_cases: number;
  num_passed: number;
  api_ms: number;
  build_ms: number;
  exec_ms: number;
  total_ms: number;
  prompt_tokens: number;
  completion_tokens: number;
  error?: string;
};

type ModelSummary = {
  model: string;
  totalPassed: number;
  totalAttempts: number;
  passRate: number;
  totalPromptTokens: number;
  totalCompletionTokens: number;
  timestamp: string;
  attempts: AttemptRaw[];
};

function parseArgs(argv: string[]): { dest: string } {
  let dest = "";
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--dest" && i + 1 < argv.length) {
      dest = argv[i + 1];
      i++;
    }
  }
  if (!dest) {
    console.error("error: --dest <path> is required");
    process.exit(2);
  }
  return { dest };
}

function listTasks(): string[] {
  return readdirSync(CORPUS_DIR)
    .filter((d) => /^\d{3}-/.test(d))
    .sort();
}

function readZeroVersion(): string {
  // The first line of version.txt is "zero <semver>". Pull the version
  // out so the manifest carries a clean string.
  const raw = readFileSync(ZERO_VERSION_FILE, "utf8");
  const first = raw.split("\n", 1)[0].trim();
  const match = first.match(/^zero\s+(.+)$/);
  return match ? match[1] : first;
}

function loadModelSummary(model: string): ModelSummary {
  const p = join(RESULTS_DIR, model, "summary.json");
  if (!existsSync(p)) {
    throw new Error(`missing summary.json for model ${model} at ${p}`);
  }
  return JSON.parse(readFileSync(p, "utf8"));
}

function ensureDir(p: string): void {
  if (!existsSync(p)) mkdirSync(p, { recursive: true });
}

function safeCopy(src: string, dst: string): boolean {
  if (!existsSync(src)) return false;
  ensureDir(dirname(dst));
  copyFileSync(src, dst);
  return true;
}

// Derive a single failure-mode label for an attempt. Buckets:
//   pass             every case passed.
//   not_extracted    model output did not yield a runnable artifact.
//   compile_error    case list is empty due to a build failure, or the
//                    first failing case carries a compiler-marker stderr
//                    in a language with a compile step (zero/rust/go/ts).
//   runtime_panic    first failing case exited non-zero with stderr text
//                    that is not a compile-marker.
//   wrong_output     first failing case exited cleanly but stdout did
//                    not match (or exited non-zero with no stderr text).
//   other            anything else (rare).
function deriveFailureMode(a: AttemptRaw): string {
  if (a.passed) return "pass";
  if (!a.extracted) return "not_extracted";
  // Empty case list with a build_error marker is a hard compile failure.
  if ((a.case_results ?? []).length === 0) {
    const err = a.error ?? "";
    if (/^build_error:|^compile_error:/.test(err)) return "compile_error";
    return "other";
  }
  // First *failing* case is the verdict — first passing cases mask
  // later failures otherwise.
  const failed = (a.case_results ?? []).find((c) => !c.passed);
  if (!failed) return "other";
  const stderr = failed.stderr ?? "";
  const compileMarker =
    /PAR\d{3}|TYP\d{3}|CGEN\d{3}|BLD\d{3}|IMP\d{3}|error\[E\d{4}\]|error TS\d+|SyntaxError|panic\.go:/;
  if (!failed.exit_zero && stderr.length > 0) {
    if (
      (a.lang === "zero" || a.lang === "rust" || a.lang === "go" || a.lang === "ts") &&
      compileMarker.test(stderr)
    ) {
      return "compile_error";
    }
    return "runtime_panic";
  }
  if (failed.exit_zero && !failed.stdout_match) return "wrong_output";
  if (!failed.exit_zero && stderr.length === 0) return "wrong_output";
  return "other";
}

function toRecord(a: AttemptRaw): Record<string, unknown> {
  return {
    model: a.model,
    task: a.task,
    lang: a.lang,
    passed: a.passed,
    extracted: a.extracted,
    numCases: a.num_cases,
    numPassed: a.num_passed,
    passRate: a.pass_rate,
    apiMs: a.api_ms,
    buildMs: a.build_ms,
    execMs: a.exec_ms,
    totalMs: a.total_ms,
    promptTokens: a.prompt_tokens,
    completionTokens: a.completion_tokens,
    mostCommonFailureMode: deriveFailureMode(a),
  };
}

function bytesOf(p: string): number {
  return statSync(p).size;
}

function main(): void {
  const { dest } = parseArgs(process.argv.slice(2));
  if (!existsSync(dest)) {
    console.error(`error: --dest path does not exist: ${dest}`);
    process.exit(2);
  }

  const tasks = listTasks();
  if (tasks.length !== 20) {
    console.error(`error: expected 20 corpus tasks, found ${tasks.length}`);
    process.exit(2);
  }

  const summaries = MODELS.map(loadModelSummary);
  const allAttempts: AttemptRaw[] = summaries.flatMap((s) => s.attempts);
  if (allAttempts.length !== MODELS.length * tasks.length * LANGS.length) {
    console.error(
      `error: expected ${MODELS.length * tasks.length * LANGS.length} attempts, ` +
        `found ${allAttempts.length}`,
    );
    process.exit(2);
  }

  // Run window: earliest model timestamp = start, latest = finish.
  // Treats per-model wall-clock as the run boundary, which matches how
  // the harness drove the three runs back-to-back.
  const timestamps = summaries.map((s) => s.timestamp).sort();
  const runStartedAt = timestamps[0];
  const runFinishedAt = timestamps[timestamps.length - 1];
  const runDate = runStartedAt.slice(0, 10);

  const harnessSha = execSync("git rev-parse HEAD", { cwd: REPO_ROOT })
    .toString()
    .trim();
  const zeroVersion = readZeroVersion();

  const tokensTotalPrompt = summaries.reduce((s, m) => s + m.totalPromptTokens, 0);
  const tokensTotalCompletion = summaries.reduce(
    (s, m) => s + m.totalCompletionTokens,
    0,
  );
  const passedTotal = summaries.reduce((s, m) => s + m.totalPassed, 0);
  const attemptsTotal = allAttempts.length;
  const passRate = passedTotal / attemptsTotal;

  const exportRoot = join(dest, "exports", runDate);
  ensureDir(exportRoot);

  // manifest.json
  const manifest = {
    datasetVersion: "1.0.0",
    runDate,
    harnessRepo: "github.com/truffle-dev/agentlang-index",
    harnessSha,
    zeroVersion,
    models: MODELS,
    tasks,
    languages: LANGS,
    attemptsTotal,
    mode: "one-shot",
    provider: "openai",
    corpus: {
      repo: "github.com/truffle-dev/agentlang-index",
      treeish: harnessSha,
      taskCount: tasks.length,
    },
    runStartedAt,
    runFinishedAt,
    tokensTotalPrompt,
    tokensTotalCompletion,
    passedTotal,
    passRate,
  };
  const manifestPath = join(exportRoot, "manifest.json");
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");

  // dashboard.json — verbatim copy.
  const dashboardSrc = join(RESULTS_DIR, "dashboard.json");
  const dashboardDst = join(exportRoot, "dashboard.json");
  copyFileSync(dashboardSrc, dashboardDst);

  // runs.json — flat array, sorted by (model, task, lang) for stable diffs.
  const records = allAttempts.map(toRecord);
  records.sort((a, b) => {
    const m = (a.model as string).localeCompare(b.model as string);
    if (m !== 0) return m;
    const t = (a.task as string).localeCompare(b.task as string);
    if (t !== 0) return t;
    return (a.lang as string).localeCompare(b.lang as string);
  });
  const runsPath = join(exportRoot, "runs.json");
  writeFileSync(runsPath, JSON.stringify(records, null, 2) + "\n");

  // attempts/<model>/<task>/<lang>/{response.md, system.md, user.md, result.json}
  let copiedFiles = 0;
  let missing: string[] = [];
  for (const a of allAttempts) {
    const srcDir = join(RESULTS_DIR, a.model, "runs", a.task, a.lang);
    const dstDir = join(exportRoot, "attempts", a.model, a.task, a.lang);
    for (const name of ["response.md", "system.md", "user.md", "result.json"]) {
      const src = join(srcDir, name);
      const dst = join(dstDir, name);
      if (safeCopy(src, dst)) {
        copiedFiles++;
      } else {
        missing.push(`${a.model}/${a.task}/${a.lang}/${name}`);
      }
    }
  }
  if (missing.length > 0) {
    console.error(`error: ${missing.length} expected attempt files missing:`);
    for (const m of missing.slice(0, 10)) console.error(`  ${m}`);
    process.exit(1);
  }

  // Walk the export tree for a byte/file tally.
  let fileCount = 0;
  let totalBytes = 0;
  function walk(dir: string): void {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const p = join(dir, entry.name);
      if (entry.isDirectory()) walk(p);
      else if (entry.isFile()) {
        fileCount++;
        totalBytes += bytesOf(p);
      }
    }
  }
  walk(exportRoot);

  const mb = (totalBytes / 1024 / 1024).toFixed(2);
  console.log(
    `wrote ${fileCount} files (${totalBytes} bytes, ${mb} MB) to ${exportRoot}`,
  );
}

main();
