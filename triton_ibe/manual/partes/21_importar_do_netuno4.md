# Importar um projeto antigo

> **Pergunta que este guia responde:** os meus estudos antigos abrem no Triton?

Os estudos guardados no formato de texto antigo de uma ferramenta de simulação anterior abrem no
Triton, e a maior parte dos dados atravessa a conversão sem perdas. O cuidado que esta secção
pede decorre de dois factos que convivem mal: alguns campos não atravessam, e a importação não
diz quais. Um estudo reaproveitado sem conferência pode, por isso, continuar a parecer o estudo
original enquanto simula outra coisa.

---

## Como importar

Basta abrir o ficheiro antigo pelo menu de abertura de projetos. O programa reconhece o formato
antigo, que é texto separado por ponto e vírgula, e converte-o para a estrutura interna da versão
atual. Feita a conversão, guarde o projeto: passa a ser gravado no formato JSON do Triton, com os
campos descritos no apêndice {{n:A}}, e o ficheiro original permanece intacto no disco, o que
convém preservar como prova do estudo anterior.

---

## O que vem na conversão

Praticamente todo o núcleo de entrada do formato antigo tem correspondente direto na versão
atual, e é convertido sem intervenção do utilizador. A tabela seguinte indica o que a importação
recupera.

<!-- tabela: Dados do formato antigo recuperados pela importação -->
| Dado | Vem? |
| :--- | :---: |
| ficheiro e data inicial da chuva | sim |
| área de captação, coeficiente de escoamento | sim |
| descarte das primeiras águas e modo | sim |
| procura total e número de moradores | sim |
| percentagem suprível por água da chuva | sim |
| reservatório superior, limiar de elevação | sim |
| reservatório inferior, intervalo e passo | sim |
| diferença entre potenciais | sim |
| tarifas de água e saneamento, impostos | sim |
| custos iniciais: mão de obra, tubagem, acessórios | sim |
| eletrobomba: potência, rendimento, caudal, tempo de arranque, custo | sim |
| tarifa de energia e impostos | sim |
| inflação, atualização, período de análise, taxa de atualização | sim |
| custos de exploração | sim |

---

## O que não vem

> **Atenção, e confira sempre.** O leitor de ficheiros antigos **não reconhece nenhuma chave de
> procura variável**. Um projeto antigo que usasse uma procura mensal ou diária é importado como
> procura **constante**, sem aviso algum.

A consequência desta limitação merece ser explicitada, porque altera resultados sem alterar o
aspeto do projeto. Se o estudo original modulava a procura por calendário (uma escola em férias,
um hotel de época), a importação degrada-o para um consumo uniforme, e o desencontro entre oferta
e procura que a modulação representava desaparece do cálculo. No hotel de Lisboa do manual, essa
degradação transformaria 10,36% em 11,07%. Confira o modo de procura logo após importar, e
reintroduza o perfil à mão se estiver em «constante» quando não devia. A secção {{n:17}} mostra
como.

Há ainda um conjunto de parâmetros que não vêm por outra razão: simplesmente não existiam no
formato antigo. São a rega e a supressão da rega por chuva, a classe de qualidade da água e a
linha de tratamento, os materiais dos reservatórios e os comprimentos de tubagem por diâmetro, os
parâmetros da avaliação de ciclo de vida, a tipologia do edifício e o número de frações
autónomas. Todos assumem o valor de partida da versão atual, e todos merecem revisão antes de o
projeto importado ser considerado pronto.

---

## Por que o resultado muda

Mesmo que a importação recupere na perfeição todos os dados de entrada, o resultado da simulação
pode não ser idêntico ao da ferramenta anterior. A diferença é deliberada e tem causa conhecida.

A causa principal está no **tratamento do descarte das primeiras águas**. A regra antiga trata a
lâmina de descarte como limiar do evento: quando a chuva do dia não a atinge, nada é captado;
quando a ultrapassa, capta-se a chuva inteira, sem subtração. O Triton subtrai a lâmina à
precipitação do dia, o que é fisicamente mais fiel, porque a água desviada para o dispositivo de
autolimpeza não chega, de facto, à cisterna. Com as mesmas entradas, a regra antiga devolve, por
isso, um potencial de poupança mais alto do que o Triton, e a diferença é maior onde é comum a
chuva fraca em muitos dias. A secção {{n:35}} trata da comparação.

---

## Comparar as duas ferramentas corretamente

Quando o trabalho compara explicitamente as duas ferramentas, há um procedimento simples que
isola o comportamento do balanço hídrico da divergência metodológica deliberada, e não exige
nenhum recurso do programa: **corra ambas com descarte igual a zero**. Sem descarte, as duas
regras coincidem por construção, e qualquer diferença que sobre é atribuível à implementação, e
não ao método.

Feita essa comparação, repita-a com o descarte real do projeto, para medir a diferença total. Os
dois números, tomados em conjunto, separam o que é mudança deliberada de método do que seria uma
eventual divergência de implementação, e essa separação é justamente o que um revisor pede.

> O programa não tem opção para emular a regra antiga de descarte. Use o caminho do descarte
> zero, que produz o mesmo resultado com um pouco mais de trabalho e nenhuma surpresa.

---

## Depois de importar

Sete conferências bastam para transformar um projeto importado num projeto fiável, e devem fazer-se
pela ordem abaixo, porque as primeiras afetam o resultado das seguintes.

1. **Modo de procura**: foi degradado para constante?
2. **Tipologia** do edifício: é a correta?
3. **Materiais** dos reservatórios: o valor de partida é o polietileno.
4. **Classe de qualidade** da água e tecnologia de desinfeção.
5. **Regime tarifário**: o formato antigo não distinguia os regimes de valor mínimo, e a secção
   {{n:16}} mostra o que isso muda.
6. **Rendimento do motor** da eletrobomba, que o formato antigo não tinha.
7. **Corra o projeto e confira o potencial** com o resultado antigo antes de confiar no ficheiro
   importado.

E guarde o ficheiro original: é a prova documental do estudo anterior, e nenhuma conversão o
substitui.
