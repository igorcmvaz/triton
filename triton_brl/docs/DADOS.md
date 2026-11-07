# Dados da Edição Brasil (BRL): o que há, de onde vem e quanto confiar

Versão 0.1.0, 05/11/2026. Este documento descreve cada conjunto de dados da edição: o que é, a fonte (URL e data), a licença, a cobertura, a resolução, o período, o tratamento de falhas, o nível de qualidade, o tamanho, como o programa o carrega e como reproduzi-lo. Todo número vem de um arquivo do repositório (os arquivos estão citados); onde a informação não existe no repositório, o texto diz «não verificado».

Tamanhos em MiB (1 MiB = 1.048.576 bytes, a unidade do aviso de 50 MB do GitHub). **Regra do projeto: nenhum arquivo rastreado passa de 50 MiB.** O script `scripts/verificar_tamanhos.py` (na raiz do repositório) falha se isso acontecer e a verificação do GitHub o roda a cada envio. O maior arquivo da edição é `data/climbra_KACE.db`, com 43,02 MiB.

## 1. Visão geral

| Conjunto | Onde | Formato | Tamanho | No Git | Licença |
| :--- | :--- | :--- | ---: | :---: | :--- |
| Base climática CLIMBra (19 modelos CMIP6) | `data/climbra_<modelo>.db` + `data/climbra_partes.json` | SQLite, uma parte por modelo | 785,1 MiB (19 arquivos de 39,98 a 43,02 MiB) | sim | CC0 1.0 |
| Séries de chuva dos exemplos | `data/rainfall/*.csv` | CSV, um valor diário por linha | 2,13 MiB (12 arquivos) | sim | CC0 1.0 (recortes do CLIMBra) |
| Banco tarifário (652 municípios) | `triton/data/brazil_cities_tariffs.json` | JSON | 5,37 MiB | sim | valores públicos transcritos; ver §4 |
| Catálogo e faixas auditadas | `tarifas/catalogo_tarifas_auditado_652.*`, `tarifas/tarifas_detalhadas_auditadas.csv` | CSV, XLSX | 5,5 MiB | sim | idem |
| Transcrições e registro de fontes | `tarifas/transcricoes/` (155 arquivos), `tarifas/fontes/{registro.json,REGISTRO.md,procedencia.tsv}` | JSON, Markdown, TSV | 1,6 MiB | sim | idem |
| Documentos oficiais de terceiros (PDF, HTML) | `tarifas/fontes/<prestador>/` | PDF, HTML | 202 MB | **não** (disco do mantenedor) | de terceiros; não se redistribui |
| Banco que reúne esses documentos | `tarifas/tarifas_fontes.db` | SQLite | 104 MB | **não** | de terceiros |
| Fator de emissão da rede (MCTI/SIRENE) | `triton/data/fatores_emissao_rede_mcti.json`, `data/fontes_externas/…xlsx` | JSON, XLSX | 0,02 MiB | sim | ver §5 |
| Custos de referência, rotas de produção de água | `triton/data/costs_database.json`, `rotas_producao_agua.json` | JSON | 0,03 MiB | sim | do projeto |
| Resultados oficiais do Netuno 4 (validação) | `data/simulation_outputs/` | CSV | 0,28 MiB | sim | ver §5 |
| Exemplos e relatórios de exemplo | `examples/`, `reports/exemplos/` | `.triton`, PDF | 0,71 MiB e 8,02 MiB | sim | do projeto |
| Visualizador 3D (HDR e JS) | `triton/data/volumetria/` | HDR, JS | 2,1 MiB | sim | CC0 (céu) e MIT (three.js) |
| Manual (PDF, site, figuras) | `manual/` | PDF, HTML, PNG | 53,3 MiB (456 arquivos) | sim | do projeto |

Ficam **de fora do Git** (e do instalador) os 6,24 GB de CSV originais do CLIMBra (medida em disco; os textos que dizem «~6,5 GB» arredondam por excesso), `dist/`, `build/` e os registros de compilação.

Os dados de **tarifas** e de **pluviometria** estão em arquivos separados entre si e separados da base CLIMBra: a chuva dos exemplos fica em `data/rainfall/`, as tarifas em `triton/data/` e `tarifas/`, a base climática em `data/climbra_*.db`.

