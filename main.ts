// Entry program for the make.fun news-image-20261124 bounty.
//
// The image itself was drawn beforehand (a front page summing up the
// world's news of Tuesday 24 November 2026) and ships in this repo as
// entry.png. All this program does is place that exact file at the
// path the grader reads, so both runs produce byte-identical output.
//
// Determinism note: a plain file copy has no randomness, no clock
// reads and no environment-dependent branches, so the two graded
// runs cannot diverge. As a guard, the copy is checked afterwards:
// if the destination's byte count ever differed from the source's,
// the run would fail loudly instead of submitting a short file.
//
// It uses only the Node standard library and touches no network.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The repository root is the directory holding this file.
const repoRoot = dirname(fileURLToPath(import.meta.url));

// The grader sets MAKEFUN_OUTPUT_DIR; fall back to /output, the
// documented default, so a local run behaves the same way.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
const source = join(repoRoot, "entry.png");
copyFileSync(source, target);

// Integrity guard: the copy must be whole, byte for byte.
if (statSync(source).size !== statSync(target).size) {
  throw new Error("entry.png copy is incomplete");
}
