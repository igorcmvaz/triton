# Mensagens de erro e o que fazer

> O que cada mensagem significa, o que a disparou, e como resolver.

O programa adota uma política deliberada diante de entradas impossíveis: ele as recusa
em vez de corrigi-las silenciosamente. A razão é que uma área de captação negativa não é
uma preferência do usuário a ser acomodada, e sim um erro de digitação que precisa ser
visto por quem o cometeu. ==Corrigir em silêncio produziria um resultado plausível a
partir de uma entrada errada, que é a pior combinação possível num programa de
simulação.==

---

## Validação física da entrada

As mensagens abaixo são emitidas antes de qualquer cálculo ser iniciado, e todas
nomeiam o campo responsável e o valor recebido, de modo que a correção não exija procura.

<!-- tabela: Mensagens de validação física da entrada e a providência de cada uma -->
| Mensagem | O que a disparou | O que fazer |
| :--- | :--- | :--- |
| «Volume do reservatório inferior negativo» | volume menor que zero | corrija; **zero é válido** e representa o cenário sem sistema |
| «Volume do reservatório superior negativo» | idem, na caixa elevada | corrija; zero significa sem caixa |
| «Área de captação negativa» | área menor que zero | corrija; use a projeção horizontal em m² |
| «Coeficiente de escoamento fora de [0, 1]» | coeficiente negativo ou acima de 1 | acima de 1 a cobertura entregaria mais água do que a chuva traz; telhados usuais ficam entre 0,80 e 0,95 |
| «Lâmina de descarte negativa» | descarte menor que zero | o descarte retira água da captação, não acrescenta |
| «Demanda diária negativa» | demanda menor que zero | corrija |
| «Fração atendível por água pluvial fora de [0, 1]» | fração maior que 1 | informe 0,4 para 40%, e não 40 |
| «… não é um número finito» | campo que chegou ao cálculo vazio, como texto ou infinito | preencha o campo nomeado com um número |
| «Modo de descarte desconhecido» | modo diferente de 1, 2 ou 3 | escolha um dos três modos; para não descartar, informe lâmina zero |
| «Intervalo de descarte inválido» | modo 3 com intervalo menor que 1 dia | informe o intervalo em dias inteiros |
| «Nível de acionamento da motobomba negativo» | nível menor que zero | corrija; zero significa acionar com a caixa vazia |

> A fração atendível é a mensagem mais frequente, e a regra que a evita é uma só: onde se
> digita, percentual de 0 a 100; onde se guarda, fração de 0 a 1. A seção {{n:5}}
> justifica a divisão. Quando a mensagem aparecer, o valor chegou como 40 num lugar que
> guarda 0,4 — tipicamente um arquivo de parâmetros editado à mão ou uma chamada de
> automação.

<!-- tabela: Mensagens da fração atendível e a providência de cada uma -->
| Mensagem | O que a disparou | O que fazer |
| :--- | :--- | :--- |
| «… parece estar em percentual» | fração entre 1 e 100 no arquivo, no vetor semanal, mensal ou diário, ou na automação | informe 0,4 para 40% |
| «… fora de [0, 100]» | percentual negativo ou acima de 100 na tela, na tabela de cenários, na planilha ou em `--share` | corrija; 40 significa 40% |
| campo laranja, ou pergunta «Simular mesmo assim?» | percentual entre 0 e 1 | se quis 40%, digite 40; se quis mesmo menos de 1%, confirme |

---

## Série de precipitação

O programa não distingue um dia seco de um dia sem registro, e por isso não adivinha: uma
falha na série interrompe o cálculo com a indicação de onde ela está. Preencher a falha,
ou recortar a série para um período sem falhas, é decisão de quem conduz o estudo, e a
decisão precisa constar do estudo.

<!-- tabela: Mensagens de erro da série de precipitação e a providência de cada uma -->
| Mensagem | Causa | O que fazer |
| :--- | :--- | :--- |
| «A série de precipitação está vazia» | arquivo sem nenhuma linha numérica | confira se o arquivo tem uma coluna de valores diários, um por linha |
| «… dia(s) sem valor numérico, o primeiro no dia N» | falha de registro: linha vazia ou texto no meio da série | preencha as falhas ou recorte a série, e declare o tratamento |
| «… valor(es) negativo(s), o primeiro de X mm no dia N» | sentinela de falha, como −999 | trate como falha: preencha ou recorte |

Uma linha de cabeçalho antes dos dados, como «Data;Precipitação», não é erro: ela é
ignorada e a leitura começa na primeira linha numérica.

