# Instalação e primeira execução

> No fim desta secção, tem o programa instalado e aberto, e uma simulação concluída com um resultado que pode conferir contra este manual.

---

## O que é preciso

<!-- tabela: Requisitos de sistema para instalar e executar o programa -->
| Requisito | O que é preciso |
| :--- | :--- |
| sistema | Windows 10 ou 11, 64 bits |
| espaço em disco | cerca de 0,7 GB |
| memória | 4 GB chegam; 8 GB deixam o varrimento mais folgado |
| privilégios | de administrador, para instalar para todos os utilizadores; sem eles, a instalação vai para a pasta do utilizador |

Não é preciso instalar mais nada. O programa é distribuído já montado, com todos os componentes de que depende para calcular, e não exige a instalação prévia de interpretadores, bibliotecas ou pacotes auxiliares. Também não precisa de ligação à internet: tudo o que consulta durante uma simulação está no próprio computador.

---

## A edição

Esta é a Edição Ibérica (IBE), o «Triton IBE», que se chamou Edição Portugal (PRT). Está em português de Portugal, trabalha em euros e, por agora, só traz dados de Portugal (a linha de cobertura do programa diz: Espanha, 0 locais): a chuva diária por concelho e os tarifários de água de Lisboa, do Porto e do Funchal. O selo vermelho no topo da barra lateral, o título da janela e o rodapé de cada relatório e de cada exportação dizem de que edição saiu o estudo.

<!-- tabela: O que a Edição Ibérica traz e o que deixa ao utilizador -->
| | Edição Ibérica (IBE) |
| :--- | :--- |
| instalador | `Triton_IBE_Setup_0_1_0.exe` |
| idioma ao abrir | português de Portugal |
| chuva | base Iberia01 por município (Portugal, Espanha, Baleares) e ERA5 nas ilhas (nível C), ou a E-OBS opcional (278 concelhos do Continente), ou série própria; série de exemplo do Funchal |
| tarifas de água, saneamento e resíduos | tarifários de Lisboa, do Porto e do Funchal; nos outros concelhos, digitadas |
| eletricidade | digitada (o Funchal traz a tarifa da EEM) |
| moeda e custos | euro, a única oferecida; custos digitados |
| fator de emissão da rede e da água potável | do local do projeto, obrigatórios |
| certificações e incentivos | LEED, EDGE, GRI |
| etapa 12 | Modulação Probabilística |
| custo da tubagem e da mão de obra | digitado |
| manual que o programa abre | este manual |
| preferências guardadas | `Triton-IBE` |

O método é o mesmo em qualquer país: o balanço diário, o descarte inicial, os coeficientes de escoamento, a análise económica e a avaliação do ciclo de vida são um só motor. O que muda de país para país são os **dados**. Os custos de obra, de bomba, de tratamento e de manutenção não vêm definidos: dependem do local e do mercado, e o utilizador introduz os seus. Os custos que este manual usa nos casos são **ilustrativos, não são preços de mercado**.

Sem os fatores de emissão do local, o programa não calcula a avaliação ambiental: um fator de outra rede elétrica daria um resultado errado sem qualquer aviso.

Quando uma exigência de uma norma nacional importa, o manual descreve-a em termos gerais e pede que consulte a norma aplicável ao local do edifício (ver a secção {{n:1}}).

---

## A instalação

1. Execute **`Triton_IBE_Setup_0_1_0.exe`**. O instalador pergunta se a instalação é para todos os utilizadores, o que exige administrador, ou só para si.
2. Escolha o idioma da instalação, leia e aceite a licença (código-fonte académico, uso não comercial).
3. Escolha o tipo de instalação. A **padrão** traz o programa, o manual, os casos, os exemplos e todos os idiomas. A **personalizada** permite desmarcar os pacotes de idioma espanhol e chinês.
4. Aceite a pasta sugerida, `C:\Program Files\Triton IBE`, ou escolha outra.
5. Marque, se quiser, **criar ícone no ambiente de trabalho**. A opção **abrir ficheiros .triton com o Triton** vem desmarcada, para não tomar os ficheiros de outra edição do Triton instalada no mesmo computador; marque-a se quiser abrir um projeto com um duplo clique.
6. No fim, o instalador oferece-se para abrir o programa.

Depois, o menu Iniciar tem dois atalhos: o programa e o seu manual em PDF (este documento). Para desinstalar, use *Aplicações e funcionalidades* do Windows, como com qualquer programa; os seus projetos ficam onde os guardou.

> **O que o instalador põe no computador.** O programa, a base de chuva diária por município (Iberia01, mais a reanálise ERA5 das ilhas), a base opcional da E-OBS, a série de exemplo do Funchal, a base de tarifários, os ficheiros de exemplo e este manual. Nada é transferido durante a utilização: o Triton funciona sem ligação à internet.

---

## Onde ficam os seus ficheiros

O programa nunca decide por si onde guardar. De cada vez que grava um projeto, um relatório ou uma exportação, pergunta a pasta.

<!-- tabela: Formatos de ficheiro que o programa grava e o conteúdo de cada um -->
| O que grava | Extensão | Contém |
| :--- | :--- | :--- |
| projeto | `.triton` | todos os dados de entrada **e a série de chuva** |
| relatório | `.pdf` | o documento completo do estudo |
| resultados | `.xlsx`, `.csv` | as tabelas, para folha de cálculo |
| esquema | `.dxf` | o desenho esquemático, para CAD |

