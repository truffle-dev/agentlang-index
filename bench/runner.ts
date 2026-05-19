#!/usr/bin/env bun
/**
 * AgentLang Index — single-attempt OpenAI benchmark runner.
 *
 * For each (model, task, language):
 *   1. Compose a prompt from prompt.md + per-language calling convention.
 *   2. Call OpenAI Chat Completions API (temperature=0, deterministic).
 *   3. Extract the source from the response (handles fenced markdown).
 *   4. Materialize the source into a scratch dir matching the language's
 *      reference layout (single-file for ts/rust/go/python, multi-file
 *      project for Zero when task uses one).
 *   5. Read each test case from tests/{public,hidden}/case-NNN.json,
 *      invoke the compiled/scripted artifact with stdin (or argv for
 *      Zero), and compare bytes exactly against expected_stdout.
 *   6. Persist prompt, response, extracted code, per-case captures, and
 *      a result.json summary.
 *
 * Usage:
 *   bun run bench/runner.ts --model gpt-5.5
 *   bun run bench/runner.ts --model gpt-4o-mini --task 000-hello-stdout
 *   bun run bench/runner.ts --model gpt-5.2-codex --lang python
 *   bun run bench/runner.ts --models gpt-5.5,gpt-4o-mini --tasks 000,001,002
 */

import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from "fs";
import { spawnSync, spawn } from "child_process";
import { join, dirname } from "path";
import { tmpdir } from "os";

const REPO_ROOT = "/home/phantom/repos/agentlang-index";
const CORPUS_DIR = join(REPO_ROOT, "corpus");
const BENCH_DIR = join(REPO_ROOT, "bench");
const RESULTS_DIR = join(BENCH_DIR, "results");
const ZERO_BIN = "/home/phantom/repos/zero/bin/zero";

const LANG_EXT: Record<string, string> = {
  zero: "0",
  ts: "ts",
  rust: "rs",
  go: "go",
  python: "py",
};

// Per-language calling convention summary baked into the prompt.
const LANG_CALL_NOTES: Record<string, string> = {
  zero: `Target: Vercel Labs' Zero 0.1.2 agent-first language. Zero 0.1.2 has no exposed stdin — read inputs from argv. Multi-file projects use \`use lib\` and a zero.json manifest. Lib functions cannot take Span<u8>, MutSpan<u8>, or shape values at the module boundary (direct ELF64 backend restriction). Output goes to world.out via \`check world.out.write("...")\` or \`check world.out.write(buf[0..n])\`. End \`main\` with explicit \`return\` to avoid trailing-write byte-count exit-code codegen quirk. No semicolons. No if-expressions in let bindings (statement-only).`,
  ts: `Target: TypeScript via tsx (Node.js). Read stdin via \`for await (const chunk of process.stdin)\`. Write to stdout via \`process.stdout.write(...)\`. Single-file program at ref.ts.`,
  rust: `Target: Rust 2021 edition. Cargo.toml with single binary at path "ref.rs". Read stdin via \`std::io::stdin().read_to_string(...)\` and write via \`std::io::stdout().write_all(...)\`. Single-file program at ref.rs.`,
  go: `Target: Go 1.21+. \`package main\` with \`func main()\`. Read stdin via \`bufio.NewReader(os.Stdin)\` and write via \`bufio.NewWriter(os.Stdout)\`. Single-file program at ref.go.`,
  python: `Target: Python 3.10+. Read stdin via \`sys.stdin.read()\` and write via \`sys.stdout.write(...)\`. Single-file program at ref.py.`,
};

type Task = {
  slug: string;
  dir: string;
  spec: any;
  promptMd: string;
  cases: TestCase[];
  hasZeroProject: boolean;
};

type TestCase = {
  name: string;
  stdin: string;
  argv: string[];
  expected_stdout: string;
  expected_stderr: string;
  expected_exit: number;
  hidden: boolean;
};

