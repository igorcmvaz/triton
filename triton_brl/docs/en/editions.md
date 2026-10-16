# The three editions: Brazil (BRL), International (INT) and Portugal (PRT)

Triton ships in three editions built from **the same code**. The calculation engine —
daily balance, first flush, runoff coefficients, economic analysis, LCA, TOPSIS — is a
single one. What separates the editions is **national data**: the Brazil Edition carries
the Brazilian data, audited; the International Edition is the neutral core, in which the
user enters the data of the project's country; the Portugal Edition starts from the neutral
core, speaks European Portuguese, works in euros and receives Portuguese data — rainfall by
municipality and the tariffs of the managing entities — as they are collected and checked
(decisions of 7 October 2026).

This document is the map for those who maintain the program. Users find the summary in
section 2 of the manual («The two editions»), in Portuguese and in English. Portuguese
version: [`../edicoes.md`](../edicoes.md).

---

## 1. What the user sees

| | Brazil Edition (BRL) | International Edition (INT) | Portugal Edition (PRT) |
| :--- | :--- | :--- | :--- |
| language on opening | Brazilian Portuguese | English | European Portuguese (VAL, entidade gestora, ficheiro, escalões) |
| sidebar badge, window title, footer of reports and exports | «Edição Brasil (BRL)», green | «International Edition (INT)», blue | «Edição Portugal (PRT)», red |
| rainfall | CLIMBra database (652 cities, CMIP6) or own series | own series | E-OBS database by municipality (278 on the mainland, observed, 1950–2025) or own series; Azores and Madeira only with own series |
| water and sewage tariffs | catalogue of 652 municipalities, with provenance by document, or typed in | typed in | typed in; tariffs of the district capitals under construction |
| step 12, Tariff Manager | present | absent | absent until there are tariffs |
| warning on non-residential tariff category | present | absent | absent |
| electricity | ANEEL B1 tariff of the distributor or typed in; tariff flags | typed in | typed in |
| currency | Brazilian real, the only one offered | none on opening («Currency not set (¤)»); the user chooses US dollar, euro, pound, yuan, rand, rupee and others | euro, the only one offered |
| reference costs (pump, chlorine, maintenance, arrangement, labour) | Brazilian prices | zero; typed in | zero; typed in |
| IPTU Verde | present | absent | absent |
| grid and potable water emission factors | MCTI and routes by region | from the project's country; without them, the LCA is not calculated | typed in, as in the International Edition |
| certifications | LEED, EDGE, GRI, AQUA-HQE, Selo Casa Azul | LEED, EDGE, GRI | LEED, EDGE, GRI |
| manual the program opens | Portuguese; English in the other interface languages | English | Portuguese |
| preferences (QSettings) | `UFSC/Triton` | `UFSC/Triton-INT` | `UFSC/Triton-PRT` |

---

## 2. Where it is in the code

The question every screen asks before offering a Brazilian datum is
`usa_dados_do_brasil()`, in `triton/core/edition.py`; for a Portuguese datum,
`usa_dados_de_portugal()`. The edition comes from the `TRITON_EDITION` environment variable
(`BRL` by default), set by the `main.py` of each folder and the
`main.py --edition brl|int|por` option. Outside Brazil, the Portugal Edition behaves like
the International one (neutral core), except where the table says otherwise.