## 2. Base climática CLIMBra (`data/climbra_<modelo>.db`)

| Campo | Valor |
| :--- | :--- |
| O que é | Projeções diárias de **precipitação** (mm/dia) do CMIP6, com correção de viés, para 652 municípios brasileiros: 19 modelos × 3 cenários × 652 municípios = 37.164 séries (1.956 por modelo) |
| Fonte | Ballarin, A. S. et al. (2023). *CLIMBra – Climate Change Dataset for Brazil*. Scientific Data 10, 47. doi:10.1038/s41597-023-01956-z. Dados: Science Data Bank, doi:10.57760/sciencedb.02316 |
| Licença | **CC0 1.0 Universal** (domínio público), declarada na `climbra_meta` de cada parte e em `infos_licenses/AVISOS_DE_TERCEIROS.txt`. Sem restrição de redistribuição |
| Cobertura | 652 municípios (27 UF, todas as capitais), os mesmos 652 do banco tarifário (conferido por nome normalizado) |
| Resolução | Grade original de 0,25° × 0,25° (cerca de 28 km), conforme `docs/base_climatica_climbra.md`. Uma série por município |
| Período | HIST: 01/01/1980 a 31/12/2013 (12.419 dias); SSP2-4.5 e SSP5-8.5: 01/01/2015 a 31/12/2100 (31.411 dias). KACE, HadGEM3-GC31-LL e UKESM1-0-LL têm um dia a menos (12.418 e 31.410) |
| Falhas | Séries contínuas, sem dias faltantes (modelo, não observação). Não há preenchimento no Triton. A correção de viés é a do CLIMBra (Quantile Delta Mapping contra a grade observacional de Xavier, King e Scanlon, 2016, segundo `docs/base_climatica_climbra.md`) |
| Tratamento do Triton | Nenhum valor é alterado além da compactação: float16 e zlib nível 6. A diferença no balanço diário entre float64 e float16 é de 0,000045% (`docs/base_climatica_climbra.md`) |
| Qualidade | O Triton **não recalcula** a qualidade do CLIMBra: ela é a do artigo. Não há medida regional própria neste repositório. Todos os 652 municípios têm as 57 séries (19 modelos × 3 cenários); a integridade das partes é conferida por SHA-256 |
| Tamanho | 785,1 MiB em 19 partes (39,98 MiB IPSL-CM6A-LR a 43,02 MiB KACE). Limite do projeto: 50 MiB por arquivo; margem mínima de 6,98 MiB |
| Carregamento | `triton/core/climate_database.py` procura `TRITON_CLIMBRA_DIR`, `TRITON_CLIMBRA_DB`/`TRITON_CLIMATE_DB`, depois `data/` do executável, do código e do diretório atual. Abre em modo somente leitura. A parte do modelo vale primeiro; o `climbra.db` antigo cobre o que faltar |
| Manifesto | `data/climbra_partes.json`: arquivo, modelo, bytes, séries, SHA-256 do arquivo e do conteúdo, `limite_github_mb` = 50 |
| Reprodução | Os CSV originais (6,24 GB) são compilados por `scripts/compilar_base_climbra.py` e divididos por `scripts/dividir_base_climbra.py` (ferramentas do mantenedor, fora do Git; ver `scripts/README.md`). Se uma parte passar do limite, o divisor separa o modelo por cenário (`climbra_<modelo>__HIST.db` etc.) e o leitor entende os dois nomes. Use `--limite-mb 50` |
| Verificação | `python -m pytest tests/unit/test_climbra_particionada.py -k reais -p no:cacheprovider`: SHA-256 de cada parte contra o manifesto e séries idênticas ao banco único |

Por região: as cinco macrorregiões e as 27 UF têm cobertura completa (todos os municípios, todos os modelos e cenários); a tabela de municípios por UF está em §4.

## 3. Séries de chuva dos exemplos (`data/rainfall/`)

