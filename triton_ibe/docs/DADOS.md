# Dados da Edição Ibérica (IBE): o que existe, de onde vem e quanto confiar

Versão 0.1.0, 24/10/2026 (secções ibéricas atualizadas em 30/10/2026). Este documento descreve cada conjunto de dados da edição: o que é, a fonte (URL e data), a licença, a cobertura, a resolução, o período, o tratamento de falhas, o nível de qualidade, o tamanho, como o programa o carrega e como o reproduzir. Todo o número vem de um ficheiro (citado); onde a informação não existe no repositório, o texto diz «não verificado».

Tamanhos em MiB (1 MiB = 1 048 576 bytes, a unidade do aviso de 50 MB do GitHub). **Regra do projeto: nenhum ficheiro rastreado passa de 50 MiB.** O script `scripts/verificar_tamanhos.py` (na raiz do repositório) falha se isso acontecer, e a verificação do GitHub corre-o a cada envio. O maior ficheiro de dados desta edição é `data/chuva_iberia01_p1.db`, com 15,19 MiB (cada parte do Iberia01 tem menos de 43 MiB).

**Âmbito atual.** A edição cobre a **Península Ibérica e as ilhas**: 308 locais de Portugal (278 concelhos do Continente e os 30 da Madeira e dos Açores) e 8 131 municípios de Espanha (incluindo as Baleares, as Canárias, Ceuta e Melilla), cada um com a sua chave oficial (código INE de 5 dígitos, ou DTMN de 4). A chuva vem do **Iberia01** (Península e Baleares: 8 319 locais); Canárias, Madeira e Açores (118 locais) vêm da reanálise ERA5, sempre com **nível C** e aviso; Ceuta e Melilla ficam sem série (fora de todas as grelhas disponíveis). A E-OBS continua como fonte **opcional e não comercial**. Tarifas: Portugal com 3 concelhos transcritos; Espanha com a **média regional do INE para todos os municípios** (camada 3, só indicativa) e **7 municípios com tarifa transcrita ainda não conferida** (camada 1, 12,0 % da população de Espanha; ver §4A).

## 1. Visão geral

| Conjunto | Onde | Formato | Tamanho | No Git | Licença |
| :--- | :--- | :--- | ---: | :---: | :--- |
| **Chuva diária por célula do Iberia01 v1.0** (Península e Baleares; 6 523 células) | `data/chuva_iberia01_p1.db` a `p4.db` (manifesto `iberia01_partes.json`) | SQLite, 4 partes | 15,19 + 13,46 + 13,55 + 13,16 MiB | sim | **ODbL 1.0**, com atribuição (§2A) |
| Municípios, células e pesos, nível de qualidade A/B/C, metadados | `data/ibe_unidades.db` | SQLite | 3,32 MiB | sim | ODbL 1.0 (derivada do Iberia01), ficheiro à parte do programa |
| Chuva das ilhas fora do Iberia01 (41 nós ERA5 de 0,25°) | `data/chuva_ilhas_era5.db` | SQLite | 0,33 MiB | sim | CC BY 4.0 (Copernicus / Open-Meteo) |
| Tabela de qualidade da E-OBS (diferença E-OBS menos Iberia01) | `data/qualidade_eobs_odbl.db` | SQLite | 0,09 MiB | sim | ODbL 1.0 (decisão de 25/10/2026) |
| Chuva diária por concelho (E-OBS v33.0e), **opcional** | `data/portugal_eobs.db` | SQLite | 5,66 MiB | sim | E-OBS: só uso não comercial em investigação e educação (§2) |
| Tarifas de Espanha (média regional INE, camada 3; 7 municípios transcritos, camada 1) | `triton/data/espanha_tarifarios.json` e `espanha_tarifarios_fontes.tsv` | JSON e TSV | 0,05 e 0,01 MiB | sim | INE, reutilização com citação (§4A); tarifas: documentos oficiais de cada operador, citados com URL e SHA-256, não redistribuídos |
| Série de exemplo do Funchal (reanálise ERA5) | `data/rainfall/Funchal.csv` | CSV, um valor diário por linha | 0,04 MiB | sim | CC BY 4.0 (Open-Meteo / Copernicus) |
| Tarifários transcritos (Lisboa, Porto, Funchal) | `triton/data/portugal_tarifarios.json` | JSON | 0,01 MiB | sim | valores públicos transcritos; ver §3 |
| Entidade gestora por concelho, confiança e procedência | `tarifas_portugal/entidades.json`, `CONFIANCA_POR_CONCELHO.csv/.md`, `FILA.md`, `fontes/FONTES.tsv` | JSON, CSV, Markdown, TSV | 0,75 MiB | sim | ERSAR: avisos legais (§3) |
| Documentos oficiais de terceiros (PDF, HTML, imagens) | `tarifas_portugal/fontes/<entidade>/` | PDF, HTML, JPG | 19 MB | **não** | de terceiros; não se redistribui |
| Banco que reúne esses documentos | `tarifas_portugal/tarifas_portugal_fontes.db` | SQLite | 16 MB | **não** | de terceiros |
| Fontes brutas E-OBS e CAOP | `data/portugal/fontes/` | NetCDF, GeoPackage | cerca de 3 GB | **não** | E-OBS (não comercial); CAOP (cc-by) |
| Fatores de emissão, custos, rotas de produção de água | `triton/data/*.json` | JSON | 0,02 MiB | sim | do projeto; sem valor local (§4) |
| Exemplos (Lisboa, Porto, Funchal) e relatórios de exemplo | `examples/`, `reports/exemplos/` | `.triton`, PDF | 0,15 MiB e 5,33 MiB | sim | do projeto |
| Visualizador 3D (HDR e JS) | `triton/data/volumetria/` | HDR, JS | 2,1 MiB | sim | CC0 (céu) e MIT (three.js) |
| Manual (PDF, sítio, figuras) | `manual/` | PDF, HTML, PNG | 41,7 MiB (445 ficheiros) | sim | do projeto |

