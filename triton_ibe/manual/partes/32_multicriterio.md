# Decisão multicritério

> Esta secção formaliza os oito critérios e os dois métodos de ordenação que o programa oferece,
> define a faixa de escolha, diz como se declaram ou se calculam os pesos e regista três desvios em
> relação à formulação canónica que um estudo publicado precisa de citar.

A análise multicritério é o ramo da investigação operacional que trata de escolher entre
alternativas quando os critérios de avaliação discordam entre si e não se podem reduzir a um único
número sem que alguém declare o que vale mais. É exatamente a situação de um projeto de
aproveitamento pluvial: o volume que entrega mais água não é o que rende mais dinheiro, nenhum
dos dois costuma ser o de menor impacto de carbono, e o maior é sempre o mais pesado.

O que os métodos desta secção fazem não é descobrir a resposta certa. ==Tornam explícita a
ponderação que, de outro modo, ficaria implícita na escolha de quem decide.== É essa a diferença
toda entre um estudo que declara os seus valores e um que os esconde atrás de um resultado
aparentemente objetivo.

---

## Os oito critérios

O programa avalia cada volume candidato segundo oito critérios, agrupados em quatro eixos. Cada
critério tem uma direção de preferência: em uns, mais é melhor; noutros, menos.

<!-- tabela: Os oito critérios de decisão, o eixo, a direção de preferência e a definição de cada um no programa -->
| # | Critério | Eixo | Direção | Definição no programa |
| :-- | :--- | :--- | :--- | :--- |
| 1 | fiabilidade volumétrica | técnico | maximizar | água de chuva consumida ÷ procura de água de chuva (usos não potáveis e rega), em % |
| 2 | eficiência de armazenamento | técnico | maximizar | água de chuva entregue por dia ÷ volume da cisterna inferior, em % (a renovação diária do volume, ou o giro anual ÷ 365) |
| 3 | economia financeira líquida | económico | maximizar | o VAL do sistema contra a linha de base sem cisterna: a fatura evitada menos o investimento e os custos de exploração, atualizados |
| 4 | custo nivelado da água (LCOW) | económico | minimizar | investimento e custos de exploração atualizados ÷ água de chuva entregue atualizada, em €/m³ |
| 5 | período de recuperação descontado | económico | minimizar | o da análise económica; quem não se recupera recebe uma penalização (ver abaixo) |
| 6 | CO₂e de ciclo de vida | ambiental | minimizar | CO₂e líquido no fim da vida útil (negativo = evitado) |
| 7 | massa a seco dos materiais | estrutural | minimizar | massa a seco do sistema — cisternas, tubagem, eletrobomba e acessórios — da calculadora de peso do programa |
| 8 | extravasamento anual | estrutural | minimizar | volume extravasado por ano, em m³ |

Os critérios de cada eixo puxam em sentidos opostos, e é isso que os torna úteis. A
fiabilidade sobe com o volume; a eficiência de armazenamento cai, e trava o
sobredimensionamento. A massa a seco sobe com o volume; o extravasamento desce. A eficiência não é
a ocupação média da cisterna: essa sobe com o volume em clima húmido, porque a cisterna grande fica
cheia de água parada. A fiabilidade volumétrica é a da secção {{n:25}}; no separador de decisão, os
rótulos vêm do programa, e ela aparece como «Confiabilidade volumétrica».

A versão 0.1.0 tinha sete critérios em três eixos, e três deles — potencial de poupança,
extravasamento e consumo de água potável — mediam a mesma água economizada, que melhora sempre
com o volume. Metade do peso ia para um único fenómeno. A 0.2.0 troca-os por critérios que não
andam juntos e acrescenta o eixo estrutural.

As alternativas submetidas à ordenação são os volumes simulados, e cada uma comparece com os oito
valores acima, calculados nas secções {{n:23}}, {{n:29}} e {{n:30}} e pela calculadora de peso. Não
há critério inventado nesta etapa: o método limita-se a ordenar o que as dimensões anteriores já
produziram.

### O custo nivelado da água

