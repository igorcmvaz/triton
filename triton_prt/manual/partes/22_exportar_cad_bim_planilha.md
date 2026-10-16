# Exportar para CAD, BIM e folha de cálculo

> **Pergunta que este guia responde:** como levar o resultado para o projeto de execução e para a
> análise própria?

---

## O que cada formato leva

<!-- tabela: Formatos de exportação e finalidade de cada um -->
| Formato | Extensão | O que leva | Para quê |
| :--- | :--- | :--- | :--- |
| relatório | HTML, PDF | resultado completo e pressupostos | entregar |
| folha de cálculo | XLSX | série diária e varredura | reanalisar |
| auditoria | XLSX | todos os campos dos pressupostos, do tarifário, do tratamento, da ACV, da economia e do arranjo | conferir |
| desenho | DXF | esquema hidráulico dimensionado | projeto de execução |
| manifesto BIM | JSON | componentes com tipo, posição, nível e parâmetros | importação no Revit |
| projeto | TRITON | todas as etapas e a série de chuva | reabrir e auditar |

---

## O ficheiro de projeto

O formato `.triton` é o único que guarda o estudo inteiro: as nove etapas, os pesos do
multicritério, as rotas de ACV e a **série diária de chuva**, incorporada no próprio ficheiro.
Um `.triton` reabre noutro computador sem o CSV de origem e reproduz o mesmo número; é com ele
que se distribuem os casos do apêndice {{n:J}}. O formato CSV antigo de uma ferramenta anterior
continua disponível na exportação, assinalado como legado, porque não preserva as etapas
acrescentadas desde então.

---

## Folha de cálculo

A exportação para folha de cálculo é o caminho de quem pretende fazer análise própria dos
resultados, seja para construir um gráfico que o programa não oferece, seja para combinar os
números do Triton com dados de outra origem. Estão disponíveis dois conjuntos de dados, que
respondem a perguntas diferentes.

A **série diária** traz uma linha por dia simulado, com a chuva registada, a chuva efetiva depois
do descarte, o volume captado, a procura do dia, o consumo pluvial, o consumo da rede, o
extravasamento, o volume armazenado nos dois reservatórios, o volume elevado e a classe de
abastecimento. É a base de qualquer gráfico ou estatística que o programa não ofereça pronta, e é
o que se usa quando a análise pretendida difere da que o programa faz.

A **varredura** traz uma linha por volume simulado, com todos os indicadores calculados para cada
um. É a base da curva de retorno decrescente apresentada na secção {{n:7}}, e o formato adequado
para quem a queira redesenhar com outra apresentação.

A etapa **10. Exportação** monta a folha de cálculo a partir de seis conjuntos, que se marcam um
a um: o resumo executivo com os metadados do projeto, o balanço hídrico diário, a curva da
varredura com a fiabilidade, o fluxo de caixa ano a ano, o inventário de ciclo de vida e a matriz
de decisão multicritério. Três escolhas completam a exportação:

<!-- tabela: Opções da exportação para folha de cálculo e quando usar cada uma -->
| Opção | Escolhas | Quando usar |
| :--- | :--- | :--- |
| formato | XLSX, CSV ou JSON | XLSX para abrir no Excel; CSV para R, Python ou outro programa; JSON para integração |
| separador do CSV | ponto e vírgula ou vírgula | ponto e vírgula no Excel em português; vírgula no R e na maior parte das ferramentas internacionais |
| filtro temporal | primeiro ano típico ou série completa | o ano para ilustrar; a série completa para qualquer estatística |
| horizonte económico | 10, 20, 25 ou 30 anos | 20 anos, uma vida útil de projeto habitual para componentes de canalização, salvo justificação em contrário |

### Exportar tudo, para auditoria

O botão **Exportar TUDO (auditoria)**, ao lado da exportação para folha de cálculo, grava um só
ficheiro Excel com as seis folhas acima e, além delas, folhas que ninguém escolhe: percorrem
**todos** os campos do que o programa usou. São os pressupostos do projeto, uma linha por
parâmetro, com o valor e a descrição tirada do próprio código; o tarifário aplicado, com o
significado de cada código de escalão, o regime, o modo do saneamento e a fatura para consumos de
0 a 50 m³; a linha de tratamento dimensionada na etapa da qualidade, com os estágios, as doses e
o carbono que a ACV soma; o inventário de ciclo de vida item a item; os resultados da simulação,
da economia e do multicritério; e o arranjo 3D, com cada peça, cada troço e o quantitativo por
diâmetro. A folha «0_Leia_me» diz o que há em cada uma.

É o ficheiro para quem precisa de conferir uma conta do princípio ao fim, ou de responder a um
avaliador que pergunte o que entrou no carbono ou na economia. Um parâmetro novo no programa
aparece nele sem que ninguém tenha de se lembrar de o acrescentar.

> **Um aviso de tamanho.** Trinta anos de série diária são 10 950 linhas por simulação. Uma
> varredura de doze volumes com série detalhada gera cento e trinta mil linhas. Exporte a série
> detalhada só do volume que interessa.

---