---

## Varredura

<!-- tabela: Mensagens de erro da varredura de volumes -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «O volume máximo da varredura deve ser finito e não negativo» | campo vazio ou negativo | informe o volume máximo em litros |
| «O passo de varredura deve ser finito e maior que zero» | passo zero ou vazio | informe o passo; ele será arredondado para o múltiplo de 250 L |

Há ainda um aviso que não constitui erro e convém não confundir com um: quando o passo
de varredura é ajustado para o múltiplo de 250 L, ou quando o limite de quarenta volumes
obriga a alargá-lo, o programa registra o ajuste e prossegue normalmente. O que esse
aviso exige do usuário é apenas que ele declare no estudo o passo efetivamente utilizado,
e não o passo originalmente pedido.

---

## Cloração

<!-- tabela: Mensagens de erro dos parâmetros de cloração -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Pureza deve ficar em (0, 1]» | pureza informada como percentual | informe 0,65 para 65%, e não 65 |
| «A dose não pode ser negativa» | dose menor que zero | corrija |
| «O fator de emissão não pode ser negativo» | fator de emissão do produto menor que zero | corrija; o fator é por quilo de produto comercial |

---

## Análise econômica

<!-- tabela: Mensagens de erro da análise econômica e a providência de cada uma -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «… deve ser um número finito e não negativo» | investimento, tarifa, custo, potência ou volume vazio, negativo ou infinito | a mensagem nomeia o campo; preencha-o com um número igual ou maior que zero |
| «O período de análise deve ser um número inteiro de anos» | período fracionário, zero ou negativo | informe o período em anos inteiros |
| «… deve ser um número finito e maior que -100%» | reajuste, inflação ou taxa de desconto de −100% ou menos | confira o sinal da taxa |
| «… parece estar em percentual» | taxa anual informada como 5 numa função que espera fração decimal | informe 0,05 para 5% |

> **Unidade das taxas.** Na interface e no arquivo de projeto, toda taxa é informada em
> percentual, com a unidade ao lado do campo: a TMA e a inflação em % ao mês (a.m.) ou em
> % ao ano (a.a.), conforme o botão ao lado, e os reajustes tarifários em % por período
> de reajuste, cujo comprimento em meses fica no campo vizinho. O projeto grava a TMA e a
> inflação em % ao mês. A conversão entre mês e ano é composta, (1 + i)^12 − 1, e não uma
> multiplicação por doze: 1% ao mês equivale a 12,68% ao ano. Na automação, as funções de
> cálculo anual recebem as taxas como fração decimal, 0,05 para 5%, e recusam um valor que
> pareça percentual em vez de reinterpretá-lo.

---

## Decisão multicritério

<!-- tabela: Mensagens de erro da decisão multicritério e a providência de cada uma -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Informe 4 pesos de eixo (técnico, econômico, ambiental, estrutural) ou 8 pesos de critério TOPSIS» | quantidade de pesos diferente de 4 ou de 8 (três também valem; veja a linha seguinte) | informe um peso por eixo ou um por critério |
| «O multicritério da versão 0.2.0 tem oito critérios em quatro eixos, e os sete valores do modelo anterior não correspondem a eles. Informe quatro pesos de eixo (técnico, econômico, ambiental, estrutural) ou oito pesos de critério.» | sete pesos ou sete partes no eixo, do modelo até a 0.1.0 | refaça a ponderação nos quatro eixos; três pesos de eixo antigos continuam aceitos, e o eixo estrutural recebe a média dos três |
| «Informe 8 partes, uma por critério TOPSIS (na ordem dos critérios).» | quantidade de partes no eixo diferente de 8 | informe uma parte por critério, na ordem da seção {{n:32}} |
| «As partes no eixo devem ser finitas e não negativas.» | parte vazia ou negativa | corrija; parte zero é válida e tira o critério da conta |
| «Ao menos um critério do eixo … deve ter parte maior que zero.» | todas as partes de um eixo zeradas | dê parte a pelo menos um critério do eixo; para tirar o eixo inteiro, zere o peso do eixo |
| «Os pesos TOPSIS devem ser finitos e não negativos» | peso vazio ou negativo | corrija; peso zero é válido e exclui o critério |
| «Ao menos um peso TOPSIS deve ser maior que zero» | todos os pesos zerados | atribua peso a pelo menos um critério |
| «O critério TOPSIS … da alternativa N não é finito» | indicador indefinido numa alternativa, tipicamente payback sem retorno | confira a alternativa indicada antes de decidir |