type AttemptResult = {
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

type CaseResult = {
  name: string;
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

function loadTask(slug: string): Task {
  const dir = join(CORPUS_DIR, slug);
  const spec = JSON.parse(readFileSync(join(dir, "spec.json"), "utf8"));
  const promptMd = readFileSync(join(dir, "prompt.md"), "utf8");

  const cases: TestCase[] = [];
  for (const subdir of ["public", "hidden"]) {
    const testDir = join(dir, "tests", subdir);
    if (!existsSync(testDir)) continue;
    for (const file of readdirSync(testDir).sort()) {
      if (!file.endsWith(".json")) continue;
      const c = JSON.parse(readFileSync(join(testDir, file), "utf8"));
      cases.push({
        name: c.name,
        stdin: c.stdin ?? "",
        argv: c.argv ?? [],
        expected_stdout: c.expected_stdout ?? "",
        expected_stderr: c.expected_stderr ?? "",
        expected_exit: c.expected_exit ?? 0,
        hidden: subdir === "hidden",
      });
    }
  }

  // Detect multi-file Zero project (zero/zero.json + zero/src/main.0 + zero/src/lib.0)
  const hasZeroProject = existsSync(join(dir, "zero", "zero.json"));

  return { slug, dir, spec, promptMd, cases, hasZeroProject };
}

function listTasks(): string[] {
  return readdirSync(CORPUS_DIR)
    .filter((d) => /^\d{3}-/.test(d))
    .sort();
}

function buildSystemPrompt(task: Task, lang: string): string {
  return `You are an expert programmer producing a complete, correct, byte-exact reference implementation in ${lang}.

The program is invoked exactly once per test case. It must match expected_stdout byte-for-byte and write nothing to stderr. It must exit with status 0 in every case (including documented error cases that write "error\\n" to stdout).

${LANG_CALL_NOTES[lang]}

Output ONLY the source code, fenced in a single \`\`\`${lang}-tagged code block. No commentary, no explanation, no surrounding prose. The code block contents will be extracted and written to disk verbatim.

If the task is a multi-file Zero project, output ALL files separated by file markers like \`=== src/main.0 ===\` (a header line) followed by the file contents. Use this only for Zero multi-file projects; single-file languages emit one code block.`;
}

function buildUserPrompt(task: Task, lang: string): string {
  let convention = "";
  if (lang === "zero" && task.hasZeroProject) {
    convention = `\n\n## Multi-file Zero project layout\n\nWrite a multi-file Zero project. Emit at minimum:\n\n=== zero.json ===\n{\n  "package": { "name": "${("t_" + task.slug.replace(/-/g, "_"))}", "version": "0.1.0", "license": "MIT" },\n  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },\n  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }\n}\n\n=== src/main.0 ===\n(your driver, with \`use lib\` to pull in helpers)\n\n=== src/lib.0 ===\n(scalar-only exports, no Span<u8>/shape values)\n\nInvoked as: zero run <projdir> -- <argv...>\n`;
  } else if (lang === "zero") {
    convention = `\n\n## Single-file Zero layout\n\nWrite a single-file Zero program (ref.zero). Read arguments from std.args (no stdin available). Invoked as: zero run ref.zero <argv...>\n`;
  }
  return `## Spec\n\n${task.promptMd}${convention}`;
}

async function callOpenAI(
  model: string,
  systemPrompt: string,
  userPrompt: string,
  apiKey: string
): Promise<{ text: string; promptTokens: number; completionTokens: number; ms: number }> {
  const t0 = Date.now();
  const body: any = {
    model,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
  };
  // gpt-5/o-series models reject temperature/top_p; use default sampling.
  if (!/^(gpt-5|o[134])/.test(model)) {
    body.temperature = 0;
  }
  // o-series and gpt-5 use max_completion_tokens; older models use max_tokens.
  const tokenField = /^(gpt-5|o[134])/.test(model) ? "max_completion_tokens" : "max_tokens";
  body[tokenField] = 8192;

  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });
  const ms = Date.now() - t0;
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`OpenAI ${res.status}: ${errText.slice(0, 500)}`);
  }
  const json: any = await res.json();
  const text = json.choices?.[0]?.message?.content ?? "";
  return {
    text,
    promptTokens: json.usage?.prompt_tokens ?? 0,
    completionTokens: json.usage?.completion_tokens ?? 0,
    ms,
  };
}

