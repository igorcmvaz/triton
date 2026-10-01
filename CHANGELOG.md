# O que há de novo em cada versão do Netuno

Este arquivo é **gerado** do capítulo de histórico do manual do usuário
(`manual/partes/38_historico_de_versoes.md`) por `manual/gerar_changelog.py`.
Não o edite à mão: escreva no manual, regere, e os dois ficam iguais.

Cada versão traz as mesmas seções: o resumo em uma frase, as novidades, **as
correções que alteram resultados de estudos já feitos**, as que não alteram e o
que mudou na documentação. A distinção entre os dois tipos de correção é a que
mais importa para quem publica com o programa: uma correção de cálculo obriga a
declarar a versão usada num trabalho; uma correção de interface, não.

A versão atual é a 5.0.0. O manual completo está em `manual/Manual-Netuno-5.pdf`
e o site de documentação, em `manual/site/index.html`.

---

## Versão 5.0.0 — 29 de setembro de 2026

> **Em uma frase.** Primeiro lançamento público do Netuno 5: o motor de simulação
> reescrito em Python e separado da interface, com avaliação de ciclo de vida, linha de
> tratamento, decisão multicritério, planta 3D da tubulação e a documentação em três
> formatos.

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
exportação para CAD, BIM e planilha. A seção 6.1 compara os dois programas número
a número, e a seção 5.3 descreve a suíte de verificação que sustenta a
comparação.

A demanda passou a ter duas parcelas declaradas: a fração não potável do consumo
interno e a demanda externa em litros por dia, suspensa nos dias de chuva. A fração
atendível total é derivada das duas e aparece num campo que não se edita. A seção
4.2 descreve a regra. Uma camada de testes abre cada projeto distribuído nas duas
pontas do programa, a interface e a linha de comando, e exige que concordem, volume a
volume, no potencial, no VPL, no payback, no carbono e nos cinco ótimos.

A tubulação passou a ser organizada pelo projetista, trecho a trecho e na ordem de
montagem, a partir de pontos de conexão dos componentes (topo, fundo e laterais do
reservatório). O programa confere se cada trecho chega ao destino declarado, recusa
tubos que ocupam o mesmo espaço e gera, com os mesmos dados, a planta 3D em DXF, o
esquema 3D com as medidas reais, a volumetria girável e os arquivos glTF e HTML para
compartilhar, além do manifesto BIM lido pelo Revit.

