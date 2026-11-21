// gta6-meme-x-01 entrypoint (Node 22, standard library only).
// The entry is the X post itself: POST.json at the repository root names the
// post's address, and the house reads the post from X (first picture, then
// text) and hands it to the judge. All this program has to do is copy
// POST.json to the output directory, where the gate reads it.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  const src = join(BOT_DIR, 'POST.json');
  // Validate first: POST.json must be a JSON object naming an X post's
  // address, otherwise the house refuses the entry.
  const parsed: unknown = JSON.parse(readFileSync(src, 'utf8'));
  if (typeof parsed !== 'object' || parsed === null ||
      typeof (parsed as { url?: unknown }).url !== 'string') {
    throw new Error('POST.json is not a JSON object with a string "url" field');
  }
  // Write atomically (temp file + rename) so the two grader runs always
  // see the same complete bytes.
  const dest = join(OUTPUT_DIR, 'POST.json');
  const tmp = `${dest}.tmp`;
  writeFileSync(tmp, readFileSync(src));
  renameSync(tmp, dest);
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
