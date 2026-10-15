# Testes do Triton

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
python -m pytest tests/test_essencial.py -v

# Caso específico
python -m pytest tests/test_essencial.py::test_descarte_apos_estiagem_atinge_apenas_o_primeiro_evento -v

# Seleção por palavra-chave
python -m pytest tests -k topsis -v
```

## Ambiente gráfico e dados

`tests/conftest.py` configura `QT_QPA_PLATFORM=offscreen` e o backend `Agg` do Matplotlib quando essas variáveis ainda não foram definidas. Assim, a suíte normalmente roda sem monitor e sem abrir janelas. Defina outro backend antes da execução apenas quando precisar investigar o comportamento gráfico real.

Os testes devem ser iniciados na raiz porque usam módulos do repositório e dados em `data/`. Arquivos temporários pertencem ao diretório fornecido pelo `pytest`; saídas científicas permanentes não devem ser atualizadas silenciosamente durante uma execução comum.

## Edições: o que roda em cada uma

O pacote `triton/` e a pasta `tests/` são **idênticos** nas três edições (`triton_brl`, `triton_int`, `triton_prt`); só os dados e o `main.py` diferem. A edição da suíte vem de `TRITON_EDITION` (`BRL`, `INT`, `PRT`; `POR` é o código antigo da PRT) e, sem a variável, do nome da pasta (`triton_int` roda como INT, qualquer outro nome como BRL). O `tests/conftest.py` é o mesmo nas três e grava a edição escolhida na variável, de modo que a suíte e o código testado concordam.

O **motor** (simulação, economia, ACV, decisão multicritério) roda em todas as edições, com o `TritonConfig()` cru, que traz os padrões históricos em qualquer uma: o motor não conhece edição. Quem conhece é a fábrica `triton.core.edition.configuracao_da_edicao` (leitores de projeto e linha de comando) e `projeto_novo_da_edicao` (interface); `tests/unit/test_fabrica_da_edicao.py` fixa o desenho.

Só o que depende de dado de uma edição fica fora das outras, por duas listas ao lado do `conftest.py`:

| Arquivo | O que lista | Fora de qual edição é saltado |
| --- | --- | --- |
| `so_da_brl.txt` | banco de 652 municípios, CLIMBra, tarifas CASAN/CORSAN, casos e séries do manual do Brasil, série do MCTI | INT e PRT |
| `so_da_prt.txt` | base E-OBS por concelho e tarifários portugueses transcritos | BRL e INT |

Cada linha é um arquivo inteiro (`tests/unit/x.py`, que nem é importado) ou um teste (`tests/unit/x.py::test_y`, que vale também para as variantes parametrizadas); `#` abre um comentário. **Não ponha aqui um teste só porque ele falha fora da BRL**: se o que falta é uma configuração, monte-a no teste (como em `test_dual_tank_pumping_com_chuva_sintetica`); a lista é só para o que lê dado que a edição não traz. `tests/unit/test_fabrica_da_edicao.py` confere que toda entrada das listas aponta para um teste que existe.

## Mapa da suíte

A suíte foi consolidada: o que testa o
programa está em dois arquivos; o que testa dado, manual e pacote continua nos seus.

| Grupo | Arquivos e escopo principal |
| --- | --- |
| Núcleo, sem interface | `test_essencial.py`: invariantes (massa, limites físicos, sentido do VPL, «economizar nunca aumenta a conta»), limites (zero, vazio, extremos) e modos de falha (série com falha, base ausente, download interrompido). Roda na integração contínua, sem Qt |
| Núcleo, com interface | `test_essencial_interface.py`: telas que levam dado ao cálculo, paridade tela × linha de comando, edições, Modulação Probabilística na tela |
| Dado com procedência | `unit/test_transcricoes.py`, `test_registro_de_fontes.py`, `test_processo_tarifario.py`, `test_regimes_tarifarios.py`, `test_tariffs_structure.py` e demais: tarifas, fatores e catálogos conferidos contra o documento |
| Manual e documentação | `unit/test_manual_confere_com_o_programa.py`, `test_manual_en.py`, `test_o_que_se_comunica.py`, `test_documentation_citations.py` e demais; `invariants/test_coerencia_da_documentacao.py` |
| Distribuição | `unit/test_empacotamento.py`, `test_instalador.py`, `test_edicoes_documentadas.py`, `test_icones.py`; `invariants/test_declared_dependencies.py`, `test_saida_de_console.py` |
| Validação contra o Netuno 4 | `benchmarking/test_replicacao_netuno4.py`, `integration/test_batch_validation.py` |

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
