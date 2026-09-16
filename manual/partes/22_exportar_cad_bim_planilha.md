# Exportar para CAD, BIM e planilha

> **Pergunta que este guia responde:** como levar o resultado para o projeto
> executivo e para a análise própria?

---

## O que cada formato leva

<!-- tabela: Formatos de exportação e finalidade de cada um -->
| Formato | Extensão | O que leva | Para quê |
| :--- | :--- | :--- | :--- |
| relatório | HTML, PDF | resultado completo e premissas | entregar |
| planilha | XLSX | série diária e varredura | reanalisar |
| desenho | DXF | esquema hidráulico dimensionado | projeto executivo |
| manifesto BIM | JSON | componentes com tipo, posição, nível e parâmetros | importação no Revit |

---

## Planilha

A exportação para planilha é o caminho de quem pretende fazer análise própria sobre os
resultados, seja para construir um gráfico que o programa não oferece, seja para
combinar os números do Netuno com dados de outra origem. Dois conjuntos de dados estão
disponíveis, e eles respondem a perguntas diferentes.

A **série diária** traz uma linha por dia simulado, com a chuva registrada, a chuva
efetiva depois do descarte, o volume captado, a demanda do dia, o consumo pluvial, o
consumo de rede, o extravasamento, o volume armazenado nos dois reservatórios, o volume
recalcado e a classe de atendimento. É a base de qualquer gráfico ou estatística que o
programa não ofereça pronta, e é o que se usa quando a análise pretendida difere da que o
programa faz.

A **varredura** traz uma linha por volume simulado, com todos os indicadores calculados
para cada um. É a base da curva de retorno decrescente apresentada na seção {{n:7}}, e o
formato adequado para quem queira redesenhá-la com outra apresentação.

> **Um aviso de tamanho.** Trinta anos de série diária são 10.950 linhas por
> simulação. Uma varredura de doze volumes com série detalhada gera cento e trinta
> mil linhas. Exporte a série detalhada só do volume que interessa.

---

## Desenho em DXF

O programa gera o esquema hidráulico do sistema dimensionado: cisterna, filtro,
descarte, bomba quando houver, reservatório superior, e a tubulação com os diâmetros
adotados.

O que o programa produz é um **esquema**, e não um projeto executivo. Ele representa os
componentes do sistema e as conexões lógicas entre eles, com os diâmetros adotados, e
serve de base para que o projetista desenhe a instalação em planta, com as cotas, o
traçado e as interferências reais da edificação. ==Um esquema não substitui projeto
hidráulico, e entregá-lo como tal seria erro de responsabilidade técnica.==

O que o programa **não** dimensiona:

- traçado e declividade da tubulação;
- perda de carga real da instalação;
- reservatório de autolimpeza do descarte, cujo volume é `A × d_f`;
- extravasor e ligação à drenagem;
- fundação e impermeabilização da cisterna.

---

## Biblioteca de blocos e manifesto BIM

Na etapa **10. Exportação**, o modo *Biblioteca de Blocos para Plantas + BIM JSON* grava os blocos DXF dos componentes em escala 1:1, em milímetros, e, ao lado deles, o arquivo `*_netuno-bim.json`. O programa não exporta IFC. O manifesto JSON é o contrato entre o dimensionamento e o modelo: cada instância declara o tipo do componente, o nível, a posição local em milímetros, a rotação e os parâmetros dimensionados, como a capacidade e o diâmetro, e a estrutura é validada antes da gravação.

A integração com o Autodesk Revit é feita por um importador distribuído com o programa, executado no motor CPython 3 do pyRevit, com um documento aberto no Revit 2022 ou posterior, e insere as instâncias do manifesto usando as famílias indicadas em `family_mapping.json`, que associa cada tipo do programa — cisterna, reservatório superior, filtro, descarte inicial, motobomba, registros, válvula de retenção, separação atmosférica, extravasor e ponto de consumo não potável — a uma família e a um tipo do escritório.

O importador não cria famílias nem substitui componentes por aproximação: instância sem família ou sem nível correspondente é listada como pendente ao fim da importação. As coordenadas são locais, e a amarração ao ponto-base e ao norte do projeto é feita no Revit, pelo projetista. O manifesto serve à coordenação e ao levantamento de quantitativos, e não substitui a modelagem da instalação hidráulica.

---

## Relatórios

Os três da seção {{n:13}}: executivo, ambiental com ESG, e científico. Em HTML para
consulta e em PDF para entrega.

> O programa tem dois geradores de PDF e usa o mais completo que a máquina permitir.
> Quando cai para o alternativo, o documento sai mais simples, com o mesmo conteúdo e
> os mesmos números.

---

## Um conselho de arquivo

Ao fechar um estudo, guarde junto, na mesma pasta:

1. o arquivo `.netuno`;
2. a **série de chuva** usada, ou sua identificação exata na base;
3. o relatório científico em PDF;
4. a planilha da varredura;
5. se houve lote, o **script** com os comandos;
6. um arquivo de texto com a **versão do programa**.

São seis itens que tornam o estudo reproduzível daqui a cinco anos. Sem eles, o
relatório em PDF é só uma afirmação.
