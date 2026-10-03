# Instalação e primeira execução

> Ao terminar esta seção você terá o programa instalado, aberto, e uma simulação
> concluída com um resultado que dá para conferir contra este manual.

---

## O que você precisa

<!-- tabela: Requisitos de sistema para instalar e executar o programa -->
| Requisito | O que é preciso |
| :--- | :--- |
| sistema | Windows 10 ou 11, 64 bits |
| espaço em disco | cerca de 1,5 GB, já com a base climática nacional |
| memória | 4 GB bastam; 8 GB deixam a varredura mais confortável |
| privilégios | de administrador para instalar para todos os usuários; sem eles, a instalação vai para a pasta do usuário |

Nada além disso precisa ser instalado. O programa é distribuído já montado, com todos os
componentes de que depende para calcular, e não requer instalação prévia de
interpretadores, bibliotecas ou pacotes auxiliares. Também não requer conexão com a
internet para funcionar: tudo o que ele consulta durante uma simulação está no próprio
computador.

---

## As duas edições

O programa tem duas edições, com instaladores próprios, que podem ficar instaladas lado a
lado. O selo verde (BRL) ou azul (INT) no alto da barra lateral, o título da janela e o
rodapé de cada relatório e exportação dizem de qual edição saiu o estudo.

<!-- tabela: O que muda entre a Edição Brasil e a International Edition -->
| | Edição Brasil (BRL) | International Edition (INT) |
| :--- | :--- | :--- |
| instalador | `Netuno_Setup_5_0_0.exe` | `Netuno_INT_Setup_5_0_0.exe` |
| idioma ao abrir | português | inglês |
| chuva | base CLIMBra (652 cidades) ou série própria | série própria |
| tarifas de água e esgoto | catálogo de 652 municípios ou digitadas | digitadas |
| energia | tarifa da ANEEL ou digitada; bandeiras tarifárias | digitada |
| moeda e custos | reais, com preços de referência | moeda escolhida; custos digitados |
| fator de emissão da rede e da água potável | bases brasileiras (MCTI, rotas por região) | do país do projeto, obrigatórios |
| certificações e incentivos | LEED, EDGE, AQUA-HQE, Selo Casa Azul, IPTU Verde | LEED, EDGE |

Sem os fatores de emissão do país, a International Edition não calcula a avaliação
ambiental: um fator brasileiro aplicado a outro país daria um resultado errado sem
nenhum aviso.

---

## A instalação

1. Execute **`Netuno_Setup_5_0_0.exe`**. O instalador pergunta se a instalação é para
   todos os usuários, o que exige administrador, ou só para você.
2. Escolha o idioma da instalação e aceite a licença, a GPL versão 3.
3. Escolha o tipo de instalação. A **padrão** traz o programa, o manual, os casos, os
   exemplos e todos os idiomas. A **personalizada** permite desmarcar os pacotes de
   idioma espanhol e chinês. Na Edição Brasil, a base climática nacional vai sempre
   junto, embutida no programa.
4. Aceite a pasta sugerida, `C:\Program Files\Netuno 5`, ou escolha outra.
5. Marque, se quiser, **criar ícone na área de trabalho**. A opção **abrir arquivos
   .netuno com o Netuno 5** vem marcada: com ela, um duplo clique num projeto o abre
   diretamente no programa.
6. Ao terminar, o instalador oferece abrir o programa.

Depois disso, o menu Iniciar traz dois atalhos: **Netuno 5**, o programa, e **Manual do
Netuno 5**, este documento em PDF. Para desinstalar, use *Aplicativos e recursos* do
Windows, como em qualquer programa; os seus projetos ficam onde foram salvos.

> **O que o instalador coloca no computador.** O programa, as quatro séries
> históricas de chuva que acompanham a instalação, a base de tarifas dos 652
> municípios e os arquivos de exemplo. Nada é baixado durante o uso: o Netuno
> funciona sem conexão com a internet.

---

## Onde ficam os seus arquivos

O programa nunca decide por você onde salvar. Cada vez que você grava um projeto, um
relatório ou uma exportação, ele pergunta a pasta.

<!-- tabela: Formatos de arquivo que o programa grava e o conteúdo de cada um -->
| O que você grava | Extensão | Contém |
| :--- | :--- | :--- |
| projeto | `.netuno` | todos os dados de entrada **e a série de chuva** |
| relatório | `.pdf` | o documento completo do estudo |
| resultados | `.xlsx`, `.csv` | as tabelas, para planilha |
| esquema | `.dxf` | o desenho esquemático, para CAD |

