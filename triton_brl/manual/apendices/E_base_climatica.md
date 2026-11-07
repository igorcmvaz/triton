# Base climática

![Logotipo do conjunto de dados CLIMBra](../figuras/CLIMBra.jpg)

---

## O que a base contém

<!-- tabela: Conteúdo da base climática nacional -->
| O que a base traz | Quantidade |
| :--- | ---: |
| cidades brasileiras | 652 |
| modelos climáticos do CMIP6 | 19 |
| cenários de emissão | 2, SSP2-4.5 e SSP5-8.5 |
| simulações por cidade e modelo | 3: histórica, SSP2-4.5 e SSP5-8.5 |
| total de séries temporais | 37.164 séries |
| formato original descompactado | ~6,5 GB (CSVs) |
| formato compilado do Triton | 19 bancos SQLite comprimidos, um por modelo (`climbra_<modelo>.db`, 785,1 MiB no total) |

Cada série é um registro diário contínuo de precipitação, em milímetros, para uma combinação de
cidade, modelo e simulação: 652 cidades × 19 modelos × 3 simulações dão as 37.164
séries. As séries vêm do **CLIMBra** (Ballarin et al., 2023, [*Scientific Data / Nature*](https://www.nature.com/articles/s41597-023-01956-z), [doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z); repositório [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316), [doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)), corrigidas de viés por
*Quantile Delta Mapping* contra a grade diária de Xavier, King e Scanlon (2016), com
resolução de 0,25°. A histórica cobre de 1980 a 2013 (12.419 dias) e as futuras, de 2015 a 2100 (31.411 dias); as
janelas de estudo são recortes livres dessas séries. Todas estão em calendário
gregoriano. Os modelos HadGEM3-GC31-LL, KACE e UKESM1-0-LL, que usam originalmente anos
de 360 dias, têm um dia a menos no fim de cada série, o que não afeta o recorte.

---

## Embarque no executável e formato otimizado

Para evitar a manipulação morosa de dezenas de milhares de arquivos de texto e viabilizar
a distribuição direta no instalador e executável do Triton, as 37.164 séries foram
compiladas e indexadas em bancos de dados **SQLite de alta eficiência**, com compressão
binária por série via `zlib`. Há um banco por modelo (`climbra_<modelo>.db`, de 39,98 a
43,02 MiB cada, 785,1 MiB ao todo), de modo que nenhum arquivo versionado passa de 50 MiB.
O arquivo `data/climbra_partes.json` registra o SHA-256 de cada parte.

- **Velocidade de acesso:** O acesso indexado no banco leva **menos de 1 milissegundo** por série, contra dezenas de milissegundos na abertura e parse de arquivos CSV em disco.
- **Transparência:** O motor de dados climáticos do Triton prioriza as partes compiladas e recorre automaticamente à pasta de arquivos `.csv` soltos se elas não forem encontradas. O banco único antigo (`climbra.db`) ainda é lido, se existir, mas não acompanha o repositório.
- **Portabilidade:** Permite ao instalador do Triton fornecer a base nacional pronta para uso sem exigir download manual e descompactação de 6,5 GB pelo usuário.

---

## Os cenários

As duas trajetórias socioeconômicas compartilhadas do CMIP6 disponíveis na base, as *Shared Socioeconomic Pathways*, estão desenhadas na seção {{n:15}}: o SSP2-4.5 é a trajetória intermediária e o SSP5-8.5 supõe emissões altas sem mitigação. O CLIMBra não inclui cenários de mitigação forte, como o SSP1-2.6.


---

## As séries de exemplo que acompanham o programa

Doze séries de exemplo acompanham a instalação, na pasta `data/rainfall` do programa,
três para cada uma de quatro cidades. **Cada uma é um recorte do CLIMBra** (um município,
um modelo e um cenário), e não um registro de pluviômetro:

<!-- tabela: Séries de precipitação de exemplo distribuídas com o programa -->
| Cidade | Arquivos |
| :--- | ---: |
| Florianópolis | 3 |
| Brasília | 3 |
| Manaus | 3 |
| São Paulo | 3 |

Os sufixos 1, 2 e 3 não seguem uma regra única; o modelo e o cenário de cada arquivo estão
em `docs/DADOS.md`. A série de Florianópolis usada no tutorial (`Florianopolis1`) é do modelo
GFDL-CM4 no cenário SSP5-8.5 e tem 86 anos; os trinta primeiros somam 1.795 mm anuais médios,
com chuva em 46% dos dias. Como toda série modelada, ela serve de exemplo e de ponto de
partida: para um projeto real, use a série medida no local.

---

## O que declarar num estudo

- **modelo ou modelos**, pelo nome, e o critério de seleção;
- **cenário** SSP;
- **janela temporal**, com os anos;
- a **série histórica** usada como referência;
- se houve *downscaling* ou correção de viés, e qual;
- a **procedência e a versão** da base.

A seção {{n:15}} trata da condução do estudo com cenários futuros, e alerta para o erro de
escolher o modelo pelo resultado.


---

## Particularidades de região e país

A Edição Brasil é a única que traz dados do Brasil, e os traz de ponta a ponta: chuva, tarifas, fator de emissão da rede e normas. Esta seção reúne o que muda de uma região para outra e o que é próprio do país. Os números vêm de `docs/DADOS.md`, que descreve cada conjunto de dados com fonte, licença e tamanho.

**Recorte territorial.** O programa cobre 652 municípios, nas 27 unidades da federação (26 estados e o Distrito Federal) e nas cinco macrorregiões, entre eles todas as capitais. São os mesmos 652 na base climática e no banco tarifário (conferidos por nome normalizado). A cobertura acompanha a população, e não o território: São Paulo tem 137 municípios, o Distrito Federal e Roraima têm um cada.

**Clima.** A base é o CLIMBra (Ballarin et al., 2023), com 19 modelos do CMIP6, três simulações por modelo (histórica, SSP2-4.5 e SSP5-8.5) e uma série por município. A cobertura é completa nas cinco macrorregiões e nas 27 UF: todo município tem as 57 séries (19 modelos × 3 simulações). A grade original é de 0,25° (cerca de 28 km), de modo que a série de um município é uma média de área. São séries **modeladas**, com correção de viés, e não registros de pluviômetro: a seção {{n:15}} trata de como escolher modelo, cenário e janela.

**Tarifas por concessionária.** No Brasil, a tarifa de água e esgoto é do prestador (uma companhia estadual, um serviço municipal ou uma empresa privada), e não do município. O banco registra 185 denominações de prestador: a SABESP atende 76 dos 652 municípios, a COPASA 47 e a EMBASA 41. A CORSAN, a COMUSA e o DMAE de Porto Alegre cobram por fórmula exponencial (36 municípios), um dos seis regimes do apêndice {{n:D}}. A tarifa de energia da bomba é a residencial B1 da distribuidora de cada município, lida da base aberta da ANEEL, em R$/kWh **sem** ICMS, PIS/Pasep, Cofins, COSIP nem bandeiras tarifárias; para 140 municípios a referência está expirada (a distribuidora não tem ato vigente na base), e o banco guarda o último valor oficial e o marca.

**Confiança tarifária por região.** Cada município tem um grau de confiança, de A a D (apêndice {{n:D}}); o grau do banco acompanha o componente de saneamento. Em 05/10/2026:

<!-- tabela: Grau de confiança do componente de saneamento do banco tarifário, por macrorregião (banco de 05/10/2026) -->
| Região | Municípios | A | B | C |
| :--- | ---: | ---: | ---: | ---: |
| Centro-Oeste | 44 | 40 | 4 | 0 |
| Nordeste | 173 | 172 | 1 | 0 |
| Norte | 71 | 53 | 13 | 5 |
| Sudeste | 255 | 212 | 43 | 0 |
| Sul | 109 | 107 | 2 | 0 |
| **Brasil** | **652** | **584** | **63** | **5** |

Os cinco municípios de grau C estão no Tocantins, onde a estrutura tarifária ficou «a conferir»; o Amazonas e o Rio de Janeiro concentram os de grau B (11 de 12 e 18 de 37). A tabela por unidade da federação está em `docs/DADOS.md`. **Confira sempre o município do seu projeto**: o grau diz quanta evidência existe, e não que a tarifa esteja certa hoje.

**Normas brasileiras.** O programa segue a ABNT NBR 15527:2019 (aproveitamento de água de chuva) no que ela fixa: área de captação como projeção horizontal (item 3.6), volume disponível com o fator de captação (4.1.6), a lista de sete usos admitidos (4.1.7), o estudo exigido para qualquer outro uso (4.1.8), o descarte de 2 mm na falta de dado local (4.1.5) e os parâmetros mínimos de qualidade da Tabela 1 (*E. coli* abaixo de 200 por 100 mL, turbidez abaixo de 5,0 uT e pH de 6 a 9). As classes de qualidade 2 a 4 do programa são **adaptações do programa**, e não da NBR 15527. O arranjo cita também a NBR 5626 (separação atmosférica e bombas). A comparação com a norma europeia EN 16941-1:2024, item a item, está em `docs/normas_nbr_x_en16941.md`.

**Fator de emissão da rede.** O programa traz a série de CO₂ do SIN do MCTI/SIRENE (inventários de 2026): é só CO₂, e não CO₂-equivalente, e não inclui perdas nem a cadeia a montante. Declare o ano do fator (`docs/procedencia_fatores_co2.md`).

**Moeda e certificações.** Os custos são em reais. As certificações avaliadas incluem as brasileiras (AQUA-HQE e Selo Casa Azul + CAIXA), descritas na seção {{n:31}}.

---

## Descrição dos dados e sua qualidade

Esta seção resume os dados que a edição traz. O inventário completo, com tamanhos, endereços das fontes, licenças e o modo de reproduzir cada item, está em `docs/DADOS.md` do repositório, e os números abaixo são os de lá. Nenhum arquivo rastreado do repositório passa de 50 MiB; o maior é `data/climbra_KACE.db`, com 43,02 MiB.

<!-- tabela: Os conjuntos de dados da Edição Brasil, a fonte e a licença -->
| Conjunto | O que é | Fonte e licença |
| :--- | :--- | :--- |
| Base climática | 19 arquivos SQLite (`climbra_<modelo>.db`), 785,1 MiB no total, 37.164 séries diárias de precipitação | CLIMBra, Ballarin et al. (2023); CC0 1.0 |
| Séries dos exemplos | 12 arquivos CSV em `data/rainfall` (quatro cidades, três cada), 2,13 MiB | recortes do CLIMBra; CC0 1.0 |
| Banco tarifário | 652 municípios, faixas de água e esgoto, parcela fixa, regime, prestador, vigência, energia B1, grau de confiança (`brazil_cities_tariffs.json`, 5,37 MiB) | valores públicos dos prestadores, das agências e da ANEEL, transcritos; a base aberta da ANEEL declara a ODbL |
| Fator de emissão da rede | série de CO₂ do SIN (`fatores_emissao_rede_mcti.json`) | MCTI/SIRENE |
| Custos de referência | catálogo interno de 2026-08, em reais, por UF | do projeto; vale só se o projeto liga os preços de catálogo |
| Resultados do Netuno 4 | duas planilhas (4.050 casos), para validar a replicação | referência de validação; licença de redistribuição não documentada |

**Chuva: o que a base é e o que não é.** Cada série é contínua, sem dias faltantes, e o Triton não preenche falhas nem recalcula a qualidade: ela é a do artigo do CLIMBra. O único tratamento do Triton é a compactação (float16 e zlib), cuja diferença no balanço diário é de 0,000045%. A integridade das 19 partes é conferida por SHA-256 contra `data/climbra_partes.json`. O período é de 01/01/1980 a 31/12/2013 na simulação histórica (12.419 dias) e de 01/01/2015 a 31/12/2100 nas projeções (31.411 dias); três modelos (HadGEM3-GC31-LL, KACE e UKESM1-0-LL) têm um dia a menos.

**Tarifas: o que há e quanto confiar.** O banco guarda os números, e não os documentos: os PDF e páginas dos prestadores ficam no disco do mantenedor e não se redistribuem; cada registro traz o endereço da fonte e a vigência. As vigências do saneamento são de 2026 em 382 municípios, 2025 em 162 e 2024 em 63. A confiança (A a D) pesa 60% do saneamento e 40% da energia. Pelo critério de procedência, 299 municípios têm as quatro categorias documentadas, 161 só a residencial, 136 têm documento com mais de 12 meses (a renovar), 8 foram auditados sem documento guardado e 48 estão a confirmar. Nenhum valor é preenchido por vizinhança: o município sem documento próprio guarda a melhor referência e fica marcado.

**Os exemplos.** As doze séries de `data/rainfall` são recortes do CLIMBra, com modelo e cenário próprios (a do tutorial, `Florianopolis1`, é do modelo GFDL-CM4 no cenário SSP5-8.5), e não registros de pluviômetro. Servem de exemplo e de ponto de partida; para um projeto real, use a série medida no local.

**O que declarar.** Ao usar a base, cite o CLIMBra (Ballarin et al., 2023), a fonte da tarifa (campo `fonte_url` do município) e o Triton. O que declarar num estudo está no fim deste apêndice.

**Pendências conhecidas.** A licença de reutilização dos portais de cada prestador não foi verificada um a um; a base aberta da ANEEL declara a ODbL, e a decisão sobre o JSON derivado é do mantenedor; o fator do MCTI está sob CC BY-ND 3.0 no site, sem afirmação de que isso valha para os arquivos; a licença das planilhas do Netuno 4 e a do logotipo do CLIMBra não estão documentadas. Estas pendências estão registradas em `docs/DADOS.md`.
