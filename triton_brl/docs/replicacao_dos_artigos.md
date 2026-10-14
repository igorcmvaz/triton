# O que dá para replicar dos artigos do grupo com o Triton

Levantamento de 21/09/2026 sobre os 67 artigos de
`Material_Referencia/Documentos_Consultados/07_Nossos_Artigos`. Cinquenta e três
deles citam o Triton — nas versões Neptune, 2.0, 3.0 e 4 —, o que faz desta pasta
o melhor conjunto de verificação externa que o programa tem: são casos publicados,
com parâmetros declarados, produzidos pelo próprio motor que o Triton substitui.

Este documento responde a três perguntas: **o que dá para replicar hoje**, **o que
muda de premissa entre os artigos e o programa** e **o que vale trazer para o
programa ou para o manual**.

Duas replicações foram executadas para não deixar a resposta no plano da opinião;
os scripts estão em `scripts/replicacao/` e os resultados, ao lado deles.

---

## 1. Três níveis de replicabilidade

### Nível A — replicação integral, com os dados em mãos

**O estudo climático nacional.** *Projected Climate Change Impacts on Rainwater
Harvesting in Brazilian Single-Family Houses* (Water, 2026, doi
10.3390/w18070792) simulou 652 cidades com chuva diária da base CLIMBra,
dezenove modelos do CMIP6 e dois cenários de emissão. Essa base está no disco, em
`climbra_data` (anteriormente `Triton future files for 652 cities`), no formato
`(Triton)Cidade_Modelo_Cenário.csv` — 61.940 arquivos, exatamente o conjunto do
artigo. O arquétipo está publicado: 60 m² de cobertura, quatro moradores, 150
L/pessoa·dia, 30% de uso não potável, coeficiente de escoamento 0,80, descarte de
2 mm e quatro pares de reservatórios de mercado (cisterna de 310, 500, 1.000 e
2.000 L, com caixa superior de 150, 250, 500 e 1.000 L).

`scripts/replicacao/cenarios_climaticos.py` roda esse desenho em quatro capitais,
com os dezenove modelos, no cenário S2:

| Cidade | Histórico | SSP2-4.5 distante | SSP5-8.5 distante | Extravasamento (hist. → SSP5-8.5 distante) |
| :--- | ---: | ---: | ---: | ---: |
| Florianópolis | 14,46% | +0,36 p.p. | +0,65 p.p. | 38,7 → 54,6 m³/ano |
| Manaus | 15,10% | −0,75 p.p. | −2,04 p.p. | 54,7 → 58,9 m³/ano |
| Fortaleza | 7,42% | +0,16 p.p. | +0,11 p.p. | 20,8 → 27,4 m³/ano |
| Brasília | 10,40% | −0,45 p.p. | −0,78 p.p. | 36,2 → 44,8 m³/ano |

O resultado reproduz o sentido do artigo: queda no Norte e no Centro-Oeste, maior
sob SSP5-8.5 e no futuro distante; no Sul, potencial estável ou em alta, com a
maior divergência entre modelos (13,45% a 17,39% em Florianópolis) e aumento
claro do extravasamento.

**A replicação nacional, aliás, já existe.** Está em
`Estudos/replicacao_projected`, com os quatro cenários de reservatório
consolidados por cidade, modelo e cenário. Comparando-a com o motor do Triton,
modelo a modelo, aparece uma diferença de cerca de 2,7 pontos percentuais — e ela
é inteiramente explicada pelo tratamento do descarte, que é a diferença de método
declarada na seção de comparação com o Netuno 4 do manual: o Netuno 4 usa a
lâmina como **limiar do evento** (abaixo dela não capta nada, acima capta a chuva
inteira), e o Triton **subtrai** a lâmina de todo dia de chuva.

Emulando a regra de limiar, e incluindo a caixa superior do cenário, os dois
programas passam a concordar:

| Cidade · modelo (histórico) | Rodada nacional | Triton, subtraindo 2 mm | Triton, com a regra do Netuno 4 |
| :--- | ---: | ---: | ---: |
| Florianópolis · ACCESS-CM2 | 17,46% | 14,26% | 17,35% |
| Manaus · ACCESS-CM2 | 17,64% | 14,98% | 17,58% |
| Brasília · MIROC6 | 12,15% | 10,40% | 12,15% |
| Fortaleza · MIROC6 | 8,74% | 7,24% | 8,78% |

