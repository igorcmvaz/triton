// Empacota src/viewer.js + three.js num único arquivo para o Triton.
//
//   cd web/volumetria && npm ci && npm run build
//
// Saída: triton/data/volumetria/triton_volumetria.js (IIFE, global
// TritonVolumetria). O cabeçalho leva a licença do three.js (MIT, que exige a
// nota de copyright) e o hash do código-fonte: tests/unit/test_volumetria_web.py
// recusa um pacote que não corresponda ao fonte atual.
import { build } from "esbuild";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "src", "viewer.js");
const out = join(here, "..", "..", "triton", "data", "volumetria", "triton_volumetria.js");
const threeVersion = JSON.parse(readFileSync(join(here, "node_modules", "three", "package.json"), "utf8")).version;
const hash = createHash("sha256").update(readFileSync(src)).digest("hex");
const license = readFileSync(join(here, "node_modules", "three", "LICENSE"), "utf8").trim();

const result = await build({
  entryPoints: [src],
  bundle: true,
  format: "iife",
  globalName: "TritonVolumetria",
  minify: true,
  target: ["es2020"],
  legalComments: "none",
  write: false,
  logLevel: "warning",
});

let code = result.outputFiles[0].text;
// O pacote vai dentro de <script> no HTML exportado: nenhum "</script" literal.
code = code.replace(/<\/script/gi, "<\\/script");
const banner = [
  "/*! Triton — visualizador da volumetria (web/volumetria/src/viewer.js).",
  ` * fonte-sha256: ${hash}`,
  ` * three.js ${threeVersion} — https://threejs.org`,
  ...license.split("\n").map((l) => ` * ${l}`),
  " */",
].join("\n");
writeFileSync(out, `${banner}\n${code}`);
console.log(`ok: ${out} (${(code.length / 1024).toFixed(0)} KiB, three ${threeVersion})`);