Entre esses formatos, o `.netuno` é o que realmente importa guardar. Ele é autocontido:
leva a série de chuva inteira dentro de si, e por isso abre em qualquer outro computador
mesmo na ausência dos arquivos que lhe deram origem. ==É também o arquivo que se anexa a
um artigo para que outra pessoa reproduza o estudo,== e essa propriedade é o que separa
um trabalho verificável de um trabalho apenas relatado.

---

## A base climática

O programa traz quatro séries históricas longas prontas para uso — Florianópolis,
Brasília, Manaus e São Paulo — e aceita qualquer série própria em CSV.

Além delas, a Edição Brasil traz a **base climática nacional**: 652 cidades, 19 modelos
climáticos do CMIP6 e 2 cenários futuros, SSP2-4.5 e SSP5-8.5, extraída do conjunto
CLIMBra. Os arquivos originais somam cerca de 6,5 GB. O programa os traz compactados num
único banco, de cerca de 800 MB, que vai embutido no instalador. Não há nada a baixar
nem a copiar: a base aparece na primeira tela como uma lista de cidades.

O apêndice {{n:E}} descreve a base, e a seção {{n:15}} mostra como usar um cenário futuro.

---

## Os arquivos de exemplo

O manual vem acompanhado de projetos prontos, que reproduzem os resultados impressos
aqui.

<!-- tabela: Arquivos de exemplo distribuídos com o programa -->
| Arquivo | Para que serve |
| :--- | :--- |
| `casos\01_tutorial_florianopolis.netuno` | o projeto que o capítulo {{c:2}} constrói, pronto |
| `casos\03_dez_dias.netuno` | o caso didático de dez dias da seção {{n:23}} |
| `casos\05_manaus.netuno` e os seguintes | o mesmo projeto em outras capitais |
| `exemplos\*.netuno` | três estudos completos: residência, escritório e escola |

Eles ficam na pasta do programa. O apêndice {{n:J}} lista os nove casos do manual, com o
capítulo de cada um e o resultado que produzem.

Convém começar pelo caso de dez dias. Abra-o, execute a simulação e compare o resultado
com a tabela impressa na seção {{n:23}}. A coincidência entre os dois confirma que a
instalação corresponde exatamente a este manual; a divergência indica que manual e
programa são de versões diferentes, e a seção {{n:38}} explica como proceder nesse caso.

---

## A primeira simulação, em cinco minutos

O programa é organizado em **etapas**, na barra lateral esquerda, na ordem em que se
trabalha. Para a primeira simulação bastam quatro delas.

1. **Projeto e Chuva.** Escolha a cidade na base climática, ou carregue o arquivo
   `Florianopolis1.csv` que acompanha o programa. Informe a área de captação de
   150 m², o coeficiente de escoamento de 0,85 e o descarte de 2,0 mm.
2. **Edificação e Consumo.** Escolha residencial unifamiliar, 4 moradores, 150 litros
   por habitante e dia, e fração atendível de 28%.
3. **Reservatório & Custos.** Informe volume fixo de 4.000 L.
4. Rode, e vá a **Resultados Técnicos**.

Você deve obter potencial de economia próximo de **27%**.

A seção {{n:6}} explica o que esse número significa, e a seção {{n:7}} faz a pergunta
seguinte: 4.000 L é o volume certo?

---

## Se alguma coisa der errado

**O programa não abre.** Verifique se a instalação terminou sem erro e reinstale por
cima; a reinstalação preserva os seus arquivos, porque eles não ficam na pasta do
programa.

**A lista de cidades está vazia.** A base climática nacional acompanha só a Edição
Brasil. Na Internacional, use um arquivo de chuva próprio.

**Falta alguma parte do programa, como a volumetria 3D.** Rode, no Prompt de Comando,
`"C:\Program Files\Netuno 5\Netuno.exe" --diagnostico`. O programa lista o que a
instalação traz: o visualizador 3D, a base climática, o banco tarifário e o manual. Cada
item sai marcado OK ou FALTA. A lista também fica gravada em `netuno_diagnostico.txt`,
na pasta temporária do Windows. Mande esse arquivo junto com o relato do problema.

**O resultado não bate com o manual.** Confira, nesta ordem: a série de chuva
carregada, a área, o coeficiente, a lâmina de descarte, a demanda e a fração
atendível. Uma divergência de resultado quase sempre é uma divergência de entrada, e a seção {{n:33}} lista os enganos mais comuns.

**Uma mensagem de erro apareceu.** A seção {{n:37}} traz as mensagens do programa, o que
cada uma significa e o que fazer.
