# Scripts

Ferramentas de linha de comando que acompanham o programa. Nenhuma é importada
por `triton/`: rodam por fora, sobre o projeto.

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
| `generate_reference_case_studies.py` | casos de referência |
| `generate_uf_tariffs_breakdown.py` | recorte tarifário por unidade da federação |
| `plot_tariff_tiers_summary.py` | figura-resumo das faixas tarifárias |
| `verificar_custos_calibrados.py` | imprime o CAPEX e o OPEX calibrados por tipologia e UF, para conferência visual (relatório, sem asserções) |
| `gerar_relatorios_exemplo.py` | regera os laudos de `reports/exemplos/` pela própria interface |
| `replicacao/` | cenários climáticos e comprimento de série usados na replicação dos artigos do grupo |

## Estudos e artigos

Os scripts que produzem os dados e as figuras dos artigos não ficam aqui. Estão na
pasta `Estudos/`, ao lado deste repositório, junto dos dados de cada estudo.
