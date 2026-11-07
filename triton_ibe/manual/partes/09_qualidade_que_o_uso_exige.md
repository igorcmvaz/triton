# Que qualidade o uso exige

> No fim desta secção, o projeto tem uma linha de tratamento definida, e sabe distinguir o que a norma exige do que o programa recomenda.

Até aqui, o tutorial tratou a água da chuva apenas como volume: quanto se capta, quanto se armazena, quanto se consome. A água é também uma qualidade, e a qualidade custa dinheiro — em equipamento, na instalação, e em consumíveis, todos os meses. Esta secção define a classe de qualidade do projeto e dimensiona a linha de tratamento correspondente.

---

## O que a norma diz, e o que não diz

Em Portugal, a ETA 0701 da ANQIP (versão 7; ver a secção {{n:1}}) trata a qualidade em função do uso. Para a rega de zonas verdes e a lavagem de pavimentos, admite que a água da chuva, cumpridas as prescrições de instalação, pode dispensar qualquer tratamento complementar físico-químico ou bacteriológico (item 4.6.3). Para o autoclismo, só admite a água sem tratamento quando respeita, no mínimo, as normas de qualidade das águas balneares (item 4.6.4); se os valores máximos dos parâmetros microbiológicos não forem cumpridos, prevê a desinfeção por ultravioletas, cloro ou outro processo adequado, e recomenda, no caso do cloro, um residual livre entre 0,2 e 0,6 mg/L (item 4.6.5). Os tratamentos básicos que admite são a filtragem, no filtro de montante, e a sedimentação, na cisterna (item 4.6.2). Não verificado nesta versão: a legislação hoje em vigor sobre a qualidade das águas balneares (a versão 7 da ETA 0701 cita o Decreto-Lei n.º 236/98 e a Diretiva 76/160/CEE), os valores-limite aplicáveis e a revisão em vigor da ETA 0701; confirme-os antes de os usar como critério.

A norma europeia EN 16941-1 também trata do tema, sem dispensar o cumprimento da regulamentação nacional ou local. Não verificado nesta versão: o que a edição em vigor da EN 16941-1 fixa para a qualidade da água e a desinfeção.

Em geral, uma norma para uso não potável fixa uma lista curta de parâmetros mínimos: um indicador microbiológico como a *E. coli*, a turvação e o pH, e, se houver cloro, um intervalo para o residual livre. A desinfeção fica muitas vezes a critério do projetista, e a monitorização pede-se com uma periodicidade indicada. Verifique a norma aplicável ao local do projeto e introduza os seus limites como critério.

O programa, por seu lado, oferece quatro classes, e a razão é prática: o autoclismo e a rega do jardim não expõem o utilizador da mesma maneira, ainda que uma norma os não distinga ({{fig:fig36_classes}}).

> **Reutilização não é aproveitamento.** Os parâmetros fixados para a **reutilização** de águas residuais tratadas costumam ser muito mais restritivos do que os do aproveitamento da água da chuva: ausência de coliformes, residual de cloro mais alto e turvação mais baixa. A água da chuva não é reutilização, e a tabela que se aplica ao aproveitamento é a da norma da água da chuva, não a da norma de reutilização.

![As quatro classes de qualidade do programa](../figuras/fig36_classes.png)

*Figura 99 — As quatro classes de qualidade do programa e a situação de cada uma. A classe 1 é o conjunto mínimo de referência, com os parâmetros menos exigentes; as classes 2 a 4 são adaptações do programa, adequadas para comparar tratamentos e impróprias para apresentar como exigência normativa.*


> **As classes 2 a 4 são adaptações do programa, não de uma norma.** O próprio Triton o declara no ecrã e no relatório. Num estudo publicado, não as apresente como exigência normativa: apresente-as como critério adotado, e cite a origem.

---

## A classe recomenda, o utilizador decide

Escolher uma classe não impõe nenhum equipamento ao projeto. A classe exprime uma recomendação do programa, fundada na exigência típica do uso pretendido, e a decisão de a adotar ou não fica com quem assina o projeto.

<!-- inclui: _tabelas/cap09_etap.md -->

A segunda tabela revela o ponto: sem o filtro de polimento, as quatro classes custam exatamente o mesmo. A classe-alvo altera uma única coisa, que é se o programa recomenda ou não a filtração fina, e o filtro correspondente só entra no orçamento quando o utilizador o assinala explicitamente.

Quando a classe recomenda o polimento e o utilizador o recusa, o programa regista a recusa no relatório, em vez de impor o equipamento em silêncio ou de deixar a decisão passar sem registo. ==É a conduta correta em qualquer programa de projeto: quem assina decide, e a decisão fica documentada para quem vier depois.==

---

## A desinfeção

A desinfeção é a etapa de que depende a segurança microbiológica da água armazenada, e o programa oferece três tecnologias. A diferença entre elas é grande, em custo e em comportamento, e o critério que as separa não é a eficácia de desinfeção — as três desinfetam — mas a persistência do efeito.