O erro máximo nos oito pares conferidos é de 0,11 ponto percentual, e sem viés de
sinal — indistinguível de arredondamento. Duas observações ficam do exercício: a
concordância é melhor com coeficiente de escoamento de 0,85 do que com os 0,80
declarados no texto do artigo (com 0,80 o Triton fica sistematicamente 0,1 a
0,3 ponto abaixo), e a diferença de descarte, que o manual mede em 1,36 ponto na
média dos casos de referência, chega a 2,7 pontos neste arquétipo — cobertura
pequena, cisterna pequena e chuva frequente, que é onde a regra do descarte mais
pesa.

**Os estudos de comprimento de série.** Três artigos do grupo — Geraldi e Ghisi
(2017, 2018, 2019) — perguntam quantos anos de chuva são necessários para que a
simulação responda como responderia com trinta. O método é autocontido: extrair
subséries de uma série longa, simular cada uma e contar a frequência de
resultados semelhantes.

`scripts/replicacao/comprimento_de_serie.py` refaz o método com os parâmetros do
artigo de 2018 (100 m², descarte de 2 mm, quatro moradores, 150 L/pessoa·dia,
coeficiente 0,80, caixa superior de 600 L) sobre as quatro séries de trinta anos
que acompanham o programa:

| Fração atendível | Florianópolis | São Paulo | Brasília | Manaus |
| :--- | ---: | ---: | ---: | ---: |
| 20% | 2 anos | 8 anos | 9 anos | 16 anos |
| 30% | 8 anos | 18 anos | 14 anos | 20 anos |
| 40% | 9 anos | 9 anos | 20 anos | 30 anos |
| 50% | 24 anos | 25 anos | 29 anos | 30 anos |

O artigo encontrou comprimentos representativos de 6 a 20 anos em treze cidades,
com 15 anos bastando em sete delas. A ordem de grandeza é a mesma, e a replicação
acrescenta um achado que o artigo não isola: **a série necessária cresce com a
fração atendível**. Quanto maior a demanda que se quer cobrir, mais a cisterna
depende de anos secos raros, e mais longa precisa ser a série.

### Nível B — replicação parcial: mesma cidade, outra chuva

A maior parte dos estudos de caso do grupo usa séries do INMET ou da ANA para uma
cidade específica, e **essas séries não acompanham os artigos**. Sem elas não há
replicação valor a valor. O que dá para fazer é comparação de ordem de grandeza,
com a série da mesma cidade que o programa distribui ou que a base CLIMBra traz.

São comparáveis assim, entre outros: Custódio e Ghisi (2019), com 18,5% a 40,8%
em Joinville; Ghisi e Ferreira (2007), em edifício multifamiliar de Florianópolis;
os estudos de escola, hospital e comércio; e os casos de escritório e de
edificação universitária. Ao comparar, a diferença de fonte de chuva tem de ser
declarada: é a primeira explicação de qualquer divergência.

### Nível C — fora do alcance do programa hoje

| Tema | Artigos | Por que não replica |
| :--- | :--- | :--- |
| Escoamento superficial e bacia | *Impact of residential rainwater harvesting on stormwater runoff* (2022) | Usa HEC-HMS com curva-número e tempo de concentração por sub-bacia; o Triton não faz propagação em bacia |
| Águas cinzas | seis artigos, de 2006 a 2024 | O programa não tem módulo de águas cinzas nem de sistema híbrido |
| Pavimento e captação em piso | oito artigos, de 2018 a 2026 | A captação é em pavimento, com camadas e infiltração; o Triton capta em cobertura |
| ACV modular por estágios | *Modular life cycle assessment approach* (2023) | A ACV do Triton é de triagem, com fatores agregados, e não por módulos A1–A5/B/C |
| Fachadas e andaimes | *Harvesting rainwater from scaffolding platforms and walls* (2020) | Área de captação vertical, com coeficiente e exposição próprios |

---

## 2. Diferenças de premissa que precisam ser declaradas

Ao comparar qualquer número do programa com qualquer número dos artigos, estas
cinco diferenças explicam quase toda a divergência:

1. **Critério de volume ideal.** Os artigos do grupo usam limiares de ganho
   marginal diferentes entre si: 0,5 %/m³ (pavimento permeável, 2020), 1 %/m³
   (ACV modular, 2023) e 2 %/m³ por 1.000 L (indicadores, 2022). O programa abre
   com 5 %/m³ e o tutorial adota 1 %/m³. O volume ideal não é propriedade do
   projeto; é propriedade do critério, e o manual já diz isso na seção do volume
   ideal.
2. **Grade de varredura.** Os artigos varrem de 1.000 a 70.000 L, com passo de
   1.000 L até 10.000 L e de 5.000 L acima. O Triton varre com passo fixo, e o
   padrão da interface vai a 10.000 L. Passo e teto mudam o volume eleito.
