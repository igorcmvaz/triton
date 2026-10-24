# Triton CLI — guia prático

Use a linha de comando para execuções reproduzíveis, automação e comparação em lote. Ela aceita projetos CSV legados e projetos estruturados `.triton` (JSON).

Execute os exemplos a partir da raiz do repositório, com o mesmo ambiente usado pela aplicação desktop. Consulte a ajuda efetiva da versão instalada com:

```powershell
python -m triton.cli --help
python -m triton.cli analyze --help
```

## Escolha do formato de projeto

| Formato | Uso recomendado | Rastreabilidade |
| --- | --- | --- |
| `.triton` | novos estudos, intercâmbio e automação | preserva entradas técnicas, econômicas, ambientais e TOPSIS; pode incorporar a chuva |
| CSV legado | compatibilidade e casos técnicos existentes | possui estrutura mais limitada; documente externamente as premissas não representadas |

Prefira `.triton` com `--embed-rainfall` quando o estudo precisar ser reproduzido em outro computador. Mesmo autocontido, o arquivo não substitui o registro de fonte, período, tratamento e controle de qualidade da série.

## Fluxo recomendado

```powershell
# 1. Crie um projeto portátil, incorporando a chuva diária.
python -m triton.cli init .\projeto.triton --rainfall Funchal.csv --embed-rainfall

# 2. Valide o arquivo antes de calcular.
python -m triton.cli validate .\projeto.triton

# 3. Rode técnica, economia, ACV e TOPSIS, com resultado auditável.
python -m triton.cli analyze .\projeto.triton --analysis all --format json --output .\saida\resultado.json
```

O comando `run` executa o balanço hídrico técnico. `analyze --analysis all` aplica, para cada volume da varredura, o balanço técnico, a análise econômica, o balanço ambiental e o ranking TOPSIS. Assim, todas as escolhas usam as mesmas alternativas simuladas.

## Comandos mais usados

| Objetivo | Comando |
| --- | --- |
| Simular um volume específico | `python -m triton.cli run .\projeto.triton --volume 5000 --analysis all` |
| Alterar premissas sem editar o projeto | `python -m triton.cli analyze .\projeto.triton --set area=150 --set rainwater_share=0.5` |
| Ajustar pesos TOPSIS | `python -m triton.cli analyze .\projeto.triton --analysis topsis --weights 0.40,0.35,0.25` |
| Avaliar robustez dos pesos | `python -m triton.cli analyze .\projeto.triton --analysis topsis --weight-sensitivity 1000 --seed 42 --format json --output .\saida\pesos.json` |
| Propagar incertezas | `python -m triton.cli uncertainty .\projeto.triton --samples 1000 --rainfall-cv 10 --demand-cv 15 --capex-cv 20 --format json --output .\saida\monte-carlo.json` |
| Gerar HTML ou XLSX | Troque `--format json` por `html` ou `xlsx` e informe `--output` |
| Executar planilha de cenários | `python -m triton.cli batch .\cenarios.xlsx --base .\projeto.triton --analysis all --format xlsx --output .\saida\lote.xlsx` |
| Combinar vários projetos e chuvas | `python -m triton.cli matrix-projects --projects .\projetos --rainfall-dir .\chuvas --recursive --output-dir .\saida\matriz` |

Os valores de `--weights` são, nesta ordem: técnico, econômico e ambiental. A CLI normaliza a soma automaticamente. As saídas gerais aceitam `text`, `json`, `csv`, `html` e `xlsx`; o comando `uncertainty` aceita `text`, `json` e `csv`. Formatos estruturados exigem `--output`. XLSX requer `pandas` e `openpyxl`.

`--set CAMPO=VALOR` pode ser repetido e altera a premissa somente para aquela execução. Registre o comando completo no protocolo do estudo, pois o arquivo de origem permanece inalterado.

## Matriz edifícios × climas

Mantenha os dois catálogos independentes: um de premissas do edifício e outro de arquivos climáticos. Isso permite comparar várias cidades para o mesmo edifício, ou vários edifícios para a mesma cidade, sem duplicar dados.

```powershell
python -m triton.cli init-catalog premises .\premissas.json
python -m triton.cli init-catalog climates .\climas.json
python -m triton.cli matrix .\premissas.json .\climas.json --analysis all --output-dir .\resultado-matriz
```

O terminal informa progresso, combinações concluídas, tempo decorrido e ETA. A pasta de saída contém `triton-matriz-resumo.csv` (uma decisão por combinação), `triton-matriz-alternativas.csv` (todos os volumes), `triton-matriz-detalhado.json` (auditoria) e `triton-matriz-painel.html` (leitura consolidada).

