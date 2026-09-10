# Scripts

Ferramentas de linha de comando que acompanham o programa. Nenhuma é importada
por `netuno/`: rodam por fora, sobre o projeto.

## Raiz — operação e manutenção

Referenciadas pela documentação, pela integração contínua ou umas pelas outras.

| Script | O que faz |
| :--- | :--- |
| `qa_runner.py` | executa as camadas de verificação; `--layer replicacao` roda a comparação completa contra o Netuno 4 |
| `audit_tariffs.py` | auditoria da base tarifária |
| `update_all_tariffs.py` | atualização das 652 estruturas a partir das fontes |
| `reconciliar_tarifas.py` | conciliação entre a coleta e a evidência primária |
| `completar_tarifas_faltantes.py` | preenche municípios sem estrutura |
| `comparar_exportacao_netuno4.py` | confronta a exportação com a do Netuno 4 |
| `run_batch_validation.py` | validação em lote |
| `bench_kernels.py` | comparação de desempenho entre o kernel Python e o compilado |
| `split_climates.py`, `split_climates_vaz.py` | fatiamento da base climática CMIP6 |
| `run_mass_simulations.py` | simulações em massa |
| `run_estudo_5_tipologias.py` | estudo das cinco tipologias residenciais |
| `recalc_full_study_with_real_tariffs.py` | recálculo do estudo com as tarifas reais |
| `generate_reference_case_studies.py` | casos de referência |
| `generate_capitais_global_vpl.py`, `generate_uf_tariffs_breakdown.py` | recortes por capital e por unidade da federação |
| `plot_tariff_tiers_summary.py` | figura-resumo das faixas tarifárias |
| `analyze_vaz_parquet.py` | leitura dos resultados em parquet |
| `build_tariff_workbook.mjs` | planilha tarifária (Node) |

## `artigos/` — preparação de manuscrito

Geradores de texto e de figuras dos artigos. São artefatos de pesquisa, presos ao
recorte de cada estudo, e não fazem parte do programa. Ficam agrupados aqui
porque nenhum é referenciado por código, documentação ou integração contínua, e
misturados à raiz escondiam as ferramentas de operação.

## `estudos/` — execuções de lote de longa duração

Pipelines completos e execuções noturnas, com a consolidação dos resultados.