A edição Brasil (BRL) e a edição Internacional (INT) partem do mesmo código e se
distinguem, nesta versão, pelo executável e pelo título da janela.

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
| a interface não restaurava a fração interna nem a demanda externa ao abrir um projeto, e simulava sempre com 35% e 0 L/dia | a interface simula com a fração do projeto; o tutorial, que declara 28%, dava 32,85% de potencial a 4.000 L na tela e passa a dar 27,12%, como o manual e a linha de comando |
| a gravação pela interface escrevia 35% e 50 L/dia como fração interna e demanda externa, quaisquer que fossem os da tela | o arquivo grava as frações simuladas; arquivos antigos que discordam são abertos com a fração total que declaram, com aviso |
| nos modos semanal, mensal e diário, a fração de reserva era a total, que já inclui a demanda externa | a fração de reserva é a interna, e a demanda externa deixa de ser contada duas vezes |
| a interface ignorava o volume fixo declarado no projeto e simulava o ótimo técnico da varredura | no modo de volume fixo, a interface simula o volume declarado, como a linha de comando |
| a aba ambiental da interface usava dose e fator de cloro próprios, e não os do projeto | a avaliação ambiental lê o cloro declarado na etapa de qualidade da água |
| a linha de comando cobrava o mesmo preço de cisterna em toda a varredura | o preço acompanha o volume, como na interface; o VPL deixa de crescer indefinidamente com a capacidade |
| a linha de comando omitia o dispositivo de descarte do carbono incorporado, convertia a potência da motobomba por outra regra e reconstruía a tubulação só com as bitolas de 50, 75, 100 e 150 mm | a avaliação ambiental da linha de comando lê o descarte, a motobomba e a tubulação do projeto, como a interface |
| a linha de comando usava 5.000 sorteios no SMAA-VIKOR e pesos 0,33/0,33/0,34 no TOPSIS; a interface, 20.000 sorteios e 0,333/0,333/0,334 | as duas usam 20.000 sorteios e os mesmos pesos |
| a alternativa sem cisterna entrava no multicritério da interface com payback zero, o melhor possível | alternativa que não se paga entra sem payback, nas duas pontas |
| a lâmina de descarte da primeira chuva valia 1,0 mm no arquivo de projeto, na leitura de planilha e no motor, e 2,0 mm no exportador CAD, na linha de comando e no relatório | o valor de recurso passou a ser 2,0 mm em todos os caminhos, conforme o item 4.1.5 da ABNT NBR 15527:2019; um projeto sem lâmina declarada descarta o dobro do que descartava, e a captação aproveitada cai na medida dos dias de chuva fraca |
| os 34 municípios da CORSAN estavam gravados como uma reta, `PB × C + serviço básico`, com esgoto de 70% sobre a conta inteira, embora a concessionária cobre `PB × Cⁿ + serviço básico` e o esgoto por m³ consumido | a água segue a Tabela de Exponenciais (`n` de 1,00 até 20 m³ a 1,13 entre 101 e 150 m³) e o esgoto, R$ 6,40/m³ no ANEXO-5; em Alegrete, reduzir o consumo de 30 para 20 m³ passou a economizar R$ 253,81 por mês, e não R$ 155,55 |

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
| Um único nome para o grupo de pesquisa: Sustainable Environments Research Group, em português Grupo de Pesquisa em Ambientes Sustentáveis. | nenhum valor calculado muda |
| Os exemplos de Brasília e de Manaus passaram a usar as tarifas oficiais da cidade, em vez das de Florianópolis. | nenhum valor calculado muda |
| Um exemplo novo, `examples/exemplo_quatro_criterios.netuno`, em que os ótimos técnico, econômico, ambiental e TOPSIS caem em quatro volumes diferentes. | nenhum valor calculado muda |
| o modelo de cenários em planilha citava séries de chuva que não são distribuídas, e um cenário sem a sua série era simulado em silêncio com a chuva de Florianópolis | o modelo usa as séries de `data/rainfall`, e a falta de uma série é erro que nomeia o cenário e o arquivo |
| a consulta às tarifas da ANEEL não tinha prazo total e gravava o arquivo em uso enquanto baixava | a consulta desiste após três minutos, e um download interrompido não deixa o cache pela metade |
| as equações do manual perdiam o sobrescrito: o VPL saía com `(1 + TMA) m` | os expoentes voltam a sair sobrescritos |
| na prancha do esquema 3D, cada acessório criava um plano de cota e um rótulo de duas linhas, e as peças ficavam umas sobre as outras | a prancha passou a folha A3 deitada, com planos de cota só nos níveis principais e as peças pequenas identificadas pelo código, com tipo e cota numa tabela ao lado |
| o ladrão sifonado era desenhado atravessado no extravasor, com vão nos dois lados | o sifão segue o sentido do tubo e encosta nas faces da peça |
| a volumetria abria com edificação, terreno, fluxo e sombras ligados, pesada na primeira abertura | abre só com os rótulos; o resto se liga no botão |
| o texto da fórmula exponencial alargava a coluna do Gestor de Tarifas e estreitava os gráficos | os gráficos mantêm a largura em qualquer município |
| os avisos do compilador de sombreadores do Direct3D (X4122, X4000) apareciam como «Qt aviso» | entram só na contagem do resumo; erro de compilação continua aparecendo |
| o CAPEX de tubulação e acessórios era uma verba estimada, e a ACV contava só os metros de tubo digitados; curvas, conexões, peças e cabos de comando do arranjo 3D não entravam em nenhum dos dois | em projeto novo, os dois passam a sair do arranjo, peça por peça, com preço e carbono de cada item; arquivos antigos mantêm os custos que declaravam |
| a mão de obra era fixada uma vez, sobre verbas genéricas, e não mudava com o volume na varredura; a varredura também deixava de cobrar o pressurizador quando não havia caixa superior | em projeto novo, a mão de obra é 30% dos materiais de cada volume, e a motobomba entra em todo arranjo que não seja por gravidade, como no motor econômico |
| o arranjo 3D usual era sempre o de recalque, com uma motobomba | o arranjo segue o abastecimento do projeto (recalque, pressurização ou gravidade) e desenha a motobomba reserva em paralelo; o CAPEX e a ACV deixam de cobrar peças de caixa superior que não existem e passam a cobrar as da reserva |

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
> A seção 2.6 desenvolve a cadeia completa.

---