O LCOW é o custo de cada metro cúbico de água de chuva entregue, com o investimento e os custos de
exploração atualizados à mesma taxa e no mesmo horizonte do projeto:

```equacao:lcow
LCOW = [ CAPEX + Σ ( C_m ÷ ( 1 + TMA )^m ) ] ÷ Σ ( V_m ÷ ( 1 + TMA )^m )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `LCOW` | custo nivelado da água de chuva entregue | €/m³ |
| `CAPEX` | investimento inicial total | € |
| `C_m` | custos de exploração do mês `m`: energia, manutenção, cloro e linha de tratamento | € |
| `V_m` | água de chuva entregue no mês `m` | m³ |
| `TMA` | taxa de atualização mensal do projeto | adimensional |
| `m` | índice mensal, de 1 até ao horizonte de cálculo | mês |

A curva do LCOW em função do volume tem a forma de um U. Nos volumes pequenos, o investimento que
não depende do volume — eletrobomba, tubagem, mão de obra — divide-se por pouca água; nos grandes,
a cisterna cresce mais depressa do que a água que entrega. A alternativa sem cisterna, que não
entrega água, recebe o pior LCOW observado mais 10%.

### O período de recuperação de quem não se recupera

O período de recuperação descontado é o da análise económica. Quem não recupera o investimento no
horizonte recebe uma penalização explícita, em vez de ficar de fora da conta: o pior período
observado mais 10%, com ao menos mais um ano e ao menos 20 anos. Quando nenhum volume se recupera,
como no tutorial de Lisboa com os custos ilustrativos, o critério fica igual em todos e não pesa
na escolha.

---

## O peso do sistema

O eixo estrutural nasce de uma calculadora que o programa passou a ter na 0.2.0: o peso do
sistema. Para cada volume, ela soma a massa a seco dos componentes — cisternas, tubagem,
eletrobomba e acessórios —, a carga de água e a carga em operação, em quilogramas e em
quilonewtons, separadas em três posições: subsolo ou nível inferior, cobertura ou nível superior,
e prumadas e rede.

O resultado aparece no relatório HTML, no XLSX — a folha `system_weight` traz o resumo do volume
escolhido, e os valores por volume ficam na folha `alternatives` — e no texto do terminal; na
linha de comandos, com `triton analyze … --analysis all` ou `--analysis system_weight` (secção
{{n:19}}).

O programa emite um alerta quando a carga passa um **limiar de atenção do próprio programa**:
500 kg sobre a cobertura com o reservatório cheio, um reservatório superior acima de 1 500 L, uma
cisterna acima de 3 000 kg a seco, ou qualquer cisterna de betão. ==Estes limiares não vêm de
nenhuma norma.== Servem para lembrar que a carga se confirma com o projeto estrutural ou de
fundações, e não substituem esse projeto.

---

## TOPSIS

O TOPSIS — *Technique for Order of Preference by Similarity to Ideal Solution*, proposto por Hwang
e Yoon em 1981 — parte de uma ideia geométrica simples. Se cada alternativa é um ponto num espaço
de oito dimensões, uma por critério, existem dois pontos de referência: a **solução ideal**,
composta pelo melhor valor de cada critério, e a **solução anti-ideal**, composta pelos piores.
Nenhuma alternativa real ocupa qualquer deles, porque nenhuma vence em tudo nem perde em tudo, e a
melhor alternativa é a que está em simultâneo mais perto do ideal e mais longe do pior caso.

O método executa cinco passos. Monta a matriz de decisão, com as alternativas nas linhas e os
critérios nas colunas; normaliza essa matriz, para que critérios medidos em euros, em
percentagens e em quilogramas passem a ocupar escalas comparáveis; aplica os pesos declarados;
identifica as soluções ideal e anti-ideal; e ordena as alternativas pela proximidade relativa ao
ideal.

```equacao:topsis
C_i = d_i⁻ ÷ ( d_i⁺ + d_i⁻ )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `C_i` | coeficiente de proximidade da alternativa `i`, entre 0 e 1 | adimensional |
| `d_i⁺` | distância euclidiana da alternativa `i` à solução ideal | adimensional |
| `d_i⁻` | distância euclidiana da alternativa `i` à solução anti-ideal | adimensional |

