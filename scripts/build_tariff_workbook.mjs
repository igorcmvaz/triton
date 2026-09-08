import fs from "node:fs/promises";
import { pathToFileURL } from "node:url";

const artifactToolUrl = pathToFileURL(
  "C:/Users/igorc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs",
).href;
const { SpreadsheetFile, Workbook } = await import(artifactToolUrl);

const input = "tarifas/catalogo_tarifas_auditado_652.csv";
const output = "tarifas/catalogo_tarifas_auditado_652.xlsx";
const csvText = await fs.readFile(input, "utf8");
const workbook = await Workbook.fromCSV(csvText, { sheetName: "Tarifas_652" });
const data = workbook.worksheets.getItem("Tarifas_652");
const used = data.getUsedRange();
const rows = used.values;
const headers = rows[0].map((v) => String(v ?? ""));
const gradeCol = headers.indexOf("confianca_global_grau");
const counts = { A: 0, B: 0, C: 0, D: 0 };
for (const row of rows.slice(1)) {
  const grade = String(row[gradeCol] ?? "").trim().charAt(0);
  if (grade in counts) counts[grade] += 1;
}

data.showGridLines = false;
data.freezePanes.freezeRows(1);
data.freezePanes.freezeColumns(3);
const header = data.getRangeByIndexes(0, 0, 1, headers.length);
header.format.fill = "#203748";
header.format.font = { bold: true, color: "#FFFFFF", size: 10 };
header.format.wrapText = true;
header.format.rowHeight = 34;
used.format.font = { name: "Calibri", size: 9 };
used.format.borders = { preset: "all", style: "thin", color: "#D9E2F3" };
used.format.verticalAlignment = "center";
data.getRangeByIndexes(1, 0, rows.length - 1, headers.length).format.wrapText = true;
for (let c = 0; c < headers.length; c += 1) {
  const name = headers[c];
  const col = data.getRangeByIndexes(0, c, rows.length, 1);
  let width = 14;
  if (/fonte|url|justificativa|alerta|observacao|tipo_evidencia/i.test(name)) width = 38;
  else if (/municipio|prestador|distribuidora|agencia/i.test(name)) width = 24;
  else if (/data|inicio|fim|vigencia|ato/i.test(name)) width = 18;
  col.format.columnWidth = width;
}

const summary = workbook.worksheets.add("Resumo_qualidade");
summary.showGridLines = false;
summary.getRange("A1:D1").merge();
summary.getRange("A1").values = [["Auditoria de tarifas — 652 municípios"]];
summary.getRange("A1:D1").format.fill = "#203748";
summary.getRange("A1:D1").format.font = { bold: true, color: "#FFFFFF", size: 16 };
summary.getRange("A1:D1").format.rowHeight = 30;
summary.getRange("A3:B8").values = [
  ["Indicador", "Valor"],
  ["Data de corte", "2026-08-24"],
  ["Municípios", rows.length - 1],
  ["Grau A", counts.A],
  ["Grau B", counts.B],
  ["Grau C", counts.C],
];
summary.getRange("A3:B3").format.fill = "#2E74B5";
summary.getRange("A3:B3").format.font = { bold: true, color: "#FFFFFF" };
summary.getRange("A4:B8").format.borders = { preset: "all", style: "thin", color: "#B4C6E7" };
summary.getRange("A10:D10").merge();
summary.getRange("A10").values = [["Critério de grau A"]];
summary.getRange("A10:D10").format.fill = "#0F6B78";
summary.getRange("A10:D10").format.font = { bold: true, color: "#FFFFFF" };
summary.getRange("A11:D14").merge(true);
summary.getRange("A11").values = [["Saneamento: fonte primária específica, vigência identificada, estrutura completa e conciliação numérica linha a linha."]];
summary.getRange("A12").values = [["Energia: TUSD+TE B1 residencial convencional em ato ANEEL vigente na data de corte."]];
summary.getRange("A13").values = [["A classificação não é promovida apenas porque existe uma página oficial; o valor modelado deve coincidir com a fonte."]];
summary.getRange("A14").values = [["Casos B/C permanecem assim até publicação ou localização de evidência suficiente; não são estimados para forçar A."]];
summary.getRange("A11:D14").format.wrapText = true;
summary.getRange("A11:D14").format.fill = "#E8EEF5";
summary.getRange("A:D").format.columnWidth = 24;
summary.getRange("A11:D14").format.rowHeight = 32;

