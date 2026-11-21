// news-image-20261120: a program that writes one image summing up the world news
// of Friday 20 November 2026 to /output/entry.png. The entry is the 20 November
// contest's front page; the program copies the committed image, so the run is
// deterministic and needs no network.
//
// The image is drawn by tools/make_image.py (a front page: Russia's largest
// strike of November on Ukraine, with missiles falling in Poland; the Wall
// Street AI sell-off; Trump's White House news conference; Cyclone Akvan; the
// Peru earthquake; and the day's briefs) and committed here as entry.png, so
// this program only has to copy it. That keeps the run deterministic: two runs
// write the same bytes, with no network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
