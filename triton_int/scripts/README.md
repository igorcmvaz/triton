# Scripts

Ferramentas de linha de comando que acompanham o programa. Nenhuma é importada
por `triton/`: rodam por fora, sobre o projeto.

## Raiz — operação e manutenção

Referenciadas pela documentação, pela integração contínua ou umas pelas outras.

| Script | O que faz |
| :--- | :--- |
| `qa_runner.py` | executa as camadas de verificação; `--layer replicacao` roda a comparação completa contra o Netuno 4 |
| `reconciliar_tarifas.py` | conciliação entre a coleta e a evidência primária |
| `completar_tarifas_faltantes.py` | preenche municípios sem estrutura |
| `run_batch_validation.py` | validação em lote |
| `bench_kernels.py` | comparação de desempenho entre o kernel Python e o compilado |
| `run_mass_simulations.py` | simulações em massa |
| `generate_reference_case_studies.py` | casos de referência |
| `verificar_custos_calibrados.py` | imprime o CAPEX e o OPEX calibrados por tipologia e UF, para conferência visual (relatório, sem asserções) |
| `gerar_relatorios_exemplo.py` | regera os laudos de `reports/exemplos/` pela própria interface |
| `replicacao/` | cenários climáticos e comprimento de série usados na replicação dos artigos do grupo |

## Estudos e artigos

Os scripts que produzem os dados e as figuras dos artigos não ficam aqui. Estão na
pasta `Estudos/`, ao lado deste repositório, junto dos dados de cada estudo.