| File | What changes outside Brazil |
| :--- | :--- |
| `triton/cli.py` | `init`, `init-catalog` and the scenario spreadsheet template start from the edition factory (`configuracao_da_edicao`) and its sample series; outside Brazil there is no preset tariff, price, green-tax incentive or grid factor; `compare-mass` and `run-vaz-study` (replication of the Brazilian study) exist only in the Brazil Edition; the help is in English (INT) or European Portuguese (PRT) |
| `triton/cli_textos.py` | help and message texts of the command line by edition (English in the International Edition, the Portugal glossary in the Portugal Edition) |
| `triton/core/bibliography.py` | outside Brazil the reference list leaves out the records that cite Brazilian standards, databases and manufacturers |
| `triton/core/cad_exporter.py` | title block and layers of the technical drawing (DXF and SVG) without a national standard outside Brazil |
| `triton/core/dados_do_relatorio.py` | report data that depends on the edition: standards, professional registration and the entity that supplies the site |
| `triton/core/diagnostico.py` | the CLIMBra database «does not apply» outside Brazil; the diagnosis states the edition |
| `triton/core/edition.py` | the active edition, label, language, currency and manual; the factories `configuracao_da_edicao`, `projeto_novo_da_edicao`, `tarifa_de_agua_de_reserva` and `serie_de_exemplo_da_edicao`; `neutralizar_para_a_internacional` clears the tariffs, electricity, pump, chlorine, maintenance, green-tax incentive and locality of a new project |
| `triton/core/environmental_justifications.py` | LCA rationale without national manufacturers, standards and inventories outside Brazil |
| `triton/core/esg_certifications.py` | ESG summary and credit matrix with the international certifications only outside Brazil |
| `triton/core/parser.py` | the `.triton` and CSV reader starts from `configuracao_da_edicao()`: what the file does not carry falls back to the historical default (BRL) or the neutral one (INT and PRT) |
| `triton/core/report_generator.py` | reports without national certifications, standards and references outside Brazil |
| `triton/core/tariff_category.py` | no tariff-category warning (there is no catalogue) |
| `triton/ui/dialogs/dialog_economic.py` | no municipality selector for tariff and electricity; piping-cost guide and billing regime without a national reference |
| `triton/ui/dialogs/pump_wizard_dialog.py` | catalogue of «reference models» (curves, nozzles and ratings) without brand or price outside Brazil |
| `triton/ui/laudo_em_ingles.py` | English texts of the report, for the International Edition |
| `triton/ui/main_window.py` | new project from the edition factory (`projeto_novo_da_edicao`), also in File > New Project; no Tariff Manager page; «How to cite» and «About» without a national standard or place; fixed texts in reais switch to the project currency (`triton/ui/moeda_na_interface.py`) |
| `triton/ui/sidebar.py` | blue (INT) or red (PRT) badge; no Tariff Manager step, and the numbering has no gap |
| `triton/ui/tab_documentation.py` | the pages lose any section, item, row or sentence that cites Brazil (`textos_da_edicao.html_da_edicao`); a page left without text is not offered; in the Portugal Edition in Portuguese it goes through the glossary; no fallback manual from another country |
| `triton/ui/tab_economic_integrated.py` | no green-tax incentive and no tariff flags |
| `triton/ui/tab_environmental.py` | emission factors empty and mandatory; replaced water: «mains supply with a user-supplied factor» or «custom»; no national routes or certifications |
| `triton/ui/tab_export.py` | file names suggested in the save dialogues and technical sheet without a national standard |
| `triton/ui/tab_modulacao_estocastica.py` | no draw amongst CLIMBra climate models; values in the project currency |
| `triton/ui/tab_project.py` | no city tariff panel; the national rainfall database is CLIMBra (BRL), E-OBS by district and municipality (PRT) or none (INT: opens the sample series of the edition, from file) |
| `triton/ui/tab_reports_pdf.py` | report languages and standards cited, by edition |
| `triton/ui/tab_tanks_simulation.py` | inflation, discount and adjustment profiles: the Brazilian ones only in the Brazil Edition, generic ones elsewhere; currencies: the International Edition has no preset currency (¤) and offers the US dollar, euro, pound, yuan, rand, rupee and others to choose from; Portugal only the euro; Brazil only the real; the project stores the currency code |
| `triton/ui/tab_water_quality.py` | treatment line and first flush without catalogue prices in reais or a national standard (only chlorine, at the price entered); the UV reactor's electricity emits at the grid factor entered for the LCA |
| `triton/ui/textos_da_edicao.py` | the per-edition variants of standards, professional registration, titles, file names and engine descriptions; the filter that removes Brazil from the documentation HTML |
| `triton/ui/translation.py` | English on opening (INT) or European Portuguese (PRT, glossary in `triton/ui/portugues_de_portugal.py`); separate preferences; the neutral texts of `translation_neutralidade.py` override the catalogue ones |

`tests/unit/test_edicoes_documentadas.py` fails if a file starts asking for the edition
without being listed in this table.

**The command line follows the edition.** `triton/cli.py` calculates with what the project file declares — tariff, costs, factors — and does not consult the catalogue or the CLIMBra database on its own; the template that `init` creates, however, starts from the edition factory (`configuracao_da_edicao`): the historical defaults in the Brazil Edition; in the International and Portugal Editions, no Brazilian tariff, price or locality. A project saved in one edition gives the same result in the other and in the CLI. The exception is explicit: `probabilistic-study --climate-models` reads the series of the chosen models from the CLIMBra database. A project that stores its rainfall as a reference to a database (CLIMBra, or E-OBS in the Portugal Edition) is reread from it in any edition and in the CLI.

---

## 3. Packaging

