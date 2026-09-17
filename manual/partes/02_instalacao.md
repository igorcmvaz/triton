# Instalação e primeira execução

> Ao terminar esta seção você terá o programa instalado, aberto, e uma simulação
> concluída com um resultado que dá para conferir contra este manual.

---

## O que você precisa

<!-- tabela: Requisitos de sistema para instalar e executar o programa -->
| Requisito | O que é preciso |
| :--- | :--- |
| sistema | Windows 10 ou 11, 64 bits |
| espaço em disco | cerca de 600 MB para o programa |
| memória | 4 GB bastam; 8 GB deixam a varredura mais confortável |
| privilégios | de administrador, só para instalar |

Nada além disso precisa ser instalado. O programa é distribuído já montado, com todos os
componentes de que depende para calcular, e não requer instalação prévia de
interpretadores, bibliotecas ou pacotes auxiliares. Também não requer conexão com a
internet para funcionar: tudo o que ele consulta durante uma simulação está no próprio
computador.

---

## A instalação

1. Execute **`Netuno_Setup_5_0_0.exe`**.
2. Escolha o idioma da instalação. Português e inglês vêm sempre; espanhol e chinês
   são pacotes opcionais, que você marca na instalação personalizada.
3. Aceite o diretório sugerido, `C:\Program Files\Netuno 5`, ou escolha outro.
4. Marque **criar ícone na área de trabalho** se quiser.
5. Ao terminar, o instalador oferece abrir o programa.

Depois disso, o Netuno aparece no menu Iniciar como **Netuno 5**. Para desinstalar,
use *Aplicativos e recursos* do Windows, como em qualquer programa.

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

Existe além disso uma **base climática nacional**, com 652 cidades, 19 modelos
climáticos do CMIP6 e 3 cenários futuros. São cerca de 6,5 GB, distribuídos à parte
justamente por causa do tamanho. Instalada, ela aparece na primeira tela como uma
lista de cidades; ausente, a tela oferece apenas o carregamento de arquivo próprio, e
todo o resto do programa funciona igual.

A seção {{n:E}} descreve a base, e a seção {{n:15}} mostra como usar um cenário futuro.

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

Eles ficam na pasta do programa. A seção {{n:J}} lista os nove casos do manual, com o
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
   por habitante e dia, e fração atendível de 40%.
3. **Reservatório & Custos.** Informe volume fixo de 5.000 L.
4. Rode, e vá a **Resultados Técnicos**.

Você deve obter potencial de economia próximo de **37%**.

A seção {{n:6}} explica o que esse número significa, e a seção {{n:7}} faz a pergunta
seguinte: 5.000 L é o volume certo?

---

## Se alguma coisa der errado

**O programa não abre.** Verifique se a instalação terminou sem erro e reinstale por
cima; a reinstalação preserva os seus arquivos, porque eles não ficam na pasta do
programa.

**A lista de cidades está vazia.** A base climática nacional não está instalada. Use
um arquivo de chuva próprio, ou instale a base — a seção {{n:E}} diz como.

**O resultado não bate com o manual.** Confira, nesta ordem: a série de chuva
carregada, a área, o coeficiente, a lâmina de descarte, a demanda e a fração
atendível. Uma divergência de resultado quase sempre é uma divergência de entrada, e a seção {{n:33}} lista os enganos mais comuns.

**Uma mensagem de erro apareceu.** A seção {{n:37}} traz as mensagens do programa, o que
cada uma significa e o que fazer.
