# Histórico de versões e o que mudou

Esta seção registra o que mudou entre as versões do programa e, sobretudo, **quais
mudanças alteram resultados já publicados**. A distinção importa mais do que parece:
uma correção de interface não afeta nenhum estudo anterior, ao passo que uma correção
de cálculo pode deslocar cada número de um trabalho já submetido. Quem publicou com o
Netuno precisa saber em que categoria cada alteração se encaixa, e é por isso que o
histórico abaixo separa as duas coisas de forma explícita.

==A regra que orienta toda esta seção é simples: correção de cálculo obriga a
declarar a versão usada; correção de interface, não.==

---

## A versão que você está usando

O número da versão aparece na barra lateral, no rodapé, e no menu **Sobre o Netuno**.
Ele também é gravado dentro de cada arquivo de projeto e impresso em cada relatório,
de modo que um estudo antigo sempre carrega consigo a identificação do programa que o
produziu. Essa redundância é deliberada: relatórios circulam separados dos arquivos, e
a pergunta «com que versão isto foi feito?» costuma aparecer meses depois, quando
ninguém lembra.

O esquema de numeração segue a convenção corrente em engenharia de software. O
primeiro número indica a geração do programa, e sua troca significa reformulação do
modelo conceitual; o segundo indica um conjunto de funcionalidades novas; e o terceiro
indica correções e ajustes que não alteram a arquitetura. A passagem do Netuno 4 para
o Netuno 5, tratada na seção {{n:35}}, é o único caso de troca do primeiro número na
história do programa.

A versão 5.0.0 é o primeiro lançamento público do Netuno 5. Os números anteriores a
ela foram de desenvolvimento, e nunca chegaram a circular; nenhum estudo foi feito com
eles.

---

## Como este histórico é mantido

Daqui em diante, cada versão publicada ganha uma entrada própria nesta seção, com a
data do lançamento e o que mudou, sempre separado em duas listas: ==o que altera
resultados de estudos já feitos e o que não altera.== A entrada mais recente vem
primeiro.

Cada entrada segue o mesmo modelo, para que duas versões possam ser comparadas sem
releitura: uma frase de resumo, as novidades, as correções que alteram resultados, as
que não alteram, e o que mudou na documentação. Seções sem conteúdo naquela versão
simplesmente não aparecem.

A mesma lista é distribuída com o código, no arquivo `CHANGELOG.md` da raiz do
repositório, e alimenta a página de versões do site de documentação. Ela não é escrita
três vezes: os três saem desta seção, e uma verificação automática recusa a montagem se
divergirem. Quem acompanha o programa pelo repositório, pelo site ou pelo manual lê o
mesmo registro.

<!-- inclui: _tabelas/cap38_versoes.md -->

---

## Versão 5.0.0 — 21 de setembro de 2026

> **Em uma frase.** Primeiro lançamento público do Netuno 5: o motor de simulação
> reescrito em Python e separado da interface, com avaliação de ciclo de vida, linha de
> tratamento, decisão multicritério e a documentação em três formatos.

A versão foi o resultado de uma revisão sistemática do programa, conduzida com
um objetivo específico: encontrar valores que fossem calculados corretamente em um
módulo e descartados antes de chegarem ao módulo seguinte. Essa classe de defeito é
particularmente perigosa porque não produz erro visível — o programa responde, o
número parece plausível, e apenas a comparação entre dois pontos do próprio programa
revela a inconsistência. A revisão percorreu cinco eixos de propagação: de módulo para
módulo, da tela para o núcleo de cálculo, entre a interface e a automação, entre
definições duplicadas de uma mesma constante, e ao longo do tempo, isto é, através da
gravação e da releitura de um projeto.

### Novidades

O programa foi reescrito em Python, com o motor de simulação separado da interface, e
ganhou o que o Netuno 4 não tinha: avaliação de ciclo de vida do carbono, linha de
tratamento dimensionada, decisão multicritério com análise de aceitabilidade
estocástica, base tarifária de 652 municípios, interface em quatro idiomas e
exportação para CAD, BIM e planilha. A seção {{n:35}} compara os dois programas número
a número, e a seção {{n:34}} descreve a suíte de verificação que sustenta a
comparação.

### Correções que alteram resultados

As alterações reunidas nesta tabela mudam números em relação ao que o programa
calculava antes de cada correção. Como a 5.0.0 é o primeiro lançamento público, nenhum
estudo depende delas; a tabela fica registrada porque descreve o que o programa passou
a calcular de outro modo, e porque é o formato que as versões seguintes vão usar.

