# O que há de novo em cada versão do Netuno

Este arquivo é **gerado** do capítulo de histórico do manual do usuário
(`manual/partes/38_historico_de_versoes.md`) por `manual/gerar_changelog.py`.
Não o edite à mão: escreva no manual, regere, e os dois ficam iguais.

Cada versão traz duas listas, e a distinção é a que mais importa para quem
publica com o programa: **o que altera resultados de estudos já feitos** e o que
não altera. Uma correção de cálculo obriga a declarar a versão usada num
trabalho; uma correção de interface, não.

A versão atual é a 5.0.0. O manual completo está em `manual/Manual-Netuno-5.pdf`
e o site de documentação, em `manual/site/index.html`.

---

## Versão 5.0.0 — 21 de setembro de 2026

Primeiro lançamento público do Netuno 5. A versão foi o resultado de uma revisão sistemática do programa, conduzida com
um objetivo específico: encontrar valores que fossem calculados corretamente em um
módulo e descartados antes de chegarem ao módulo seguinte. Essa classe de defeito é
particularmente perigosa porque não produz erro visível — o programa responde, o
número parece plausível, e apenas a comparação entre dois pontos do próprio programa
revela a inconsistência. A revisão percorreu cinco eixos de propagação: de módulo para
módulo, da tela para o núcleo de cálculo, entre a interface e a automação, entre
definições duplicadas de uma mesma constante, e ao longo do tempo, isto é, através da
gravação e da releitura de um projeto.

### O que o Netuno 5 traz

O programa foi reescrito em Python, com o motor de simulação separado da interface, e
ganhou o que o Netuno 4 não tinha: avaliação de ciclo de vida do carbono, linha de
tratamento dimensionada, decisão multicritério com análise de aceitabilidade
estocástica, base tarifária de 652 municípios, interface em quatro idiomas e
exportação para CAD, BIM e planilha. A seção 6.1 compara os dois programas número
a número, e a seção 5.3 descreve a suíte de verificação que sustenta a
comparação.

A documentação acompanha o lançamento em três formatos, montados das mesmas fontes: o
manual completo, sete volumes avulsos e um site de documentação com figuras
interativas, em que o leitor muda os parâmetros e vê o resultado que o programa
calculou.

### Correções que alteram resultados

As alterações reunidas nesta tabela mudam números em relação ao que o programa
calculava antes de cada correção. Como a 5.0.0 é o primeiro lançamento público, nenhum
estudo depende delas; a tabela fica registrada porque descreve o que o programa passou
a calcular de outro modo, e porque é o formato que as versões seguintes vão usar.

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

| O que foi corrigido | O que muda para você |
| :--- | :--- |
| a modulação de demanda por calendário não era gravada no arquivo do projeto | um projeto com perfil semanal, mensal ou diário reabre como foi salvo |
| arquivo JSON de esquema desconhecido era aceito e abria um projeto inteiramente padrão | a abertura é interrompida com mensagem própria |
| a caixa de seleção da motobomba reserva forçava duas bombas em qualquer situação | a quantidade informada é respeitada |
| seis campos eram gravados no arquivo e nunca lidos de volta | a seção 5.2 lista os que permanecem nessa condição |

> **Aprofundamento: por que a correção do bombeamento é a mais relevante.** A ABNT NBR
> 17094-2:2016 determina que o rendimento do motor seja marcado na placa
> **separadamente** da potência, o que significa que a potência de placa é a potência
> disponível no eixo, e não a potência consumida na tomada. Tratar uma pela outra
> subestima o consumo por um fator igual ao rendimento do motor, que para uma máquina
> de meio cavalo com dois polos é de 60,5%. O efeito é grande em termos relativos,
> ainda que pequeno em termos absolutos, porque a energia de bombeamento de um sistema
> predial de aproveitamento pluvial é modesta frente ao restante do balanço econômico.
> A seção 2.6 desenvolve a cadeia completa.

---
