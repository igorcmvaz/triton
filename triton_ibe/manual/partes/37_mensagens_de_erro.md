# Mensagens de erro e o que fazer

> O que cada mensagem significa, o que a provocou e como a resolver.

O programa segue uma política deliberada perante entradas impossíveis: recusa-as em vez de as
corrigir em silêncio. A razão é que uma área de captação negativa não é uma preferência do
utilizador a acomodar, mas um erro de digitação que precisa de ser visto por quem o cometeu.
==Corrigir em silêncio produziria um resultado plausível a partir de uma entrada errada, que é a
pior combinação possível num programa de simulação.==

> **As mensagens do núcleo de cálculo são emitidas tal como o código as escreve.** As verificações
> que correm dentro do cálculo levantam as suas mensagens em português, por vezes sem acentos e com
> um vocabulário que pode diferir do deste manual (por exemplo, «motobomba» onde o manual diz
> «eletrobomba»). As tabelas abaixo citam cada mensagem com acentos, para facilitar a leitura, e
> explicam-na em seguida; reconhece-a pelo sentido e pelo nome do campo.

---

## Validação física da entrada

As mensagens abaixo são emitidas antes de qualquer cálculo começar, e todas nomeiam o campo
responsável e o valor recebido, de modo que a correção não exija procura.

<!-- tabela: Mensagens de validação física da entrada e a providência de cada uma -->
| Mensagem | O que a provocou | O que fazer |
| :--- | :--- | :--- |
| «Volume do reservatório inferior negativo» | volume menor do que zero | corrija; **zero é válido** e representa o cenário sem sistema |
| «Volume do reservatório superior negativo» | idem, no reservatório elevado | corrija; zero significa sem reservatório superior |
| «Área de captação negativa» | área menor do que zero | corrija; use a projeção horizontal em m² |
| «Coeficiente de escoamento fora de [0, 1]» | coeficiente negativo ou acima de 1 | acima de 1 a cobertura entregaria mais água do que a chuva traz; as coberturas usuais ficam entre 0,80 e 0,95 |
| «Lâmina de descarte negativa» | descarte menor do que zero | o descarte retira água à captação, não a acrescenta |
| «Demanda diária negativa» | procura menor do que zero | corrija |
| «Fração atendível por água pluvial fora de [0, 1]» | fração maior do que 1 | introduza 0,4 para 40%, e não 40 |
| «… não é um número finito» | campo que chegou ao cálculo vazio, como texto ou infinito | preencha o campo indicado com um número |
| «Modo de descarte desconhecido» | modo diferente de 1, 2 ou 3 | escolha um dos três modos; para não descartar, introduza uma lâmina zero |
| «Intervalo de descarte inválido» | modo 3 com um intervalo menor do que 1 dia | introduza o intervalo em dias inteiros |
| «Nível de acionamento da motobomba negativo» | nível menor do que zero | corrija; zero significa acionar com o reservatório vazio |

> A fração atendível é a mensagem mais frequente, e a regra que a evita é uma só: onde se digita,
> uma percentagem de 0 a 100; onde se guarda, uma fração de 0 a 1. A secção {{n:5}} justifica a
> divisão. Quando a mensagem surge, o valor chegou como 40 num sítio que guarda 0,4 — tipicamente
> um ficheiro de parâmetros editado à mão ou uma chamada de automação.

<!-- tabela: Mensagens da fração atendível e a providência de cada uma -->
| Mensagem | O que a provocou | O que fazer |
| :--- | :--- | :--- |
| «… parece estar em percentual» | fração entre 1 e 100 no ficheiro, no vetor semanal, mensal ou diário, ou na automação | introduza 0,4 para 40% |
| «… fora de [0, 100]» | percentagem negativa ou acima de 100 no ecrã, na tabela de cenários, na folha de cálculo ou em `--share` | corrija; 40 significa 40% |
| campo laranja, ou pergunta «Simular mesmo assim?» | percentagem entre 0 e 1 | se queria 40%, digite 40; se queria mesmo menos de 1%, confirme |

---

## Série de precipitação

O programa não distingue um dia seco de um dia sem registo, e por isso não adivinha: uma falha na
série interrompe o cálculo, com a indicação de onde está. Preencher a falha, ou recortar a série
para um período sem falhas, é uma decisão de quem conduz o estudo, e a decisão tem de constar do
estudo.