| Campo | Valor |
| :--- | :--- |
| O que é | 12 arquivos CSV (`Florianopolis1..3`, `Brasilia1..3`, `Manaus1..3`, `SaoPaulo1..3`), um valor de precipitação diária (mm) por linha, sem data |
| Origem verificada | Cada arquivo é um **recorte do CLIMBra**: comparado com as 19 partes, cada um coincide (diferença máxima abaixo de 0,1 mm, por causa do float16) com uma série de município, modelo e cenário. Os sufixos 1, 2 e 3 não seguem uma regra única: `Florianopolis1` = GFDL-CM4/SSP5-8.5; `Florianopolis2` = NESM3/SSP2-4.5; `Florianopolis3` = UKESM1-0-LL/HIST; `Manaus1` = EC-EARTH3/SSP2-4.5; `Manaus2` = MPI-ESM1-2/HIST; `Manaus3` = UKESM1-0-LL/SSP5-8.5; `SaoPaulo1` = ACCESS-CM2/SSP2-4.5; `SaoPaulo2` = CMCC-ESM2/HIST; `SaoPaulo3` = TaiESM1/SSP5-8.5; `Brasilia1` = ACCESS-ESM1-5/SSP2-4.5; `Brasilia2` = INM-CM5/HIST; `Brasilia3` = UKESM1-0-LL/SSP5-8.5 |
| Licença | CC0 1.0 (a do CLIMBra) |
| Período | HIST 12.418 ou 12.419 dias; futuro 31.410 ou 31.411 dias, a partir de 01/01/2015 (arquivos de futuro) |
| Qualidade | A do CLIMBra: são séries modeladas, não de pluviômetro. Servem de exemplo e de ponto de partida; para um projeto real, use a série medida |
| Tamanho | 2,13 MiB no total |
| Uso | Séries dos exemplos e dos casos do manual; carregadas por `triton/core/parser.py` (`data/rainfall/`) |

Correção de 24/10/2026: `triton/core/bibliography.py` registrava o BDMEP do INMET como origem destas séries. A comparação acima mostra que são séries CLIMBra, e a nota da referência `inmet_bdmep` foi reescrita para dizer isso (o INMET fica como referência de séries medidas, não como origem dos arquivos).

## 4. Tarifas de água, esgoto e energia

### O que há

| Arquivo | Conteúdo |
| :--- | :--- |
| `triton/data/brazil_cities_tariffs.json` | O banco que o programa lê: 652 municípios em 27 UF; faixas de água, esgoto, parcela fixa, regime de mínimo, prestador, agência reguladora, vigência, documento de origem, categorias (comercial, industrial, pública, social), energia B1 por distribuidora, grau de confiança. Versão 2026-09-08, última atualização 05/10/2026 |
| `tarifas/tarifas_detalhadas_auditadas.csv` | 3.604 registros por município e faixa (auditoria de 24/08/2026) |
| `tarifas/catalogo_tarifas_auditado_652.csv/.xlsx` | Uma linha por município, com valores, fontes, alertas e escores |
| `tarifas/transcricoes/*.json` | Uma transcrição por documento oficial (tabelas, municípios, contas de conferência); `ALTERACOES.md` e `historico.json` guardam o antes e o depois; `FILA.md` o que falta |
| `tarifas/fontes/registro.json`, `REGISTRO.md`, `procedencia.tsv` | Registro de cada documento recebido: URL, SHA-256, data, prestador, vigência e o que foi feito |
| `tarifas/PANORAMA_TARIFAS_E_CONFIABILIDADE.md`, `FONTES_E_METODOLOGIA.md` | Panorama e metodologia da auditoria de 24/08/2026 |

### Fonte, licença e restrições

