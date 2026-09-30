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
| auditoria | XLSX | todos os campos das premissas, da tarifa, do tratamento, da ACV, da economia e do arranjo | conferir |
| desenho | DXF | esquema hidráulico dimensionado | projeto executivo |
| manifesto BIM | JSON | componentes com tipo, posição, nível e parâmetros | importação no Revit |
| projeto | NETUNO | todas as etapas e a série de chuva | reabrir e auditar |

---

## O arquivo de projeto

O formato `.netuno` é o único que guarda o estudo inteiro: as nove etapas, os pesos do
multicritério, as rotas de ACV e a **série diária de chuva**, incorporada ao próprio
arquivo. Um `.netuno` reabre em outra máquina sem o CSV de origem e reproduz o mesmo
número; é com ele que os casos do apêndice {{n:J}} são distribuídos. O CSV do Netuno 4 continua
disponível na exportação, marcado como legado, porque não preserva as etapas acrescentadas
desde então.

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

A etapa **10. Exportação** monta a planilha a partir de seis conjuntos, que se marcam
um a um: o resumo executivo com os metadados do projeto, o balanço hídrico diário, a
curva da varredura com a confiabilidade, o fluxo de caixa ano a ano, o inventário de
ciclo de vida e a matriz de decisão multicritério. Três escolhas completam a exportação:

<!-- tabela: Opções da exportação de planilha e quando usar cada uma -->
| Opção | Escolhas | Quando usar |
| :--- | :--- | :--- |
| formato | XLSX, CSV ou JSON | XLSX para abrir no Excel; CSV para R, Python ou outro programa; JSON para integração |
| separador do CSV | ponto e vírgula ou vírgula | ponto e vírgula no Excel em português; vírgula no R e na maior parte das ferramentas internacionais |
| filtro temporal | primeiro ano típico ou série completa | o ano para ilustrar; a série completa para qualquer estatística |
| horizonte econômico | 10, 20, 25 ou 30 anos | 20 anos, a vida útil de projeto mínima do sistema hidrossanitário (ABNT NBR 15575-1:2025, Tabela 25), salvo justificativa |

### Exportar tudo, para auditoria

O botão **Exportar TUDO (auditoria)**, ao lado da exportação da planilha, grava um só
arquivo Excel com as seis abas acima e, além delas, abas que não são escolhidas por
ninguém: percorrem **todos** os campos do que o programa usou. São as premissas do
projeto, uma linha por parâmetro, com o valor e a descrição tirada do próprio código; a
tarifa aplicada, com o significado de cada código de faixa, o regime, o modo do esgoto e
a conta para consumos de 0 a 50 m³; a linha de tratamento dimensionada na etapa de
qualidade, com os estágios, as doses e o carbono que a ACV soma; o inventário de ciclo de
vida item por item; os resultados da simulação, da economia e do multicritério; e o
arranjo 3D, com cada peça, cada trecho e o quantitativo por diâmetro. A aba «0_Leia_me»
diz o que há em cada uma.

É o arquivo para quem precisa conferir uma conta do início ao fim, ou responder a um
avaliador que pergunte o que entrou no carbono ou na economia. Um parâmetro novo no
programa aparece nele sem que ninguém precise se lembrar de acrescentá-lo.

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

O esquema também não carrega, e o projeto executivo precisa acrescentar, os requisitos
de instalação predial da ABNT NBR 15527:2019 para água não potável:

- tubulação de água de chuva pintada ou identificada em **roxo** (Munsell 2.5RP 3/10 ou
  similar), com a inscrição «ÁGUA NÃO POTÁVEL» a cada 3 m nas aparentes (item 4.5.5);
- sistema de distribuição independente do de água potável, sem conexão cruzada
  (4.5.8), com separação atmosférica na alimentação de reserva pela rede, conforme a
  ABNT NBR 5626:2020 (6.15.2);
