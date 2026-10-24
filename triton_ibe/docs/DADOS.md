# Dados da Edição Ibérica (IBE): o que existe, de onde vem e quanto confiar

Versão 0.1.0, 24/10/2026. Este documento descreve cada conjunto de dados da edição: o que é, a fonte (URL e data), a licença, a cobertura, a resolução, o período, o tratamento de falhas, o nível de qualidade, o tamanho, como o programa o carrega e como o reproduzir. Todo o número vem de um ficheiro (citado); onde a informação não existe no repositório, o texto diz «não verificado».

Tamanhos em MiB (1 MiB = 1 048 576 bytes, a unidade do aviso de 50 MB do GitHub). **Regra do projeto: nenhum ficheiro rastreado passa de 50 MiB.** O script `scripts/verificar_tamanhos.py` (na raiz do repositório) falha se isso acontecer, e a verificação do GitHub corre-o a cada envio. O maior ficheiro de dados desta edição é `data/portugal_eobs.db`, com 5,74 MiB.

**Âmbito atual.** A edição chama-se IBE (Península Ibérica), mas esta versão só traz dados de **Portugal**: 278 concelhos do Continente com série de chuva observada (E-OBS); as ilhas só com série da estação; a Espanha foi ensaiada (capitais de província), mas **o programa traz 0 locais espanhóis** (`espanha_locais` = 0 nos metadados da base).

## 1. Visão geral

| Conjunto | Onde | Formato | Tamanho | No Git | Licença |
| :--- | :--- | :--- | ---: | :---: | :--- |
| Chuva diária por concelho (E-OBS v33.0e) | `data/portugal_eobs.db` | SQLite | 5,74 MiB | sim | E-OBS: só uso não comercial em investigação e educação (§2) |
| Série de exemplo do Funchal (reanálise ERA5) | `data/rainfall/Funchal.csv` | CSV, um valor diário por linha | 0,04 MiB | sim | CC BY 4.0 (Open-Meteo / Copernicus) |
| Tarifários transcritos (Lisboa, Porto, Funchal) | `triton/data/portugal_tarifarios.json` | JSON | 0,01 MiB | sim | valores públicos transcritos; ver §3 |
| Entidade gestora por concelho, confiança e procedência | `tarifas_portugal/entidades.json`, `CONFIANCA_POR_CONCELHO.csv/.md`, `FILA.md`, `fontes/FONTES.tsv` | JSON, CSV, Markdown, TSV | 0,75 MiB | sim | ERSAR: avisos legais (§3) |
| Documentos oficiais de terceiros (PDF, HTML, imagens) | `tarifas_portugal/fontes/<entidade>/` | PDF, HTML, JPG | 19 MB | **não** | de terceiros; não se redistribui |
| Banco que reúne esses documentos | `tarifas_portugal/tarifas_portugal_fontes.db` | SQLite | 16 MB | **não** | de terceiros |
| Fontes brutas E-OBS e CAOP | `data/portugal/fontes/` | NetCDF, GeoPackage | cerca de 3 GB | **não** | E-OBS (não comercial); CAOP (cc-by) |
| Fatores de emissão, custos, rotas de produção de água | `triton/data/*.json` | JSON | 0,02 MiB | sim | do projeto; sem valor local (§4) |
| Exemplos (Lisboa, Porto, Funchal) e relatórios de exemplo | `examples/`, `reports/exemplos/` | `.triton`, PDF | 0,15 MiB e 5,33 MiB | sim | do projeto |
| Visualizador 3D (HDR e JS) | `triton/data/volumetria/` | HDR, JS | 2,1 MiB | sim | CC0 (céu) e MIT (three.js) |
| Manual (PDF, sítio, figuras) | `manual/` | PDF, HTML, PNG | 41,6 MiB (445 ficheiros) | sim | do projeto |

Os dados de **tarifas** e de **pluviometria** estão em ficheiros separados entre si: a chuva em `data/`, as tarifas em `triton/data/` e `tarifas_portugal/`. Esta edição não leva a base CLIMBra (só a Edição Brasil).

## 2. Chuva por concelho (`data/portugal_eobs.db`)