/**
 * Extract source from model response. Handles:
 *   - Single fenced block: ```lang\n...\n```
 *   - Single fenced block without lang: ```\n...\n```
 *   - Raw code (no fence)
 *   - Multi-file response with === path === headers
 */
function extractFiles(
  response: string,
  lang: string
): { files: Record<string, string>; ok: boolean } {
  // Check for multi-file markers first.
  const multiFileRe = /^===\s*([^\s=]+(?:\s+[^\s=]+)*)\s*===\s*$/gm;
  const matches = [...response.matchAll(multiFileRe)];
  if (matches.length > 0) {
    const files: Record<string, string> = {};
    for (let i = 0; i < matches.length; i++) {
      const path = matches[i][1].trim();
      const start = matches[i].index! + matches[i][0].length;
      const end = i + 1 < matches.length ? matches[i + 1].index! : response.length;
      let content = response.slice(start, end).trim();
      // Strip surrounding code fence if present.
      content = stripFence(content);
      files[path] = content;
    }
    return { files, ok: true };
  }

  // Single fenced block.
  const fenceRe = /```(?:\w+)?\s*\n([\s\S]*?)\n```/;
  const m = response.match(fenceRe);
  if (m) {
    return { files: { __single__: m[1] }, ok: true };
  }

  // Fallback: assume the entire response is code (rare for chat models).
  if (response.trim().length > 0) {
    return { files: { __single__: response.trim() }, ok: true };
  }
  return { files: {}, ok: false };
}

function stripFence(s: string): string {
  const m = s.match(/^```(?:\w+)?\s*\n([\s\S]*?)\n```\s*$/);
  return m ? m[1] : s;
}

function materializeFiles(
  scratchDir: string,
  lang: string,
  files: Record<string, string>,
  task: Task
): { ok: boolean; entrypoint: string; error?: string } {
  mkdirSync(scratchDir, { recursive: true });

  if (lang === "zero" && task.hasZeroProject) {
    // Multi-file Zero project. Expect zero.json + src/main.0 + src/lib.0.
    const projDir = join(scratchDir, "zero");
    mkdirSync(join(projDir, "src"), { recursive: true });
    if (files.__single__) {
      // Model only emitted one block — assume it's main.0 and synthesize a manifest.
      writeFileSync(
        join(projDir, "zero.json"),
        JSON.stringify(
          {
            package: { name: ("t_" + task.slug.replace(/-/g, "_")), version: "0.1.0", license: "MIT" },
            targets: {
              cli: {
                kind: "exe",
                main: "src/main.0",
                defaultTarget: "linux-musl-x64",
                devTarget: "host",
                releaseProfile: "release-small",
              },
            },
            deps: {},
            profiles: {
              dev: { inherits: "dev" },
              "release-small": { inherits: "release-small" },
            },
          },
          null,
          2
        )
      );
      writeFileSync(join(projDir, "src", "main.0"), files.__single__);
      return { ok: true, entrypoint: projDir };
    }
    // Multi-file mode: write each file declared.
    for (const [path, content] of Object.entries(files)) {
      const target = join(projDir, path);
      mkdirSync(dirname(target), { recursive: true });
      writeFileSync(target, content);
    }
    if (!existsSync(join(projDir, "zero.json"))) {
      return { ok: false, entrypoint: "", error: "missing zero.json in response" };
    }
    return { ok: true, entrypoint: projDir };
  }

  // Single-file languages.
  const fileName = lang === "zero" ? "ref.zero" : `ref.${LANG_EXT[lang]}`;
  const content = files.__single__ ?? Object.values(files)[0] ?? "";
  if (!content) return { ok: false, entrypoint: "", error: "no content extracted" };
  writeFileSync(join(scratchDir, fileName), content);

  if (lang === "rust") {
    // Generate a minimal Cargo.toml.
    const cargoToml = `[package]
name = "${("t_" + task.slug.replace(/-/g, "_"))}"
version = "0.1.0"
edition = "2021"
publish = false

[[bin]]
name = "${("t_" + task.slug.replace(/-/g, "_"))}"
path = "ref.rs"

[profile.release]
opt-level = "z"
`;
    writeFileSync(join(scratchDir, "Cargo.toml"), cargoToml);
  } else if (lang === "go") {
    const goMod = `module ${("t_" + task.slug.replace(/-/g, "_"))}\n\ngo 1.21\n`;
    writeFileSync(join(scratchDir, "go.mod"), goMod);
  }

  return { ok: true, entrypoint: join(scratchDir, fileName) };
}