<!-- tabela: Mensagens de erro da série de precipitação e a providência de cada uma -->
| Mensagem | Causa | O que fazer |
| :--- | :--- | :--- |
| «A série de precipitação está vazia» | ficheiro sem nenhuma linha numérica | confira se o ficheiro tem uma coluna de valores diários, um por linha |
| «… dia(s) sem valor numérico, o primeiro no dia N» | falha de registo: linha vazia ou texto a meio da série | preencha as falhas ou recorte a série, e declare o tratamento |
| «… valor(es) negativo(s), o primeiro de X mm no dia N» | sentinela de falha, como −999 | trate-o como falha: preencha ou recorte |

Uma linha de cabeçalho antes dos dados, como «Data;Precipitação», não é erro: é ignorada e a
leitura começa na primeira linha numérica.

---

## Varredura

<!-- tabela: Mensagens de erro da varredura de volumes -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «O volume máximo da varredura deve ser finito e não negativo» | campo vazio ou negativo | introduza o volume máximo em litros |
| «O passo de varredura deve ser finito e maior que zero» | passo zero ou vazio | introduza o passo; será arredondado para o múltiplo de 250 L |

Há ainda um aviso que não é um erro e convém não confundir com um: quando o passo da varredura é
ajustado para o múltiplo de 250 L, ou quando o limite de quarenta volumes obriga a alargá-lo, o
programa regista o ajuste e prossegue normalmente. O que esse aviso exige do utilizador é apenas
que declare no estudo o passo efetivamente utilizado, e não o passo originalmente pedido.

---

## Cloragem

<!-- tabela: Mensagens de erro dos parâmetros de cloragem -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Pureza deve ficar em (0, 1]» | pureza introduzida como percentagem | introduza 0,65 para 65%, e não 65 |
| «A dose não pode ser negativa» | dose menor do que zero | corrija |
| «O fator de emissão não pode ser negativo» | fator de emissão do produto menor do que zero | corrija; o fator é por quilograma de produto comercial |

---

## Análise económica

<!-- tabela: Mensagens de erro da análise económica e a providência de cada uma -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «… deve ser um número finito e não negativo» | investimento, tarifa, custo, potência ou volume vazio, negativo ou infinito | a mensagem nomeia o campo; preencha-o com um número igual ou maior do que zero |
| «O período de análise deve ser um número inteiro de anos» | período fracionário, zero ou negativo | introduza o período em anos inteiros |
| «… deve ser um número finito e maior que -100%» | atualização, inflação ou taxa de atualização de −100% ou menos | confira o sinal da taxa |
| «… parece estar em percentual» | taxa anual introduzida como 5 numa função que espera uma fração decimal | introduza 0,05 para 5% |

> **Unidade das taxas.** Na interface e no ficheiro de projeto, toda a taxa é introduzida em
> percentagem, com a unidade ao lado do campo: a taxa de atualização e a inflação em % por mês ou
> em % por ano, conforme o botão ao lado, e as atualizações tarifárias em % por período de
> atualização, cujo comprimento em meses está no campo vizinho. O projeto grava a taxa de
> atualização e a inflação em % por mês. A conversão entre mês e ano é composta, (1 + i)^12 − 1, e
> não uma multiplicação por doze: 1% por mês equivale a 12,68% por ano. Na automação, as funções
> de cálculo anual recebem as taxas como fração decimal, 0,05 para 5%, e recusam um valor que
> pareça uma percentagem em vez de o reinterpretar.

---

## Decisão multicritério