O coeficiente da Equação {{eq:topsis}} valeria 1 para uma alternativa que coincidisse com a
solução ideal em todos os critérios, e 0 para uma que coincidisse com a anti-ideal. Como nenhuma
alternativa real ocupa esses extremos, o que interessa não é o valor absoluto do coeficiente, mas a
ordenação que ele produz.

---

Aplicado à varredura completa do projeto do tutorial (Lisboa), de 1 a 20 m³ em passos de 1 m³,
com os quatro eixos a 25%, a pontuação decresce em todo o intervalo, e o maior valor fica no
menor volume, 1 000 L, sozinho na faixa de escolha ({{fig:fig22_topsis}}). Na secção {{n:12}}, com
sete candidatos, a faixa vai de 2 000 a 3 000 L. A diferença não é erro: o ideal e o anti-ideal constroem-se a partir do conjunto
avaliado, e acrescentar volumes grandes desloca os dois pontos de referência e pode alterar a
ordenação — o fenómeno conhecido como inversão de ordem (*rank reversal*). Declare o conjunto de
candidatos junto com os pesos.

![A pontuação TOPSIS ao longo da varredura completa](../figuras/fig22_topsis.png)

*Figura 99 — Pontuação TOPSIS de cada volume da varredura do projeto do tutorial, de 1 a 20 m³, com cisterna de polietileno, os quatro eixos a 25% e partes iguais no eixo; a estrela marca o volume de maior pontuação. Os custos que alimentam os critérios económicos são ilustrativos, não são preços de mercado. Figura gerada pelo próprio programa.*

---

## A faixa de escolha

Quando vários volumes pontuam quase igual, apontar um deles como «o melhor» exagera a precisão do
método. O programa relata, em vez disso, uma **faixa de escolha**: os volumes com resultados
multicritério semelhantes ao do volume de maior pontuação. ==Num estudo, a frase a escrever é
«volumes de 2 000 a 3 000 L têm resultados multicritério semelhantes», e não «3 000 L é o volume
ótimo».==

A regra é a mesma para os quatro métodos. A medida de cada volume maior do que zero — a pontuação
do TOPSIS, o índice Q do VIKOR (menor é melhor), o fluxo líquido do PROMETHEE II ou a aceitabilidade
de primeiro lugar do SMAA — é normalizada entre a pior (0) e a melhor (1) do conjunto avaliado, e
entram na faixa os volumes que ficam a até a **tolerância** da melhor. Por omissão, a tolerância é
5% dessa amplitude. O programa informa também o volume de maior pontuação, como informação e não
como veredito, e se a faixa é contígua: quando um volume avaliado no meio fica de fora, a faixa
lista os volumes em vez de dar um intervalo.

<!-- inclui: _tabelas/cap32_faixas.md -->

No tutorial, o TOPSIS, o VIKOR e o PROMETHEE II dão a mesma faixa, de 2 000 a 3 000 L. O SMAA-VIKOR
estreita-a para 3 000 L: nenhum outro volume chega a 5% da amplitude das aceitabilidades do
primeiro, embora o próprio 3 000 L vença em menos de um quarto dos sorteios.

**A faixa não é um intervalo de confiança.** Não tem significado estatístico: depende de duas
escolhas que o estudo tem de declarar. A primeira é a **tolerância** — a segunda tabela mostra a
faixa do tutorial a ir de um volume só, com tolerância zero, a cinco volumes, com 20%. A segunda é a
**grade de volumes avaliada**: a faixa só contém volumes que foram avaliados, e a normalização usa a
pior e a melhor medida do conjunto, de modo que acrescentar ou tirar candidatos pode mudá-la. Uma
grade mais fina tende a pôr mais volumes na faixa; uma grade grossa pode deixá-la num volume só.