function build(
  lang: string,
  scratchDir: string,
  entrypoint: string,
  task: Task
): { ok: boolean; runner: string[]; ms: number; error?: string } {
  const t0 = Date.now();

  if (lang === "ts") {
    return { ok: true, runner: ["bun", "run", entrypoint], ms: Date.now() - t0 };
  }
  if (lang === "python") {
    return { ok: true, runner: ["python3", entrypoint], ms: Date.now() - t0 };
  }
  if (lang === "go") {
    // go run is acceptable here — pre-build per task is heavier and not the
    // point. For repeated runs we could `go build -o bin/main` but the
    // tradeoff favors simplicity for now.
    return { ok: true, runner: ["go", "run", entrypoint], ms: Date.now() - t0 };
  }
  if (lang === "rust") {
    const res = spawnSync("cargo", ["build", "--release", "--quiet"], {
      cwd: scratchDir,
      env: { ...process.env, PATH: process.env.PATH! },
      stdio: ["ignore", "pipe", "pipe"],
      timeout: 60_000,
    });
    if (res.status !== 0) {
      return {
        ok: false,
        runner: [],
        ms: Date.now() - t0,
        error: `cargo build failed: ${res.stderr?.toString().slice(0, 500)}`,
      };
    }
    return {
      ok: true,
      runner: [join(scratchDir, "target", "release", ("t_" + task.slug.replace(/-/g, "_")))],
      ms: Date.now() - t0,
    };
  }
  if (lang === "zero") {
    // Zero compiles on `zero run`. Smoke-build with `zero build` if available;
    // otherwise just trust the runner.
    if (task.hasZeroProject) {
      // entrypoint is the project dir.
      return {
        ok: true,
        runner: [ZERO_BIN, "run", entrypoint, "--"],
        ms: Date.now() - t0,
      };
    }
    return { ok: true, runner: [ZERO_BIN, "run", entrypoint], ms: Date.now() - t0 };
  }
  return { ok: false, runner: [], ms: Date.now() - t0, error: `unknown lang: ${lang}` };
}

function runCase(
  runner: string[],
  testCase: TestCase,
  lang: string,
  timeoutMs: number,
  fixtureCwd?: string
): CaseResult {
  const t0 = Date.now();
  let cmdArgs: string[];
  let useStdin: boolean;
  if (lang === "zero") {
    // Zero gets the input via argv (after the -- separator).
    cmdArgs = [...runner.slice(1), ...testCase.argv];
    useStdin = false;
  } else {
    cmdArgs = runner.slice(1);
    useStdin = true;
  }

  const res = spawnSync(runner[0], cmdArgs, {
    input: useStdin ? testCase.stdin : undefined,
    timeout: timeoutMs,
    cwd: fixtureCwd,
  });

  const ms = Date.now() - t0;
  const stdout = res.stdout ? Buffer.from(res.stdout).toString("utf8") : "";
  const stderr = res.stderr ? Buffer.from(res.stderr).toString("utf8") : "";
  const exitCode = res.status ?? -1;

  const stdoutMatch = stdout === testCase.expected_stdout;
  const stderrEmpty = stderr === testCase.expected_stderr;
  const exitZero = exitCode === testCase.expected_exit;

  return {
    name: testCase.name,
    hidden: testCase.hidden,
    passed: stdoutMatch && stderrEmpty && exitZero,
    stdout_match: stdoutMatch,
    stderr_empty: stderrEmpty,
    exit_zero: exitZero,
    stdout: stdout.slice(0, 4096),
    stderr: stderr.slice(0, 4096),
    exit_code: exitCode,
    ms,
  };
}

