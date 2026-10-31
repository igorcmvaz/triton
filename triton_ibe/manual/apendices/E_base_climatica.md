# Base climática

> **Desde 30/10/2026 a fonte primária da Edição Ibérica é o Iberia01** (Península e Baleares, 8 319 municípios, 1971–2015, ODbL; Canárias, Madeira e Açores pela ERA5, nível C), em ficheiros separados do programa; ver `docs/DADOS.md` (§2A). O que se segue descreve a base E-OBS, que continua como fonte opcional e não comercial.
>
> **A Edição Ibérica traz duas bases de chuva.** O Iberia01 (fonte por defeito) vem em `data/chuva_iberia01_p1.db` a `p4.db`, com `data/ibe_unidades.db`, e a E-OBS opcional em `data/portugal_eobs.db`. Canárias, Madeira e Açores usam a ERA5 de 0,25° (`data/chuva_ilhas_era5.db`, nível C); Ceuta e Melilla ficam sem série, e a série é um ficheiro do utilizador (secção {{n:4}}). O exemplo do Funchal usa a ERA5 de ilha.

---

## O que a base contém

<!-- tabela: Conteúdo da base de precipitação por concelho da Edição Ibérica -->
| O que a base traz | Valor |
| :--- | :--- |
| fonte | E-OBS v33.0e, precipitação diária (RR), média do conjunto, grelha regular de 0,1° |
| período | 01/01/1950 a 31/12/2025 (27 759 dias) |
| concelhos com série | 278, todos no Continente, em 18 distritos |
| concelhos sem série | 30: os 19 dos Açores e os 11 da Madeira |
| limites dos concelhos | CAOP2025, Direção-Geral do Território (Aviso n.º 3502/2026/2, DR, 2.ª série, n.º 34, 18/02/2026) |
| formato | base SQLite (`portugal_eobs.db`), uma série comprimida por concelho |

**Como se obtém a série de um concelho.** É a média diária das células da grelha cujo centro cai dentro do
limite do concelho. Num concelho pequeno, sem nenhum centro de célula dentro do limite, usa-se a célula mais
próxima do centroide. Um dia sem dado em todas as células do concelho fica como falha (NaN), e a simulação
recusa a série, em vez de a tratar como dia seco. A grelha tem cerca de 10 km: a série de um concelho é uma
média de área, e suaviza as chuvadas intensas.

**Que concelhos ficam de fora, e porquê.** Os Açores situam-se a oeste de 25° W, fora do domínio da E-OBS.
Na Madeira, a E-OBS só tem a célula das estações que funcionavam em cada ano, e todos os concelhos faltam em
mais de 1% dos dias de 1991 a 2020 (o Funchal, em 22%). O critério da base é rejeitar o concelho com mais de
1% de dias sem dado nessa normal. Nenhum concelho recebe a série de um vizinho.