<!-- tabela: Mensagens de erro da decisão multicritério e a providência de cada uma -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «O multicritério da versão 0.2.0 tem oito critérios em quatro eixos, e os sete valores do modelo anterior não correspondem a eles. Informe quatro pesos de eixo (técnico, econômico, ambiental, estrutural) ou oito pesos de critério.» | sete pesos ou sete partes no eixo, do modelo de sete critérios (até à versão 0.1.0) | refaça a ponderação com quatro pesos de eixo ou oito de critério; três pesos de eixo antigos continuam aceites, com o eixo estrutural na média dos três |
| «Informe 4 pesos de eixo (técnico, econômico, ambiental, estrutural) ou 8 pesos de critério TOPSIS» | número de pesos diferente de 3, 4, 7 ou 8 | introduza um peso por eixo ou um por critério |
| «Os pesos TOPSIS devem ser finitos e não negativos» | peso vazio ou negativo | corrija; o peso zero é válido e exclui o critério |
| «Ao menos um peso TOPSIS deve ser maior que zero» | todos os pesos a zero | atribua peso a pelo menos um critério |
| «O critério TOPSIS … da alternativa N não é finito» | indicador indefinido numa alternativa, tipicamente um período de recuperação sem retorno | confira a alternativa indicada antes de decidir |
| «Informe 8 partes, uma por critério TOPSIS (na ordem dos critérios)» | número de partes no eixo diferente de oito | introduza uma parte por critério, pela ordem do separador de decisão |
| «As partes no eixo devem ser finitas e não negativas» | parte vazia ou negativa | corrija; a parte zero é válida e tira o critério da conta |
| «Ao menos um critério do eixo … deve ter parte maior que zero» | todos os critérios de um eixo com parte zero | dê parte a pelo menos um critério do eixo; para tirar o eixo da conta, ponha a zero o peso do eixo, e não as partes |

---

## Eletrobomba

<!-- tabela: Mensagens de erro dos parâmetros da eletrobomba -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Rendimento deve ficar em (0, 1]» | rendimento como percentagem no núcleo | use 0,55 para 55% |
| «Rendimento do motor deve ficar em (0, 1]» | idem, no campo do motor | deixe em branco para o programa adotar a sua tabela de rendimentos predefinida |

---

## Ficheiros

<!-- tabela: Situações de erro na leitura e na gravação de ficheiros -->
| Situação | O que acontece | O que fazer |
| :--- | :--- | :--- |
| série de chuva ilegível | a leitura é interrompida com uma mensagem | confira o formato: uma leitura por linha, em mm, coluna única |
| ficheiro `.triton` com JSON inválido | a abertura é interrompida | o ficheiro pode estar truncado; recorra à cópia de segurança |
| secção em falta no ficheiro | os campos assumem o valor por omissão da classe | esperado ao abrir um ficheiro de versão anterior; reveja o separador correspondente |
| base de chuva por concelho não encontrada | o separador oferece só um ficheiro próprio | veja a secção {{n:2}} |

---

## Avisos que não interrompem

Os avisos reunidos nesta tabela não impedem o cálculo e não indicam defeito: são observações que o
programa faz sobre as condições em que o resultado foi produzido. Todas têm de ser transportadas
para o texto do estudo, porque todas afetam a interpretação do número e nenhuma é evidente no
resultado isolado.

<!-- tabela: Avisos que não interrompem o cálculo e têm de constar do estudo -->
| Aviso | O que significa |
| :--- | :--- |
| tipologia não residencial com tarifa residencial | o resultado económico está **subestimado**; veja a secção {{n:18}} |
| a classe-alvo recomenda filtração fina e esta foi dispensada | decisão registada no relatório |
| fator de emissão com etiqueta de triagem | o fator não tem fonte primária; declare-o |
| estrutura tarifária incompleta | a estrutura introduzida tem uma lacuna; confira-a com o tarifário publicado |
| passo de varredura ajustado | o passo efetivo difere do pedido |
| extrapolação de preço com R² baixo | o volume está fora da tabela de preços e a regressão não é fiável |

---

## Quando o resultado parece errado

Antes de suspeitar de um defeito do programa, três conferências resolvem a maior parte dos casos em
que o resultado surpreende, e cada uma corresponde a um erro de entrada com assinatura própria.

Quando o **potencial sai maior do que o esperado**, o suspeito imediato é a fração satisfazível: é
o teto de todo o resultado, e uma fração demasiado generosa infla tudo o que vem depois sem que
nada no relatório denuncie a origem.

Quando o **potencial sai muito menor**, confira a lâmina de descarte. O engano correspondente está
descrito na secção {{n:33.3}}, e consiste em introduzir o descarte em litros quando o campo pede
milímetros — o que descarta, tipicamente, a chuva inteira de todos os dias.

Quando o **retorno do investimento sai absurdo**, em qualquer das duas direções, confira a
estrutura tarifária (parte fixa, escalões, saneamento). É a causa mais frequente de um resultado
económico implausível, e a secção {{n:16}} traz o teste que a identifica em dois minutos.

Vale ainda percorrer as quatro etapas de entrada antes de aceitar qualquer resultado. A barra
lateral assinala as que continuam com pendência, e conferir quatro ecrãs custa menos tempo do que
descobrir o engano depois de o relatório estar emitido.