- **Saneamento.** Estruturas tarifárias lidas das páginas, resoluções e tabelas dos prestadores e das agências reguladoras (CAESB/ADASA, CASAN/ARESC, SANEPAR/AGEPAR, SABESP/ARSESP, CORSAN/AGERGS e outras), cada uma com URL no `tarifas/fontes/REGISTRO.md` e em `fonte_url`/`fonte_documento` do município. Referência nacional: SINISA (https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa) e lista positiva da Tarifa Social da ANA, para conferir prestadores.
- **Energia.** Base aberta «Tarifas de aplicação das distribuidoras de energia elétrica» da ANEEL (https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e/resource/fcf2906c-7c32-4b9b-a637-054e7a5234f4), consultada em 24/08/2026. Valores em R$/kWh **sem** ICMS, PIS/Pasep, Cofins, COSIP nem bandeiras.
- **Licença da base ANEEL.** A página do conjunto «Tarifas de aplicação das distribuidoras de energia elétrica» declara a **Licença Aberta para Bases de Dados (ODbL) do Open Data Commons** (https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e, acesso em 24/10/2026). A ODbL exige atribuição e que uma base derivada de uso público seja oferecida também em ODbL: os valores de energia do `brazil_cities_tariffs.json` (R$/kWh por distribuidora) são extraídos dessa base; se o JSON for publicado como conjunto de dados à parte, a atribuição à ANEEL e a oferta em ODbL precisam ser decididas. **Decisão do titular (25/10/2026): aprovado usar o JSON extraído**, por serem dados públicos; a atribuição devida é «Dados: ANEEL, Tarifas de aplicação das distribuidoras de energia elétrica, ODbL (https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e)».
- **Licença.** O repositório contém os números (fatos públicos regulados) e as referências, não os documentos: os PDF e páginas de terceiros ficam só no disco do mantenedor (`.gitignore`) e **não se redistribuem**. A licença de reutilização dos portais dos prestadores e das agências não foi verificada um a um (não verificado nesta versão); o uso é de transcrição de valores públicos com a fonte citada.

### Cobertura, resolução e período

652 municípios (1 no Distrito Federal e em Roraima, 137 em São Paulo), uma estrutura por município, por prestador e vigência. Vigências do saneamento: 2026 em 382 municípios, 2025 em 162 e 2024 em 63; os demais trazem texto em vez de data (ver o campo `vigencia_saneamento`). Corte da auditoria: 24/08/2026; banco atualizado em 05/10/2026.

### Tratamento de falhas

Não se preenche valor por vizinhança. O município sem documento específico guarda a melhor referência disponível e fica marcado: `update_status_sanitation` = `MANUAL_REVIEW_NEEDED` (48 municípios) ou `VERIFIED_AUDIT` (8, auditado pelo catálogo, sem documento guardado). Energia sem ato vigente na base aberta guarda o último valor oficial e o marca como `EXPIRED_ANEEL_REF` (140 municípios). Formas de cobrança que o banco ainda não representa (parcela fixa que muda com a faixa; cobrança de todo o volume pelo preço da faixa) ficam como «dado ruim» com o motivo.

### Nível de qualidade

Duas escalas, ambas lidas do banco e de `tarifas/transcricoes/FILA.md` (05/10/2026).

**Confiança (A a D).** A, 85 a 100 pontos: evidência primária específica, atual, estrutura completa e conciliação; B, 70 a 84,9: evidência oficial suficiente com uma ressalva; C, 50 a 69,9: evidência incompleta, histórica ou derivada; D, abaixo de 50: fallback. O escore global é 60% saneamento + 40% energia (`tarifas/FONTES_E_METODOLOGIA.md`).

| Região | Municípios | A | B | C |
| :--- | ---: | ---: | ---: | ---: |
| Centro-Oeste | 44 | 40 | 4 | 0 |
| Nordeste | 173 | 172 | 1 | 0 |
| Norte | 71 | 53 | 13 | 5 |
| Sudeste | 255 | 212 | 43 | 0 |
| Sul | 109 | 107 | 2 | 0 |
| **Brasil** | **652** | **584** | **63** | **5** |

**Classe de procedência** (`FILA.md`, 05/10/2026): documentada com as quatro categorias, 299; só a residencial documentada, 161; documentada com vigência de mais de 12 meses (a renovar), 136; auditada sem documento guardado, 8; a confirmar, 48; dado ruim, 0.

**Energia.** 512 municípios com ato vigente na base da ANEEL; 140 com a referência expirada (Equatorial Pará 42, CELESC 30, Neoenergia Elektro 27, Equatorial Maranhão 22, Energisa Paraíba 10, Sulgipe 2 e outras).

Municípios por UF e grau de confiança (banco de 05/10/2026):