Os dados de **tarifas** e de **pluviometria** estão em ficheiros separados entre si: a chuva em `data/`, as tarifas em `triton/data/` e `tarifas_portugal/`. Esta edição não leva a base CLIMBra (só a Edição Brasil).

## 2A. Chuva do Iberia01 por município (fonte primária)

| Campo | Valor |
| :--- | :--- |
| O que é | Precipitação diária (mm) de cada município de Portugal continental, Espanha peninsular e Baleares, calculada na leitura como a média, ponderada, das células de 0,1° do Iberia01 que o servem |
| Fonte | Iberia01 v1.0, «Iberia010reg», Santander Meteorology Group (UC-CSIC), precipitação diária, grelha regular de 0,1° (79 × 137), 01/01/1971 a 31/12/2015 (16 436 dias), 6 523 células válidas, `kg m-2` (= mm/dia). Citação: Herrera, S., Cardoso, R. M., Soares, P. M. M., Espírito-Santo, F., Viterbo, P., Gutiérrez, J. M. (2019), *Earth System Science Data* 11, 1947-1956, doi:10.5194/essd-11-1947-2019; dados: doi:10.20350/digitalCSIC/8641. SHA-256 do ficheiro NetCDF de origem: `9c0393487f0d0e12accc0538681d02448f58ac123d08011d7ec7bfa008307022` (678,7 MiB, fora do Git) |
| Limites | Portugal: CAOP 2025, DGT (308 municípios, chave DTMN). Espanha: Eurostat/GISCO, Local Administrative Units 2023 (`LAU_RG_01M_2023_4326`, SHA-256 `c0636cb1010ea5e1c6b336c60a469af80d7919033ccfac35a4aa4bdddf100e29`), 8 131 municípios com o código INE de 5 dígitos. O pedido original apontava para o CNIG/IGN (CC BY 4.0), cujo centro de descargas não oferece ligação estável nem acesso por script: ver `auditoria/iberia/DECISOES_ASSUMIDAS.md` |
| Licença | **ODbL 1.0**: uso comercial permitido, com atribuição; a base derivada tem de ser distribuída também em ODbL e fica em ficheiros **separados do programa** (as quatro partes, `ibe_unidades.db` e `qualidade_eobs_odbl.db`). Relatórios e gráficos são «Produced Works»: pedem só a atribuição, que o rodapé do laudo leva: «Contains information from Iberia01, made available under the Open Database License (ODbL 1.0).» A licença foi confirmada no artigo da ESSD e nos metadados do ficheiro; a página do registo no DIGITAL.CSIC bloqueou o acesso automático (confirmar num navegador) |
| Método | Média das células com centro dentro do limite do município; sem nenhum centro dentro, a célula válida mais próxima do ponto representativo (até 0,25°), registada em `metodo`. Quantização em inteiros de 0,1 mm (planos de bytes + zlib); viés medido no total anual: −0,06% (amostra de 20 células). Dia sem dado seria NaN (falha), nunca zero; o Iberia01 não tem falhas nas células válidas |
| Células e partes | Quatro partes por faixa de longitude (1 631, 1 631, 1 631 e 1 630 células; 15,19 / 13,46 / 13,55 / 13,16 MiB). SHA-256 de cada parte no manifesto `iberia01_partes.json`. `pacote_id` `iberia01-v1.0-b214eb601c3d` (SHA-256 do conteúdo das células). O programa abre só as células de que precisa; uma parte em falta dá uma mensagem clara e não impede as outras |
| Cobertura | **Portugal 308 locais** (278 do Continente com o Iberia01 e 30 das ilhas com ERA5); **Espanha 8 131 locais** (8 041 pelo Iberia01, incluindo as 67 das Baleares; 88 das Canárias pela ERA5; Ceuta e Melilla sem série). Ao todo: Iberia01 8 319, ERA5 118, sem série 2. A linha de cobertura do ecrã e dos laudos é lida do banco |
| Período padrão | **1986–2015** (30 anos). A normal 1991–2020 deixa de existir nesta fonte; os atalhos de recorte são 1986–2015, 1971–2000 e a série completa 1971–2015. O autor do Iberia01 recomenda 1971–2000 como referência e desaconselha a análise de tendências (o número de estações varia no tempo) |
| Diferença para a E-OBS | A E-OBS dá em média 13,3% menos chuva que o Iberia01 (Península; Portugal −8,0%) em 1971–2015: os totais e as sobras da edição sobem de 8% a 16% em relação às versões que usavam a E-OBS |
| Carregamento | `triton/core/base_climatica_iberica.py` (pasta `data/` ou a indicada em `TRITON_IBERIA_DADOS`; no programa instalado, `_internal/data/`) |
| Reprodução | `python scripts/dados/compilar_base_iberia01.py` (Iberia01, CAOP, LAU: fora do Git) e `python scripts/dados/compilar_ilhas_era5.py` (Open-Meteo, com cache das respostas); o resultado é determinístico (o `pacote_id` repete-se) |