function fixtureScriptFor(task: Task): string | null {
  // Tasks 012-014 have a fixture_server.py that must be running.
  if (task.spec.tags?.includes("http")) {
    const fixturePath = join(task.dir, "fixture_server.py");
    if (existsSync(fixturePath)) return fixturePath;
  }
  return null;
}

async function runAttempt(
  model: string,
  task: Task,
  lang: string,
  apiKey: string
): Promise<AttemptResult> {
  const t0 = Date.now();
  const outDir = join(RESULTS_DIR, model, "runs", task.slug, lang);
  mkdirSync(outDir, { recursive: true });

  const systemPrompt = buildSystemPrompt(task, lang);
  const userPrompt = buildUserPrompt(task, lang);
  writeFileSync(join(outDir, "system.md"), systemPrompt);
  writeFileSync(join(outDir, "user.md"), userPrompt);

  let apiResp;
  try {
    apiResp = await callOpenAI(model, systemPrompt, userPrompt, apiKey);
  } catch (e: any) {
    const result: AttemptResult = {
      model,
      task: task.slug,
      lang,
      passed: false,
      extracted: false,
      case_results: [],
      pass_rate: 0,
      num_cases: task.cases.length,
      num_passed: 0,
      api_ms: Date.now() - t0,
      build_ms: 0,
      exec_ms: 0,
      total_ms: Date.now() - t0,
      prompt_tokens: 0,
      completion_tokens: 0,
      error: `api_error: ${e.message}`,
    };
    writeFileSync(join(outDir, "result.json"), JSON.stringify(result, null, 2));
    return result;
  }
  writeFileSync(join(outDir, "response.md"), apiResp.text);

  const { files, ok: extracted } = extractFiles(apiResp.text, lang);
  if (!extracted) {
    const result: AttemptResult = {
      model,
      task: task.slug,
      lang,
      passed: false,
      extracted: false,
      case_results: [],
      pass_rate: 0,
      num_cases: task.cases.length,
      num_passed: 0,
      api_ms: apiResp.ms,
      build_ms: 0,
      exec_ms: 0,
      total_ms: Date.now() - t0,
      prompt_tokens: apiResp.promptTokens,
      completion_tokens: apiResp.completionTokens,
      error: "no_code_extracted",
    };
    writeFileSync(join(outDir, "result.json"), JSON.stringify(result, null, 2));
    return result;
  }

  const scratchDir = join(outDir, "scratch");
  const mat = materializeFiles(scratchDir, lang, files, task);
  if (!mat.ok) {
    const result: AttemptResult = {
      model,
      task: task.slug,
      lang,
      passed: false,
      extracted: true,
      case_results: [],
      pass_rate: 0,
      num_cases: task.cases.length,
      num_passed: 0,
      api_ms: apiResp.ms,
      build_ms: 0,
      exec_ms: 0,
      total_ms: Date.now() - t0,
      prompt_tokens: apiResp.promptTokens,
      completion_tokens: apiResp.completionTokens,
      error: `materialize_error: ${mat.error}`,
    };
    writeFileSync(join(outDir, "result.json"), JSON.stringify(result, null, 2));
    return result;
  }

  const build0 = Date.now();
  const built = build(lang, scratchDir, mat.entrypoint, task);
  const buildMs = Date.now() - build0;
  if (!built.ok) {
    const result: AttemptResult = {
      model,
      task: task.slug,
      lang,
      passed: false,
      extracted: true,
      case_results: [],
      pass_rate: 0,
      num_cases: task.cases.length,
      num_passed: 0,
      api_ms: apiResp.ms,
      build_ms: buildMs,
      exec_ms: 0,
      total_ms: Date.now() - t0,
      prompt_tokens: apiResp.promptTokens,
      completion_tokens: apiResp.completionTokens,
      error: `build_error: ${built.error}`,
    };
    writeFileSync(join(outDir, "result.json"), JSON.stringify(result, null, 2));
    return result;
  }

  // Start HTTP fixture if needed.
  let fixtureProc: any = null;
  const fixture = fixtureScriptFor(task);
  if (fixture) {
    const port = 18000 + parseInt(task.slug.slice(0, 3), 10);
    fixtureProc = spawn("python3", [fixture, String(port)], {
      stdio: ["ignore", "pipe", "pipe"],
    });
    // Wait up to 5s for "ready" marker.
    let ready = false;
    const start = Date.now();
    await new Promise<void>((resolve) => {
      fixtureProc.stdout.on("data", (chunk: Buffer) => {
        if (chunk.toString().includes("ready")) {
          ready = true;
          resolve();
        }
      });
      setTimeout(() => resolve(), 5000);
    });
    if (!ready) {
      try { fixtureProc.kill(); } catch {}
      const result: AttemptResult = {
        model,
        task: task.slug,
        lang,
        passed: false,
        extracted: true,
        case_results: [],
        pass_rate: 0,
        num_cases: task.cases.length,
        num_passed: 0,
        api_ms: apiResp.ms,
        build_ms: buildMs,
        exec_ms: 0,
        total_ms: Date.now() - t0,
        prompt_tokens: apiResp.promptTokens,
        completion_tokens: apiResp.completionTokens,
        error: "fixture_failed_to_start",
      };
      writeFileSync(join(outDir, "result.json"), JSON.stringify(result, null, 2));
      return result;
    }
  }

  const exec0 = Date.now();
  const caseResults: CaseResult[] = [];
  const wallMax = task.spec.acceptance?.wall_time_max_ms ?? 5000;
  for (const tc of task.cases) {
    const cr = runCase(built.runner, tc, lang, wallMax + 2000);
    caseResults.push(cr);
  }
  const execMs = Date.now() - exec0;

  if (fixtureProc) {
    try { fixtureProc.kill(); } catch {}
  }

  const numPassed = caseResults.filter((c) => c.passed).length;
  const passed = numPassed === caseResults.length && caseResults.length > 0;
  const result: AttemptResult = {
    model,
    task: task.slug,
    lang,
    passed,
    extracted: true,
    case_results: caseResults,
    pass_rate: caseResults.length > 0 ? numPassed / caseResults.length : 0,
    num_cases: caseResults.length,
    num_passed: numPassed,
    api_ms: apiResp.ms,
    build_ms: buildMs,
    exec_ms: execMs,
    total_ms: Date.now() - t0,
    prompt_tokens: apiResp.promptTokens,
    completion_tokens: apiResp.completionTokens,
  };
  writeFileSync(join(outDir, "result.json"), JSON.stringify(result, null, 2));
  return result;
}

