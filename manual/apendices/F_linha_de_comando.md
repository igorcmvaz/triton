# Apêndice F — Referência da linha de comando

Gerado do próprio `argparse` do programa por `manual/gerar_apendices.py`.
O guia 19 ensina a usar; este apêndice lista as opções.

## F.1. Uso geral

```
usage: cli.py [-h]
              {run,analyze,econ,validate,init,init-catalog,matrix,matrix-projects,batch,uncertainty,compare-mass,run-vaz-study} ...

Netuno CLI: simulaÃ§Ã£o, economia, ACV, TOPSIS e automaÃ§Ã£o reproduzÃ­vel.

positional arguments:
  {run,analyze,econ,validate,init,init-catalog,matrix,matrix-projects,batch,uncertainty,compare-mass,run-vaz-study}
    run                 Simula; padrÃ£o tÃ©cnico compatÃ­vel com o legado
    analyze             Executa cadeia completa de anÃ¡lises
    econ                Atalho legado para anÃ¡lise econÃ´mica
    validate            Valida a estrutura e as premissas de um projeto
    init                Cria um template .netuno estruturado e editÃ¡vel
    init-catalog        Cria catÃ¡logo JSON de premissas ou de climas
    matrix              Combina premissas de edifÃ­cio com catÃ¡logo climÃ¡tico
    matrix-projects     Executa arquivos .netuno em lista, pasta de chuva ou
                        matriz fatorial declarada no projeto
    batch               Executa cenÃ¡rios de uma planilha CSV/XLSX
    uncertainty         Propaga incertezas por Monte Carlo para uma decisÃ£o de
                        volume
    compare-mass        Executa simulaÃ§Ã£o paralela em massa dos 4 casos de
                        reservatÃ³rios combinados e compara com TesteMassivo
    run-vaz-study       Executa estudo massivo de tipologias residenciais de
                        Vaz em Parquet com ACV, Financeiro e TOPSIS

options:
  -h, --help            show this help message and exit
```

## F.2. `run` — Simula um projeto

```
usage: cli.py run [-h]
                  [--analysis {technical,economic,environmental,topsis,all}]
                  [--volume VOLUME] [--weights WEIGHTS] [--rainfall RAINFALL]
                  [--start-date START_DATE] [--set CAMPO=VALOR]
                  [--format {text,json,csv,html,xlsx}] [--output OUTPUT]
                  [--weight-sensitivity N] [--seed SEED]
                  file

positional arguments:
  file                  Projeto CSV legado, .netuno ou JSON estruturado

options:
  -h, --help            show this help message and exit
  --analysis {technical,economic,environmental,topsis,all}
  --volume VOLUME       ForÃ§a um volume de cisterna inferior (L)
  --weights WEIGHTS     Pesos TOPSIS: tÃ©cnico,econÃ´mico,ambiental
  --rainfall RAINFALL   Substitui a chuva do projeto por este arquivo
  --start-date START_DATE
                        Data inicial dd/mm/aaaa; necessÃ¡ria para sazonalidade
                        mensal
  --set CAMPO=VALOR     Sobrescreve campo do projeto; pode ser repetido
  --format {text,json,csv,html,xlsx}
  --output OUTPUT       Arquivo de saÃ­da obrigatÃ³rio para json/csv/html/xlsx
  --weight-sensitivity N
                        Amostra N combinaÃ§Ãµes de pesos TOPSIS e informa a
                        frequÃªncia vencedora
  --seed SEED           Semente para anÃ¡lises estocÃ¡sticas
```

## F.3. `analyze` — Executa a cadeia completa de análises

```
usage: cli.py analyze [-h]
                      [--analysis {technical,economic,environmental,topsis,all}]
                      [--volume VOLUME] [--weights WEIGHTS]
                      [--rainfall RAINFALL] [--start-date START_DATE]
                      [--set CAMPO=VALOR] [--format {text,json,csv,html,xlsx}]
                      [--output OUTPUT] [--weight-sensitivity N] [--seed SEED]
                      file

positional arguments:
  file                  Projeto CSV legado, .netuno ou JSON estruturado

options:
  -h, --help            show this help message and exit
  --analysis {technical,economic,environmental,topsis,all}
  --volume VOLUME       ForÃ§a um volume de cisterna inferior (L)
  --weights WEIGHTS     Pesos TOPSIS: tÃ©cnico,econÃ´mico,ambiental
  --rainfall RAINFALL   Substitui a chuva do projeto por este arquivo
  --start-date START_DATE
                        Data inicial dd/mm/aaaa; necessÃ¡ria para sazonalidade
                        mensal
  --set CAMPO=VALOR     Sobrescreve campo do projeto; pode ser repetido
  --format {text,json,csv,html,xlsx}
  --output OUTPUT       Arquivo de saÃ­da obrigatÃ³rio para json/csv/html/xlsx
  --weight-sensitivity N
                        Amostra N combinaÃ§Ãµes de pesos TOPSIS e informa a
                        frequÃªncia vencedora
  --seed SEED           Semente para anÃ¡lises estocÃ¡sticas
```

