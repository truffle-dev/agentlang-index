/**
 * Hermetic tests for the runner's provider-selection and prompt-flatten
 * logic. These cover the pure pieces of the claude-cli provider added on
 * top of the original OpenAI path — no network, no subprocess, no API key.
 *
 * Run: bun test bench/runner.test.ts
 */

import { test, expect } from "bun:test";
import { flattenClaudePrompt, inferProvider } from "./runner.ts";

test("inferProvider defaults to openai for gpt models", () => {
  expect(inferProvider(["gpt-5"])).toBe("openai");
  expect(inferProvider(["gpt-4o", "gpt-4o-mini"])).toBe("openai");
});

test("inferProvider picks claude-cli for claude-family model names", () => {
  expect(inferProvider(["opus"])).toBe("claude-cli");
  expect(inferProvider(["claude-opus-4-6"])).toBe("claude-cli");
  expect(inferProvider(["sonnet"])).toBe("claude-cli");
  expect(inferProvider(["haiku"])).toBe("claude-cli");
});

test("inferProvider is case-insensitive on the model prefix", () => {
  expect(inferProvider(["Opus"])).toBe("claude-cli");
  expect(inferProvider(["SONNET"])).toBe("claude-cli");
});

test("inferProvider stays openai when the set is mixed", () => {
  // A mixed run is ambiguous; only an all-claude set flips the default.
  expect(inferProvider(["opus", "gpt-5"])).toBe("openai");
});

test("inferProvider defaults to openai for an empty model list", () => {
  expect(inferProvider([])).toBe("openai");
});

test("flattenClaudePrompt puts the system block above a labeled user turn", () => {
  const out = flattenClaudePrompt("SYS", "USER");
  expect(out).toBe("SYS\n\nUser:\nUSER");
});

test("flattenClaudePrompt omits an empty system block", () => {
  const out = flattenClaudePrompt("   ", "USER");
  expect(out).toBe("User:\nUSER");
});
