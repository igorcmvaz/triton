# Quanto custa e em quanto se paga

> Ao terminar esta seção você terá o fluxo de caixa de vinte anos, e saberá por
> que o **regime tarifário do seu município** decide a viabilidade mais do que
> qualquer parâmetro do projeto.

---

## A economia é a diferença entre duas contas

O erro mais comum na análise econômica de sistemas pluviais consiste em multiplicar o
volume poupado por uma tarifa média. O resultado quase nunca é correto, e a razão está na
estrutura das tarifas brasileiras, que são progressivas por faixa de consumo, conforme a
seção {{n:16}} detalha: ==o metro cúbico que se deixa de consumir é o último da conta,
que é o mais caro, e não o médio.==

O Netuno evita o problema calculando duas faturas completas — a que a edificação pagaria
sem o sistema e a que ela paga com ele — e tomando a diferença entre as duas.

<!-- inclui: _tabelas/cap10_economico.md -->

O resultado merece atenção. O sistema poupa 6,84 m³ por mês e a fatura cai R$ 195,77, o
que equivale a R$ 28,62 por metro cúbico economizado — valor bem acima dos R$ 14,31 da
faixa em que o consumo se situava. A diferença tem duas origens que atuam juntas: a
progressividade, que faz o metro cúbico economizado valer o preço da faixa mais alta, e o
esgoto, que em Florianópolis é cobrado a 100% da tarifa de água e portanto dobra o valor
de cada metro cúbico poupado.

> **O esgoto é percentual da tarifa de água, não da fatura.** Cem por cento da água
> significa que a parcela de esgoto iguala a de água, e portanto o esgoto é metade
> da fatura. Economizar água economiza as duas parcelas, e é por isso que o valor
> efetivo do metro cúbico poupado quase dobra.

---

## O regime tarifário da CASAN

Florianópolis pratica o regime de disponibilidade, no qual a concessionária cobra uma
taxa fixa mensal de R$ 46,34 que se soma ao consumo medido, e tarifa as faixas
progressivas a partir do primeiro metro cúbico consumido.

Para um projeto de aproveitamento pluvial, essa é a configuração mais favorável que
existe: cada metro cúbico economizado gera desconto desde o primeiro, porque a taxa fixa
é cobrada por disponibilizar a rede, e não por um volume incluído. Ela continua sendo
paga, e não impede a economia sobre o consumo.

Nem todo município adota esse regime, e a diferença entre eles decide a viabilidade de
projetos inteiros. O programa distingue cinco.

<!-- tabela: Os cinco regimes de mínimo tarifário e o efeito de cada um sobre a economia -->
| Regime | O que acontece ao economizar | Municípios na base |
| :--- | :--- | ---: |
| disponibilidade | cada m³ economizado desconta | 156 |
| sem mínimo | idem | 165 |
| franquia no mínimo | economizar abaixo da franquia **não desconta nada** | 329 |
| franquia retroativa | passando da franquia, tarifa-se tudo desde zero | 2 |
| piso de pagamento | a conta não cai abaixo do piso | 0 |

> **Atenção, e é o ponto que mais derruba estudo.** Em município com **franquia no
> mínimo** — a maioria da base, 329 dos 652 — a concessionária cobra um valor fixo
> que já inclui, digamos, 10 m³. Uma residência que consome 12 m³ e economiza 3
> desce para 9, entra na franquia, e **a conta para de cair**. O sistema economiza
> água e não economiza dinheiro.
>
> Rodar esse caso com a tarifa de Florianópolis produziria um payback que não existe.
> A seção {{n:16}} ensina a montar a estrutura do seu município corretamente.

---

## O investimento

R$ 13.379,79, assim distribuídos:

<!-- tabela: Composição do investimento inicial do projeto do tutorial -->
| Rubrica | Valor |
| :--- | ---: |
| cisterna de concreto de 5.000 L | R$ 6.300 |
| mão de obra e escavação | R$ 3.500 |
| tubulação | R$ 1.200 |
| acessórios | R$ 1.800 |
| linha de tratamento, incremento | R$ 580 |

Os preços de reservatório vêm da base do programa, que traz valores por volume e por
material, com procedência declarada. Para volumes fora da tabela, o programa
interpola; para extrapolar além dela, só o faz se a regressão tiver R² acima de
0,90, e avisa quando não tem.

---

## O resultado

<!-- tabela: Indicadores econômicos do projeto do tutorial em vinte anos -->
| | |
| :--- | ---: |
| valor presente líquido | R$ 15.295 |
| taxa interna de retorno | 15,12% ao ano |
| payback descontado | 8,7 anos |

Um projeto que devolve o investimento em menos de nove anos e rende 15% ao ano acima
da taxa mínima é, financeiramente, muito bom. Boa parte disso vem da tarifa de
Florianópolis, que é alta, e do esgoto a 100%.

**O custeio é irrisório:** R$ 4,74 por ano, só de pastilha de cloro. Sem caixa
superior não há bomba, e portanto não há energia. É a vantagem escondida da decisão
da seção {{n:8}}.

---

## O que a projeção assume

Vinte anos são muito tempo, e a projeção depende de premissas que convém declarar:

<!-- tabela: Premissas da projeção econômica e o peso de cada uma no resultado -->
| Premissa | Valor adotado | Onde ela pesa |
| :--- | ---: | :--- |
| taxa mínima de atratividade | 0,5% ao mês | desconta o fluxo; quanto maior, pior o VPL |
| inflação dos custos | 0,35% ao mês | incide só sobre o custeio |
| reajuste da tarifa de água | 5% ao ano | incide sobre a economia |
| reajuste da tarifa de esgoto | 5% ao ano | idem, e é indexado à parte |
| intervalo de reajuste | 12 meses | em degraus, não continuamente |
| período de análise | 20 anos | vida útil adotada |

> **Os reajustes de água e de esgoto são separados**, e não um índice único sobre a
> conta agregada. As duas parcelas são reajustadas por atos diferentes da
> concessionária, e tratá-las juntas indexa metade da conta pelo índice errado.

O reajuste tarifário é a premissa mais frágil da lista. Cinco por cento ao ano por
vinte anos multiplica a tarifa por 2,65. Se a tarifa real subir mais que isso, o
projeto rende mais; se subir menos, rende menos. Um estudo sério declara o valor
adotado e mostra a sensibilidade — a seção {{n:20}} ensina como.

---

## O que temos até aqui

<!-- tabela: Estado do projeto do tutorial após a análise econômica -->
| Projeto até aqui | |
| :--- | ---: |
| volume | 5.000 L, concreto |
| investimento | R$ 13.380 |
| economia anual | R$ 2.349 |
| VPL em 20 anos | R$ 15.295 |
| payback | 8,7 anos |

O dinheiro diz sim, com folga.

Falta ouvir o carbono. E ele vai discordar.