**Onde se declara.** No separador de decisão, as linhas da conclusão dão a faixa de cada método,
com o volume de maior pontuação: «Faixa TOPSIS», «Faixa VIKOR / SMAA» e «Faixa PROMETHEE II». Na
linha de comandos, `--score-band`, de 0 a 1 (por omissão, 0,05), em todos os comandos que aceitam
`--weights`; o texto do terminal escreve a faixa do TOPSIS, o relatório HTML traz o parágrafo «Faixa
de escolha (TOPSIS)» e o JSON as chaves `topsis.choice_band`, `choice_band_min_volume_l`,
`choice_band_max_volume_l` e `smaa_vikor.choice_band`. No ficheiro de projeto, a tolerância é
`analysis.topsis_score_band`; no estudo declarativo, `analise.tolerancia_faixa`, e as métricas
`faixa_topsis_min_l` e `faixa_topsis_max_l` levam a faixa para as tabelas do artigo (secção {{n:19}}).

---

## Três desvios a declarar

A implementação do programa afasta-se da formulação canónica em três pontos, todos deliberados, e
um estudo publicado precisa de os declarar para não atribuir aos métodos originais um
comportamento que é do programa.

**A normalização é uma variante.** A formulação canónica de Hwang e Yoon emprega a normalização
vetorial, que pressupõe valores não negativos em todos os critérios. O valor atual líquido, porém,
é com frequência negativo nos volumes pequenos, em que o investimento não se paga, e o CO₂e de
ciclo de vida é negativo quando a emissão é evitada. O programa contorna a restrição transladando
cada critério por `x − min(x)` antes de normalizar. A escolha é necessária e deliberada, mas
apresentar o resultado como TOPSIS canónico seria incorreto: declare a variante.

**As condições de Opricovic não estão implementadas.** O método VIKOR, na formulação de Opricovic,
exige duas verificações sobre a solução de compromisso encontrada — a de vantagem aceitável e a de
estabilidade aceitável — e, quando qualquer uma falha, devolve um **conjunto** de soluções
equivalentes em vez de um único vencedor. O programa devolve sempre a melhor alternativa, sem
realizar o teste. Na prática, isto significa que a solução de compromisso do VIKOR deve ser lida
ao lado da análise de sensibilidade aos pesos, e nunca sozinha.

**A atribuição do código.** A implementação do VIKOR e do SMAA-VIKOR foi escrita de forma
independente e verificada contra a biblioteca `crispyn`, de Aleksandra Bączkiewicz. O TOPSIS foi
verificado contra a formulação original de Hwang e Yoon num caso de valores todos positivos, em que
a translação descrita acima é inócua e as duas formulações têm de coincidir.

---

## SMAA-VIKOR

O SMAA — *Stochastic Multicriteria Acceptability Analysis* — existe para responder à pergunta a
que o TOPSIS não responde: e se os pesos fossem outros? Em vez de exigir um conjunto de pesos
definido de antemão, o método sorteia milhares de vetores de oito pesos, um por critério, e
devolve, para cada alternativa, a probabilidade de ocupar cada posição da ordenação. Informa
também o peso central de cada alternativa — a média dos pesos que a elegeram —, agregado nos
quatro eixos, e o fator de confiança: se a alternativa vence quando avaliada com o seu próprio
peso central.

**Cada eixo recebe, em média, 25%.** Os pesos saem de uma distribuição de Dirichlet com parâmetros
(1, 1, 2/3, 2/3, 2/3, 2, 1, 1), pela ordem dos critérios: a soma dos parâmetros de cada eixo é 2, e
o peso esperado de cada critério é o padrão do TOPSIS — 12,5% para cada critério técnico e
estrutural, 8,3% para cada económico e 25% para o ambiental. Um sorteio uniforme sobre os oito
critérios daria ao eixo económico, com três critérios, 37,5% do peso em média, e ao ambiental, com
um, 12,5%: seria o número de critérios de cada eixo a decidir a ponderação.

O método de ordenação de cada sorteio é, por omissão, o VIKOR (SMAA-VIKOR). O programa oferece
também o SMAA-TOPSIS, que ordena cada sorteio pelo TOPSIS do programa, com a mesma normalização
transladada da secção anterior e o mesmo fator de confiança.