- pontos de consumo de uso restrito, como a torneira de jardim, com placa «ÁGUA NÃO
  POTÁVEL» (4.5.9);
- reservatórios de água potável e não potável separados, com no mínimo 60 cm entre as
  faces externas quando lado a lado, e o não potável embaixo quando sobrepostos (4.5.10
  e 4.5.11);
- bombeamento conforme a ABNT NBR 5626 (4.5.2), o que inclui as duas bombas do item
  6.5.11.2 daquela norma.

O que o programa **não** dimensiona:

- traçado e declividade da tubulação;
- perda de carga real da instalação;
- arranjo hidráulico do dispositivo de descarte, do qual o programa calcula apenas o volume, `A × d_f`, e o custo;
- extravasor e ligação à drenagem;
- fundação e impermeabilização da cisterna.

---

## Biblioteca de blocos e manifesto BIM

Na etapa **10. Exportação**, o modo *Biblioteca de Blocos para Plantas + BIM JSON* grava os blocos DXF dos componentes em escala 1:1, em milímetros, e, ao lado deles, o arquivo `*_netuno-bim.json`. O programa não exporta IFC. O manifesto JSON é o contrato entre o dimensionamento e o modelo: cada instância declara o tipo do componente, o nível, a posição local em milímetros, a rotação e os parâmetros dimensionados, como a capacidade e o diâmetro, e a estrutura é validada antes da gravação.

A integração com o Autodesk Revit é feita por um importador distribuído com o programa, executado no motor CPython 3 do pyRevit, com um documento aberto no Revit 2022 ou posterior, e insere as instâncias do manifesto usando as famílias indicadas em `family_mapping.json`, que associa cada tipo do programa — cisterna, reservatório superior, filtro, descarte inicial, motobomba, registros, válvula de retenção, separação atmosférica, extravasor, ponto de consumo não potável, freio d'água, sucção flutuante, chave de nível, válvula solenoide, hidrômetro, válvula de pé com crivo, respiro e quadro de comando — a uma família e a um tipo do escritório.

Sem organização salva, o programa pré-preenche o arranjo usual dessas instalações, a partir do estudo: captação do telhado, filtro e descarte inicial; cisterna com entrada calma pelo freio d'água, captação pela sucção flutuante com válvula de pé e crivo, chave de nível contra marcha a seco, respiro com tela e extravasor com ladrão sifonado e retenção antirrefluxo para a rede pluvial; registros de manutenção dos dois lados da motobomba, válvula de retenção no recalque e quadro de comando; caixa superior com chave de nível, respiro com tela, extravasor com descarga visível, limpeza com registro junto à saída e distribuição com registro até um ponto de utilização identificado; e o abastecimento potável de reserva — hidrômetro, registro e válvula solenoide — que só abre quando falta água de chuva e descarrega na caixa superior por separação atmosférica, como pede a ABNT NBR 5626:2020. Quem decide é o quadro de comando: com a caixa superior no nível de partida e água na cisterna, liga a motobomba; com a cisterna no mínimo, bloqueia a motobomba e abre a solenoide, que enche a caixa só até a boia de backup, mais baixa, para sobrar volume para a próxima chuva. Motobomba e solenoide nunca funcionam juntas. Na volumetria, os cabos de comando — das chaves de nível ao quadro e dele à motobomba e à solenoide — aparecem tracejados, e a lógica completa está na ficha do quadro. O arranjo é um ponto de partida: posições, percursos e peças são do projetista.

Com esses dados o programa monta também a prancha do esquema 3D, fora de escala e em folha A3 deitada. Só os níveis que organizam a instalação — cisterna, reservatório superior, motobomba, filtro e descarte — ganham plano de cota; as peças pequenas aparecem no desenho pelo código, e o tipo e a cota de cada uma estão na tabela «Peças e acessórios», ao lado da sequência de montagem e do quantitativo por diâmetro.

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
