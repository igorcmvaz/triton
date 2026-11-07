# Precisa de reservatório superior?

> No fim desta secção, sabe responder à pergunta com um número, e não por hábito. A resposta costuma surpreender.

O arranjo clássico do aproveitamento pluvial emprega dois reservatórios: uma cisterna enterrada, que recebe a água da cobertura, e um reservatório elevado, que alimenta os pontos de consumo por gravidade; entre os dois, uma eletrobomba faz a elevação. O arranjo é tão difundido que quase todos os projetos o adotam sem examinar a razão, e esta secção examina-a.

---

## Para que serve o reservatório superior

==O reservatório superior não serve para guardar mais água; serve para a entregar.== A distinção parece subtil e decide toda a análise, porque tudo o que se segue depende de não confundir capacidade de armazenamento com capacidade de distribuição.

A cisterna está enterrada, e os pontos de consumo — autoclismo, tanque, torneira de jardim — ficam acima dela. Alguma coisa tem de vencer esse desnível, e há duas maneiras de o fazer com bomba.

- **Pressurização direta.** Uma bomba pequena com pressostato liga sempre que se abre um ponto de consumo. Não há reservatório superior.
- **Elevação para um reservatório elevado.** A bomba enche o reservatório de tempos a tempos, e a gravidade faz o resto.

Quando a cisterna fica acima dos pontos de uso, há ainda uma terceira: a **gravidade**, sem bomba. A etapa **4. Reservatório & Custos** pergunta qual dos três arranjos o projeto adota, e é esta resposta que define a energia e as eletrobombas no custo e no carbono.

<!-- tabela: Os três arranjos de abastecimento e o que cada um acrescenta ao projeto -->
| Arranjo | Energia calculada | Reservatório superior e eletrobombas |
| :--- | :--- | :--- |
| elevação para reservatório superior | volume elevado, pela altura manométrica, mais os arranques | entram no custo e no carbono |
| pressurização direta | todo o volume pluvial consumido, pela pressão de trabalho | só as eletrobombas |
| gravidade | nenhuma | nenhuma |

Na pressurização direta, a etapa 4 pede o modelo do sobrepressor, escolhido num catálogo de seis modelos genéricos de referência, de A a F, cada um com uma curva caudal × pressão ilustrativa (nenhum é um produto real), a pressão de trabalho e o caudal do ponto de uso. O sobrepressor liga a cada descarga, 5,05 por pessoa e por dia segundo o levantamento de usos finais de Mayer et al. (1999), e fica ligado enquanto o autoclismo acoplado enche, ao ritmo da torneira de bóia. A energia é esse tempo vezes a potência elétrica. No tutorial, a uma pressão de 18 m, o menor modelo gastaria 26,7 kWh por ano, cerca de cinco vezes os 5,3 kWh da elevação; a secção {{n:28}} explica porquê e mostra que o modelo escolhido pesa mais do que a pressão. Não verificado nesta versão: o valor de 5,05 descargas por pessoa e por dia e a referência de Mayer et al. (1999) numa fonte aberta; uma consulta de 24/10/2026 não o confirmou.

A elevação para um reservatório elevado tem três vantagens práticas reais. A eletrobomba liga poucas vezes por dia, em vez de dezenas, o que prolonga a vida do equipamento; a pressão nos pontos de consumo é constante, porque decorre da altura da coluna de água e não do funcionamento da bomba; e há reserva disponível durante uma falha de energia. ==Nenhuma destas três vantagens é poupança de água==, e é justamente essa a confusão que a secção desfaz.

---

## A comparação justa

Comparar um sistema de 5 000 L sem reservatório elevado com outro de 5 000 L mais 1 000 L de reservatório superior é uma armadilha metodológica, porque o segundo dispõe de mais armazenamento total e ganharia por essa razão, não pelo arranjo. Para isolar o efeito do arranjo, é preciso manter o armazenamento constante: comparam-se, portanto, 6 000 L num único reservatório contra 5 000 L em baixo mais 1 000 L em cima.

<!-- inclui: _tabelas/cap08_reservatorio_superior.md -->

Com o mesmo armazenamento, o arranjo com reservatório elevado entrega 0,32 pontos percentuais a menos de economia do que o reservatório único (18,28% contra 18,59%). A diferença não é erro de arredondamento, e tem uma causa: **a cisterna extravasa enquanto o reservatório superior ainda tem espaço**.

A chuva entra só pela cisterna, e o extravasamento é calculado nela antes do consumo do dia. A elevação, porém, só acontece quando há consumo e o reservatório superior desce abaixo do limiar de acionamento. Assim, num dia de chuva com a cisterna cheia, a água que excede os 5 000 L de baixo perde-se mesmo que o reservatório de cima tenha centenas de litros livres. Um reservatório único de 6 000 L guardá-la-ia.