function parseArgs(): {
  models: string[];
  tasks: string[];
  langs: string[];
  skipExisting: boolean;
} {
  const argv = process.argv.slice(2);
  let models: string[] = [];
  let tasks: string[] = [];
  let langs: string[] = ["zero", "ts", "rust", "go", "python"];
  let skipExisting = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--model") {
      models = [argv[++i]];
    } else if (argv[i] === "--models") {
      models = argv[++i].split(",");
    } else if (argv[i] === "--task") {
      tasks = [argv[++i]];
    } else if (argv[i] === "--tasks") {
      tasks = argv[++i].split(",");
    } else if (argv[i] === "--lang") {
      langs = [argv[++i]];
    } else if (argv[i] === "--langs") {
      langs = argv[++i].split(",");
    } else if (argv[i] === "--skip-existing") {
      skipExisting = true;
    }
  }
  if (models.length === 0) {
    console.error("Error: --model or --models required");
    process.exit(2);
  }
  if (tasks.length === 0) {
    tasks = listTasks();
  } else {
    // Allow short prefixes like "000" matching "000-hello-stdout".
    const all = listTasks();
    tasks = tasks.flatMap((t) => {
      const matches = all.filter((slug) => slug.startsWith(t));
      return matches.length > 0 ? matches : [t];
    });
  }
  return { models, tasks, langs, skipExisting };
}