### Nível de qualidade A, B ou C (base ibérica)

Sem a E-OBS como referência, o nível descreve a **representação espacial** do município pela grelha, e não uma validação com pluviómetros: **A** = 3 ou mais células com centro dentro do município; **B** = 1 ou 2 células, ou município contido numa única célula de 0,1°; **C** = célula emprestada de fora do limite, ou reanálise ERA5. Resultado: Portugal continental A 140, B 138, C 0; Espanha peninsular e Baleares A 321, B 7 719, C 1; as 118 ilhas C. Está em `unidade.nivel` e `unidade.motivo` de `ibe_unidades.db`. Um município pequeno cai em B porque uma célula de ~100 km² não distingue o interior dele; a média dos 8 131 municípios de Espanha é de 62 km².

### Ilhas (ERA5, nível C)

Canárias (88 municípios), Madeira (11) e Açores (19) não estão no Iberia01. Usa-se a reanálise **ERA5** (Hersbach et al., 2020, doi:10.1002/qj.3803), soma diária de 00 a 24 UTC, grelha de 0,25° (41 nós), 1971–2015, via API de arquivo da Open-Meteo (dados CC BY 4.0; a API é gratuita para uso não comercial, e o script só é executado pelo mantenedor). O plano previa a ERA5-Land (0,1°), mas a Open-Meteo devolve precipitação nula para esse modelo (testado a 30/10/2026) e o Climate Data Store exige conta e chave. Cada município usa o nó mais próximo do seu ponto representativo. **Nível C fixo**: nos testes do projeto a ERA5 subestimou a chuva das estações de ilha de 8% a 47%. O aviso aparece no ecrã e no rodapé dos laudos; para um projeto real, use a série da estação (importar CSV). Exemplo: Funchal, 531 mm/ano em 1986–2015.

## 2. Chuva por concelho da E-OBS, opcional (`data/portugal_eobs.db`)