## F.4. `validate` — Confere a estrutura e as premissas de um projeto

```
usage: cli.py validate [-h] [--rainfall RAINFALL] file

positional arguments:
  file

options:
  -h, --help           show this help message and exit
  --rainfall RAINFALL
```

## F.5. `init` — Cria um modelo .netuno editável

```
usage: cli.py init [-h] [--rainfall RAINFALL] [--embed-rainfall] file

positional arguments:
  file                 Destino .netuno

options:
  -h, --help           show this help message and exit
  --rainfall RAINFALL  Arquivo de chuva de referÃªncia
  --embed-rainfall     Incorpora a sÃ©rie no .netuno
```

## F.6. `matrix` — Combina premissas de edificação com catálogo climático

```
usage: cli.py matrix [-h]
                     [--analysis {technical,economic,environmental,topsis,all}]
                     [--weights WEIGHTS]
                     [--weight-sensitivity WEIGHT_SENSITIVITY] [--seed SEED]
                     [--output-dir OUTPUT_DIR] [--quiet]
                     premises climates

positional arguments:
  premises              CatÃ¡logo JSON com schema netuno-premises-catalog
  climates              CatÃ¡logo JSON com schema netuno-climate-catalog

options:
  -h, --help            show this help message and exit
  --analysis {technical,economic,environmental,topsis,all}
  --weights WEIGHTS
  --weight-sensitivity WEIGHT_SENSITIVITY
  --seed SEED
  --output-dir OUTPUT_DIR
  --quiet               Oculta a barra de progresso e ETA
```

## F.7. `matrix-projects` — Executa vários projetos de uma lista ou pasta

```
usage: cli.py matrix-projects [-h] --projects PROJECTS [PROJECTS ...]
                              [--rainfall-dir RAINFALL_DIR]
                              [--ignore-project-factors] [--recursive]
                              [--analysis {technical,economic,environmental,topsis,all}]
                              [--weights WEIGHTS]
                              [--weight-sensitivity WEIGHT_SENSITIVITY]
                              [--seed SEED] [--output-dir OUTPUT_DIR]
                              [--quiet]

options:
  -h, --help            show this help message and exit
  --projects PROJECTS [PROJECTS ...]
                        Arquivos .netuno/.json ou pastas contendo arquivos
                        .netuno
  --rainfall-dir RAINFALL_DIR
                        Pasta de sÃ©ries CSV/TXT/DAT; combina cada projeto com
                        cada sÃ©rie
  --ignore-project-factors
                        Ignora o bloco cli_factorial dos projetos
  --recursive           Procura projetos e sÃ©ries tambÃ©m nas subpastas
  --analysis {technical,economic,environmental,topsis,all}
  --weights WEIGHTS
  --weight-sensitivity WEIGHT_SENSITIVITY
  --seed SEED
  --output-dir OUTPUT_DIR
  --quiet               Oculta a barra de progresso e ETA
```

## F.8. `batch` — Executa cenários de uma planilha

```
usage: cli.py batch [-h] [--base BASE]
                    [--analysis {technical,economic,environmental,topsis,all}]
                    [--weights WEIGHTS] [--format {text,json,csv,html,xlsx}]
                    [--output OUTPUT]
                    [--weight-sensitivity WEIGHT_SENSITIVITY] [--seed SEED]
                    file

positional arguments:
  file                  Planilha de cenÃ¡rios

options:
  -h, --help            show this help message and exit
  --base BASE           Projeto .netuno/CSV com parÃ¢metros econÃ´micos e
                        ambientais base
  --analysis {technical,economic,environmental,topsis,all}
  --weights WEIGHTS
  --format {text,json,csv,html,xlsx}
  --output OUTPUT       Arquivo de saÃ­da
  --weight-sensitivity WEIGHT_SENSITIVITY
  --seed SEED
```

## F.9. `uncertainty` — Propaga incertezas por Monte Carlo

```
usage: cli.py uncertainty [-h]
                          [--analysis {technical,economic,environmental,all}]
                          [--volume VOLUME] [--samples SAMPLES] [--seed SEED]
                          [--rainfall-cv RAINFALL_CV] [--area-cv AREA_CV]
                          [--demand-cv DEMAND_CV] [--capex-cv CAPEX_CV]
                          [--weights WEIGHTS] [--set CAMPO=VALOR]
                          [--format {text,json,csv}] [--output OUTPUT]
                          file

positional arguments:
  file                  Projeto CSV, .netuno ou JSON

options:
  -h, --help            show this help message and exit
  --analysis {technical,economic,environmental,all}
  --volume VOLUME       Volume analisado; padrÃ£o: Ã³timo tÃ©cnico do caso-base
  --samples SAMPLES
  --seed SEED
  --rainfall-cv RAINFALL_CV
                        CV percentual da chuva
  --area-cv AREA_CV     CV percentual da Ã¡rea
  --demand-cv DEMAND_CV
                        CV percentual da demanda
  --capex-cv CAPEX_CV   CV percentual de CAPEX
  --weights WEIGHTS
  --set CAMPO=VALOR
  --format {text,json,csv}
  --output OUTPUT
```