| | Brazil | International | Portugal |
| :--- | :--- | :--- | :--- |
| entry point | `main.py` in `triton_brl` | `main.py` in `triton_int` | `main.py` in `triton_prt` |
| build | `python build_exe.py`, inside each folder | same | same |
| folder | `dist/Triton/`, `Triton.exe` | `dist/Triton_INT/`, `Triton_INT.exe` | `dist/Triton_PRT/`, `Triton_PRT.exe` |
| installer | `Triton_Setup_0_1_0.exe` (`/DEdition=BRL`) | `Triton_INT_Setup_0_1_0.exe` (`/DEdition=INT`) | `Triton_PRT_Setup_0_1_0.exe` (`/DEdition=PRT`) |
| installation folder | `Triton` | `Triton International` | `Triton Portugal` |
| `.triton` file association | ticked | unticked | unticked |
| CLIMBra database (`data/climbra.db`, ~784 MB) | embedded; the build stops if it is missing | removed after PyInstaller | removed after PyInstaller |
| Portugal E-OBS database (`data/portugal_eobs.db`, ~6 MB, in git) | removed after PyInstaller | removed after PyInstaller | embedded; the build stops if it is missing |
| Portugal raw sources (`data/portugal/fontes`, ~3 GB, outside git) | removed | removed | removed |
| `tarifas/` folder (official documents and transcriptions, ~150 MB) | included, without `entrada` | removed after PyInstaller | removed after PyInstaller |
| manuals in the package | Portuguese and English | Portuguese and English | Portuguese and English |

`python build_exe.py --edition all` builds the three.

Installer details in [`../instalador.md`](../instalador.md) (Portuguese).

---

## 4. Data and documents of each edition

**Brazil Edition only.** Everything that feeds the Brazilian data:

| Material | Content |
| :--- | :--- |
| [`../../tarifas/`](../../tarifas/README.md) | catalogue of 652 municipalities, official documents, transcriptions and provenance |
| `triton/data/brazil_cities_tariffs.json` | the tariff database the program reads |
| [`../base_climatica_climbra.md`](../base_climatica_climbra.md) | the national climate database |
| [`../../tarifas/categorias/`](../../tarifas/categorias/) | official tables of the non-residential categories |

**Both editions.** Method, verification and use: [`model.md`](model.md),
[`verification.md`](verification.md), [`../normas_nbr_x_en16941.md`](../normas_nbr_x_en16941.md)
(what changes between the Brazilian standards and the European one, chiefly useful in the
International Edition), [`../certificacao_edge.md`](../certificacao_edge.md) and the CLI
guide [`../../infos_licenses/CLI_USAGE.md`](../../infos_licenses/CLI_USAGE.md).
[`../procedencia_fatores_co2.md`](../procedencia_fatores_co2.md) applies to both, but the
grid and potable water factors it documents are the ones only the Brazil Edition
pre-fills.

**The manual.** A single one, in both languages, for both editions. What exists only in
the Brazil Edition carries the note «Brazil Edition (BRL) only» / «Só na Edição Brasil
(BRL)»; how to proceed in the International Edition, the note «In the International
Edition (INT)» / «Na International Edition (INT)». `manual/en/conferir.py` requires the
same notes, in the same order, in both languages.

---

**Portugal Edition only.** Daily rainfall by municipality extracted from E-OBS v33.0e
(Copernicus/KNMI, 0.1° grid, 1950–2025; cite Cornes et al., 2018, doi:10.1029/2017JD028200,
and acknowledge UERRA, C3S and ECA&D), with the CAOP2025 boundaries (DGT): the series is the
mean of the cells whose centre lies inside the municipality. The script `compilar_base_eobs_portugal.py` of the Portugal Edition
builds `data/portugal_eobs.db` from the sources in `data/portugal/fontes` (addresses and SHA-256
in `LEIA.txt`). Left without a series, with the reason stored in the database, are the 19
municipalities of the Azores (outside the E-OBS domain, west of 25° W) and the 11 of Madeira
(E-OBS only has there the cells of the stations in operation; Funchal lacks data on 22% of the
days of 1991–2020, and the criterion admits at most 1%). Under construction: the tariffs of the managing entities, starting with the district capitals, transcribed
from the official documents and checked like the Brazilian ones. The Portuguese bill adds
water, sanitation, waste (often indexed to the m³ of water), the water resources levy and
VAT; the tariff engine will represent those parts.

## 5. When adding a Brazilian datum

1. Ask `usa_dados_do_brasil()` before offering it; in the International Edition, the field
   starts empty or at zero, and the user enters it.
2. Add the file to the table in section 2.
3. Test both editions in `tests/test_essencial_interface.py`, section «Interface» (and, if the datum enters the
   calculation, parity with the CLI).
4. In the manual, mark it with the edition notes in both languages.