const method = workbook.worksheets.add("Metodologia");
method.showGridLines = false;
method.getRange("A1:D1").merge();
method.getRange("A1").values = [["Rubrica auditável de confiança"]];
method.getRange("A1:D1").format.fill = "#203748";
method.getRange("A1:D1").format.font = { bold: true, color: "#FFFFFF", size: 15 };
method.getRange("A3:D10").values = [
  ["Componente", "Peso/pontos", "Regra", "Evidência necessária"],
  ["Saneamento no global", "60%", "Rubrica de 100 pontos", "Tabela/ato oficial e reconciliação numérica"],
  ["Autoridade/especificidade", "35", "Tabela/ato > página institucional", "URL primária específica"],
  ["Atualidade", "20", "2026/27 > 2025 > 2023/24", "Vigência ou data do ato"],
  ["Conciliação", "25", "SIM/PENDENTE/NÃO", "Igualdade das faixas, fixa e esgoto"],
  ["Completude", "15", "Faixas e regra de esgoto", "Estrutura residencial completa"],
  ["Operador", "5", "Prestador/agência coerentes", "Concessão atual"],
  ["Energia no global", "40%", "ANEEL vigente tem maior escore", "TUSD+TE B1 e ato homologatório"],
];
method.getRange("A3:D3").format.fill = "#2E74B5";
method.getRange("A3:D3").format.font = { bold: true, color: "#FFFFFF" };
method.getRange("A3:D10").format.borders = { preset: "all", style: "thin", color: "#B4C6E7" };
method.getRange("A3:D10").format.wrapText = true;
method.getRange("A:D").format.columnWidth = 27;

const sources = workbook.worksheets.add("Fontes_chave");
sources.showGridLines = false;
sources.getRange("A1:D1").merge();
sources.getRange("A1").values = [["Fontes primárias e rastreabilidade"]];
sources.getRange("A1:D1").format.fill = "#203748";
sources.getRange("A1:D1").format.font = { bold: true, color: "#FFFFFF", size: 15 };
sources.getRange("A3:D9").values = [
  ["Componente", "Órgão", "Fonte", "Uso"],
  ["Energia", "ANEEL", "https://dadosabertos.aneel.gov.br/dataset/tarifas-distribuidoras-energia-eletrica", "TUSD+TE B1 e vigência"],
  ["Saneamento", "Prestadores e agências", "URLs individualizadas na aba Tarifas_652", "Faixas, parcela fixa, esgoto e operador"],
  ["EMBASA", "EMBASA/AGERSA", "https://www.embasa.ba.gov.br/w/tarifas-2026", "Tabela vigente desde 20/07/2026"],
  ["CAGECE", "CAGECE", "https://www.cagece.com.br/produtos-e-servicos/precos-e-prazos/estrutura-tarifaria/", "Tabela vigente desde 05/11/2025"],
  ["SANEAGO", "AGR/AR/SANEAGO", "https://www.saneago.com.br/2026/arquivos/Res_Normativa_Conjunta_AGR_AR_01_2026.pdf", "Resolução conjunta 1/2026"],
  ["COMPESA", "ARPE", "https://www.arpe.pe.gov.br/images/COORDENADORIAS/TARIFAS/SANEAMENTO/Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf", "Estrutura homologada"],
];
sources.getRange("A3:D3").format.fill = "#2E74B5";
sources.getRange("A3:D3").format.font = { bold: true, color: "#FFFFFF" };
sources.getRange("A3:D9").format.borders = { preset: "all", style: "thin", color: "#B4C6E7" };
sources.getRange("A3:D9").format.wrapText = true;
sources.getRange("A:D").format.columnWidth = 30;

const check = await workbook.inspect({ kind: "sheet", include: "id,name", maxChars: 3000 });
console.log(check.ndjson ?? check);
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(output);
const preview = await workbook.render({ sheetName: "Resumo_qualidade", autoCrop: "all", scale: 1, format: "png" });
await fs.writeFile("tmp/tariff_workbook_preview.png", new Uint8Array(await preview.arrayBuffer()));
console.log(`${output}: A=${counts.A}, B=${counts.B}, C=${counts.C}, D=${counts.D}`);