| Campo | Valor |
| :--- | :--- |
| O que é | Precipitação diária (mm) de cada concelho do Continente, calculada a partir da grelha E-OBS: média diária das células com centro dentro do limite do concelho; sem centro dentro, a célula mais próxima do centroide |
| Fonte | E-OBS v33.0e, precipitação diária (RR), média do conjunto, grelha de 0,1° (ECA&D / Copernicus). https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php. Citação: Cornes, R. C. et al. (2018), J. Geophys. Res. Atmos. 123(17), 9391-9409, doi:10.1029/2017JD028200 |
| Limites dos concelhos | CAOP 2025, Direção-Geral do Território (Aviso n.º 3502/2026/2, DR 2.ª série n.º 34, de 18/02/2026) |
| Rastreio | `metadados`: `pacote_id` PT-EOBS-v33.0e-37fcba20, `sha256_pacote` 37fcba2091965e4235f3f69251b1dd483aff200f41e65f5914d4270f6992041d, `sha256_eobs` 053ada85a200880debfcea04b21f7e2b44830b29e101ec3579830124aaa8b58b e os SHA-256 dos quatro GeoPackage da CAOP. SHA-256 do ficheiro `portugal_eobs.db`: `1dd28da75c94c83195963ab020a2d721c1e66a0b4a950d6b31f8a6f2da993c8d` |
| Licença | **E-OBS e ECA&D: «strictly for use in non-commercial research and education projects only»**; os resultados científicos devem ser publicados em literatura aberta; citar Cornes et al. (2018) e o reconhecimento do UERRA, do Copernicus e do ECA&D (licença do produto E-OBS, https://ecds.ecmwf.int/licences/licence-to-use-E-OBS-products). **A licença não trata da redistribuição nem de produtos derivados**: risco baixo a moderado, não eliminado (nenhum pedido ao KNMI foi feito). CAOP 2025: cc-by no registo oficial da DGT em dados.gov.pt; o texto da licença na página da DGT não foi encontrado. Fonte: `LICENCAS_DOS_DADOS.md`, 23/10/2026 |
| Restrição no programa | No primeiro arranque o programa mostra o aviso da licença e pede o uso (investigação/educação ou comercial); a declaração fica registada nos laudos. Por defeito não bloqueia a E-OBS (`BLOQUEAR_E_OBS_EM_USO_COMERCIAL = False`, `triton/core/licenca_eobs.py`). Para uso comercial: carregar a série própria. O texto do aviso ainda precisa de revisão da UFSC |
| Cobertura | 278 concelhos do Continente (todos). **Não cobertos: 30**, as ilhas: 11 na Madeira (4 com 22% de dias sem dado em 1991–2020, 3 com 32%, 4 com 93%, contra o limite de 1%) e 19 nos Açores (fora do domínio da E-OBS, a oeste de 25° O) |
| Resolução | Grelha de 0,1° (cerca de 10 km). 71 concelhos têm uma só célula; 20 usam a célula mais próxima do centroide; 14 repetem a série de outro concelho (partilham a mesma célula) |
| Período | 01/01/1950 a 31/12/2025, 27 759 dias |
| Falhas | Dia sem dado em todas as células do concelho = falha. Critério de entrada: concelho com mais de 1% de dias sem dado em 1991–2020 fica fora. Nos 278 concelhos da base **não há nenhum dia em falta** (`falhas` = 0 em todas as séries) |
| Média anual | de 485 mm (menor valor, num concelho do distrito de Faro) a 1994 mm (maior, no distrito de Viana do Castelo); média dos concelhos 908 mm |
| Tamanho | 5,74 MiB (`series` 278, `nao_cobertos` 30, `qualidade` 278, `metadados` 18 linhas) |
| Carregamento | `triton/core/base_climatica_portugal.py`: `data/portugal_eobs.db` (ou o ficheiro indicado em `TRITON_PORTUGAL_DB`; no programa instalado, em `_internal/data/`); o instalador leva só esta base |
| Reprodução | `scripts/compilar_base_eobs_portugal.py` (ficheiros E-OBS e CAOP, cerca de 3 GB, fora do Git) gera a base; `scripts/acrescentar_qualidade_ao_banco.py` acrescenta a tabela `qualidade`. Ferramentas do mantenedor, descritas em `scripts/README.md` |

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

(O protótipo de validação, fora do repositório, deu A 68, B 111 e C 99 com um primeiro conjunto de limiares; vale a base do programa, a tabela acima.)

### Iberia01 e a correção de escala

O Iberia01 v1.0 (CSIC, DIGITAL.CSIC 10261/183071; Herrera et al., 2019, doi:10.20350/digitalCSIC/8641) só serve aqui de **referência de comparação** para o nível de qualidade. Licença: ODbL («Open Database License»; direitos sobre os conteúdos individuais sob a Database Contents License). Uma base derivada de uso público tem de ser oferecida também em ODbL. A correção de escala mensal opcional, calibrada com o Iberia01, **não faz parte desta versão** (não há código nem ficheiro dela no pacote); se vier a ser distribuída, os fatores irão num ficheiro separado em ODbL, desligada por defeito.

### Espanha

A Espanha está fora do pacote desta versão. Foram ensaiadas as 52 capitais de província (fora do repositório, `validacao_precipitacao_prt/qualidade_espanha_capitais.csv`): 39 em nível B, 9 em C e 4 sem série. O pacote por região para Espanha depende dos limites municipais do CNIG (compatível com CC-BY 4.0, confirmado em 23/10/2026) e de uma decisão sobre a licença da E-OBS para redistribuição.

### Ilhas

Madeira e Açores não entram pela grelha: só com a série da estação (decisão de 22/10/2026). O exemplo do Funchal usa reanálise (§ seguinte), por ser a única série de ilha distribuída.

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
- Os valores dos tarifários municipais são preços públicos regulados; a licença de reutilização dos sítios das entidades não foi verificada caso a caso.

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
- Eletricidade, só no Funchal: 0,1673 €/kWh (EEM, 6,90 kVA, sem IVA), de uma **fonte secundária** (comparador luzegas.pt, atualizada a 20/02/2025); a confirmar na EEM ou na ERSE.

### Atualização e reprodução

Ferramentas do mantenedor (fora do Git): `importar_ersar.py` (índice da ERSAR e `FONTES.tsv`), `procedencia_pt.py` (calcula `CONFIANCA_POR_CONCELHO`), `monitorar_tarifas.py` (vigia os URLs, uma vez por ano, sem agendamento). Passos em `tarifas_portugal/PROCEDENCIA_LEIA.md`. Teste: `TRITON_EDITION=IBE python -m pytest tests/unit/test_procedencia_tarifaria_pt.py`.

## 5. Outros dados

| Conjunto | Estado |
| :--- | :--- |
| Fator de emissão da rede elétrica (`fatores_emissao_rede_padrao.json`) | **Sem valor**: a edição não traz série oficial; o fator é 0 até o utilizador indicar o da rede do projeto. As fontes portuguesas e espanholas (APA, MITECO, REE) foram avaliadas e não estão incorporadas; APA e MITECO sem licença expressa, REE com reutilização não autorizada no aviso geral (`LICENCAS_DOS_DADOS.md`) |
| Custos de referência (`costs_database.json`) | Ficheiro do núcleo; esta edição não aplica preços de catálogo: custos de obra, bomba, tratamento e manutenção ficam a zero nos exemplos, para o utilizador indicar os seus |
| Rotas de produção de água (`rotas_producao_agua.json`) | Do projeto; o fator evitado por m³ depende da rota substituída e deve ser indicado pelo utilizador |
| Exemplos (`examples/portugal/*.triton`) e relatórios (`reports/exemplos/`) | Gerados pelo projeto; os resultados económicos dos exemplos **não são resultados** (custos a zero) |
| Visualizador 3D | Céu «Quarry» do Poly Haven (CC0 1.0) e three.js (MIT), em `triton/data/volumetria/LICENCAS.md` |

## 6. Limites de tamanho e verificação

- Limite: 50 MiB por ficheiro rastreado. Maior ficheiro de dados: 5,74 MiB. A edição rastreada soma 61,9 MiB, dos quais 41,6 MiB são o manual.
- Verificação: `python scripts/verificar_tamanhos.py` (da raiz) e `tests/unit/test_tamanho_dos_dados.py`.
- Atualização anual da chuva: acrescentar o ano novo à E-OBS, regenerar `portugal_eobs.db` e recalcular `qualidade`; a base continua muito abaixo do limite.

## 7. Atribuição a manter

- E-OBS: «We acknowledge the E-OBS dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and the Copernicus Climate Change Service, and the data providers in the ECA&D project (https://www.ecad.eu)». Cornes et al. (2018), doi:10.1029/2017JD028200.
- ERA5 / Open-Meteo: «Contains modified Copernicus Climate Change Service information»; Hersbach et al. (2020).
- ERSAR: «Fonte: ERSAR, www.ersar.pt. © ERSAR 2026. Todos os direitos reservados.»
- CAOP 2025: Direção-Geral do Território (cc-by).

## 8. Pendências conhecidas

- Licença da E-OBS para redistribuir a base derivada (omissa): decisão da UFSC e, se se quiser eliminar o risco, pergunta ao KNMI.
- Tabela `qualidade`: contém diferenças percentuais agregadas derivadas do Iberia01 (ODbL); não foi decidido se exige a ODbL.
- `data/rainfall/LEIA.md`, sobre os exemplos, ainda cita o Funchal como exemplo ERA5, enquanto a decisão para as ilhas é série da estação.
- Textos do manual e do aviso da E-OBS a rever antes da primeira distribuição.
