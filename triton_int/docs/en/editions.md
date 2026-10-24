# The International Edition (INT)

Triton ships in editions built from **the same code**: the Brazil Edition (BRL), this
International Edition (INT) and the Iberian Edition (IBE). The calculation engine — daily
balance, first flush, runoff coefficients, economic analysis, LCA, TOPSIS — is one. What
separates the editions is **national data**. The International Edition is the neutral core:
it carries no tariff, price, climate record, standard or emission factor of any country.
The user enters the rainfall series, the tariffs, the costs and the emission factors of the
project's country, in the currency they choose.

This document is the map for those who maintain the program. Portuguese note:
[`../edicoes.md`](../edicoes.md).

---

## 1. What the user sees

| | International Edition (INT) |
| :--- | :--- |
| language on opening | English (Portuguese, Spanish and Chinese are offered) |
| sidebar badge, window title, footer of reports and exports | «International Edition (INT)», blue |
| rainfall | the user's own daily series (CSV/TXT/DAT); a sample series (New York, London or Cape Town, ERA5 reanalysis, `data/rainfall/`) opens as a starting point |
| water and sewage tariffs | typed in |
| electricity | typed in |
| currency | none preset («Currency not set (¤)»); the user chooses US dollar, euro, pound, yuan, rand, rupee, Australian or Canadian dollar, or Swiss franc |
| reference costs (pump, chlorine, maintenance, arrangement, labour) | zero; typed in |
| pump catalogue of the assistant | «reference models» A to E (curves, nozzles, ratings), without brand or price |
| inflation, discount and tariff-adjustment profiles | generic, defined by the user |
| grid and potable-water emission factors | typed in, for the project's country; without them the LCA does not credit avoided emissions |
| certifications | LEED, EDGE, GRI |
| standards cited | none by number; the texts say «reference standard» |
| manual the program opens | the English manual of this edition, when it is installed |
| preferences (QSettings) | `UFSC/Triton-INT` |

---

## 2. Where it is in the code

The question every screen asks before offering a national datum is `usa_dados_do_brasil()`
(Brazil only) or `usa_dados_de_portugal()` (Portugal only), in `triton/core/edition.py`. The
edition comes from the `TRITON_EDITION` environment variable, set by the `main.py` of each
folder (or the `main.py --edition brl|int|por` option). The International Edition receives
the neutral answer to every one of them.