| Região | UF | Municípios | A | B | C |
| :--- | :--- | ---: | ---: | ---: | ---: |
| Centro-Oeste | DF | 1 | 1 | 0 | 0 |
| Centro-Oeste | GO | 24 | 24 | 0 | 0 |
| Centro-Oeste | MS | 6 | 6 | 0 | 0 |
| Centro-Oeste | MT | 13 | 9 | 4 | 0 |
| Nordeste | AL | 10 | 9 | 1 | 0 |
| Nordeste | BA | 41 | 41 | 0 | 0 |
| Nordeste | CE | 37 | 37 | 0 | 0 |
| Nordeste | MA | 22 | 22 | 0 | 0 |
| Nordeste | PB | 10 | 10 | 0 | 0 |
| Nordeste | PE | 33 | 33 | 0 | 0 |
| Nordeste | PI | 5 | 5 | 0 | 0 |
| Nordeste | RN | 8 | 8 | 0 | 0 |
| Nordeste | SE | 7 | 7 | 0 | 0 |
| Norte | AC | 2 | 2 | 0 | 0 |
| Norte | AM | 12 | 1 | 11 | 0 |
| Norte | AP | 2 | 2 | 0 | 0 |
| Norte | PA | 42 | 42 | 0 | 0 |
| Norte | RO | 7 | 6 | 1 | 0 |
| Norte | RR | 1 | 0 | 1 | 0 |
| Norte | TO | 5 | 0 | 0 | 5 |
| Sudeste | ES | 10 | 8 | 2 | 0 |
| Sudeste | MG | 71 | 59 | 12 | 0 |
| Sudeste | RJ | 37 | 19 | 18 | 0 |
| Sudeste | SP | 137 | 126 | 11 | 0 |
| Sul | PR | 34 | 34 | 0 | 0 |
| Sul | RS | 43 | 41 | 2 | 0 |
| Sul | SC | 32 | 32 | 0 | 0 |

Particularidades: os 5 municípios de grau C estão no Tocantins; o Amazonas e o Rio de Janeiro concentram os B (11 de 12 e 18 de 37). A CORSAN, a COMUSA e o DMAE de Porto Alegre cobram por fórmula exponencial (36 municípios, `regime_tarifario` = `exponencial`), representada por expoentes transcritos. O banco registra 185 denominações de prestador de saneamento; a SABESP atende 76 municípios, a COPASA 47 e a EMBASA 41.

**Por que o panorama e o banco diferem** (verificado cruzando o `catalogo_tarifas_auditado_652.xlsx`, corte de 24/08/2026, com o `brazil_cities_tariffs.json`, de 05/10/2026):

- O `confianca_grau` do banco acompanha o componente **saneamento**, e não o grau global do panorama (620 A / 32 B é o global; o saneamento era 586 A / 66 B em 24/08). Em 05/10 o saneamento é 584 A / 63 B / 5 C: 3 municípios subiram de B para A com os documentos transcritos depois do corte, e os 5 de Tocantins passaram de A (95 pontos) para C (55 pontos), porque a estrutura tarifária deles ficou «a conferir».
- Os **valores de energia são idênticos** nos dois (0 diferenças nos 652). Só mudou o rótulo: 66 municípios cuja resolução ANEEL terminava entre 26 e 28/08/2026 (fim de vigência posterior ao corte de 24/08) aparecem como `EXPIRED_ANEEL_REF` no banco; somados aos 74 já expirados em 24/08 (42 da Equatorial Pará, 30 da CELESC e 2 da Sulgipe), dão os 140.
- Vale o banco, que é o que o programa lê. O panorama é a fotografia de 24/08/2026; uma nota de atualização foi acrescentada ao topo dele.

O `tarifas/catalogo_tarifas_auditado_652.csv` traz só o cabeçalho (274 bytes, sem linhas); a versão completa do catálogo é o `.xlsx`. Regerar o CSV é tarefa pendente.

### Carregamento, atualização e reprodução

- O programa lê só `triton/data/brazil_cities_tariffs.json` (`triton/core/tariffs_database.py`); a pasta `tarifas/` acompanha a edição como procedência consultável.
- Atualização: ferramentas do mantenedor (fora do Git), descritas em `tarifas/README.md`: coleta e registro do documento (`processar_entrada.py`), transcrição (`transcricoes/<prestador>.json`, à mão, com o documento aberto), gravação com antes e depois (`aplicar_transcricoes.py --aplicar`) e energia ANEEL (`atualizar_tarifas.py --aneel-only`). Cada transcrição traz contas de conferência que os testes exigem reproduzidas ao centavo.
- Reprodução da auditoria: `scripts/audit_tariffs.py` sobre a cópia oficial da ANEEL.