A leitura do resultado é direta e informativa. Um volume que vence em 80% dos sorteios é uma
recomendação robusta, que não depende de uma ponderação específica para se sustentar. Um volume
que vence em 30% é uma recomendação frágil, e o texto do estudo tem de o dizer em vez de
apresentar o vencedor como se fosse consensual.

> É a ferramenta certa quando não há consenso sobre os pesos — que é o caso normal em projetos
> reais, nos quais o cliente, o projetista e a entidade licenciadora costumam valorizar dimensões
> diferentes.

---

A leitura mais útil da análise estocástica não é o vencedor, mas a margem com que vence. Um volume
que fica em primeiro lugar em três quartos dos sorteios de pesos é uma escolha estável, que
sobrevive a uma mudança de prioridades do decisor; dois volumes tecnicamente empatados indicam o
contrário, e nesse caso declarar o peso adotado deixa de ser formalidade e passa a ser a única
informação que sustenta a recomendação ({{fig:fig23_smaa}}).

![A aceitabilidade de primeiro lugar de cada volume](../figuras/fig23_smaa.png)

*Figura 99 — Aceitabilidade de primeiro lugar (b¹) de cada volume candidato, obtida com cinco mil vetores de oito pesos sorteados com 25% esperado em cada eixo. O volume destacado é o que mais vezes fica em primeiro lugar, e os restantes repartem o resto.*

### O tutorial, pelos dois métodos

A tabela põe lado a lado a pontuação TOPSIS, com os quatro eixos a 25% e partes iguais, e a
aceitabilidade de primeiro lugar do SMAA-VIKOR, com cinco mil vetores de oito pesos sorteados com
25% esperado em cada eixo, para os sete volumes do tutorial de Lisboa em polietileno com reservatório superior. O
investimento e o carbono por trás das pontuações são os valores ilustrativos da secção {{n:10}}
(ilustrativo, não é preço de mercado).

<!-- inclui: _tabelas/cap32_decisao.md -->

Os dois métodos põem 3 000 L à frente, e nenhum o separa dos vizinhos. O TOPSIS dá-lhe a maior
pontuação, à frente de 2 000 L por 0,0004, uma diferença que nenhum dado de entrada sustenta. O
SMAA mede essa fragilidade: 3 000 L vencem em 24,1% dos sorteios, 5 000 L em 20,5% e 2 000 L em
18,2%, com 1 000 L e 4 000 L logo atrás. Os 5 000 L, quintos no TOPSIS com os eixos iguais, são
segundos no SMAA: há ponderações plausíveis que os põem à frente. Pela régua desta secção, nenhum
volume é uma recomendação robusta, e o estudo deve declarar as alternativas. Os volumes grandes
quase nunca vencem: 8 000 L em 4,6% dos sorteios e 12 000 L em 1,0%.

---

## Os pesos

O programa aceita **quatro pesos de eixo** — técnico, económico, ambiental e estrutural, 25% cada
por omissão —, **oito pesos de critério**, um por critério, que valem sem repartição, ou os
**pesos objetivos do CRITIC**, calculados dos resultados (ver abaixo). O peso de
cada eixo reparte-se pelos seus critérios segundo as **partes no eixo**: só a proporção dentro do
eixo importa, e a parte zero tira o critério da conta. Por omissão, as partes são iguais. Com os
quatro eixos iguais, os dois critérios técnicos e os dois estruturais valem 12,5% cada, os três
económicos 8,3% cada e o ambiental 25%. O TOPSIS, o VIKOR e o PROMETHEE II usam a mesma regra.

**Projetos e estudos anteriores.** Três pesos — técnico, económico e ambiental, como nos projetos
e estudos feitos até à 0.1.0 — continuam aceites: o eixo estrutural, que não existia, recebe a
média dos três, de modo que três pesos iguais continuam a dar quatro eixos iguais. Sete valores,
pesos ou partes do modelo de sete critérios, são recusados, com a mensagem «O multicritério da
versão 0.2.0 tem oito critérios em quatro eixos, e os sete valores do modelo anterior não
correspondem a eles» (secção {{n:37}}). Os sete critérios antigos não correspondem aos oito
atuais, e o programa não inventa a correspondência.