## Desenho em DXF

O programa gera o esquema hidráulico do sistema dimensionado: cisterna, filtro, descarte, bomba
quando houver, reservatório superior, e a tubagem com os diâmetros adotados.

O que o programa produz é um **esquema**, e não um projeto de execução. Representa os componentes
do sistema e as ligações lógicas entre eles, com os diâmetros adotados, e serve de base para que
o projetista desenhe a instalação em planta, com as cotas, o traçado e as interferências reais do
edifício. ==Um esquema não substitui o projeto de águas, e entregá-lo como tal seria um erro de
responsabilidade técnica.==

O esquema também não traz, e o projeto de execução tem de acrescentar, os requisitos de instalação
predial para água não potável. Em Portugal, o ponto de partida para os sistemas de aproveitamento
de águas pluviais em edifícios são a especificação técnica **ETA 0701** da ANQIP (Associação
Nacional para a Qualidade nas Instalações Prediais), na versão 12 que a associação disponibiliza,
e a norma europeia **EN 16941-1**, que trata do projeto, dimensionamento, instalação,
identificação, entrada em serviço e manutenção destes sistemas para usos não potáveis. Os
requisitos habituais, a verificar nesses documentos e na regulamentação em vigor, são:

- tubagem de água da chuva identificada por cor e por inscrição de água não potável, a
  intervalos regulares nos troços à vista;
- rede de distribuição independente da de água potável, sem ligação cruzada, com separação
  atmosférica na alimentação de reserva a partir da rede pública;
- pontos de utilização de uso restrito, como a torneira do jardim, com placa de água não
  potável;
- reservatórios de água potável e não potável separados, com separação clara entre eles;
- bombagem de acordo com as regras de abastecimento de água a edifícios, que em regra pedem uma
  bomba de reserva.

[A COMPLETAR: cores, inscrições, distâncias de separação e requisitos de bombagem exatos da ETA
0701 (versão 12) e da EN 16941-1, e do regulamento nacional de distribuição predial de água; não
foram lidos nesta revisão. Ver `auditoria/pendencias_manual_prt_cap16-30.md`.]

O que o programa **não** dimensiona:

- traçado e inclinação da tubagem;
- perda de carga real da instalação;
- arranjo hidráulico do dispositivo de descarte, de que o programa calcula apenas o volume,
  `A × d_f`, e o custo;
- descarga de superfície e ligação à drenagem;
- fundação e impermeabilização da cisterna.

---

## Biblioteca de blocos e manifesto BIM

Na etapa **10. Exportação**, o modo *Biblioteca de Blocos para Plantas + BIM JSON* grava os
blocos DXF dos componentes à escala 1:1, em milímetros, e, ao lado deles, o ficheiro
`*_triton-bim.json`. O programa não exporta IFC. O manifesto JSON é o contrato entre o
dimensionamento e o modelo: cada instância declara o tipo do componente, o nível, a posição local
em milímetros, a rotação e os parâmetros dimensionados, como a capacidade e o diâmetro, e a
estrutura é validada antes de ser gravada.

A integração com o Autodesk Revit faz-se por um importador distribuído com o programa, executado
no motor CPython 3 do pyRevit, com um documento aberto no Revit 2022 ou posterior, e insere as
instâncias do manifesto usando as famílias indicadas em `family_mapping.json`, que associa cada
tipo do programa (cisterna, reservatório superior, filtro, descarte inicial, grupo
eletrobomba, válvulas de seccionamento, válvula de retenção, separação atmosférica, descarga de
superfície, ponto de utilização não potável, entrada tranquilizada, aspiração flutuante,
interruptor de nível, eletroválvula, contador de água, válvula de pé com ralo, respiro e quadro
de comando) a uma família e a um tipo do gabinete.

Sem organização guardada, o programa pré-preenche o arranjo habitual destas instalações, a partir
do estudo: captação da cobertura, filtro e descarte inicial; cisterna com entrada tranquilizada,
aspiração flutuante com válvula de pé e ralo, interruptor de nível contra o funcionamento a seco,
respiro com rede e descarga de superfície com sifão e válvula antirretorno para a rede pluvial;
válvulas de seccionamento dos dois lados do grupo eletrobomba, válvula de retenção na elevação e
quadro de comando; reservatório superior com interruptor de nível, respiro com rede, descarga de
superfície com saída visível, esgoto de limpeza com válvula junto à saída e distribuição com
válvula até um ponto de utilização identificado; e o abastecimento potável de reserva (contador,
válvula e eletroválvula), que só abre quando falta água da chuva e descarrega no reservatório
superior por separação atmosférica, como a boa prática pede. Quem decide é o quadro de comando:
com o reservatório superior no nível de arranque e água na cisterna, liga a eletrobomba; com a
cisterna no mínimo, bloqueia a eletrobomba e abre a eletroválvula, que enche o reservatório só até
à bóia de reserva, mais baixa, para sobrar volume para a chuva seguinte. Eletrobomba e
eletroválvula nunca funcionam juntas. Na volumetria, os cabos de comando (dos interruptores de
nível ao quadro e deste à eletrobomba e à eletroválvula) aparecem a tracejado, e a lógica
completa está na ficha do quadro. O arranjo é um ponto de partida: posições, percursos e peças
são do projetista.