É também por isso que um limiar de acionamento maior rende mais: com ele, a bomba enche o reservatório mais cedo, a cisterna está mais vazia quando a chuva chega, e extravasa menos. A reserva abaixo do limiar não fica imobilizada, porque é consumida logo a seguir a cada elevação e quando a cisterna seca.

> **O reservatório superior não aumenta a poupança de água. Custa.** No nosso projeto, custa o reservatório, custa a bomba, custa 5,3 kWh por ano de energia, e custa 0,32 pontos de potencial em relação a um reservatório único do mesmo volume total.
>
> Isto não o torna errado. Torna a decisão **hidráulica**, e não hídrica: adote-o se o projeto precisa de pressão por gravidade ou de reserva contra falhas de energia, e não à espera de que renda mais água.

---

## O limiar de acionamento

Se adotar o reservatório superior, há um parâmetro a ajustar: o volume de reserva que não se consome, abaixo do qual a bomba arranca.

<!-- inclui: _tabelas/cap08_limiar.md -->

Um limiar maior significa **mais potencial e mais arranques**, pela razão acima. De 0 para 500 L, o potencial sobe 0,19 pontos (de 18,23% para 18,42%) e os arranques passam de 46 para 83 por ano.

A troca é entre um ganho hídrico marginal e o desgaste da eletrobomba. As eletrobombas residenciais suportam bem alguns arranques por dia; o que as mata é o liga-desliga contínuo. Oitenta e três arranques por ano são menos de dois por semana, e nenhum dos valores da tabela chega perto de ser um problema.

> **Onde o limiar importa a sério** é nos edifícios com procura concentrada, em que o reservatório esvazia depressa. Aí pode passar dos mil arranques por ano, e convém dimensionar o reservatório em vez de mexer no limiar.

---

## A energia, e porque é pequena

Cinco vírgula três quilowatts-hora por ano. A 0,20 € por quilowatt-hora, valor ilustrativo, não é preço de mercado, são 1,05 € por ano.

Parece pouco demais, e vale a pena perceber porquê. Elevar um metro cúbico de água a dez metros custa, em energia hidráulica, cerca de 0,027 kWh. Com os rendimentos da bomba e do motor, e somados os arranques, o programa chega a cerca de 0,13 kWh por metro cúbico elevado. Os 40,1 metros cúbicos elevados por ano dão os 5,3 quilowatts-hora da tabela.

A água é pesada, mas a altura de um edifício pequeno é pouca. É por isso que o custo energético do aproveitamento pluvial é desprezável face à poupança na fatura da água e do saneamento — e é por isso também que o argumento de que «bombear água gasta mais energia do que poupa» não se sustenta num edifício de pequeno porte.

> **Atenção à potência de placa.** O programa pede o rendimento **da bomba** e o rendimento **do motor** em separado. A potência de placa é a potência mecânica no veio, e o rendimento do motor é o que separa o que o veio entrega do que o contador regista. Em branco, o programa adota um rendimento de motor por omissão, que depende da potência nominal; substitua-o pelo valor da ficha técnica do motor. A secção {{n:28}} detalha.

---

## A decisão do tutorial

**Adotamos a elevação para um reservatório superior de 1 000 L, com limiar de 100 L.**

A decisão é hidráulica, e não hídrica. O reservatório elevado dá pressão constante nos pontos de uso sem depender da bomba a cada descarga, mantém água disponível durante uma falha de energia e faz a eletrobomba arrancar 51 vezes por ano, em vez das mais de sete mil partidas de um sobrepressor acionado a cada descarga por quatro moradores, que gastaria entre 27 e 69 kWh por ano conforme o modelo genérico. O preço é o que a tabela mostra: o reservatório, as bombas, 5,3 kWh por ano e 0,32 pontos de potencial face a um reservatório único de 6 000 L. As bombas são duas, a principal e a de reserva, a precaução habitual num sistema de elevação de que o edifício não pode prescindir.

Em relação à cisterna de 5 000 L sozinha, o potencial sobe de 17,87% para 18,28%, porque o reservatório acrescenta 1 000 L de armazenamento. Daqui em diante, o custo, o carbono e a decisão do tutorial incluem o reservatório superior, as duas eletrobombas e a energia da elevação.

<!-- tabela: Estado do projeto do tutorial depois da decisão sobre o reservatório superior -->
| Projeto até aqui | |
| :--- | ---: |
| volume do reservatório inferior | 5 000 L |
| arranjo | elevação para reservatório superior |
| reservatório superior | 1 000 L, limiar de 100 L |
| potencial de economia | 18,28% |

Já sabemos quanta água o sistema entrega. Falta saber **que água** é essa.