<!-- tabela: Onde se declaram os pesos e as partes no eixo -->
| Onde | Pesos | Partes no eixo |
| :--- | :--- | :--- |
| separador de decisão | quatro cartões, um por eixo (Técnico, Económico, Ambiental, Estrutural), com o peso do eixo em cima, 25% cada; perfis «Equilibrado: 25% em cada eixo», «Priorizar …» (70% num eixo e 10% em cada um dos outros) e «Pesos objetivos (CRITIC), calculados dos resultados» | em cada cartão, por baixo do peso do eixo, as partes dos seus critérios; sob os cartões, os botões «Partes iguais» e «Recalcular» |
| linha de comandos | `--weights t,e,a,s` (ou oito valores, ou `critic`; três ainda aceites) | `--criterion-shares`, com oito valores (por omissão, `1,1,1,1,1,1,1,1`) |
| ficheiro de projeto | `analysis.topsis_weights` (quatro ou oito valores, ou `"critic"`) | `analysis.topsis_criterion_shares` (oito valores) |
| estudo declarativo | `analise.pesos` (quatro ou oito, ou `"critic"`; três aceites) | `analise.partes_no_eixo` (oito valores) |

A escolha, contudo, não é técnica: é uma declaração de valor, e por isso tem de constar do texto
do estudo. ==Uma faixa do TOPSIS sem os quatro pesos, as partes no eixo e a tolerância é impossível
de reproduzir,== e dois estudos com pesos diferentes chegam a faixas diferentes sem que nenhum dos
dois esteja errado.

No tutorial, a escolha dos pesos desloca a faixa. Com os quatro eixos iguais, a faixa do TOPSIS vai
de 2 000 a 3 000 L. Com 70% no eixo técnico e 10% em cada um dos outros, fica em 1 000 L; com 70% no
económico, vai de 2 000 a 4 000 L; no ambiental, de 1 000 a 3 000 L; no estrutural, de 3 000 a
4 000 L. Com os pesos do CRITIC, sobe para 4 000 a 5 000 L (secção {{n:12}}).

Quatro condutas são defensáveis, e a escolha entre elas depende do que se sabe sobre as
prioridades de quem decide. Pesos iguais, declarados explicitamente como ausência de preferência,
constituem a posição neutra. Pesos justificados, com a razão de cada um, são preferíveis quando as
prioridades são conhecidas. O SMAA, que reporta a gama de resultados em vez de um vencedor único, é
a conduta mais completa quando não há consenso. E os pesos objetivos do CRITIC servem a quem não
tem consenso e não quer impor uma preferência, com os limites que se seguem.

### Pesos objetivos: o CRITIC

O CRITIC — *Criteria Importance Through Intercriteria Correlation*, de Diakoulaki, Mavrotas e
Papayannakis (1995) — tira os pesos dos próprios resultados, em vez de os pedir a quem decide. Um
critério pesa mais quando separa bem as alternativas (**contraste**) e quando diz o que os outros
não dizem (**independência**).

O programa normaliza cada critério de 0, o pior valor observado, a 1, o melhor, no sentido do
critério. A informação de cada critério combina o contraste com o conflito com os demais
(Equação {{eq:critic_informacao}}), e o peso é a parte de cada critério na informação total
(Equação {{eq:critic_peso}}).

```equacao:critic_informacao
C_j = s_j × Σ ( 1 − r_jk )
```

