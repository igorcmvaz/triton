# Importar um projeto do Netuno 4

> **Pergunta que este guia responde:** meus estudos antigos abrem no Netuno 5?

Abrem, e a maior parte dos dados atravessa a conversão sem perda. O cuidado que esta
seção pede decorre de dois fatos que convivem mal: alguns campos não atravessam, e a
importação não avisa quais foram. Um estudo reaproveitado sem conferência pode, por isso,
continuar parecendo o estudo original enquanto simula outra coisa.

---

## Como importar

Basta abrir o arquivo antigo pelo menu de abertura de projetos. O programa reconhece o
formato legado, que é texto separado por ponto e vírgula, e o converte para a estrutura
interna da versão atual. Feita a conversão, salve o projeto: ele passa a ser gravado no
formato JSON do Netuno 5, com os 103 campos descritos na seção {{n:A}}, e o arquivo
original permanece intacto no disco, o que convém preservar como evidência do estudo
anterior.

---

## O que vem na conversão

Praticamente todo o núcleo de entrada do Netuno 4 tem correspondente direto na versão
atual, e é convertido sem intervenção do usuário. A tabela abaixo relaciona o que a
importação recupera.

| Dado | Vem? |
| :--- | :---: |
| arquivo e data inicial da chuva | sim |
| área de captação, coeficiente de escoamento | sim |
| descarte de primeiras águas e modo | sim |
| demanda total e número de moradores | sim |
| percentual atendível por água pluvial | sim |
| reservatório superior, limiar de recalque | sim |
| reservatório inferior, faixa e passo | sim |
| diferença entre potenciais | sim |
| tarifas de água e esgoto, impostos | sim |
| custos iniciais: mão de obra, tubulação, acessórios | sim |
| motobomba: potência, rendimento, vazão, tempo de partida, custo | sim |
| tarifa de energia e impostos | sim |
| inflação, reajuste, período de análise, TMA | sim |
| custos operacionais | sim |

---

## O que não vem

> **Atenção, e confira sempre.** O leitor de arquivos antigos **não reconhece nenhuma
> chave de demanda variável**. Um projeto do Netuno 4 que utilizasse demanda mensal ou
> diária é importado como demanda **constante**, sem aviso algum.

A consequência dessa limitação merece ser explicitada, porque ela altera resultados sem
alterar a aparência do projeto. Se o estudo original modulava a demanda por calendário —
uma escola em férias, um hotel de temporada — a importação o degrada a consumo uniforme,
e o descasamento entre oferta e demanda que a modulação representava desaparece do
cálculo. Confira o modo de demanda logo após importar, e relance o perfil manualmente se
ele estiver em «constante» quando não deveria estar. A seção {{n:17}} mostra como.

Há ainda um conjunto de parâmetros que não vêm por razão diversa: eles simplesmente não
existiam no Netuno 4. São a irrigação e a supressão de rega por chuva, a classe de
qualidade da água e a linha de tratamento, os materiais dos reservatórios e os
comprimentos de tubulação por diâmetro, os parâmetros de avaliação de ciclo de vida, os
incentivos fiscais de IPTU verde, a tipologia da edificação e o número de economias.
Todos assumem o valor padrão da versão 5, e todos merecem revisão antes que o projeto
importado seja considerado pronto.

---

## Por que o resultado muda

Ainda que a importação recupere perfeitamente todos os dados de entrada, o resultado da
simulação não será idêntico ao da versão anterior. A diferença é deliberada, tem causa
conhecida e está quantificada.

A causa principal está no **tratamento do descarte de primeiras águas**. O Netuno 4 trata
a lâmina de descarte como limiar do evento: quando a chuva do dia não atinge a lâmina,
nada é captado; quando a ultrapassa, capta-se a chuva inteira, sem subtração. O Netuno 5
subtrai a lâmina da precipitação do dia, o que é fisicamente mais fiel, porque a água
desviada para o dispositivo de autolimpeza efetivamente não chega à cisterna.

Sobre 4.050 casos de referência, o Netuno 5 estima em média de **2,3 a 2,7 pontos
percentuais menos** economia de água potável que o Netuno 4. ==Metade dessa divergência
vem do tratamento do descarte:== 1,36 ponto percentual dos 2,71 medidos no conjunto de
Manaus e São Paulo. As demais causas estão decompostas na seção {{n:35}}.

---

## Comparar as duas versões corretamente

Quando o trabalho compara explicitamente as duas versões, existe um procedimento simples
que isola o comportamento do balanço hídrico da divergência metodológica deliberada, e
ele não exige recurso algum do programa: **rode ambas as versões com descarte igual a
zero**. Sem descarte, as duas regras coincidem por construção, e qualquer diferença
remanescente é atribuível à implementação, e não ao método.

Feita essa comparação, repita-a com o descarte real do projeto para medir a diferença
total. Os dois números tomados em conjunto separam o que é mudança deliberada de método
do que seria eventual divergência de implementação, e essa separação é justamente o que
um revisor pede.

> O protocolo de verificação interno menciona uma opção para emular automaticamente a
> regra antiga de descarte. **Essa opção não está implementada.** Use o caminho do
> descarte zero, que produz o mesmo resultado com um pouco mais de trabalho e nenhuma
> surpresa.

---

## Depois de importar

Sete conferências bastam para transformar um projeto importado num projeto confiável, e
elas devem ser feitas na ordem abaixo, porque as primeiras afetam o resultado das
seguintes.

1. **Modo de demanda** — foi degradado para constante?
2. **Tipologia** da edificação — está na correta?
3. **Materiais** dos reservatórios — o padrão adotado é polietileno.
4. **Classe de qualidade** da água e tecnologia de desinfecção.
5. **Regime tarifário** do município — o Netuno 4 não distinguia os regimes, e a
   seção {{n:16}} mostra o que isso muda.
6. **Rendimento do motor** da motobomba, que o Netuno 4 não tinha.
7. **Rode o projeto e confira o potencial** contra o resultado antigo antes de confiar
   no arquivo importado.

E guarde o arquivo original: ele é a evidência documental do estudo anterior, e nenhuma
conversão o substitui.
