# Decisão multicritério

> Esta secção formaliza os oito critérios e os dois métodos de ordenação que o programa oferece,
> diz como se declaram os pesos e regista três desvios em relação à formulação canónica que um
> estudo publicado precisa de citar.

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
menor volume, 1 000 L ({{fig:fig22_topsis}}). Na secção {{n:12}}, com sete candidatos, o vencedor
é 3 000 L. A diferença não é erro: o ideal e o anti-ideal constroem-se a partir do conjunto
avaliado, e acrescentar volumes grandes desloca os dois pontos de referência e pode alterar a
ordenação — o fenómeno conhecido como inversão de ordem (*rank reversal*). Declare o conjunto de
candidatos junto com os pesos.

![A pontuação TOPSIS ao longo da varredura completa](../figuras/fig22_topsis.png)

*Figura 99 — Pontuação TOPSIS de cada volume da varredura do projeto do tutorial, de 1 a 20 m³, com cisterna de polietileno, os quatro eixos a 25% e partes iguais no eixo; a estrela marca o volume de maior pontuação. Os custos que alimentam os critérios económicos são ilustrativos, não são preços de mercado. Figura gerada pelo próprio programa.*

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
definido de antemão, o método sorteia milhares de vetores de oito pesos, um por critério,
uniformes no simplex, e devolve, para cada alternativa, a probabilidade de ocupar cada posição da
ordenação. Informa também o peso central de cada alternativa — a média dos pesos que a elegeram —,
agregado nos quatro eixos.

O sorteio é uniforme sobre os oito critérios, e não sobre os eixos. Em média, cada critério
recebe um oitavo do peso, pelo que o eixo económico, com três critérios, recebe 37,5%, e o
ambiental, com um, 12,5%. Leia a aceitabilidade com isso em mente.

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

*Figura 99 — Aceitabilidade de primeiro lugar (b¹) de cada volume candidato, obtida com cinco mil vetores de oito pesos sorteados no simplex. O volume destacado é o que mais vezes fica em primeiro lugar, e os restantes repartem o resto.*

### O tutorial, pelos dois métodos

A tabela põe lado a lado a pontuação TOPSIS, com os quatro eixos a 25% e partes iguais, e a
aceitabilidade de primeiro lugar do SMAA-VIKOR, com cinco mil vetores de oito pesos sorteados,
para os sete volumes do tutorial de Lisboa em polietileno com reservatório superior. O
investimento e o carbono por trás das pontuações são os valores ilustrativos da secção {{n:10}}
(ilustrativo, não é preço de mercado).

<!-- inclui: _tabelas/cap32_decisao.md -->

Os dois métodos discordam no vencedor, e nenhum o separa dos vizinhos. O TOPSIS põe 3 000 L à
frente de 2 000 L por 0,0004 de pontuação, uma diferença que nenhum dado de entrada sustenta. O
SMAA mede essa fragilidade: 5 000 L vencem em 22,2% dos sorteios, 3 000 L em 22,0% e 2 000 L em
19,3%, com 4 000 L e 1 000 L logo atrás. Pela régua desta secção, nenhum volume é uma
recomendação robusta, e o estudo deve declarar as alternativas. Os volumes grandes quase nunca
vencem: 8 000 L em 5,4% dos sorteios e 12 000 L em 1,5%.

---

## Os pesos

O programa aceita **quatro pesos de eixo** — técnico, económico, ambiental e estrutural, 25% cada
por omissão — ou **oito pesos de critério**, um por critério, que valem sem repartição. O peso de
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
| separador de decisão | quatro controlos (Técnico, Económico, Ambiental, Estrutural), 25% cada; perfis «Equilibrado: 25% em cada eixo» e «Priorizar …» (70% num eixo e 10% em cada um dos outros) | linha «Partes no eixo», com oito controlos e o botão «Partes iguais» |
| linha de comandos | `--weights t,e,a,s` (ou oito valores; três ainda aceites) | `--criterion-shares`, com oito valores (por omissão, `1,1,1,1,1,1,1,1`) |
| ficheiro de projeto | `analysis.topsis_weights` (quatro ou oito valores) | `analysis.topsis_criterion_shares` (oito valores) |
| estudo declarativo | `analise.pesos` (quatro ou oito; três aceites) | `analise.partes_no_eixo` (oito valores) |

A escolha, contudo, não é técnica: é uma declaração de valor, e por isso tem de constar do texto
do estudo. ==A afirmação «volume ótimo pelo TOPSIS», sem os quatro pesos e as partes no eixo, é
impossível de reproduzir,== e dois estudos com pesos diferentes chegam a volumes diferentes sem que
nenhum dos dois esteja errado.

No tutorial, a escolha dos pesos desloca o resultado. Com os quatro eixos iguais, o TOPSIS
recomenda 3 000 L (com 2 000 L em segundo). Com 70% no eixo técnico e 10% em cada um dos outros,
recomenda 1 000 L; com 70% no económico, 3 000 L; no ambiental, 2 000 L; no estrutural, 4 000 L
(secção {{n:12}}).

Três condutas são defensáveis, e a escolha entre elas depende do que se sabe sobre as prioridades
de quem decide. Pesos iguais, declarados explicitamente como ausência de preferência, constituem a
posição neutra. Pesos justificados, com a razão de cada um, são preferíveis quando as prioridades
são conhecidas. E o SMAA, que reporta a gama de resultados em vez de um vencedor único, é a conduta
mais completa quando não há consenso.

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
decide pelo valor atual líquido menos mau); o compromisso com os quatro eixos iguais escolhe
3 000 L.

---

## O que o método não faz

Convém terminar pelos limites, porque os métodos multicritério são frequentemente apresentados com
uma autoridade que não têm.

**Não escolhem os pesos.** A ponderação é do analista, e é uma decisão de valor, não de técnica.
Nenhum procedimento estatístico a substitui.

**Não validam os critérios.** Se o valor atual líquido estiver errado porque a estrutura tarifária
foi mal introduzida, o TOPSIS ordenará o erro com precisão impecável. O método ordena o que recebe.

**Não incorporam restrições.** O espaço disponível no terreno, o orçamento máximo, a carga que a
laje suporta, uma exigência regulamentar: tudo isso são filtros anteriores à ordenação, aplicados
pelo projetista ao decidir quais volumes chegam sequer a entrar na comparação.