```equacao:critic_peso
w_j = C_j ÷ Σ C
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `C_j` | informação do critério `j` | adimensional |
| `s_j` | desvio-padrão do critério `j` normalizado, entre os volumes avaliados: o contraste | adimensional |
| `r_jk` | correlação de Pearson entre os critérios `j` e `k`; a soma corre pelos oito critérios `k` | adimensional |
| `w_j` | peso do critério `j`; a soma dos oito é 1 | adimensional |

Um critério constante não informa e pesa zero; sem contraste nenhum, os pesos ficam iguais. Os pesos
saem só das alternativas com volume maior do que zero: a alternativa sem cisterna entra no TOPSIS
com as penalizações do LCOW e do período de recuperação, que inflariam o contraste. São recalculados
a cada análise, dos próprios resultados, e valem para o TOPSIS, o VIKOR e o PROMETHEE II; as partes
no eixo não se aplicam, e o SMAA continua a sortear os pesos. Na sensibilidade de pesos
(`--weight-sensitivity`), com `critic`, sorteiam-se os quatro pesos de eixo.

<!-- inclui: _tabelas/cap32_critic.md -->

No tutorial, o período de recuperação, igual em todos os volumes, pesa zero. A fiabilidade
volumétrica e o extravasamento, que melhoram com o volume quando quase todos os outros critérios
pioram, ficam com 20,4% cada, e o eixo ambiental cai de 25% para 11,5%. Com estes pesos, a faixa do
TOPSIS sobe para 4 000 a 5 000 L (secção {{n:12}}).

**O que mede, e quando serve.** O CRITIC mede o contraste e a independência dos critérios nos
resultados do próprio estudo. Serve quando não há consenso sobre os pesos e não se quer impor uma
preferência. É uma escolha de método, e não o padrão: por omissão, cada eixo vale 25%.

**Os limites.** Os pesos mudam com o conjunto de volumes avaliado, porque o contraste e as
correlações mudam. Não exprimem a preferência de ninguém. E um critério que varia muito entre os
volumes ganha peso mesmo que importe pouco ao projeto: contraste não é importância.

**Onde se escolhe.** No separador de decisão, o perfil «Pesos objetivos (CRITIC), calculados dos
resultados»: os quatro cartões passam a mostrar, só para leitura, a soma por eixo dos pesos
calculados, e as partes no eixo desaparecem. Na linha de comandos, `--weights critic`; no ficheiro
de projeto, `analysis.topsis_weights: "critic"`; no estudo declarativo, `analise.pesos: "critic"`.
Um estudo que use o CRITIC di-lo e informa os pesos calculados.

---

## Os melhores por critério isolado

Além da ordenação ponderada, o programa identifica o vencedor técnico, o financeiro e o ambiental
e reporta os três em separado. São números que vale a pena publicar em conjunto, porque cada um
responde a uma pergunta legítima e diferente. O eixo estrutural não tem vencedor isolado: os seus
dois critérios apontam para extremos opostos, a menor massa no menor volume e o menor
extravasamento no maior.

Quando os vencedores coincidem, a recomendação é forte e a decisão dispensa ponderação. Quando
divergem, que é o caso comum e o do tutorial, ==a divergência **é** o resultado:== escondê-la atrás
de um único número ponderado empobrece o estudo e transfere para o leitor uma conclusão que ele não
tem como avaliar. No tutorial de Lisboa, o critério técnico — a maior fiabilidade volumétrica —
escolhe 12 000 L, o ambiental 2 000 L e o financeiro 1 000 L (nenhum volume recupera o
investimento com a tarifa de Lisboa e estes custos ilustrativos, pelo que o critério financeiro se
decide pelo valor atual líquido menos mau); o compromisso com os quatro eixos iguais dá a faixa de
2 000 a 3 000 L.

---

## O que o método não faz

Convém terminar pelos limites, porque os métodos multicritério são frequentemente apresentados com
uma autoridade que não têm.

**Não escolhem os pesos.** A ponderação é do analista, e é uma decisão de valor, não de técnica.
O CRITIC calcula pesos, mas não a substitui: mede o contraste e a independência dos critérios nos
resultados, e não o que importa a quem decide.

**Não separam volumes que pontuam quase igual.** É o que a faixa de escolha regista. Um estudo que
apresente um volume só, quando a faixa tem vários, atribui ao método uma precisão que ele não tem.

**Não validam os critérios.** Se o valor atual líquido estiver errado porque a estrutura tarifária
foi mal introduzida, o TOPSIS ordenará o erro com precisão impecável. O método ordena o que recebe.

**Não incorporam restrições.** O espaço disponível no terreno, o orçamento máximo, a carga que a
laje suporta, uma exigência regulamentar: tudo isso são filtros anteriores à ordenação, aplicados
pelo projetista ao decidir quais volumes chegam sequer a entrar na comparação.
