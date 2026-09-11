# Por onde começar, conforme o seu objetivo

Este manual reúne quarenta e nove seções distribuídas em sete capítulos, e não foi
concebido para ser lido do começo ao fim. Ele funciona melhor como obra de consulta, em
que cada leitor entra pelo ponto que corresponde ao que precisa fazer, e esta seção
existe justamente para indicar esse ponto de entrada.

---

## Roteiro por objetivo

A tabela abaixo relaciona os cinco propósitos mais comuns de quem abre o programa, com o
percurso de leitura correspondente a cada um deles.

| Você quer | Leia |
| :--- | :--- |
| **aprender a usar** o programa | o capítulo {{c:2}} inteiro, seções {{n:4}} a {{n:13}}, na ordem |
| **resolver um caso** hoje | as três perguntas abaixo, e depois o guia do capítulo {{c:3}} que couber |
| **publicar** um estudo | o capítulo {{c:4}}, que traz o método, e a seção {{n:13}}, com a lista de declaração |
| **revisar** um estudo alheio | o capítulo {{c:6}}, e as seções {{n:A}} e {{n:B}} |
| **migrar** do Netuno 4 | as seções {{n:21}} e {{n:35}} |
| **não errar** | a seção {{n:33}}, com os dez enganos mais comuns |

Quem dispõe de uma hora e nenhuma familiaridade prévia deve ler o tutorial do capítulo
{{c:2}}. Ele constrói um estudo completo em torno de um único projeto, e cada seção
encerra mostrando onde esse projeto chegou, de modo que o leitor acompanha a construção
em vez de receber o resultado pronto.

---

## As três perguntas que definem um estudo

Antes mesmo de abrir o programa, convém responder a três perguntas, porque elas
determinam boa parte das decisões subsequentes e porque respondê-las depois costuma
implicar refazer trabalho.

### Que usos a água pluvial vai atender?

A resposta define a **fração atendível**, e a fração atendível é o teto de todo o resto:
um sistema cuja fração é de 40% jamais economizará mais que 40% do consumo total, por
maior que seja a cisterna e por mais que chova. Nenhuma decisão posterior de projeto
altera esse limite, razão pela qual ele merece ser estabelecido antes de qualquer outra
coisa.

| Se os usos são | Fração típica | Onde se trata |
| :--- | ---: | :--- |
| bacia sanitária apenas | 20 a 30% | seção {{n:5}} |
| bacia, máquina de lavar e área externa | 35 a 45% | seção {{n:5}} |
| tudo menos chuveiro, cozinha e beber | 45 a 60% | seção {{n:5}} |
| edificação comercial, quase só bacia e limpeza | 70 a 85% | seção {{n:18}} |

### Vai comparar volumes ou avaliar um só?

A distinção entre avaliar um volume conhecido e procurar o volume adequado determina o
modo de simulação e, com ele, o tempo de máquina e a riqueza do resultado.

| Se você quer | Use | Onde se trata |
| :--- | :--- | :--- |
| avaliar uma cisterna que já existe | volume fixo | seção {{n:6}} |
| descobrir o volume a comprar | **varredura** | seções {{n:7}} e {{n:24}} |
| escolher entre critérios que discordam | varredura e multicritério | seções {{n:12}} e {{n:32}} |

==A varredura é quase sempre a resposta certa.== Ela custa mais tempo de máquina, na
ordem de segundos, e produz a curva de retorno decrescente, que é o argumento mais forte
de que qualquer estudo pode dispor ao justificar um volume.

### Precisa de reservatório superior?

A terceira pergunta é hidráulica, e a resposta depende da altura da edificação e da
pressão exigida nos pontos de consumo.

| Se a edificação | Então | Onde se trata |
| :--- | :--- | :--- |
| é térrea e os pontos ficam próximos da cisterna | pressurização direta, sem caixa | seção {{n:8}} |
| é sobrado ou prédio | caixa elevada, por **pressão** | seção {{n:8}} |
| precisa de reserva contra falta de energia | caixa elevada | seção {{n:8}} |

> A caixa elevada **não aumenta** a economia de água. Mantido o mesmo armazenamento
> total, ela entrega ligeiramente menos e consome energia de recalque. A decisão de
> adotá-la deve ser hidráulica, e nunca fundada na expectativa de maior aproveitamento.

---

## A ordem de trabalho no programa

A barra lateral do programa está numerada, e a numeração corresponde à ordem em que se
trabalha. As quatro primeiras etapas são de entrada de dados, as cinco seguintes
apresentam resultados, e as três últimas reúnem ferramentas auxiliares.

| Etapa | O que se faz nela | Onde se trata |
| :--- | :--- | :--- |
| 1. Projeto e Chuva | a série de precipitação e a captação | seção {{n:4}} |
| 2. Edificação Consumo | quem ocupa, quanto consome, que parte a chuva atende | seção {{n:5}} |
| 3. Qualidade & ETAP | a classe de água e o tratamento | seção {{n:9}} |
| 4. Reservatório & Custos | o volume, ou a varredura, e o orçamento | seções {{n:6}}, {{n:7}} e {{n:10}} |
| 5. Resultados Técnicos | quanta água o sistema entrega | seção {{n:6}} |
| 6. Resultados Econômicos | em quanto tempo se paga | seção {{n:10}} |
| 7. Resultados Ambientais & ESG | carbono e certificações | seção {{n:11}} |
| 8. Decisão Multicritério | qual volume escolher | seção {{n:12}} |
| 9. Relatórios PDF | o documento do estudo | seção {{n:13}} |
| 10. Exportação | planilhas, desenho e dados | seção {{n:22}} |
| 11. Documentação | o método dentro do próprio programa | — |
| 12. Gestor de Tarifas | a tarifa do seu município | seção {{n:16}} |

Convém salvar o projeto ao concluir cada etapa. Os 103 parâmetros são gravados e
relidos integralmente, e o arquivo resultante é a evidência documental do estudo, tanto
para quem o refará no futuro quanto para quem o avaliará.

---

## Antes de publicar

Três leituras são obrigatórias para quem pretende publicar resultados, e nenhuma delas é
longa. A seção {{n:13}} traz a lista do que declarar num artigo, acompanhada de um
parágrafo de método pronto para adaptação. A seção {{n:33}} reúne os dez enganos de
projeto que o programa não tem como impedir. E a seção {{n:36}} relaciona as limitações
conhecidas — das quais interessa ler não todas, mas as que afetam o caso em mãos.

A seção {{n:I}} condensa as três em fichas de uma página, para consulta rápida.
