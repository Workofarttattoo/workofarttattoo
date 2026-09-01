#!/usr/bin/env node
/**
 * IndexNow submission CLI — delegates to woa_indexnow.py (shared validation + tests).
 *
 * Usage:
 *   node scripts/submit-indexnow.mjs --initial
 *   node scripts/submit-indexnow.mjs --from-deploy
 *   node scripts/submit-indexnow.mjs --urls https://www.workofarttattoo.com/start_here/
 */
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const result = spawnSync("python3", [join(root, "woa_indexnow.py"), ...args], {
  stdio: "inherit",
  cwd: root,
});
process.exit(result.status ?? 1);