Na linha de comando, `--weights` e `--criterion-shares` conferem os valores antes de calcular, com
mensagem própria: «Use quatro pesos de eixo (técnico, econômico, ambiental, estrutural) ou oito de
critério, não negativos e separados por vírgula; a soma deve ser positiva. Os sete pesos do modelo
anterior à 0.2.0 não valem mais.» e «Use oito partes não negativas separadas por vírgula (uma por
critério TOPSIS), com ao menos uma positiva em cada dimensão», seguida da causa. No estudo
declarativo, as mensagens começam pelo campo: «analise.pesos: quatro números não negativos (técnico,
econômico, ambiental, estrutural) ou oito (um por critério), com soma positiva» e
«analise.partes_no_eixo:», seguida da causa.

---

## Motobomba

<!-- tabela: Mensagens de erro dos parâmetros da motobomba -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Rendimento deve ficar em (0, 1]» | rendimento como percentual no núcleo | use 0,55 para 55% |
| «Rendimento do motor deve ficar em (0, 1]» | idem, no campo do motor | deixe em branco para o programa adotar a tabela da NBR 17094-2 |

---

## Arquivos

<!-- tabela: Situações de erro na leitura e na gravação de arquivos -->
| Situação | O que acontece | O que fazer |
| :--- | :--- | :--- |
| série de chuva ilegível | a leitura é interrompida com mensagem | confira o formato: uma leitura por linha, em mm, coluna única |
| arquivo `.triton` com JSON inválido | a abertura é interrompida | o arquivo pode estar truncado; recorra à cópia de segurança |
| seção ausente no arquivo | os campos caem no padrão da classe | esperado ao abrir arquivo de versão anterior; revise a aba correspondente |
| base climática não instalada | a aba oferece só arquivo próprio | veja a seção {{n:2}} |

---

## Avisos que não interrompem

Os avisos reunidos nesta tabela não impedem o cálculo e não indicam defeito: são
observações que o programa faz sobre as condições em que o resultado foi produzido. Todas
elas precisam ser transportadas para o texto do estudo, porque todas afetam a
interpretação do número e nenhuma delas fica evidente no resultado isolado.

<!-- tabela: Avisos que não interrompem o cálculo e precisam constar do estudo -->
| Aviso | O que significa |
| :--- | :--- |
| tipologia não residencial com tarifa residencial | o resultado econômico está **subestimado**; veja a seção {{n:18}} |
| a classe alvo recomenda filtração fina e ela foi dispensada | decisão registrada no relatório |
| fator de emissão com rótulo de triagem | o fator não tem fonte primária; declare-o |
| estrutura tarifária incompleta | a tabela do município tem lacuna; confira contra a resolução |
| passo de varredura ajustado | o passo efetivo difere do pedido |
| extrapolação de preço com R² baixo | o volume está fora da tabela de preços e a regressão não é confiável |
| alerta de carga do peso do sistema | a carga passou de um limiar de atenção do programa, e não de norma: 500 kg na cobertura com o reservatório cheio, reservatório superior acima de 1.500 L, cisterna acima de 3.000 kg a seco ou cisterna de concreto; confirme a carga com o projeto estrutural ou de fundações (seção {{n:32}}) |

---

## Quando o resultado parece errado

Antes de suspeitar de defeito no programa, três conferências resolvem a maior parte dos
casos em que o resultado surpreende, e cada uma delas corresponde a um erro de entrada
com assinatura própria.

Quando o **potencial sai maior que o esperado**, o suspeito imediato é a fração
atendível: ela é o teto de todo o resultado, e uma fração generosa demais infla tudo o
que vem depois sem que nada no relatório denuncie a origem.

Quando o **potencial sai muito menor**, confira a lâmina de descarte. O engano
correspondente está descrito na seção {{n:33.3}}, e consiste em informar o descarte em
litros quando o campo pede milímetros — o que descarta, tipicamente, a chuva inteira de
todos os dias.

Quando o **retorno do investimento sai absurdo**, em qualquer das duas direções, confira
o regime tarifário do município. É a causa mais frequente de resultado econômico
implausível, e a seção {{n:16}} traz o teste que a identifica em dois minutos.

Vale ainda percorrer as quatro etapas de entrada antes de aceitar qualquer resultado. A
barra lateral assinala as que permanecem com pendência, e conferir quatro telas custa
menos tempo que descobrir o engano depois de o relatório estar emitido.
