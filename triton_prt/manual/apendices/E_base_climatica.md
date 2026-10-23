# Base climática

> **A Edição Portugal traz a base E-OBS por concelho.** A precipitação diária de 278 concelhos do
> Continente vem no programa, em `data/portugal_eobs.db`. Os Açores e a Madeira não têm série na base:
> para eles, a série é sempre um ficheiro do utilizador (secção {{n:4}}). Um exemplo, o Funchal, vem com
> uma série de reanálise ERA5.

---

## O que a base contém

<!-- tabela: Conteúdo da base de precipitação por concelho da Edição Portugal -->
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

**Correção opcional.** A edição traz, em ficheiro separado, fatores mensais de correção do total, calibrados
com o Iberia01 em 1971–2000 (o período de referência que os autores recomendam) e **desligados por defeito**.
Ligá-los multiplica a chuva de cada mês pelo fator do concelho; o programa regista no projeto que a correção
foi usada. Os fatores derivam do Iberia01, que está sob a Open Database License, e por isso seguem sob a
mesma licença.

**Uso comercial.** A E-OBS é de uso estritamente não comercial em pesquisa e educação. No primeiro arranque o
programa pergunta o uso pretendido e o laudo repete a licença e a citação.

**Reprodutibilidade.** Cada projeto grava o identificador do pacote de chuva (`PT-EOBS-v33.0e-37fcba20`), a
versão da E-OBS e o SHA-256 do pacote, e por defeito leva a série dentro do ficheiro. Se reabrir um projeto
com um pacote diferente, o programa avisa e o laudo regista a mudança.

**Cobertura.** O ecrã inicial, o título da janela e o rodapé dos laudos mostram uma linha lida da base:
Portugal continental, 278 concelhos (A 45, B 159, C 74); Espanha: 0 locais. A grelha cobre a Península, mas a
edição só tem concelhos de Portugal por enquanto.

---

## A série que vem como ficheiro

Uma série diária acompanha o programa na pasta `data/rainfall`. É uma **reanálise**, e não um registo de
udómetro.

<!-- tabela: Série de precipitação distribuída com a Edição Portugal -->
| Ficheiro | Local | Período | Dias | Chuva média anual | Fonte |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `Funchal.csv` | Funchal (32,65° N, 16,90° O, célula de grelha a 323 m de altitude) | 01/01/1991 a 31/12/2020 | 10 958 | cerca de 538 mm | reanálise ERA5, via Open-Meteo |

O formato é um valor por linha: a precipitação diária em milímetros, sem data. A data do primeiro dia vem
do projeto (1 de janeiro de 1991 neste ficheiro).

**O que é.** A ERA5 é a reanálise global de quinta geração do Centro Europeu de Previsões Meteorológicas de
Médio Prazo (ECMWF), produzida pelo serviço Copernicus de alterações climáticas (Hersbach et al., 2020,
*Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049). A série foi extraída para uma
célula de grelha de cerca de 9 km, pela interface de arquivo da Open-Meteo.com (licença CC BY 4.0), em
14/10/2026. Uma célula é uma média de área: suaviza as chuvadas intensas e exagera o número de dias de
chuva fraca, e por isso é um ponto de partida, e não um substituto de um registo medido.

**Porque o Funchal usa a ERA5.** A E-OBS não serve ao Funchal (22% de dias sem dado em 1991-2020, acima do
limite de 1%). A média anual da reanálise pode diferir da média medida na estação. Num projeto real,
use a série medida.

**Os projetos de exemplo.** Lisboa e Porto usam a base E-OBS por concelho, e o ficheiro do projeto guarda a
referência da série e a impressão digital dos valores; por defeito a série vai dentro do ficheiro, com o identificador do pacote. O Funchal traz
a série ERA5 dentro do ficheiro.

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

A Edição Portugal não traz projeções de modelos climáticos. Para estudar um clima futuro, prepare a série
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