**Cloragem por pastilhas.** Um doseador com pastilhas de hipoclorito de cálcio na linha, numa só etapa. É a opção predefinida. Deixa **residual** na água, o que protege o reservatório e a rede interior contra a recontaminação. A edição não traz catálogo de equipamentos, pelo que o custo da linha é o que indicar na etapa económica, a partir dos seus orçamentos; este manual não cita nenhum preço de equipamento de tratamento.

**Ultravioleta.** Um reator com lâmpada UV, numa segunda etapa a seguir à cloragem. A lâmpada e o reator consomem 37,5 kWh por ano neste projeto. **Não deixa residual**: desinfeta o que passa por ele, e nada protege a água depois.

**Ozonização.** Também uma segunda etapa a seguir à cloragem, também sem residual.

> **Atenção.** No programa, o ultravioleta e o ozono entram como barreira **adicional** à cloragem, não como substitutos. É a prática correta: sem residual, a água tratada volta a contaminar-se no caminho até ao ponto de uso.
>
> Por isso, as linhas de UV e de ozono somam-se à do cloro em vez de a substituir. Quem esperava que trocar o cloro pelo UV **reduzisse** o custo verá o contrário.

O impacto de carbono segue a mesma ordem: 0,2 kg CO₂e por ano com cloragem, 18,2 com ultravioleta e 15,2 com ozonização, para o volume tratado neste projeto, com o fator de rede ilustrativo de 0,40 kg CO₂e/kWh. A diferença está toda na eletricidade consumida pela lâmpada e pelo gerador de ozono, já que o consumível químico da cloragem tem uma emissão de fabrico modesta em comparação.

---

## O filtro de entrada

Antes de qualquer desinfeção vem o filtro mecânico de entrada, que retira folhas e sólidos grosseiros da água antes de ela chegar ao reservatório. O programa dimensiona-o pela área da cobertura, e não pela classe de qualidade pretendida, porque o que este filtro tem de vencer é o caudal de ponta da cobertura — uma grandeza que não depende do destino final da água.

<!-- tabela: Filtro mecânico de entrada dimensionado pela área da cobertura -->
| Cobertura | Filtro | Malha |
| :--- | :--- | ---: |
| até 200 m² | vórtex autolimpante DN 100 | 350 µm |
| até 500 m² | vórtex autolimpante DN 150 | 400 µm |
| acima | cesto ou ciclónico DN 200 | 500 µm |

A nossa cobertura de 150 m² fica no primeiro escalão. Estes filtros retêm partículas de algumas centenas de micrómetros, muito abaixo de um milímetro; a ETA 0701 recomenda, para o filtro a montante da cisterna, uma malha entre 0,2 mm e 0,8 mm (item 4.4.2).

---

## A regra incremental do custo

O investimento na linha de tratamento não se soma por inteiro ao investimento total do sistema, para evitar a dupla contagem. O orçamento de um sistema pluvial já reserva uma verba genérica de tratamento na rubrica dos acessórios, porque nenhum projetista orça um sistema sem prever alguma filtragem; somar a linha detalhada por cima dessa verba cobraria o tratamento duas vezes. O programa desconta a verba genérica e soma só o incremento, como a Equação {{eq:capex_etap}} formaliza na secção {{n:27}}.

O mesmo vale para o custo de exploração: a cloragem já se paga na linha de consumíveis químicos do fluxo de caixa, e a linha de tratamento desconta essa parcela para não cobrar duas vezes o hipoclorito.

E na avaliação do ciclo de vida, a linha de tratamento **substitui** o termo da cloragem em vez de se lhe somar. A secção {{n:27}} detalha a regra.

---

## A decisão do tutorial

**Classe 1, cloragem por pastilhas, sem filtro de polimento.**

A água vai para o autoclismo e para a área exterior. A classe 1, o conjunto mínimo de referência do programa (um limite de *E. coli*, a turvação e o pH, com um intervalo de cloro livre), cobre ambos. Um projeto que acrescente a máquina de lavar roupa sai dos usos que a maioria das normas lista, e o responsável tem de definir e declarar o critério de qualidade para ela, como a secção {{n:5}} regista. A cloragem deixa residual, é a mais simples das três linhas, e tem a energia e o carbono mais baixos: 0,2 kg CO₂e por ano. O descarte inicial dimensiona-se na mesma etapa; a sua câmara é a de 300 L da secção {{n:4}}.

<!-- tabela: Estado do projeto do tutorial depois da definição da classe de qualidade -->
| Projeto até aqui | |
| :--- | ---: |
| volume | 5 000 L |
| classe de qualidade | 1, conjunto mínimo de referência |
| desinfeção | cloragem por pastilhas |
| filtro de polimento | não |
| carbono anual da linha de tratamento | 0,2 kg CO₂e |

Temos volume, arranjo e qualidade. Agora, a pergunta que decide se o projeto sai do papel.