O arranjo segue duas escolhas do projeto:

- **Número de eletrobombas.** Com duas, a de reserva é desenhada em paralelo com a principal, com
  válvula de seccionamento na aspiração, válvula de retenção e válvula de seccionamento na
  elevação próprias. Liga-se às linhas da principal por tês.
- **Arranjo de abastecimento.** Muda o que existe na instalação:
  - **Elevação para reservatório superior:** é o arranjo descrito acima.
  - **Pressurização direta:** não há reservatório superior. O sobrepressor leva a água da cisterna
    diretamente ao ponto de utilização. O abastecimento potável de reserva descarrega na própria
    cisterna, também por separação atmosférica, e só até uma bóia de reserva instalada nela.
  - **Gravidade:** não há bomba. A cisterna fica sobre uma base, acima do ponto de utilização, e a
    água sai por uma saída lateral baixa com válvula. O abastecimento potável de reserva
    descarrega na cisterna, como na pressurização.

Enquanto os troços não estão organizados, o arranjo é refeito a cada mudança do volume, do
abastecimento ou do número de bombas.

Com estes dados, o programa monta também a prancha do esquema 3D, fora de escala e em folha A3 na
horizontal. Só os níveis que organizam a instalação (cisterna, reservatório superior, grupo
eletrobomba, filtro e descarte) ganham plano de cota; as peças pequenas aparecem no desenho pelo
código, e o tipo e a cota de cada uma estão na tabela «Peças e acessórios», ao lado da sequência
de montagem e do quantitativo por diâmetro.

O importador não cria famílias nem substitui componentes por aproximação: uma instância sem
família ou sem nível correspondente fica listada como pendente no fim da importação. As
coordenadas são locais, e a amarração ao ponto de base e ao norte do projeto faz-se no Revit,
pelo projetista. O manifesto serve a coordenação e o levantamento de quantidades, e não substitui
a modelação da instalação de águas.

### Do arranjo ao CAPEX e à ACV

O mesmo arranjo alimenta o custo e o carbono. O programa levanta, peça a peça:

- os metros de tubo por diâmetro;
- as curvas, uma por mudança de direção do percurso;
- as ligações, uma em cada extremo de percurso ligado a uma peça;
- cada peça do manifesto, por tipo;
- os metros de cabo de comando.

Cada item recebe um preço e uma massa. O preço vai para o CAPEX: tubos e ligações em *Tubagem*,
peças e cabos em *Acessórios*. A massa, vezes o fator do material, vai para a ACV na etapa A1–A3.
Cisterna, reservatório superior e grupo eletrobomba já têm linha própria nas duas análises e não
são contados de novo. O filtro e o descarte inicial entram no CAPEX pela linha de tratamento,
quando está ativa, e na ACV pelo subsistema de descarte, quando está ativo.

Um teste automático confere que nenhuma peça, nenhum metro de tubo, nenhuma curva, nenhum tê e
nenhum cabo do arranjo fica sem custo ou sem carbono. O teste cobre os três arranjos de
abastecimento, com uma e com duas eletrobombas. A folha `Auditoria_Quantitativo` do *Exportar
tudo* lista cada item com o seu destino no CAPEX e na ACV, e fecha a soma contra os valores que as
análises usaram. A mesma folha confere ainda se o arranjo é coerente com o projeto: um arranjo
organizado à mão pode ficar para trás quando o projeto muda o abastecimento ou o número de
bombas, e a divergência aparece aí.

Os preços e as massas das peças são um cenário de referência, e não uma cotação. Estão em
`costs_database.json`, na chave `pecas_do_arranjo`, e podem ser alterados aí. Na etapa económica,
o projetista pode também digitar outros valores de tubagem e acessórios: a partir daí o programa
usa os valores digitados. Um projeto novo parte do arranjo. Um ficheiro antigo mantém os custos
que já declarava. Na Edição Portugal o programa não aplica os preços de referência da base de
custos: os custos são digitados, em euros, e os casos do próprio manual usam números redondos
declarados como ilustrativos, não como preços de mercado.

---

## Relatórios

Os três da secção {{n:13}}: executivo, ambiental com ESG, e científico. Em HTML para consulta e em
PDF para entrega.

> O programa tem dois geradores de PDF e usa o mais completo que o computador permitir. Quando
> recorre ao alternativo, o documento sai mais simples, com o mesmo conteúdo e os mesmos números.

---

## Um conselho de arquivo

Ao fechar um estudo, guarde junto, na mesma pasta:

1. o ficheiro `.triton`;
2. a **série de chuva** usada, ou a sua identificação exata na base;
3. o relatório científico em PDF;
4. a folha de cálculo da varredura;
5. se houve execução em lote, o **script** com os comandos;
6. um ficheiro de texto com a **versão do programa**.

São seis itens que tornam o estudo reprodutível daqui a cinco anos. Sem eles, o relatório em PDF
é só uma afirmação.