3. **Coeficiente de escoamento.** Os artigos do grupo adotam 0,80, por segurança
   e por compatibilidade entre eles. O programa abre com 0,75 (telha cerâmica,
   MIX Sustentável 2020) e o tutorial usa 0,85, que é o η da NBR 15527:2019.
4. **Reservatório superior.** Os estudos de série fixam 600 L; o estudo climático
   usa 150 a 1.000 L conforme o cenário; o tutorial do manual usa 1.000 L.
5. **Modelo de balanço.** Cordova e Ghisi (2011) mostraram que o Triton é
   estatisticamente equivalente ao YAS e ao YBS, e o artigo de 2026 descreve o
   programa como intermediário entre os dois — nem conservador como o YAS, nem
   otimista como o YBS. É exatamente o que a seção do balanço diário do manual
   afirma, e agora com citação do próprio grupo.

A definição de confiabilidade volumétrica coincide: os artigos usam
`Cv = E / Dr`, potencial dividido pela fração atendível, que é a identidade
`Rv = Epot / f` da seção de indicadores do manual.

---

## 3. O que vale trazer para o programa

Em ordem de proveito por esforço:

1. **Varredura com passo variável e teto maior.** Permitir 1.000 a 70.000 L com
   passo que cresce, como nos artigos. Hoje o passo é fixo. É a mudança que mais
   aproxima o programa da prática publicada do grupo. Esforço baixo.
2. **Análise de comprimento representativo de série.** Transformar o método dos
   três artigos numa função do programa: dada a série carregada, responder em
   quantos anos os resultados se estabilizam, e avisar quando a série informada
   for curta demais para o projeto em questão. O script da replicação já é o
   protótipo. Esforço médio; valor alto, porque hoje o usuário não tem como saber
   se a série que tem basta.
3. **Demanda diária estocástica.** Silva e Ghisi (2016) mostraram que a variação
   estocástica do consumo desloca o potencial em até 4,8 pontos percentuais e o
   volume ideal em até 9,4%. O Triton modula a demanda por calendário, mas não
   sorteia: a incerteza do consumo não aparece em lugar nenhum do resultado.
   Esforço médio.
4. **Indicadores de período seco no painel de índices.** O artigo de 2022 conclui
   que o índice de sazonalidade e os indicadores de período seco são os que mais
   explicam o desempenho. O programa já calcula o SI e o CDD; falta apresentar a
   relação com o desempenho, e considerar os quatro indicadores estatísticos de
   período seco de Silva e Ghisi (2016). Esforço baixo a médio.
5. **Módulo de águas cinzas.** Seis artigos do grupo combinam chuva e cinza, e o
   programa não faz isso. É a maior lacuna de escopo em relação à produção do
   grupo. Esforço alto, e decisão de escopo antes de tudo.

---

## 4. O que apresentar no manual como comparação

Proposta de uma seção nova no capítulo de verificação, com três partes:

1. **O que a literatura do grupo encontrou.** Tabela com cidade, tipologia,
   potencial publicado e fonte, cobrindo de 2006 a 2026. Serve de faixa de
   referência: um resultado do programa fora dessa faixa pede explicação.
2. **Uma replicação feita ponta a ponta.** A do comprimento de série é a melhor
   candidata: não depende de dado externo, usa as séries que acompanham o
   programa e produz uma tabela curta. A conclusão — a série necessária cresce
   com a fração atendível — é útil ao leitor que vai escolher a série.
3. **A declaração das diferenças.** As cinco premissas da seção 2 deste
   documento, com a explicação de por que o programa não adota automaticamente as
   dos artigos.

O estudo climático nacional daria uma segunda replicação, com figura de mapa, mas
depende da base de 6,4 GB que não acompanha o repositório: fica melhor como guia
(«como reproduzir o estudo de 652 cidades com o programa») do que como figura.

---

## 5. Limites deste levantamento

- As séries de chuva dos estudos de caso não foram fornecidas com os artigos;
  sem elas, nenhuma replicação é valor a valor.
- Os parâmetros foram lidos do texto publicado. Onde o artigo não declara um
  parâmetro — coeficiente de escoamento de alguns casos antigos, por exemplo —, a
  replicação adota o do próprio artigo posterior do grupo, e isso está anotado no
  script.
- As duas replicações usam o motor do Triton, e não o Netuno 4 dos artigos. A
  comparação, portanto, mistura duas fontes de diferença: a de dados e a de
  versão do programa. A seção de comparação com o Netuno 4 do manual trata da
  segunda.