| File | What it does |
| :--- | :--- |
| `triton/cli.py` | `init`, `init-catalog` and the scenario spreadsheet template start from the edition factory (`configuracao_da_edicao`) and its sample series; outside Brazil there is no preset tariff, price, green-tax incentive or grid factor; `compare-mass` and `run-vaz-study` (replication of the Brazilian study) exist only in the Brazil Edition; the help is in English (INT) or European Portuguese (IBE) |
| `triton/cli_textos.py` | help and message texts of the command line by edition (English in the International Edition, the Portugal glossary in the Iberian Edition) |
| `triton/core/cost_estimates.py` | cost bank: outside the Brazil Edition `costs_database.json` carries no prices and the estimator returns zero (the user enters the costs) |
| `triton/core/bibliography.py` | outside Brazil the reference list leaves out the records that cite Brazilian standards, databases and manufacturers |
| `triton/core/cad_exporter.py` | title block and layers of the technical drawing (DXF and SVG) without a national standard outside Brazil |
| `triton/core/dados_do_relatorio.py` | report data that depends on the edition: standards, professional registration and the entity that supplies the site |
| `triton/core/diagnostico.py` | the CLIMBra database «does not apply» outside Brazil; the diagnosis states the edition |
| `triton/core/edition.py` | the active edition, label, language, currency and manual; the factories `configuracao_da_edicao`, `projeto_novo_da_edicao`, `tarifa_de_agua_de_reserva` and `serie_de_exemplo_da_edicao`; `neutralizar_para_a_internacional` clears the tariffs, electricity, pump, chlorine, maintenance, green-tax incentive and locality of a new project |
| `triton/core/licenca_eobs.py` | Portugal only (IBE): E-OBS licence notice, remembered choice of use, blocking behind a constant that is off, and the licence and citation footer of the reports |
| `triton/core/environmental_justifications.py` | LCA rationale without national manufacturers, standards and inventories outside Brazil |
| `triton/core/esg_certifications.py` | ESG summary and credit matrix with the international certifications only outside Brazil |
| `triton/core/parser.py` | the `.triton` and CSV reader starts from `configuracao_da_edicao()`: what the file does not carry falls back to the historical default (BRL) or the neutral one (INT and IBE) |
| `triton/core/numero.py` | numeric convention of the interface: decimal comma and dotted thousands in Portuguese and Spanish and in the BRL edition; decimal point and comma thousands in English and Chinese outside the BRL edition (showing and reading numbers both go through it) |
| `triton/core/report_generator.py` | reports without national certifications, standards and references outside Brazil |
| `triton/core/tariff_category.py` | no tariff-category warning (there is no catalogue) |
| `triton/ui/dialogs/dialog_economic.py` | no municipality selector for tariff and electricity; piping-cost guide and billing regime without a national reference |
| `triton/ui/dialogs/pump_wizard_dialog.py` | catalogue of «reference models» (curves, nozzles and ratings) without brand or price outside Brazil |
| `triton/ui/laudo_em_ingles.py` | English texts of the report, for the International Edition |
| `triton/ui/main_window.py` | new project from the edition factory (`projeto_novo_da_edicao`), also in File > New Project; no Tariff Manager page; «How to cite» and «About» without a national standard or place; fixed texts in reais switch to the project currency (`triton/ui/moeda_na_interface.py`) |
| `triton/ui/sidebar.py` | blue (INT) or red (IBE) badge; no Tariff Manager step, and the numbering has no gap |
| `triton/ui/tab_documentation.py` | the pages lose any section, item, row or sentence that cites Brazil (`textos_da_edicao.html_da_edicao`); a page left without text is not offered; in the Iberian Edition in Portuguese it goes through the glossary; no fallback manual from another country |
| `triton/ui/tab_economic_integrated.py` | no green-tax incentive and no tariff flags |
| `triton/ui/tab_environmental.py` | emission factors empty and mandatory; replaced water: «mains supply with a user-supplied factor» or «custom»; no national routes or certifications |
| `triton/ui/tab_export.py` | file names suggested in the save dialogues and technical sheet without a national standard |
| `triton/ui/tab_modulacao_estocastica.py` | no draw amongst CLIMBra climate models; values in the project currency |
| `triton/ui/tab_project.py` | no city tariff panel; the national rainfall database is CLIMBra (BRL), E-OBS by district and municipality (IBE) or none (INT: opens the sample series of the edition, from file) |
| `triton/ui/tab_reports_pdf.py` | report languages and standards cited, by edition |
| `triton/ui/tab_tanks_simulation.py` | inflation, discount and adjustment profiles: the Brazilian ones only in the Brazil Edition, generic ones elsewhere; currencies: the International Edition has no preset currency (¤) and offers the US dollar, euro, pound, yuan, rand, rupee and others to choose from; Portugal only the euro; Brazil only the real; the project stores the currency code |
| `triton/ui/tab_water_quality.py` | treatment line and first flush without catalogue prices in reais or a national standard (only chlorine, at the price entered); the UV reactor's electricity emits at the grid factor entered for the LCA |
| `triton/ui/textos_da_edicao.py` | the per-edition variants of standards, professional registration, titles, file names and engine descriptions; the filter that removes Brazil from the documentation HTML |
| `triton/ui/translation.py` | English on opening (INT) or European Portuguese (IBE, glossary in `triton/ui/portugues_de_portugal.py`); separate preferences; the neutral texts of `translation_neutralidade.py` override the catalogue ones |

`tests/unit/test_edicoes_documentadas.py` fails if a file starts asking for the edition
without being listed in this table. `tests/unit/test_neutralidade_interface.py` opens the
window, walks through the steps, the dialogues and the Documentation tab, and fails if any
text mentions a national datum.

**The command line follows the edition.** `triton init` writes a template without tariff,
price, locality or grid factor; `triton init-catalog` writes the climate catalogue of this
edition's sample series. A project saved in one edition gives the same result in the others
and in the CLI.

---

## 3. Packaging

| | International |
| :--- | :--- |
| entry point | `main.py` in `triton_int` |
| build | `python build_exe.py`, inside the folder |
| folder | `dist/Triton_INT/`, `Triton_INT.exe` |
| installer | `Triton_INT_Setup_0_1_0.exe` (`/DEdition=INT`) |
| installation folder | `Triton International` |
| `.triton` file association | unticked |
| national databases | none: the package carries no climate or tariff database |

Installer details in [`../instalador.md`](../instalador.md) (Portuguese).

---

## 4. Data and documents of this edition

[`model.md`](model.md), [`verification.md`](verification.md) and
[`getting-started.md`](getting-started.md) are the English documents. The user manual of
this edition is distributed separately; the Documentation tab of the program lists the
topics (method, rainfall indices, reservoirs, water quality, economics, LCA, references,
command line) without national sources.

## 5. When adding a national datum

1. Ask `usa_dados_do_brasil()` or `usa_dados_de_portugal()` before offering it; in the
   International Edition the field starts empty or at zero, and the user enters it.
2. Add the file to the table in section 2.
3. Run `tests/unit/test_neutralidade_interface.py` in the three editions.
