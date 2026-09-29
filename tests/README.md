# Testes do Netuno 5.0.0

Esta pasta reúne a verificação automatizada do motor, das interfaces de entrada e saída e dos fluxos gráficos. Os testes demonstram consistência interna com regras e casos de referência; não substituem validação externa com medições independentes.

## Início rápido

Execute os comandos a partir da raiz do repositório, com o ambiente virtual ativo:

```powershell
python -m pip install PySide6 numpy pandas matplotlib openpyxl reportlab numpy-financial pytest pytest-cov

# Ciclo rápido durante o desenvolvimento
python scripts/qa_runner.py --layer unit --no-cov

# Verificação completa com cobertura
python scripts/qa_runner.py --layer all
```

O runner aceita `unit`, `integration`, `invariants`, `ui`, `benchmarking` e `all`. Com cobertura ativa, o relatório navegável é gravado em `reports/coverage/index.html`.

## Qual camada executar

| Camada | Finalidade | Quando executar |
| --- | --- | --- |
| `unit` | equações, parsers, CLI e regras isoladas | a cada alteração localizada |
| `invariants` | conservação de massa e coerência financeira | após alterações no balanço ou fluxo de caixa |
| `integration` | encadeamento de cenários, relatórios e ferramentas | após mudanças entre módulos |
| `ui` | nove etapas da interface e documentação integrada | após mudanças visuais ou de navegação |
| `benchmarking` | utilitários de comparação com referências históricas | em estudos de compatibilidade e desempenho |
| `all` | todas as camadas | antes de distribuir uma versão |

Também é possível chamar o `pytest` diretamente:

```powershell
# Suíte completa, saída concisa
python -m pytest tests -q

# Arquivo específico
python -m pytest tests/unit/test_economic.py -v

# Caso específico
python -m pytest tests/unit/test_discard_modes.py::test_discard_mode_2_after_dry_spell -v

# Seleção por palavra-chave
python -m pytest tests -k topsis -v
```

## Ambiente gráfico e dados

`tests/conftest.py` configura `QT_QPA_PLATFORM=offscreen` e o backend `Agg` do Matplotlib quando essas variáveis ainda não foram definidas. Assim, a suíte normalmente roda sem monitor e sem abrir janelas. Defina outro backend antes da execução apenas quando precisar investigar o comportamento gráfico real.

Os testes devem ser iniciados na raiz porque usam módulos do repositório e dados em `data/`. Arquivos temporários pertencem ao diretório fornecido pelo `pytest`; saídas científicas permanentes não devem ser atualizadas silenciosamente durante uma execução comum.

## Mapa da suíte

| Grupo | Arquivos e escopo principal |
| --- | --- |
| Núcleo hídrico | `unit/test_simulation.py`, `test_daily_water_balance.py`, `test_discard_modes.py`: YAS, reservatórios, descarte, grade e balanço diário |
| Dados e clima | `unit/test_parser.py`, `test_calculator.py`: leitura, conversões, índices e sazonalidade |
| Economia e energia | `unit/test_economic.py`, `test_pump_energy_details.py`; `integration/test_financial_robustness.py`: tarifas, OPEX, bomba, VPL, TIR e payback |
| Ambiental e multicritério | `unit/test_environmental.py`, `test_environmental_sync.py`, `test_topsis.py`: inventário, sincronização por volume, ranking e distâncias |
| CLI e automação | `unit/test_cli.py`; `integration/test_batch_validation.py`, `test_new_tools.py`: projetos, formatos, lotes, matrizes e incerteza |
| Relatórios e documentação | `unit/test_reference_documents.py`; `integration/test_report_generator.py`: consistência dos documentos e artefatos exportados |
| Interface | `ui/test_ui_flow.py`, `test_documentation_tab.py`: fluxo pelas nove etapas e conteúdo metodológico |
| Invariantes | `invariants/test_mass_conservation.py`, `test_financial_invariants.py`: propriedades que devem valer em conjuntos amplos de entradas |

## Estudos de referência e lotes

```powershell
# Regenera os estudos documentais derivados do motor
python scripts/generate_reference_case_studies.py

# Executa a matriz de validação do repositório
python scripts/run_batch_validation.py

# Mostra opções das simulações em massa
python scripts/run_mass_simulations.py --help
```

Regenerar referências é uma ação deliberada: revise o diff e confirme se a mudança numérica era esperada. A concordância entre documento e motor é verificação de implementação, pois ambos podem compartilhar as mesmas hipóteses.

## Diagnóstico de falhas

| Sintoma | Verificação recomendada |
| --- | --- |
| `ModuleNotFoundError` | confirme o interpretador ativo e instale a dependência ausente no mesmo ambiente |
| erro de plugin Qt | confirme que `tests/conftest.py` foi carregado e remova uma variável `QT_QPA_PLATFORM` incompatível definida externamente |
| arquivo de dados ausente | execute da raiz e confirme a presença de `data/rainfall/` e demais entradas do caso |
| `PermissionError` em `pytest-of-...` | indique uma pasta temporária gravável com `--basetemp`, conforme o exemplo abaixo |
| divergência numérica | registre entradas, volume, regra de descarte, tolerância, valor esperado e valor obtido |
| teste intermitente | fixe sementes, elimine dependência de ordem e preserve o artefato mínimo que reproduz a falha |
| falha apenas com cobertura | instale `pytest-cov` ou use `--no-cov` no runner |

No PowerShell, uma execução isolada da pasta temporária global pode ser feita assim:

```powershell
$testTemp = Join-Path (Get-Location) "tmp\pytest-local"
python -m pytest tests -q --basetemp=$testTemp -p no:cacheprovider
```

Use uma pasta descartável dedicada aos testes, nunca a raiz do projeto ou uma pasta com resultados científicos.

## Política para novos testes

- Um defeito corrigido deve ganhar um teste que falhava antes da correção.
- Equações novas devem incluir caso calculável à mão, limites e unidades esperadas.
- Comparações de ponto flutuante devem usar tolerância explícita e justificada.
- Testes não devem depender da ordem de execução, rede ou relógio sem controle.
- Mudanças no balanço hídrico ou financeiro devem preservar os testes de invariantes.
- Não fixe na documentação uma contagem de testes: o resumo do `pytest` é a evidência da revisão executada.