## 5. Outros dados

| Conjunto | Fonte e licença | Observação |
| :--- | :--- | :--- |
| Fator de emissão da rede elétrica (`fatores_emissao_rede_mcti.json`) | MCTI/SIRENE, «Fatores de emissão de CO₂ para inventários corporativos» (https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao), arquivo `Inventario_2026_janjul.xlsx`, recuperado em 08/09/2026, SHA-256 `e447b0f5421425778b1d47dbf92d6eb44cd598cffbb3ed6cf73febe37c919ac2` (arquivado em `data/fontes_externas/`). Licença: a página (acesso em 24/10/2026) diz que todo o conteúdo do site está sob Creative Commons Atribuição-SemDerivações 3.0 (CC BY-ND 3.0), mas não afirma que isso vale para os arquivos de dados. A cópia do arquivo é fiel; a série extraída para o JSON pode contar como derivação. **Decisão do titular (25/10/2026): aprovado usar o JSON extraído**, por serem dados públicos; a atribuição devida é «Fonte: MCTI/SIRENE, Fatores de emissão de CO₂ para inventários corporativos (CC BY-ND 3.0 no site)». O MCTI não foi consultado; o arquivo original é copiado sem alteração. | Série de **CO₂ apenas**, não CO₂-equivalente; geração do SIN, sem perdas nem cadeia a montante. Declare o ano do fator (`docs/procedencia_fatores_co2.md`) |
| Custos de referência (`costs_database.json`) | Catálogo interno do projeto, 2026-08, em reais, regionalizado por UF; só vale quando o projeto liga os preços de catálogo | Substitua pelos preços do seu fornecedor |
| Rotas de produção de água (`rotas_producao_agua.json`) | Do projeto (`docs/rotas_de_producao_de_agua.md`) | O fator evitado por m³ depende da rota substituída |
| Resultados do Netuno 4 (`data/simulation_outputs/`) | Planilhas exportadas pelo Netuno 4 (referência de validação da replicação, duas planilhas que somam os 4.050 casos e três arquivos de teste do leitor). Licença de redistribuição não documentada em arquivo; **mantidas por decisão do titular**: «autorização dos criadores, registrada pelo titular em 25/10/2026» (não há documento anexo) | Servem à replicação (`docs/protocolo_netuno4.md`); o manual e as demais saídas do Netuno 4 não vão no repositório |
| Visualizador 3D (`triton/data/volumetria/`) | Céu «Quarry» do Poly Haven (CC0 1.0); three.js 0.186.1 (MIT) | `LICENCAS.md` na pasta |
| Exemplos, relatórios e figuras do manual | Geradas pelo projeto, sob a licença do Triton (`LICENSE.md`) | Os relatórios de exemplo são PDF gerados pelo programa |
| Logotipo CLIMBra (`icons/CLIMBra.*`) | Licença do logotipo não encontrada em fonte pública; **mantido por decisão do titular**: «autorização dos criadores, registrada pelo titular em 25/10/2026» (não há documento anexo); o CLIMBra em si é CC0 | Só nesta edição |

## 6. Limites de tamanho e verificação

- Limite: 50 MiB por arquivo rastreado. Maior arquivo da edição: 43,02 MiB (`climbra_KACE.db`). A edição rastreada soma 872,0 MiB: 785,1 MiB de clima e 86,8 MiB do resto, dos quais 53,3 MiB são o manual.
- Conferência: `python scripts/verificar_tamanhos.py` (da raiz do repositório) e `tests/unit/test_tamanho_dos_dados.py`.
- O repositório inteiro tem cerca de 976 MiB rastreados e o `.git`, 1,4 GB (as 19 partes respondem por 785 MiB). O plano de lançamento sem inflar o histórico (publicar as partes como *release assets* nas próximas versões e não regerá-las sem necessidade) não faz parte do repositório; é decisão do mantenedor.

## 7. Como atualizar sem estourar o limite

1. Dados novos de clima: regerar só o modelo que mudou (cada regeração soma ~41 MiB ao histórico) e atualizar o manifesto. Parte que passe de 50 MiB: dividir por cenário.
2. Tarifas: atualizar o JSON e as transcrições; texto e tabelas, ordem de KiB a poucos MiB por vez.
3. Antes de enviar: `python scripts/verificar_tamanhos.py`.