| Campo | Valor |
| :--- | :--- |
| O que é | Precipitação diária (mm) de cada concelho do Continente, calculada a partir da grelha E-OBS: média diária das células com centro dentro do limite do concelho; sem centro dentro, a célula mais próxima do centroide |
| Fonte | E-OBS v33.0e, precipitação diária (RR), média do conjunto, grelha de 0,1° (ECA&D / Copernicus). https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php. Citação: Cornes, R. C. et al. (2018), J. Geophys. Res. Atmos. 123(17), 9391-9409, doi:10.1029/2017JD028200 |
| Limites dos concelhos | CAOP 2025, Direção-Geral do Território (Aviso n.º 3502/2026/2, DR 2.ª série n.º 34, de 18/02/2026) |
| Rastreio | `metadados`: `pacote_id` PT-EOBS-v33.0e-37fcba20, `sha256_pacote` 37fcba2091965e4235f3f69251b1dd483aff200f41e65f5914d4270f6992041d, `sha256_eobs` 053ada85a200880debfcea04b21f7e2b44830b29e101ec3579830124aaa8b58b e os SHA-256 dos quatro GeoPackage da CAOP. SHA-256 do ficheiro `portugal_eobs.db`: `1dd28da75c94c83195963ab020a2d721c1e66a0b4a950d6b31f8a6f2da993c8d` |
| Licença | **E-OBS e ECA&D: «strictly for use in non-commercial research and education projects only»**; os resultados científicos devem ser publicados em literatura aberta; citar Cornes et al. (2018) e o reconhecimento do UERRA, do Copernicus e do ECA&D (licença do produto E-OBS, https://ecds.ecmwf.int/licences/licence-to-use-E-OBS-products). **A licença não trata da redistribuição nem de produtos derivados**: risco baixo a moderado, não eliminado (nenhum pedido ao KNMI foi feito). CAOP 2025: cc-by no registo oficial da DGT em dados.gov.pt; o texto da licença na página da DGT não foi encontrado. Fonte: `scripts/dados/resultados/LICENCAS_DOS_DADOS.md`, 23/10/2026 |
| Restrição no programa | **Só vale para projetos cuja fonte é a E-OBS**; o Iberia01 não bloqueia. No primeiro arranque o programa mostra o aviso da licença e pede o uso (investigação/educação ou comercial); a declaração fica registada nos laudos. Por defeito não bloqueia a E-OBS (`BLOQUEAR_E_OBS_EM_USO_COMERCIAL = False`, `triton/core/licenca_eobs.py`). Para uso comercial: carregar a série própria. O texto do aviso ainda precisa de revisão da UFSC |
| Cobertura | 278 concelhos do Continente (todos). **Não cobertos: 30**, as ilhas: 11 na Madeira (4 com 22% de dias sem dado em 1991–2020, 3 com 32%, 4 com 93%, contra o limite de 1%) e 19 nos Açores (fora do domínio da E-OBS, a oeste de 25° O) |
| Resolução | Grelha de 0,1° (cerca de 10 km). 71 concelhos têm uma só célula; 20 usam a célula mais próxima do centroide; 14 repetem a série de outro concelho (partilham a mesma célula) |
| Período | 01/01/1950 a 31/12/2025, 27 759 dias |
| Falhas | Dia sem dado em todas as células do concelho = falha. Critério de entrada: concelho com mais de 1% de dias sem dado em 1991–2020 fica fora. Nos 278 concelhos da base **não há nenhum dia em falta** (`falhas` = 0 em todas as séries) |
| Média anual | de 485 mm (menor valor, num concelho do distrito de Faro) a 1994 mm (maior, no distrito de Viana do Castelo); média dos concelhos 908 mm |
| Tamanho | 5,66 MiB (`series` 278, `nao_cobertos` 30, `metadados` 14 linhas; a tabela `qualidade` passou para `qualidade_eobs_odbl.db`). SHA-256 do ficheiro: `4aed46dfe4d4c020ff3396a39fcfafa59e70c91aa5a289756af659b578fa26ba` (o do conteúdo das séries, `sha256_pacote`, não mudou) |
| Carregamento | `triton/core/base_climatica_portugal.py`: `data/portugal_eobs.db` (ou o ficheiro indicado em `TRITON_PORTUGAL_DB`; no programa instalado, em `_internal/data/`); o instalador leva só esta base |
| Reprodução | No Git: `scripts/dados/compilar_base_eobs_portugal.py` (ficheiros E-OBS e CAOP, cerca de 3 GB, fora do Git) gera a base e `scripts/acrescentar_qualidade_ao_banco.py` acrescenta a tabela `qualidade`; os passos, as variáveis de ambiente e a conferência estão em `scripts/dados/LEIA.md`. **Reproduzido em 24/10/2026**: com a E-OBS v33.0e e a CAOP 2025 originais, os dois passos dão um ficheiro com o mesmo SHA-256 (`1dd28da7…3c8`) que o do repositório, com 278 séries, 30 não cobertos e A 45, B 159, C 74 (Python 3.13, numpy, xarray, geopandas, shapely) |

### Nível de qualidade A, B ou C

Fórmula única, em `triton/core/qualidade_chuva.py` (o banco, o programa e o manual leem os mesmos limiares). Mede-se a **diferença entre a E-OBS e o Iberia01** nas células do concelho, em 1971–2000: `dtot` no total anual e `drx` no máximo diário anual (E-OBS menos Iberia01). Não é viés contra a verdade: o Iberia01 também tem erro.

- Concordância: A se |dtot| ≤ 10% e |drx| ≤ 15%; B se |dtot| ≤ 20% e |drx| ≤ 25%; C nos restantes casos.
- Geometria: B se menos de 3 células efetivas, ou método «centroide», ou série repetida de outro concelho; A nos restantes. A geometria só desce até B.
- Nível = o pior dos dois. Os limiares são convenção (debate de 23/10/2026), não resultado de um ajuste.

Resultado nos 278 concelhos: **A 45, B 159, C 74**. A diferença média do total anual é −10,1% (a E-OBS dá menos chuva do que o Iberia01); por nível, −3,1% (A), −7,1% (B) e −20,7% (C); a dos extremos, −9,7%, −13,4% e −30,3%. Os C concentram-se no distrito de Faro (15 de 16 concelhos), em Santarém (11), Braga (10), Vila Real (8) e Porto (7) e correspondem a subestimação, sobretudo dos extremos: usar com cautela ou carregar série própria.

| Distrito | Concelhos | A | B | C | Média anual (mm), mín.–máx. |
| :--- | ---: | ---: | ---: | ---: | :--- |
| Aveiro | 19 | 1 | 17 | 1 | 993–1552 |
| Beja | 14 | 6 | 5 | 3 | 500–564 |
| Braga | 14 | 1 | 3 | 10 | 1275–1716 |
| Bragança | 12 | 1 | 7 | 4 | 569–879 |
| Castelo Branco | 11 | 0 | 7 | 4 | 632–993 |
| Coimbra | 17 | 2 | 13 | 2 | 900–1118 |
| Évora | 14 | 4 | 10 | 0 | 497–625 |
| Faro | 16 | 0 | 1 | 15 | 485–579 |
| Guarda | 14 | 6 | 7 | 1 | 616–1419 |
| Leiria | 16 | 1 | 11 | 4 | 715–1172 |
| Lisboa | 16 | 2 | 14 | 0 | 673–748 |
| Portalegre | 15 | 9 | 6 | 0 | 521–719 |
| Porto | 18 | 0 | 11 | 7 | 1177–1395 |
| Santarém | 21 | 2 | 8 | 11 | 619–848 |
| Setúbal | 13 | 3 | 10 | 0 | 576–701 |
| Viana do Castelo | 10 | 2 | 6 | 2 | 1620–1994 |
| Vila Real | 14 | 0 | 6 | 8 | 734–1450 |
| Viseu | 24 | 5 | 17 | 2 | 778–1531 |
| **Continente** | **278** | **45** | **159** | **74** | 485–1994 |

(A coluna `nivel` de `tests/dados_ibe/qualidade_prototipo.csv` vem de um primeiro conjunto de limiares, que dava A 68, B 111 e C 99; não vale. Vale o nível que o programa calcula com `triton/core/qualidade_chuva.py` sobre as diferenças `dtot` e `drx` desse ficheiro, a tabela acima.)

### Iberia01 e a E-OBS

A tabela de qualidade da E-OBS (A 45, B 159, C 74 nos 278 concelhos, com base na diferença E-OBS menos Iberia01 em 1971–2000) mora agora em `data/qualidade_eobs_odbl.db`, ficheiro à parte sob ODbL com atribuição ao Iberia01 (decisão de 25/10/2026), e só se mostra quando a fonte escolhida é a E-OBS. A correção de escala mensal opcional **não faz parte desta versão**. A diferença media 13,3% entre os dois produtos, nas células comuns.

## 3. Série de exemplo do Funchal (`data/rainfall/Funchal.csv`)

| Campo | Valor |
| :--- | :--- |
| O que é | Precipitação diária (mm) numa célula da reanálise ERA5, 32,65° N, 16,90° O, grelha a 323 m de altitude |
| Fonte | Open-Meteo, API de arquivo (`archive-api.open-meteo.com`), obtida em 14/10/2026; baseada na reanálise ERA5 do ECMWF (Hersbach et al., 2020, Q. J. R. Meteorol. Soc. 146, 1999-2049) |
| Licença | CC BY 4.0 (termos do Open-Meteo, https://open-meteo.com/en/terms; ERA5 sob CC-BY-4.0 no catálogo do CDS, conferido em 23/10/2026). Exige atribuição |
| Período, resolução | 01/01/1991 a 31/12/2020, 10 958 dias; célula de cerca de 9 km |
| Falhas | Sem falhas (nenhum valor em falta; máximo diário 74,6 mm) |
| Qualidade | Reanálise, não registo de estação; a média anual (cerca de 538 mm) pode diferir da média medida no Funchal. É um exemplo e um ponto de partida; para um projeto real, use a série medida |
| Porquê | A E-OBS não cobre o Funchal (22% de dias sem dado, acima do limite de 1%) |
| Tamanho, carregamento | 0,04 MiB; lido como qualquer série CSV de `data/rainfall/` (`triton/core/parser.py`) |

## 4. Tarifários de água, saneamento e resíduos

### O que existe

| Ficheiro | Conteúdo |
| :--- | :--- |
| `triton/data/portugal_tarifarios.json` | O que o programa lê: tarifários transcritos de **Lisboa, Porto e Funchal** (água, saneamento, parcelas), com entidade, vigência, fontes e o bloco `procedencia` (serviços transcritos, documentos com URL e SHA-256, conferência, pendências com o efeito estimado na fatura) |
| `tarifas_portugal/entidades.json` | Os 280 concelhos (278 do Continente, mais Funchal e Ponta Delgada), 316 entidades, por serviço (água, saneamento, resíduos), com a ficha tarifária ERSAR mais recente |
| `tarifas_portugal/CONFIANCA_POR_CONCELHO.csv/.md` | Estado de cada concelho e serviço, vigência, o que falta, URL do documento |
| `tarifas_portugal/fontes/FONTES.tsv` | Registo de cada documento: caminho, URL de origem, SHA-256, data de recolha (07/10/2026), entidade, concelhos, vigência, `redistribuivel` (0 em todos) |
| `tarifas_portugal/FILA.md` | Resultado do monitor de alterações dos URLs |

### Fontes e licença

- **Documentos tarifários** (tarifários e editais de EPAL, Câmara Municipal de Lisboa, Águas e Energia do Porto, Câmara Municipal do Funchal e outras entidades): cada um com URL de origem e SHA-256 em `FONTES.tsv` e em `examples/LEIA.md`. São documentos de terceiros, **não se redistribuem** (ficam no disco do mantenedor); o Git leva o registo.
- **Entidade gestora por concelho**: índice «Pesquisa por concelho» da ERSAR (https://www.ersar.pt/docs/pesquisa-tarifa-concelho/tarifa-concelho.json), 2 331 registos de 2024 a 2026, 278 concelhos continentais; acedido em 23/10/2026, SHA-256 `20057b868191dda9f465d7652d3f80eb05cd490a8430d532a232c1f98a701fad`.
- **Licença ERSAR** (avisos legais, https://www.ersar.pt/pt_avisos-legais.html): os materiais podem ser copiados ou distribuídos com a referência ao documento original em www.ersar.pt e o aviso «© ERSAR AAAA. Todos os direitos reservados». **Não é licença aberta**; obras derivadas não são tratadas. Os ficheiros derivados citam a ERSAR.
- Os valores dos tarifários municipais são preços públicos regulados. Termos de reutilização dos sítios das entidades (consulta de 24/10/2026): **Águas e Energia do Porto** (https://www.aguasdoporto.pt/): o rodapé só traz a linha «© Águas e Energia do Porto, EM 2014 - 2026» e ligações de privacidade e cookies; não se encontrou aviso legal nem termos de reutilização, logo nada autoriza nem proíbe expressamente a reprodução. **EPAL**: a página de aviso legal tentada devolveu 404. **Câmara Municipal de Lisboa, Câmara Municipal do Funchal e restantes entidades:** não verificado nesta versão (os termos de reutilização dos seus sítios não foram lidos). Por isso os documentos não são redistribuídos e o Git leva só os valores transcritos, o URL e o SHA-256.

### Cobertura e período

Três concelhos com tarifário transcrito (Lisboa, Porto, Funchal), vigência 01/01/2026. Para os restantes concelhos o programa **não traz tarifário**: o utilizador digita-o, e a ficha da ERSAR indica onde o procurar.

### Nível de qualidade

Três estados, por concelho **e por serviço**, só para o utilizador doméstico (regra em `triton/core/tarifarios_portugal.py::avaliar_servico`): verde (documento arquivado com URL e SHA-256, reconfirmado há menos de 12 meses, transcrição conferida, verificação independente registada); amarelo (há documento arquivado ou transcrito, mas falta algum requisito do verde); cinzento (sem documento, entidade por identificar ou dado ruim). Estado em 23/10/2026:

| Estado | Concelhos | Água | Saneamento | Resíduos |
| :--- | ---: | ---: | ---: | ---: |
| Verde, verificado | 0 | 0 | 0 | 0 |
| Amarelo, a validar | 42 | 42 | 42 | 11 |
| Cinzento, sem dado | 238 | 238 | 238 | 269 |
| **Total** | **280** | **280** | **280** | **280** |

**Nenhum concelho é verde**: não existe nenhuma verificação independente registada (`verificado_por` vazio). Isto não quer dizer que os valores de Lisboa, Porto e Funchal estejam errados: foram conferidos à mão com as faturas impressas nos documentos (ver `examples/LEIA.md`); falta a segunda verificação.

| Distrito | Amarelo | Cinzento | Total |
| :--- | ---: | ---: | ---: |
| Aveiro | 10 | 9 | 19 |
| Beja | 1 | 13 | 14 |
| Braga | 1 | 13 | 14 |
| Bragança | 3 | 9 | 12 |
| Castelo Branco | 1 | 10 | 11 |
| Coimbra | 1 | 16 | 17 |
| Évora | 1 | 13 | 14 |
| Faro | 1 | 15 | 16 |
| Guarda | 1 | 13 | 14 |
| Leiria | 1 | 15 | 16 |
| Lisboa | 1 | 15 | 16 |
| Portalegre | 1 | 14 | 15 |
| Porto | 1 | 17 | 18 |
| Região Autónoma da Madeira (Funchal) | 1 | 0 | 1 |
| Região Autónoma dos Açores (Ponta Delgada) | 1 | 0 | 1 |
| Santarém | 1 | 20 | 21 |
| Setúbal | 1 | 12 | 13 |
| Viana do Castelo | 7 | 3 | 10 |
| Vila Real | 6 | 8 | 14 |
| Viseu | 1 | 23 | 24 |

Particularidades e pendências (`tarifas_portugal/PROCEDENCIA_LEIA.md`, `examples/LEIA.md`):

- Funchal: o IVA de 4% **não está confirmado**; o 1.º escalão do saneamento e dos resíduos não tem valor impresso (tratado como zero); a TRH não vem impressa.
- Porto: a disponibilidade de água do utilizador doméstico foi lida por inferência do layout; a TRH das águas residuais não foi incluída.
- Lisboa: o «Adicional C.M. Lisboa» foi tratado sem IVA; saneamento e resíduos sem IVA, como declara o tarifário.
- Vigência com mais de 12 meses: Beja, Évora, Ponta Delgada e Bragança (2021).
- Eletricidade, só no Funchal: 0,1673 €/kWh (EEM, 6,90 kVA, sem IVA). **Fonte secundária, estado amarelo:** vem do comparador luzegas.pt (atualizada a 20/02/2025), não de um documento primário da EEM ou da ERSE, e é mais antiga do que o resto do exemplo. Não foi verificada na EEM nem na ERSE. O valor está no exemplo `funchal.triton` e no manual (rotulado como fonte secundária); para um projeto real, introduza a tarifa do seu contrato.

### Atualização e reprodução

Ferramentas (no Git, em `tarifas_portugal/`): `importar_ersar.py` (índice da ERSAR e `FONTES.tsv`), `procedencia_pt.py` (calcula `CONFIANCA_POR_CONCELHO`), `monitorar_tarifas.py` (vigia os URLs, uma vez por ano, sem agendamento). Os documentos de terceiros que elas lêem (`tarifas_portugal/fontes/<entidade>/`) não estão no Git. Passos em `tarifas_portugal/PROCEDENCIA_LEIA.md`. Teste: `TRITON_EDITION=IBE python -m pytest tests/unit/test_procedencia_tarifaria_pt.py`.

## 4A. Tarifas de Espanha (camadas)

Não existe conjunto aberto nacional de tarifas de água por município em Espanha (verificado no plano de 29/10/2026). O programa usa três camadas, no mesmo padrão de confiança que Portugal (`triton/core/tarifarios_espanha.py`, dados em `triton/data/espanha_tarifarios.json`):

| Camada | O que é | Municípios hoje | Aviso no programa |
| :--- | :--- | ---: | :--- |
| 1. Transcrita | tarifário do município, de documento oficial arquivado (URL, data de acesso e SHA-256), com conta de conferência | **7** (12,0 % da população) | «Tarifa transcrita, ainda não conferida (segunda leitura pendente)», com a fonte e a vigência; no ecrã e nos laudos |
| 2. Herdada | município sem documento próprio que herda o da entidade (`herda_de`) | **0** | «tarifa de outro município da mesma entidade; confirme na sua fatura» |
| 3. Média regional | média do INE por comunidade autónoma, um preço total por m³ (água e saneamento juntos), sem parte fixa | **8 124** (os restantes; Ceuta e Melilla com o valor conjunto do INE, 1,46, embora sem série de chuva) | «média regional de 2024; não é a tarifa do município; use só para ordem de grandeza» |

Fonte da camada 3: INE, *Encuesta sobre el suministro y saneamiento del agua* 2024, nota de imprensa de 02/07/2026 (https://ine.es/dyngs/Prensa/ESSA2024.htm, acedida a 30/10/2026, SHA-256 do documento `9412ca7fa82ba9dc55a8d744f6c626ef17b07cb7686d268b816b4d76022e21a6`). Os valores foram lidos dos dados do gráfico da própria página: média nacional 2,02 €/m³; La Rioja 1,26; Asturias 1,27; Castilla y León e Galicia 1,29; Ceuta e Melilla 1,46; Cantabria 1,53; Navarra 1,56; Castilla-La Mancha 1,62; Aragón 1,69; Extremadura 1,71; Madrid 1,74; Andalucía 1,86; Canarias 2,27; País Vasco 2,32; Murcia 2,60; Comunitat Valenciana 2,63; Cataluña 2,72; Illes Balears 2,80. O rodapé da página indica CC BY-SA 4.0 e a ligação aponta para CC BY 4.0: **confirmar qual vale**. A camada 3 pode errar por fatores de 2 entre municípios da mesma comunidade. FACUA, OCU e AEAS-AGA não foram usados (direitos reservados). Município sem camada 1, 2 ou 3 fica «sem tarifa» e o utilizador digita a tarifa; **nenhum valor foi inventado**.

**Camada 1 (integrada em 30/10/2026).** Sete municípios, com os valores tal como foram transcritos, sem alteração: Madrid 28079 (Canal de Isabel II), Sevilla 41091 (EMASESA), Murcia 30030 (EMUASA), A Coruña 15030 (EMALCSA), Las Palmas de Gran Canaria 35016 (EMALSA), Gijón 33024 (EMA) e Valladolid 47186 (Agua de Valladolid). Somam 5 881 477 habitantes, 12,0 % dos 49 114 494 de Espanha (INE, tabela 29005, 1/1/2025). Cada registo traz a fonte, o URL, a data de acesso (30/10/2026), o SHA-256 de cada documento, a vigência, as conversões feitas (bimestral e trimestral para mensal; EUR/dia para EUR/mês; 3 habitantes nos blocos por habitante de Sevilla e do canon da Galiza) e `conferido: false`. O arquivo `espanha_tarifarios_fontes.tsv` lista os documentos e o seu SHA-256 está em `arquivo_de_fontes` do JSON (verificado pelos testes).

**IVA nulo.** Onde o documento não indica a taxa, `iva_pct` é `null` e `iva_observacao` explica porquê (Valladolid: água e saneamento; A Coruña: saneamento e o canon da Galiza; Las Palmas: o IGIC do saneamento). O leitor trata `null` como 0 % no cálculo (a conta não leva uma taxa suposta, logo fica subestimada) e o ecrã, os laudos e os estudos avisam «IVA do saneamento não consta da fonte» (ou da água, ou das parcelas adicionais).

**Limitações.** Nenhum dos 7 registos teve a segunda leitura humana; Las Palmas (tabelas lidas em imagem) e A Coruña pedem mais atenção. Faltam o canon ESAMUR e a taxa de resíduos de Murcia, o canon de mejora de Sevilla, a tasa de basuras em todos e as cuotas de conservação em Gijón. Vigência incerta: Valladolid (tabelas rotuladas 2018), Gijón (exercício de 2025), Madrid (PDF «Tarifas 2026» sem data de início). Madrid usa a tarifa de inverno (a de verão está em `extra`). Um só operador por município. Os documentos de Málaga, Córdoba, Alicante e Granada foram arquivados mas **não** transcritos.

**Municípios sem tarifa transcrita.** Todos os outros 8 124 usam a média regional (camada 3) com o aviso de média regional. Tentados e não obtidos (rede ou ambiguidade): Barcelona/AMB, València, Zaragoza, Palma, Bilbao, Vitoria-Gasteiz, Vigo, Santa Cruz de Tenerife, Pamplona, Santander, Logroño, Badajoz, Córdoba (falta o saneamento de 2025), Málaga, Alicante e Granada. Portugal manteve os 3 concelhos transcritos: completar mais exige os documentos de cada entidade gestora (lista em `tarifas_portugal/entidades.json`) e a segunda leitura humana que leva ao estado verde.

## 5. Outros dados

| Conjunto | Estado |
| :--- | :--- |
| Fator de emissão da rede elétrica (`fatores_emissao_rede_padrao.json`) | **Sem valor**: a edição não traz série oficial; o fator é 0 até o utilizador indicar o da rede do projeto. As fontes portuguesas e espanholas (APA, MITECO, REE) foram avaliadas e não estão incorporadas; APA e MITECO sem licença expressa, REE com reutilização não autorizada no aviso geral (`scripts/dados/resultados/LICENCAS_DOS_DADOS.md`) |
| Custos de referência (`costs_database.json`) | Ficheiro do núcleo, neutro nesta edição (preços a zero, sem moeda nem fatores regionais); não há preços de catálogo: custos de obra, bomba, tratamento e manutenção ficam a zero nos exemplos, para o utilizador indicar os seus |
| Rotas de produção de água (`rotas_producao_agua.json`) | Do projeto; o fator evitado por m³ depende da rota substituída e deve ser indicado pelo utilizador |
| Exemplos (`examples/portugal/*.triton`) e relatórios (`reports/exemplos/`) | Gerados pelo projeto; os resultados económicos dos exemplos **não são resultados** (custos a zero) |
| Visualizador 3D | Céu «Quarry» do Poly Haven (CC0 1.0) e three.js (MIT), em `triton/data/volumetria/LICENCAS.md` |

## 6. Limites de tamanho e verificação

- Limite: 50 MiB por ficheiro rastreado. Maior ficheiro de dados: 15,19 MiB. Dados ibéricos novos: 59,9 MiB em oito ficheiros (`tests/unit/test_dados_iberia_ibe.py` confere tamanhos e SHA-256 contra o manifesto).
- Verificação: `python scripts/verificar_tamanhos.py` (da raiz) e `tests/unit/test_tamanho_dos_dados.py`.
- Atualização da chuva: o Iberia01 v1.0 acaba em 2015 (não há versão posterior encontrada); a extensão 2016–2025 só existe na E-OBS (não comercial) e não se mistura com o Iberia01 sem correção de homogeneidade (0.2.0).

## 7. Atribuição a manter

- E-OBS: «We acknowledge the E-OBS dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and the Copernicus Climate Change Service, and the data providers in the ECA&D project (https://www.ecad.eu)». Cornes et al. (2018), doi:10.1029/2017JD028200.
- Iberia01: «Contains information from Iberia01, made available under the Open Database License (ODbL 1.0).» Herrera et al. (2019), doi:10.5194/essd-11-1947-2019.
- ERA5 / Open-Meteo: «Contains modified Copernicus Climate Change Service information»; Hersbach et al. (2020).
- Limites de Espanha: Eurostat/GISCO, Local Administrative Units 2023 (© EuroGeographics para os limites administrativos); INE (códigos e população).
- INE, *Encuesta sobre el suministro y saneamiento del agua*, 2024.
- ERSAR: «Fonte: ERSAR, www.ersar.pt. © ERSAR 2026. Todos os direitos reservados.»
- CAOP 2025: Direção-Geral do Território (cc-by).

## 8. Pendências conhecidas

- Licença da E-OBS para redistribuir a base derivada (omissa): uso comercial bloqueado e avisado por decisão do titular (§9.1); a pergunta ao KNMI continua opcional.
- Tabela `qualidade`: separada em 30/10/2026 (`data/qualidade_eobs_odbl.db`, ODbL; §9.2).
- Confirmar a ODbL no registo do DIGITAL.CSIC com um navegador; confirmar a licença do rodapé do INE (CC BY-SA ou CC BY); confirmar os termos de uso do LAU do Eurostat; perguntas à ACA (tarifas da Catalunha) e à AEMET.
- Camada 1 de Espanha: segunda leitura humana dos 7 registos e mais municípios; mais concelhos de Portugal: transcrição manual (§4A).
- Ilhas: a ERA5 é mais grosseira que a ERA5-Land prevista; correção por estação fica para a 0.2.0.
- `data/rainfall/LEIA.md`, sobre os exemplos, ainda cita o Funchal como exemplo ERA5, enquanto a decisão para as ilhas é série da estação.
- Textos do manual e do aviso da E-OBS a rever antes da primeira distribuição.
- Termos de reutilização dos sítios das entidades dos tarifários: ver §4 (Porto sem termos encontrados; as restantes não verificadas).
- Decisões do titular sobre a E-OBS e a ODbL: ver §9 (decididas em 25/10/2026).

## 9. Decisões do titular (25/10/2026)

O titular dos direitos do software (UFSC/GPAS) decidiu as duas questões que estavam pendentes. Princípio: segurança jurídica, com avisos de «não pode ser usado comercialmente» onde houver dúvida.

### 9.1 E-OBS: uso comercial bloqueado e avisado

- **Facto.** A licença do produto E-OBS (https://ecds.ecmwf.int/licences/licence-to-use-E-OBS-products) permite o uso «strictly for use in non-commercial research and education projects only». **Não trata da redistribuição nem de produtos derivados.** Nenhum pedido foi feito ao KNMI.
- **Decisão.** (a) O uso comercial da chuva E-OBS fica **bloqueado** no programa (`BLOQUEAR_E_OBS_EM_USO_COMERCIAL` passa a `True`: quem declara uso comercial só pode carregar a série própria). (b) Os relatórios indicam, **em vermelho e em tamanho grande, que a chuva E-OBS não pode ser usada comercialmente**, possivelmente como marca de água. (c) Quem usar a base assume o uso não comercial; o titular não responde por uso comercial.
- **Estado da implementação.** A decisão é do titular; a mudança no código (constante, aviso vermelho nos relatórios, marca de água) é feita à parte e é conferida pelos testes da edição. Até lá, vale o aviso do primeiro arranque descrito na §2.
- **Não decidido:** perguntar ao KNMI/ECA&D se a redistribuição da base derivada é permitida (continua sendo uma opção para eliminar o risco).

### 9.2 Tabela `qualidade` e a ODbL do Iberia01

- **Facto.** A tabela `qualidade` guarda, por concelho, diferenças percentuais agregadas (`dtot`, `drx`) entre a E-OBS e o Iberia01 em 1971–2000. O Iberia01 v1.0 está sob a Open Database License (ODbL), segundo o mantenedor; **a licença não pôde ser confirmada em linha** (o repositório DIGITAL.CSIC bloqueou o pedido automático).
- **Decisão.** A tabela `qualidade` (derivada do Iberia01) passa para um **ficheiro separado, sob a ODbL, com atribuição** ao Iberia01 (Herrera et al., 2019, doi:10.20350/digitalCSIC/8641): «Contains information from Iberia01, made available under the Open Database License». O banco de séries `portugal_eobs.db` fica sem ela.
- **Estado da implementação (30/10/2026).** Feito: `scripts/separar_qualidade_odbl.py` moveu a tabela para `data/qualidade_eobs_odbl.db`, com a licença, a citação e o aviso nos metadados; `portugal_eobs.db` ficou só com as séries.

### 9.3 Outros registos de 25/10/2026

- **Repositório:** privado nesta fase; o README não promete ligação pública.
- **DOI do Zenodo:** ainda não criado. **Data de lançamento:** a definir pelo titular.
- **Eletricidade do Funchal:** fonte secundária, estado amarelo (§4); mantida e rotulada.