Destes formatos, o `.triton` é o que mais importa guardar. É autocontido: leva dentro de si a série de chuva e, por isso, abre em qualquer outro computador mesmo sem os ficheiros que lhe deram origem. Uma exceção: a chuva das bases que acompanham o programa (Iberia01 e E-OBS). O ficheiro guarda a referência da série — município (`Nome [código]`), fonte e intervalo de datas —, com o número de dias, o total e uma impressão digital (SHA-256) dos valores, e o programa recompõe-na a partir da base ao abrir o projeto, conferindo a impressão. Uma série alterada depois de carregada, ou uma base indisponível ao gravar, continua a ir inteira para o ficheiro. ==É também o ficheiro a anexar a um artigo para que outra pessoa reproduza o estudo,== e é esta propriedade que separa um trabalho verificável de um trabalho apenas relatado.

---

## A base climática

O programa traz a chuva diária de 8 319 municípios de Portugal continental, Espanha peninsular e Baleares, calculada a partir do Iberia01 v1.0 (Herrera et al., 2019; grelha de 0,1°, 1971 a 2015, licença ODbL, uso comercial permitido, com atribuição). A série de um município é a média das células da grelha com centro dentro dos seus limites; o período padrão é 1986–2015. Canárias, Madeira e Açores usam a reanálise ERA5 de 0,25° (nível C, com aviso). A E-OBS v33.0e (278 concelhos do Continente, 1950 a 2025, uso só não comercial) continua disponível como fonte opcional, com o aviso vermelho nos laudos. Aceita ainda qualquer série própria em CSV: precipitação diária em milímetros, um valor por dia, como descreve o apêndice {{n:F}}.

O Iberia01 é uma grelha interpolada de observações, não um registo de pluviómetro. Serve para estudos e para os exemplos deste manual. Num projeto real, use a série medida no local sempre que a tiver.

> **Dados de reanálise no Funchal.** O Funchal está fora do domínio do Iberia01 (e a E-OBS falha em 22% dos dias de 1991 a 2020, acima do máximo admitido de 1%). A série do exemplo do Funchal é por isso reanálise ERA5, de um nó de 0,25° (cerca de 25 km), com nível de qualidade C, e pode diferir da média medida na estação.

---

## Os ficheiros de exemplo

O manual vem acompanhado de projetos prontos, que reproduzem os resultados impressos aqui.

<!-- tabela: Ficheiros de exemplo distribuídos com o programa -->
| Ficheiro | Para que serve |
| :--- | :--- |
| `casos\01_tutorial_lisboa.triton` | o projeto que o capítulo {{c:2}} constrói, pronto |
| `casos\05_dez_dias.triton` | o caso didático de dez dias da secção {{n:23}} |
| `casos\02_porto.triton` e `casos\03_funchal.triton` | a mesma moradia noutras cidades |
| `exemplos\portugal\*.triton` | três estudos completos: Lisboa, Porto e Funchal |

Ficam na pasta do programa. O apêndice {{n:J}} lista os dez casos do manual, com o capítulo de cada um e o resultado que produzem.

Convém começar pelo caso de dez dias. Abra-o, execute a simulação e compare o resultado com a tabela impressa na secção {{n:23}}. Se coincidirem, a instalação corresponde exatamente a este manual. Se divergirem, o manual e o programa são de versões diferentes, e a secção {{n:38}} explica o que fazer.

---

## A primeira simulação, em cinco minutos

O programa organiza-se em **etapas**, na barra lateral esquerda, pela ordem em que se trabalha. Para a primeira simulação bastam quatro.

1. **Projeto e Chuva.** Escolha o concelho de Lisboa na base climática. Indique a área de captação de 150 m², o coeficiente de escoamento de 0,85 e o descarte de 2,0 mm.
2. **Edificação e Consumo.** Escolha moradia unifamiliar, 4 moradores, 150 litros por habitante e dia, e fração atendível de 28%.
3. **Reservatório & Custos.** Indique um volume fixo de 3.000 L.
4. Simule e vá a **Resultados Técnicos**.

Deve obter um potencial de economia próximo de **16%** (15,77% com a série de Lisboa, Iberia01, 1986–2015).

A secção {{n:6}} explica o que este número significa, e a secção {{n:7}} faz a pergunta seguinte: serão 3.000 L o volume certo?

---

## Se algo correr mal

**O programa não abre.** Verifique se a instalação terminou sem erros e reinstale por cima; a reinstalação preserva os seus ficheiros, porque não ficam na pasta do programa.

**A lista de concelhos está vazia.** Confirme que as bases de chuva (`data\chuva_iberia01_p1.db` a `p4.db` e `ibe_unidades.db`) estão na pasta do programa; se faltarem, reinstale. Em Ceuta e Melilla, use um ficheiro de chuva próprio.

**Falta alguma parte do programa, como a volumetria 3D.** Execute, na Linha de Comandos, `"C:\Program Files\Triton IBE\Triton_IBE.exe" --diagnostico` (com a pasta predefinida). O programa lista o que a instalação traz: o visualizador 3D, a base de chuva, a base de tarifários e o manual. Cada item sai marcado OK ou FALTA. A lista fica também gravada em `triton_diagnostico.txt`, na pasta temporária do Windows. Envie esse ficheiro com a descrição do problema.

**O resultado não bate com o manual.** Confira, por esta ordem: a série de chuva carregada, a área, o coeficiente, a lâmina de descarte, a procura e a fração atendível. Uma divergência de resultado é quase sempre uma divergência de entrada, e a secção {{n:33}} lista os enganos mais comuns.

**Apareceu uma mensagem de erro.** A secção {{n:37}} traz as mensagens do programa, o que cada uma significa e o que fazer.