**Citação exigida pela fonte.** Cornes, R. C., van der Schrier, G., van den Besselaar, E. J. M., Jones, P. D.
(2018). An Ensemble Version of the E-OBS Temperature and Precipitation Data Sets. *Journal of Geophysical
Research: Atmospheres*, 123(17), 9391-9409. doi:10.1029/2017JD028200. Reconhecimento: *We acknowledge the E-OBS
dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and the Copernicus Climate Change Service, and the
data providers in the ECA&D project (https://www.ecad.eu).*

**Recortes.** A normal climatológica de 1991 a 2020 é o recorte inicial. O programa oferece ainda as normais
de 1981-2010, 1971-2000 e 1961-1990 e o período dos últimos trinta anos (1996-2025); as janelas de estudo
são recortes livres da série.

---

## Quanto confiar na série da E-OBS

Comparámos a E-OBS (versão 33.0e) com o Iberia01, uma grelha de 0,1° feita com uma rede de 3 486 estações
da Península (AEMET, IPMA e APA), entre 1971 e 2000, célula a célula e dia a dia. Resultado:

- Em Portugal, a E-OBS dá em média 8% menos chuva que o Iberia01 (nos 10% de células mais afastadas, até 18%
  menos). Na Espanha, entre 10% e 16% menos.
- Os extremos saem alisados: o percentil 95 dos dias de chuva fica cerca de 9% abaixo em Portugal, e o máximo
  diário anual, 14% abaixo. Isto tende a subestimar o extravasamento de um reservatório.
- O calendário dos dias é bom (correlação diária mediana de 0,86 em Portugal).

Em três estações do GHCN-Daily que a E-OBS não usa (Faro, Évora e Castelo Branco), a E-OBS deu 19% a 22%
menos chuva. São poucas estações, por isso este resultado é preliminar. O Iberia01 termina em 2015 e os seus
autores avisam que não serve para análise de tendência histórica; por isso este manual não afirma nenhuma
tendência de longo prazo da chuva.

**Nível de qualidade por concelho.** O programa mostra um nível, A, B ou C, e o motivo. O nível é o pior de
duas medidas. *Concordância com o Iberia01*: A se a diferença do total anual é de 10% ou menos e a do máximo
diário anual de 15% ou menos; B se são de 20% e 25% ou menos; C no resto. Falamos de «diferença para o
Iberia01», e não de «viés»: o Iberia01 é também uma grelha interpolada, não uma medição. *Geometria*: só
rebaixa até B, quando o concelho tem menos de três células, quando nenhuma célula tem o centro lá dentro ou
quando a série é igual à de outro concelho.

<!-- tabela: Concelhos de Portugal continental por nível de qualidade da chuva -->
| Nível | Concelhos | O que significa |
| :--- | ---: | :--- |
| A | 45 | três células ou mais e boa concordância com o Iberia01 |
| B | 159 | concordância razoável, ou poucas células |
| C | 74 | diferença grande para o Iberia01 |

Para 148 concelhos a geometria é o motivo de ficarem fora de A (menos de três células). O Algarve tem 15
dos 16 concelhos em C, e Braga, Vila Real e Santarém mais de metade. O nível não é uma nota de exatidão: diz
onde a base é mais frágil. Em C, valide com uma série local.

**E em Espanha?** A base ibérica traz 8 131 municípios de Espanha (8 041 pelo Iberia01, incluindo as 67 das Baleares; 88 das Canárias pela ERA5; Ceuta e Melilla sem série), com o limite municipal do Eurostat/GISCO (LAU 2023) e o código INE de cinco dígitos. O nível é geométrico (sem a E-OBS como referência): na Península e nas Baleares, A 321, B 7 719 e C 1; as ilhas são C. É a representação do município pela grelha, e não uma validação com pluviómetros. O ensaio que as 52 capitais de província tiveram antes desta base (feito fora do programa, com a E-OBS) já não vale como nível de nenhum município.

**Correção de escala: não incluída.** Estudou-se uma correção mensal do total, calibrada com o Iberia01 em
1971–2000 (o período de referência que os autores recomendam), mas **ela não faz parte desta versão**: o
pacote não traz nem o código nem o ficheiro dos fatores. Se vier a ser distribuída, os fatores irão num ficheiro
separado, sob a Open Database License do Iberia01, e ficará desligada por defeito. Até lá, nos concelhos de
nível C, valide a série com uma série local ou carregue a sua.

**Uso comercial.** O Iberia01 (ODbL) e a ERA5 (CC BY 4.0) permitem o uso comercial, com atribuição, que o rodapé do laudo leva (Herrera et al., 2019, doi:10.5194/essd-11-1947-2019). A E-OBS, opcional, é de uso estritamente não comercial em pesquisa e educação: só o projeto cuja fonte é a E-OBS mostra o aviso vermelho, e o laudo repete a licença e a citação.

**Reprodutibilidade.** Cada projeto grava o município (`Nome [código]`), a fonte e o SHA-256 da série; com a E-OBS, grava também o identificador do pacote (`PT-EOBS-v33.0e-37fcba20`), a
versão da E-OBS e o SHA-256 do pacote, e por defeito leva a série dentro do ficheiro. Se reabrir um projeto
com um pacote diferente, o programa avisa e o laudo regista a mudança.

**Cobertura.** O ecrã inicial, o título da janela e o rodapé dos laudos mostram uma linha lida da base: «Cobertura: Portugal 308 locais, Espanha 8131 locais; chuva Iberia01 8319, ERA5 (nível C) 118, sem série 2». Com a E-OBS escolhida, a linha é a da E-OBS (278 concelhos do Continente: A 45, B 159, C 74).

---

## A série que vem como ficheiro

Uma série diária acompanha o programa na pasta `data/rainfall`. É uma **reanálise**, e não um registo de
udómetro.

<!-- tabela: Série de precipitação distribuída com a Edição Ibérica -->
| Ficheiro | Local | Período | Dias | Chuva média anual | Fonte |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `Funchal.csv` | Funchal (32,65° N, 16,90° O, célula de grelha a 323 m de altitude) | 01/01/1991 a 31/12/2020 | 10 958 | cerca de 538 mm | reanálise ERA5, via Open-Meteo (série de exemplo da edição; o projeto de exemplo do Funchal usa a mesma ERA5 pela base das ilhas, 1986–2015, 531 mm) |

O formato é um valor por linha: a precipitação diária em milímetros, sem data. A data do primeiro dia vem
do projeto (1 de janeiro de 1991 neste ficheiro).

**O que é.** A ERA5 é a reanálise global de quinta geração do Centro Europeu de Previsões Meteorológicas de
Médio Prazo (ECMWF), produzida pelo serviço Copernicus de alterações climáticas (Hersbach et al., 2020,
*Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049). A série foi extraída para uma
célula de grelha de cerca de 9 km, pela interface de arquivo da Open-Meteo.com (licença CC BY 4.0), em
14/10/2026. Uma célula é uma média de área: suaviza as chuvadas intensas e exagera o número de dias de
chuva fraca, e por isso é um ponto de partida, e não um substituto de um registo medido.

**Porque o Funchal usa a ERA5.** O Funchal está fora do domínio do Iberia01, e a E-OBS não serve (22% de dias sem dado em 1991-2020, acima do
limite de 1%). A média anual da reanálise pode diferir da média medida na estação. Num projeto real,
use a série medida.

**Os projetos de exemplo.** Lisboa, Porto, Madrid e Palma usam o Iberia01 (normal 1986–2015), e o Funchal a ERA5 de ilha (nível C); em todos, o ficheiro do projeto guarda o município pelo código (`Lisboa [PT-1106]`), a referência da série e a impressão digital dos valores, e o programa recompõe a série da base ao abrir. Nenhum exemplo usa a E-OBS, e por isso nenhum leva o aviso vermelho de uso não comercial. Medido no mesmo período de 1991 a 2015, o Iberia01 dá 0,4% mais chuva do que a E-OBS em Lisboa e 2,4% mais no Porto; a normal 1991–2020 da E-OBS, que os exemplos usavam antes, dava 719 mm em Lisboa e 1 199 mm no Porto, contra 746 mm e 1 197 mm do Iberia01 em 1986–2015.

---

## Usar a sua própria série

1. Obtenha um registo diário, em milímetros, do serviço meteorológico ou do udómetro mais próximo do local.
   Anote a estação, a distância ao local, o período e a fonte.
2. Guarde-o num CSV com um valor por dia. Aceita-se o ponto ou a vírgula como separador decimal, e uma linha
   de cabeçalho é ignorada.
3. Abra-o na etapa 1 (Projeto e chuva) e indique a data do primeiro dia.

Um ano incompleto é descartado na leitura, para não enviesar os totais anuais. Exigem-se dados diários: as
médias mensais escondem os períodos secos que decidem o volume (secção {{n:33.2}}).

**Que extensão de série.** A extensão necessária para estabilizar o volume ideal não é uma constante
geográfica: cresce com a fração atendível e com a procura do edifício (glossário, apêndice {{n:G}}). A série
de cada concelho da base tem trinta anos na normal 1991-2020.

---

## Cenários futuros

A Edição Ibérica não traz projeções de modelos climáticos. Para estudar um clima futuro, prepare a série
diária projetada, a partir da fonte que escolher, e carregue-a como qualquer outro ficheiro. O fator de chuva
da modulação probabilística (secção {{n:40}}) permite testar uma série mais seca ou mais húmida por uma
percentagem declarada. A secção {{n:15}} trata da condução do estudo.

---

## O que declarar num estudo

- a **fonte** da série (E-OBS v33.0e, estação ou produto de reanálise) e a sua versão;
- o **local**: o concelho da base, ou, para um udómetro, a distância ao local;
- o **período**, com o primeiro e o último ano;
- se a série foi **corrigida, preenchida ou regionalizada**, e como;
- para uma projeção, o modelo, o cenário e a janela, e o método de correção do enviesamento;
- o número de **anos** de dados;
- a citação e o reconhecimento exigidos pela E-OBS, e, para a ERA5, a atribuição à Open-Meteo.


---

## Particularidades de região e país

A Edição Ibérica chama-se assim porque foi desenhada para a Península Ibérica: a chuva cobre **Portugal e Espanha**, e os tarifários de Portugal (três concelhos transcritos) e de Espanha (média regional do INE para todos os municípios; sete com tarifa transcrita ainda não conferida). Esta secção diz o que existe, o que falta e o que é próprio de cada país. Os números vêm de `docs/DADOS.md`, que descreve cada conjunto de dados com fonte, licença e tamanho.

<!-- tabela: Cobertura geográfica da Edição Ibérica nesta versão -->
| Território | Chuva no programa | Tarifário no programa |
| :--- | :--- | :--- |
| Portugal continental | 278 concelhos, Iberia01 de 1971 a 2015 (padrão 1986–2015), com nível de qualidade A, B ou C; a E-OBS é opcional | Lisboa e Porto transcritos; os restantes concelhos digitados pelo utilizador |
| Madeira (11 concelhos) | ERA5 de 0,25°, nível C, com aviso | Funchal transcrito |
| Açores (19 concelhos) | ERA5 de 0,25°, nível C, com aviso | nenhum transcrito (Ponta Delgada consta do registo de entidades) |
| Espanha | 8 131 municípios: 8 041 pelo Iberia01 (incluindo as Baleares), 88 das Canárias pela ERA5 (nível C); Ceuta e Melilla sem série | média regional do INE (indicativa); sete municípios com tarifa transcrita ainda não conferida |

**Portugal continental.** Os 278 concelhos têm uma série diária de chuva, calculada a partir da grelha do Iberia01 de 0,1° (cerca de 10 km) ou, em alternativa, da E-OBS; a série de um concelho é uma média de área e suaviza as chuvadas intensas. Cada concelho traz um nível de qualidade (A, B ou C), explicado na secção anterior e resumido abaixo.

**Ilhas.** A Madeira, os Açores e as Canárias não entram pela grelha do Iberia01 (nem a Madeira pela E-OBS: todos os concelhos faltam em mais de 1% dos dias de 1991 a 2020). Usam a reanálise ERA5 de 0,25°, sempre em nível C e com aviso no ecrã e nos laudos; para um projeto real, use a série da estação. O exemplo do Funchal mostra o caso.

**Espanha.** A chuva vem do Iberia01 por município (limites LAU 2023 do Eurostat/GISCO, código INE). Os custos de Espanha não existem, e as tarifas são a média regional do INE (camada 3, só indicativa) ou, em sete municípios (entre eles Madrid), uma tarifa transcrita de documento oficial, ainda não conferida: o laudo diz «Tarifa transcrita, ainda não conferida (segunda leitura pendente)». Os exemplos `examples/espanha/madrid.triton` e `palma.triton` mostram os dois casos.

**Licença da chuva.** O Iberia01 é ODbL (uso comercial permitido, com atribuição). A E-OBS e o ECA&D são de uso estritamente não comercial, em investigação e educação. A licença não trata da redistribuição nem de produtos derivados (nenhum pedido foi feito ao KNMI). No primeiro arranque o programa mostra o aviso e pede o uso pretendido; a declaração fica registada nos laudos. Por defeito, o programa não bloqueia a E-OBS em uso comercial. Num uso comercial, carregue a sua série. O texto do aviso ainda precisa de revisão pela UFSC.

**Níveis de qualidade da chuva.** O nível é o pior de duas medidas: a diferença entre a E-OBS e o Iberia01 (total anual e máximo diário anual, em 1971–2000) e a geometria da série (poucas células, método do centroide ou série repetida de outro concelho). Nos 278 concelhos, 45 são A, 159 são B e 74 são C. A diferença média do total anual, sobre os 278 concelhos, é de −10,1% (a E-OBS dá menos chuva; o −8% da secção anterior é a média célula a célula em Portugal): −3,1% em A, −7,1% em B e −20,7% em C. Os C concentram-se no distrito de Faro (15 dos 16 concelhos), em Santarém (11), Braga (10), Vila Real (8) e Porto (7). O nível não é uma nota de exatidão: diz onde a base é mais frágil, e em C convém validar com uma série local.

**Tarifários e entidades gestoras.** Em Portugal, a fatura soma três serviços, cada um com a sua entidade gestora e o seu tarifário: água, saneamento e resíduos urbanos. A ERSAR, a entidade reguladora, publica a ficha tarifária por concelho; o programa usa-a para indicar a entidade de cada serviço em 280 concelhos (os 278 do Continente, mais o Funchal e Ponta Delgada), com 316 entidades. Só Lisboa, Porto e Funchal têm o tarifário transcrito (vigência de 01/01/2026); nos restantes, o utilizador digita-o, e a ficha da ERSAR indica onde o procurar (apêndice {{n:D}}).

**Confiança tarifária.** Cada concelho e cada serviço tem um estado: verde (documento arquivado com endereço e SHA-256, reconfirmado há menos de 12 meses, transcrição conferida e verificação independente), amarelo (há documento, mas falta algum requisito do verde) ou cinzento (sem documento, entidade por identificar ou dado ruim). Em 23/10/2026: **0 verdes**, 42 amarelos e 238 cinzentos na água e no saneamento (nos resíduos, 11 amarelos e 269 cinzentos). Nenhum concelho é verde porque nenhuma verificação independente está registada, o que não quer dizer que os valores de Lisboa, Porto e Funchal estejam errados: foram conferidos à mão com as faturas impressas nos documentos.

**Normas e entidades de referência.** A norma europeia de referência é a EN 16941-1 (sistemas de água não potável no local), e em Portugal a especificação técnica ETA 0701 da ANQIP trata o aproveitamento de águas pluviais em edifícios; a secção {{n:1}} e a secção {{n:9}} dizem o que o manual verificou de cada uma. As referências a rever antes de citar estão marcadas nessas secções: a edição da EN 16941-1 em vigor e a sua transposição para a norma portuguesa, e a revisão em vigor da ETA 0701. O programa não avalia a conformidade com nenhuma delas.

**Moeda e IVA.** Os valores são em euros. A taxa de IVA depende do serviço e da entidade, e o programa trata-a em cada tarifário transcrito: no Funchal, o IVA de 4% não está confirmado, e em Lisboa o adicional da Câmara e o saneamento e os resíduos foram tratados sem IVA, como declara o tarifário.

**Fator de emissão da rede.** A edição não traz série oficial: o fator é zero até o utilizador indicar o da rede do projeto. As fontes portuguesas e espanholas avaliadas (APA, MITECO, REE) não estão incorporadas.

---

## Descrição dos dados e sua qualidade

Esta secção resume os dados que a edição traz. O inventário completo, com tamanhos, endereços das fontes, licenças e o modo de reproduzir cada item, está em `docs/DADOS.md` do repositório, e os números abaixo são os de lá. Nenhum ficheiro rastreado do repositório passa de 50 MiB; o maior ficheiro de dados é `data/chuva_iberia01_p1.db`, com 15,19 MiB.

<!-- tabela: Os conjuntos de dados da Edição Ibérica, a fonte e a licença -->
| Conjunto | O que é | Fonte e licença |
| :--- | :--- | :--- |
| Chuva por município (fonte por defeito) | quatro partes `chuva_iberia01_p1.db` a `p4.db` (13 a 15 MiB cada), `ibe_unidades.db` (3,3 MiB) e `chuva_ilhas_era5.db` (0,33 MiB): 6 523 células do Iberia01, de 01/01/1971 a 31/12/2015, e 41 nós ERA5 das ilhas | Iberia01 v1.0 (Herrera et al., 2019): ODbL 1.0, com atribuição; limites da CAOP 2025 (Portugal) e do Eurostat/GISCO LAU 2023 (Espanha); ERA5 (Copernicus, via Open-Meteo): CC BY 4.0 |
| Chuva por concelho (opcional) | base SQLite `portugal_eobs.db` (5,74 MiB): 278 séries diárias, de 01/01/1950 a 31/12/2025 (27 759 dias) | E-OBS v33.0e (ECA&D / Copernicus): só uso não comercial em investigação e educação; limites dos concelhos da CAOP 2025 (Direção-Geral do Território, cc-by) |
| Série de exemplo do Funchal | `data/rainfall/Funchal.csv` (0,04 MiB), 10 958 dias, de 01/01/1991 a 31/12/2020 | reanálise ERA5 via Open-Meteo; CC BY 4.0 |
| Tarifários transcritos | Lisboa, Porto e Funchal (`portugal_tarifarios.json`) | documentos oficiais das entidades, com endereço e SHA-256 registados |
| Entidade gestora, confiança e proveniência | 280 concelhos (`tarifas_portugal/`, 0,75 MiB) | índice da ERSAR (avisos legais: citar a fonte, sem licença aberta) |
| Fatores de emissão, custos e rotas de produção de água | ficheiros do núcleo (0,02 MiB) | do projeto; sem valor local |

**Chuva: o que a base é.** O pacote é identificado por `PT-EOBS-v33.0e-37fcba20`, com o SHA-256 da E-OBS, da CAOP e do próprio pacote nos metadados da base, e cada projeto grava esse identificador. Nos 278 concelhos da base não há nenhum dia em falta; o critério de entrada é rejeitar o concelho com mais de 1% de dias sem dado em 1991–2020. A média anual vai de 485 mm (num concelho do distrito de Faro) a 1994 mm (no distrito de Viana do Castelo), e a média dos concelhos é de 908 mm. Setenta e um concelhos têm uma só célula, 20 usam a célula mais próxima do centroide e 14 repetem a série de outro concelho.

**Chuva: o que a base não é.** A E-OBS é um produto interpolado, e não um registo de pluviómetro. Comparada com o Iberia01 (uma grelha feita com uma rede mais densa de estações) em 1971–2000, dá menos chuva e alisa os extremos; por isso o manual não afirma nenhuma tendência de longo prazo da chuva. O Iberia01 só serve aqui de referência para o nível de qualidade (licença ODbL; a tabela `qualidade` guarda diferenças percentuais agregadas derivadas dele, e ainda não está decidido se isso exige a ODbL). No Funchal, a reanálise ERA5 tem uma média anual de cerca de 538 mm, que pode diferir da medida na estação.

**Chuva do Iberia01.** A E-OBS dá em média 13,3% menos chuva do que o Iberia01 na Península (8% em Portugal) em 1971–2015, e o autor do Iberia01 recomenda 1971–2000 como referência e desaconselha a análise de tendências. O nível de qualidade do Iberia01 descreve a representação espacial do município pela grelha (A: três ou mais células; B: uma ou duas; C: célula emprestada ou ERA5), e não uma validação com pluviómetros.

**Tarifas: o que há.** O programa lê só o tarifário transcrito de Lisboa, Porto e Funchal. Os documentos oficiais em que ele se baseia (cada um com endereço de origem e SHA-256 em `tarifas_portugal/fontes/FONTES.tsv`, recolhidos em 07/10/2026) não se redistribuem: o Git leva só o registo e os valores transcritos. As pendências de cada tarifário estão em `examples/LEIA.md`; entre elas, o IVA do Funchal, a leitura por inferência da disponibilidade de água no Porto e a vigência de mais de 12 meses de Beja, Évora, Ponta Delgada e Bragança.

**Eletricidade.** Só o exemplo do Funchal traz tarifa: 0,1673 €/kWh (Empresa de Eletricidade da Madeira, sem IVA), de uma fonte secundária (um comparador de preços, atualizado em 20/02/2025), a confirmar na EEM ou na ERSE.

**Exemplos.** Os resultados económicos dos exemplos **não são resultados**: os custos de obra, bomba, tratamento e manutenção ficam a zero, porque nenhuma fonte oficial aberta foi usada para eles (secção {{n:10}}).

**O que declarar.** Ao usar a base, cite Cornes et al. (2018) e repita o reconhecimento exigido pela E-OBS; para a série do Funchal, a atribuição à Open-Meteo (CC BY 4.0) e a Hersbach et al. (2020); para os tarifários, a ERSAR («Fonte: ERSAR, www.ersar.pt. © ERSAR 2026. Todos os direitos reservados.») e a entidade do documento.

**Pendências conhecidas.** A licença da E-OBS para redistribuir a base derivada é omissa; por decisão do titular (25/10/2026), o uso comercial é bloqueado e avisado, e a tabela de qualidade, derivada do Iberia01 (ODbL), vai para um ficheiro separado sob a ODbL, com atribuição; os termos de reutilização dos sítios das entidades gestoras não foram encontrados (Águas e Energia do Porto) ou não foram verificados (as restantes); o texto do aviso da E-OBS e partes deste manual precisam de revisão antes da primeira distribuição. Estas pendências estão registadas em `docs/DADOS.md`.