## 8. Citação

Cite o CLIMBra (Ballarin et al., 2023) ao usar a base climática, a fonte de cada tarifa (campo `fonte_url`) e o Triton (`CITATION.cff`).

## 9. Pendências conhecidas

- **Resolvido em 24/10/2026:** origem das séries `data/rainfall/` (CLIMBra, não INMET) corrigida no `bibliography.py`; artigo do CLIMBra confirmado como Scientific Data 10, art. 47 (Crossref, doi 10.1038/s41597-023-01956-z, 20/01/2023) e corrigido no `bibliography.py`, na aba de documentação e nos scripts de compilação.
- O metadado `source_article` **dentro das 19 partes** ainda diz «Nature Scientific Data, 10, art. 48». Corrigi-lo mudaria os 19 arquivos (e o histórico do Git ganharia outros ~785 MiB); fica para a próxima regeração, e os scripts já gravam 47. O `content_sha256` das séries não muda.
- Panorama tarifário: explicado acima e com nota de atualização; os números completos (global, por componente) não foram regerados (pendente).
- Decididas em 25/10/2026: planilhas do Netuno 4 e logotipo CLIMBra mantidos (autorização dos criadores, registrada pelo titular); ANEEL (ODbL) e MCTI (CC BY-ND) aprovados com atribuição. Seguem sem verificação os portais dos prestadores.
- `tarifas/transcricoes/.cobertura_cache.json` (cache gerado) saiu do controle de versão e entrou no `.gitignore`.

## 10. Estudos de caso de Santa Catarina (`estudos/santa-catarina/`, fora do repositório)

> Estes estudos são pesquisa própria do grupo e **não vão no repositório nem no instalador**; a descrição abaixo documenta como foram feitos. O programa traz apenas o mecanismo (`expansao`, `clima.climbra`, `tarifa`).

Seis estudos `triton-estudo` (escolar, comercial, residencial unifamiliar, residencial multifamiliar, hospitalar, aeroportuário), gerados por `scripts/gerar_estudos_sc.py`. O esquema ganhou, só na BRL, `clima.climbra` (município, UF, modelo, cenário e recorte da CLIMBra), `tarifa` (município e categoria do catálogo de tarifas) e `expansao` (município × modelo × recorte); ver apêndice F do manual.

- **Municípios.** A CLIMBra do programa tem 652 cidades e não traz UF nem código IBGE. O recorte de Santa Catarina cruza o nome com os 295 municípios do IBGE (API de localidades, código 42xxxxx) e confere a UF no catálogo de tarifas: **32 de 295** estão na CLIMBra; os outros 263 não têm série. Quatro nomes da CLIMBra coincidem com municípios de SC mas são de outras UFs (Ipirá, BA; Irati, PR; Praia Grande, SP; São Carlos, SP) e foram excluídos. Lista completa em `estudos/santa-catarina/_fontes/municipios_sc_climbra.json`.
- **Aeroportos.** Lista de aeródromos públicos da ANAC (dados abertos, atualizada em 15/10/2026): 21 em SC. Critério de «voos regulares»: ao menos um voo regular realizado (VRA 2025, ANAC) em cada um dos 12 meses de 2025. Atendem: Florianópolis (SBFL), Navegantes (SBNF), Joinville (SBJV), Chapecó (SBCH) e Jaguaruna (SBJA). Jaguaruna não tem série na CLIMBra e fica fora até o autor decidir como representar o clima; Correia Pinto (SNCP) teve voos em 5 meses e não entra. Fontes, URL, data de acesso (29/10/2026) e SHA-256 em `_fontes/FONTES.json`.
- **Clima.** Os 19 modelos da CLIMBra e os sete recortes de `RECORTES_SUGERIDOS`. A CLIMBra não tem série observada por município: o histórico é simulado e corrigido de viés (QDM) contra a grade de Xavier et al. (2016).
- **Edificação.** Arquétipos: estimativas, a refinar pelo autor; nenhum valor é medido nem de norma.
- **Tarifas e custos.** Os do catálogo e das estimativas preliminares do programa; categoria `publica` ou `comercial` quando o município tem tabela coletada, senão a residencial (com alerta no resultado).
