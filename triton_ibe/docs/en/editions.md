# The Iberian Edition (IBE)

Triton ships in editions built from **the same code**: Brazil (BRL), International (INT)
and Ibérica (IBE). The engine is one; what separates the editions is national data. The
Iberian Edition starts from the neutral core, speaks European Portuguese, works in euros
and carries Portuguese data: daily rainfall by municipality (E-OBS) and the tariffs of
Lisbon, Porto and Funchal.

**Name and codes.** The edition used to be called "Portugal" (code `PRT`, earlier `POR`) and is now **Triton IBE**, for the Iberian Peninsula. The internal value is `IBE`; `PRT` and `POR` are still accepted as synonyms (`TRITON_EDITION`, `--edition`, `set_current_edition`) and normalise to `IBE`, and `is_prt_edition` is an alias of `is_ibe_edition`. Today only Portuguese municipalities have data (the coverage line reads "Spain: 0 sites"); no Spanish data is invented.

The full map is in Portuguese: [`../edicoes.md`](../edicoes.md). The table below is the same.

## Where it is in the code

The question every screen asks before offering a national datum is `usa_dados_do_brasil()`
(Brazil only) or `usa_dados_de_portugal()` (Portugal only), in `triton/core/edition.py`.

| File | What it does |
| :--- | :--- |
| `triton/cli.py` | `init`, `init-catalog` and the scenario spreadsheet template start from the edition factory (`configuracao_da_edicao`) and its sample series; outside Brazil there is no preset tariff, price, green-tax incentive or grid factor; `compare-mass` and `run-vaz-study` (replication of the Brazilian study) exist only in the Brazil Edition; the help is in English (INT) or European Portuguese (IBE) |
| `triton/cli_estudo.py` | `triton estudo` (`init`, `validate`, `run`, `resumo`, `lote`, `texto`, `esquema`, `apelidos`): arguments, messages and exit codes (0 ok, 1 a case failed, 2 invalid use); the help text goes through `cli_textos`, and the catalogue of aliases and metrics is printed in the language of the edition |
| `triton/cli_textos.py` | help and message texts of the command line by edition (English in the International Edition, the Portugal glossary in the Iberian Edition) |
| `triton/core/economics/cost_estimates.py` | cost bank: outside the Brazil Edition `costs_database.json` carries no prices and the estimator returns zero (the user enters the costs) |
| `triton/core/system/bibliography.py` | outside Brazil the reference list leaves out the records that cite Brazilian standards, databases and manufacturers |
| `triton/core/cad_bim/cad_exporter.py` | title block and layers of the technical drawing (DXF and SVG) without a national standard outside Brazil |
| `triton/core/reporting/dados_do_relatorio.py` | report data that depends on the edition: standards, professional registration and the entity that supplies the site |
| `triton/core/system/diagnostico.py` | the CLIMBra database «does not apply» outside Brazil; the diagnosis states the edition |
| `triton/core/system/edition.py` | the active edition, label, language, currency and manual; the factories `configuracao_da_edicao`, `projeto_novo_da_edicao`, `tarifa_de_agua_de_reserva` and `serie_de_exemplo_da_edicao`; `neutralizar_para_a_internacional` clears the tariffs, electricity, pump, chlorine, maintenance, green-tax incentive and locality of a new project |
| `triton/core/climate/licenca_eobs.py` | Portugal only (IBE): E-OBS licence notice, remembered choice of use, blocking behind a constant that is off, and the licence and citation footer of the reports |
| `triton/core/lca/environmental_justifications.py` | LCA rationale without national manufacturers, standards and inventories outside Brazil |
| `triton/core/lca/esg_certifications.py` | ESG summary and credit matrix with the international certifications only outside Brazil |
| `triton/core/reporting/estudo.py` | batch studies from JSON: schema of `estudo.json`, parameter aliases, metrics and paper-ready tables; the language of the outputs (`auto`) is pt-BR in Brazil, pt-PT in Portugal and English in the International Edition; the project template «edicao» starts from the edition factory; with no currency declared in the project, the real (BRL), the euro (IBE) or none (INT) applies |
| `triton/core/system/parser.py` | the `.triton` and CSV reader starts from `configuracao_da_edicao()`: what the file does not carry falls back to the historical default (BRL) or the neutral one (INT and IBE) |
| `triton/core/system/numero.py` | numeric convention of the interface: decimal comma and dotted thousands in Portuguese and Spanish and in the BRL edition; decimal point and comma thousands in English and Chinese outside the BRL edition (showing and reading numbers both go through it) |
| `triton/core/reporting/report_generator.py` | reports without national certifications, standards and references outside Brazil |
| `triton/core/tariffs/tariff_category.py` | no tariff-category warning (there is no catalogue) |
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
without being listed in this table.