<!-- tabela: Correções que alteram resultados de estudos feitos em versão anterior -->
| O que foi corrigido | Efeito no resultado |
| :--- | :--- |
| a potência de placa da motobomba era tratada como potência elétrica de entrada, quando é potência de eixo | consumo específico de bombeamento passou de 0,0654 para 0,1080 kWh/m³ |
| a energia de partida dividia a potência de placa pelo rendimento da bomba, embora não haja vazão na partida | parcela de partidas corrigida, cerca de 14% da energia anual |
| a demanda de irrigação atendida pela rede não aparecia no resumo | demanda não atendida deixou de ser subestimada em 10,85 L/dia no caso de referência |
| quatro campos de imposto eram zerados a cada confirmação do diálogo econômico | as faturas de água e de energia passaram a incluir os tributos declarados |
| a cloração, o ultravioleta e o ozônio eram tratados como mutuamente exclusivos | linha de tratamento passou a compor estágios, conforme o item 4.6.5 da ABNT NBR 15527:2019 |
| o econômico só cobrava energia com caixa superior, e a avaliação ambiental cobrava bombeamento em qualquer arranjo e perdia a cloração sem caixa | o arranjo de abastecimento passou a ser declarado na etapa 4, e custo e carbono leem a mesma energia; projetos sem caixa superior deixam de ter bombeamento implícito no carbono e passam a ter cloração |
| o fator de emissão do hipoclorito era 1,85 kg CO₂e/kg, sem processo declarado | passou a 1,72 kg CO₂e/kg, do Ecoinvent 3.8 na base de cloro ativo |

### Correções que não alteram resultados

As alterações abaixo corrigem o comportamento do programa sem tocar em nenhum valor
calculado. Nenhum resultado muda por causa delas; apenas ficou mais difícil produzir um
estudo errado.

<!-- tabela: Correções de comportamento que não alteram resultado calculado -->
| O que foi corrigido | O que muda para você |
| :--- | :--- |
| a modulação de demanda por calendário não era gravada no arquivo do projeto | um projeto com perfil semanal, mensal ou diário reabre como foi salvo |
| arquivo JSON de esquema desconhecido era aceito e abria um projeto inteiramente padrão | a abertura é interrompida com mensagem própria |
| a caixa de seleção da motobomba reserva forçava duas bombas em qualquer situação | a quantidade informada é respeitada |
| seis campos eram gravados no arquivo e nunca lidos de volta | a seção {{n:36}} lista os que permanecem nessa condição |

### Documentação

A documentação acompanha o lançamento em três formatos, montados das mesmas fontes: o
manual completo em PDF, sete volumes avulsos para quem só precisa de uma parte, e um
site de documentação com dezoito figuras interativas, em que o leitor muda os
parâmetros e vê o resultado que o programa calculou. Os três, mais o `CHANGELOG.md`
distribuído com o código, saem dos mesmos arquivos de texto.

> **Aprofundamento: por que a correção do bombeamento é a mais relevante.** A ABNT NBR
> 17094-2:2016 determina que o rendimento do motor seja marcado na placa
> **separadamente** da potência, o que significa que a potência de placa é a potência
> disponível no eixo, e não a potência consumida na tomada. Tratar uma pela outra
> subestima o consumo por um fator igual ao rendimento do motor, que para uma máquina
> de meio cavalo com dois polos é de 60,5%. O efeito é grande em termos relativos,
> ainda que pequeno em termos absolutos, porque a energia de bombeamento de um sistema
> predial de aproveitamento pluvial é modesta frente ao restante do balanço econômico.
> A seção {{n:28}} desenvolve a cadeia completa.

---

## Como saber se a sua versão tem uma correção

O procedimento é direto e não depende de consultar ninguém: abra um dos arquivos de
exemplo que acompanham o programa, descritos no apêndice {{n:J}}, rode-o, e compare o
resultado obtido com o valor impresso neste manual. Cada caso de exemplo foi gerado
pela mesma versão do programa que gerou este manual, e cada número publicado tem
verificação automática correspondente, conforme a seção {{n:34}} descreve. Uma
divergência, portanto, indica que o programa instalado não é o da versão deste manual.

==Se os números baterem, a sua instalação corresponde exatamente ao manual que você
tem em mãos.== Se não baterem, a diferença não é um defeito da sua instalação, e sim
uma diferença de versão que precisa ser identificada antes de qualquer estudo.

---

## O que declarar num trabalho publicado

A boa prática de reprodutibilidade computacional exige que um trabalho identifique de
modo inequívoco o programa que produziu os resultados. No caso do Netuno, quatro
informações bastam, e todas estão disponíveis sem esforço: a versão do programa, que
aparece no relatório; a origem da série de precipitação, com o período utilizado; a
estrutura tarifária adotada, com a data de vigência; e a declaração de quais parâmetros
foram alterados em relação aos valores padrão. A seção {{n:13}} traz a lista completa,
com um parágrafo de método pronto para ser adaptado.

Anexar o arquivo `.netuno` ao material suplementar resolve as quatro de uma vez, porque
o arquivo é autocontido e traz a série de chuva dentro dele. É a forma mais econômica
de tornar um estudo verificável por terceiros, e custa um anexo de cerca de 160 kB.
