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
| «Fração atendível fora de [0, 1]» | fração maior que 1 | informe 0,4 para 40%, e não 40 |

> A última é a mais frequente. O campo aceita fração **ou** percentual em alguns
> pontos da interface e só fração no núcleo; quando a mensagem aparecer, é porque o
> valor chegou como 40 em vez de 0,4.

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
| «Dose negativa» | dose menor que zero | corrija |

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
| arquivo `.netuno` com JSON inválido | a abertura é interrompida | o arquivo pode estar truncado; recorra à cópia de segurança |
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