### Matriz de projetos

Use `matrix-projects` quando cada configuração já estiver em um ou mais arquivos `.triton`, ou quando o próprio projeto declarar fatores experimentais em `cli_factorial`:

```powershell
python -m triton.cli matrix-projects --projects .\projetos --output-dir .\resultado-projetos
python -m triton.cli matrix-projects --projects .\projetos --rainfall-dir .\chuvas --recursive --output-dir .\resultado-climas
```

Use `--ignore-project-factors` para desconsiderar temporariamente o bloco fatorial gravado nos projetos. Fixe `--seed` quando houver sensibilidade estocástica dos pesos.

## Cenários em planilha

`batch` lê CSV ou XLSX. Com `--base`, as linhas herdam do projeto-base as premissas econômicas e ambientais que a planilha não substitui:

```powershell
python -m triton.cli batch .\examples\triton-cli-scenarios.csv --base .\projeto.triton --analysis all --format csv --output .\saida\cenarios.csv
```

Valide primeiro o projeto-base e preserve a planilha de entrada junto do resultado. Um lote compara cenários declarados; ele não cria automaticamente distribuições de incerteza.

## Simulação em massa e comparação com TesteMassivo

Para rodar em massa a separação de séries futuras e comparar a nova versão do motor contra a base de dados de referência (`TesteMassivo/`):

```powershell
# 1. Separe as séries climáticas futuras em Near Future (2015-2059) e Far Future (2060-2100):
python scripts/split_climates.py

# 2. Execute a simulação paralela multi-core dos 4 casos de reservatórios combinados da Tabela 2 e gera o relatório comparativo:
python -m triton.cli compare-mass
```

Parâmetros opcionais de `compare-mass`:

- `--input-dir`: Pasta com os arquivos de chuva divididos (`TesteMassivo/Triton_future_files_split`)
- `--reference-dir`: Pasta com os arquivos CSVs consolidados de referência (`TesteMassivo`)
- `--output-dir`: Pasta de destino dos novos CSVs consolidados e relatórios (`TesteMassivo/nova_versao`)
- `--area`, `--residents`, `--demand`, `--share`, `--runoff` e `--discard`: premissas do caso comparado
- `--workers`: Número de núcleos de CPU para processamento em paralelo

## Estudo massivo de tipologias residenciais de Vaz

Para executar a divisão em quatro horizontes temporais (Histórico, Near, Middle e Far) e rodar o estudo completo em Parquet:

```powershell
# 1. Separar séries climáticas futuras em Near (2015-2044), Middle (2045-2074) e Far Future (2075-2100):
python scripts/split_climates_vaz.py

# 2. Executar o estudo massivo das cinco tipologias e exportar em Parquet:
python -m triton.cli run-vaz-study
```

Parâmetros opcionais de `run-vaz-study`:

- `--input-dir`: Pasta com as séries climáticas divididas (`TesteMassivo/Triton_vaz_files_split`)
- `--output-dir`: Pasta de destino para o arquivo Parquet e relatórios (`TesteMassivo/estudo_vaz`)
- `--workers`: Número de processos paralelos; por padrão, o comando preserva um núcleo para o sistema quando possível

O estudo Vaz requer `pyarrow` para Parquet. Avalie espaço em disco, memória e temperatura da máquina antes de aumentar `--workers`; mais processos não garantem ganho linear.

## Reprodutibilidade e auditoria

Para cada execução usada em relatório ou publicação, preserve:

- arquivo `.triton`, catálogos ou planilha de cenários efetivamente usados;
- série de chuva e sua proveniência, salvo quando incorporada ao projeto;
- comando completo, versão do Triton e versão do Python;
- semente de qualquer análise estocástica;
- arquivos de saída sem edição manual e um registro das interpretações posteriores.

Sensibilidade de pesos e Monte Carlo respondem a perguntas diferentes. A primeira mede estabilidade do ranking diante das preferências; a segunda propaga incerteza das entradas declaradas. Nenhuma delas corrige dados de baixa qualidade ou hipóteses omitidas.

## Boas práticas

- Use `--embed-rainfall` quando o projeto precisar circular entre computadores.
- Execute `validate` antes de processar lotes.
- Use caminhos de saída diferentes para cenários diferentes e não sobrescreva evidências sem revisão.
- Fixe `--seed` em análises de pesos e Monte Carlo para reproduzir exatamente uma execução.
- Comece lotes grandes com uma amostra pequena e confira unidades, colunas e ordem de grandeza.
- Use `python -m triton.cli <comando> --help` quando este guia e a versão instalada divergirem.