async function main() {
  const apiKey = (process.env.OPENAI_API_KEY ?? "").trim();
  if (!apiKey) {
    console.error("Error: OPENAI_API_KEY not set");
    process.exit(2);
  }
  const { models, tasks, langs, skipExisting } = parseArgs();
  mkdirSync(RESULTS_DIR, { recursive: true });

  console.log(`Models: ${models.join(", ")}`);
  console.log(`Tasks: ${tasks.length} (${tasks[0]}..${tasks[tasks.length - 1]})`);
  console.log(`Langs: ${langs.join(", ")}`);
  console.log("");

  for (const model of models) {
    const all: AttemptResult[] = [];
    const summaryPath = join(RESULTS_DIR, model, "summary.json");
    // Load prior summary if skip-existing.
    let prior: Record<string, AttemptResult> = {};
    if (skipExisting && existsSync(summaryPath)) {
      const p = JSON.parse(readFileSync(summaryPath, "utf8"));
      for (const r of p.attempts ?? []) {
        prior[`${r.task}:${r.lang}`] = r;
      }
    }
    for (const taskSlug of tasks) {
      let task: Task;
      try {
        task = loadTask(taskSlug);
      } catch (e: any) {
        console.log(`SKIP ${model} ${taskSlug}: ${e.message}`);
        continue;
      }
      for (const lang of langs) {
        if (!task.spec.languages?.includes(lang)) continue;
        const key = `${taskSlug}:${lang}`;
        if (skipExisting && prior[key]) {
          all.push(prior[key]);
          const r = prior[key];
          const tag = r.passed ? "PASS" : (r.extracted ? "FAIL" : "NOCODE");
          console.log(`SKIP ${model} ${taskSlug} ${lang.padEnd(6)} -> cached ${tag} ${r.num_passed}/${r.num_cases}`);
          continue;
        }
        const r = await runAttempt(model, task, lang, apiKey);
        all.push(r);
        const tag = r.passed ? "PASS" : (r.extracted ? "FAIL" : "NOCODE");
        const err = r.error ? ` [${r.error.slice(0, 40)}]` : "";
        console.log(
          `${tag.padEnd(6)} ${model} ${taskSlug} ${lang.padEnd(6)} ${r.num_passed}/${r.num_cases} ` +
            `api=${r.api_ms}ms build=${r.build_ms}ms exec=${r.exec_ms}ms${err}`
        );
      }
    }
    const summary = aggregate(all, model);
    writeFileSync(summaryPath, JSON.stringify({ ...summary, attempts: all }, null, 2));
    console.log("");
    console.log(`=== ${model} ===`);
    console.log(JSON.stringify(summary.perLang, null, 2));
    console.log(`Overall: ${summary.totalPassed}/${summary.totalAttempts} (${(summary.passRate * 100).toFixed(1)}%)`);
  }
}

function aggregate(attempts: AttemptResult[], model: string) {
  const perLang: Record<string, { passed: number; total: number; rate: number }> = {};
  for (const a of attempts) {
    if (!perLang[a.lang]) perLang[a.lang] = { passed: 0, total: 0, rate: 0 };
    perLang[a.lang].total += 1;
    if (a.passed) perLang[a.lang].passed += 1;
  }
  for (const lang of Object.keys(perLang)) {
    perLang[lang].rate = perLang[lang].total > 0 ? perLang[lang].passed / perLang[lang].total : 0;
  }
  const totalPassed = attempts.filter((a) => a.passed).length;
  const totalAttempts = attempts.length;
  const passRate = totalAttempts > 0 ? totalPassed / totalAttempts : 0;
  const totalPromptTokens = attempts.reduce((s, a) => s + a.prompt_tokens, 0);
  const totalCompletionTokens = attempts.reduce((s, a) => s + a.completion_tokens, 0);
  const langTax: Record<string, number> = {};
  const zeroRate = perLang["zero"]?.rate ?? 0;
  for (const lang of Object.keys(perLang)) {
    if (lang === "zero") continue;
    langTax[lang] = perLang[lang].rate - zeroRate;
  }
  return {
    model,
    perLang,
    totalPassed,
    totalAttempts,
    passRate,
    totalPromptTokens,
    totalCompletionTokens,
    langTax,
    timestamp: new Date().toISOString(),
  };
}

main().catch((e) => {
  console.error("Fatal:", e);
  process.exit(1);
});
