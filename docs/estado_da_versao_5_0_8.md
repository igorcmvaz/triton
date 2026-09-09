# Netuno 5.0.8 — o que mudou e o que precisa da sua decisão

Documento de leitura, escrito ao fim da revisão. O detalhe valor a valor está em
[`procedencia_fatores_co2.md`](procedencia_fatores_co2.md).

**527 testes passando.** Trabalho em `versao-5.0.8-procedencia`, dez commits,
nada mesclado ao `main`.

---

## 1. Precisa da sua decisão

**Com dados brasileiros de energia, o sistema pluvial deixa de compensar em
carbono no horizonte de vinte anos.**

O SNIS publica 0,67 kWh por m³ de água distribuída em 2022. Com a matriz
elétrica brasileira, que é limpa, a emissão evitada por metro cúbico cai de
0,350 para 0,147 kg CO₂e/m³. Numa cisterna de 5.000 L com 40 m de tubulação:

| | Padrão atual | Dados brasileiros |
| :--- | ---: | ---: |
| Payback ambiental | 8,2 anos | **23,0 anos** |
| Economia em 20 anos | +372 kg | **−34 kg** |

Não é artefato de modelagem. Água tratada no Brasil carrega pouco carbono,
então deslocá-la economiza pouco, enquanto o reservatório e a tubulação custam
carbono para fabricar do mesmo jeito. É o inverso do que se vê em país de matriz
suja.

**Não troquei o padrão.** Trocar inverte a conclusão de todo estudo ambiental já
feito com o programa. A rota brasileira está selecionável na aba ambiental, sob
«Rede pública brasileira (SNIS + matriz elétrica local)».

Três ressalvas antes de decidir: a parcela não energética de 0,09 kg CO₂e/m³ é
deduzida de fonte espanhola, não medida no Brasil; o indicador do SNIS é energia
por m³ **produzido**, e as perdas de distribuição elevariam a emissão evitada
por m³ entregue; e carbono não é o único critério — economia de água potável,
de dinheiro e de escoamento superficial continuam de pé.

---

## 2. Erros de lógica corrigidos

Cinco defeitos que davam resposta errada em silêncio.

**Cloração, ultravioleta e ozônio eram exclusivos entre si**, e o programa
admitia «sem desinfecção». Contraria o item 4.6.5 da NBR 15527:2019, que
trabalha com cloro residual livre: residual é proteção continuada, e nem
ultravioleta nem ozônio deixam residual. A cloração passou a ser sempre
aplicada, com as outras como estágios adicionais.

**A energia do reator ultravioleta não entrava em custo nem em emissão.** Era
calculada e descartada. O ultravioleta aparecia quase de graça.

**O cloro tinha três convenções incompatíveis.** Dose de 2,0 mg/L no módulo
ambiental contra 1,5 no de qualidade; fator por quilo de cloro puro contra por
quilo de pastilha a 65%; e o econômico cobrava o preço sobre cloro ativo,
subestimando o custo em 35%. O fator de 25,0 kg CO₂e/kg não tinha fonte, é
implausível por uma ordem de grandeza, e era **idêntico** ao preço de 25,00
R$/kg no banco de custos.

**Os parâmetros do Netuno 4 não eram lidos.** O Netuno 4 exporta só a tabela de
varredura e guarda a configuração no nome do arquivo. O parser ignorava o nome e
devolvia a configuração padrão inteira, com aparência de leitura bem-sucedida.
Um arquivo que diz `Descarte2` e `Percentual90` era lido como 1 mm e 40%.

**O coeficiente de escoamento tinha quatro padrões diferentes** — 0,75 na
interface, 0,85 no exportador CAD, 0,90 no motor e na planilha. O mesmo projeto
rendia captações diferentes conforme o caminho de entrada.

**Os módulos econômico e ambiental calculavam a energia da bomba de dois
jeitos.** O econômico por potência vezes horas dividido pelo rendimento; o
ambiental por volume vezes um consumo específico de 0,40 kWh/m³ sem origem. A
mesma física dá 0,333 para a bomba padrão. O valor passou a ser derivado, de
modo que os dois caminhos não podem mais divergir.

**As faixas do pré-filtro contradiziam os próprios rótulos.** Os limites eram
150 e 400 m², contra rótulos de «até 200 m²» e «até 500 m²». Um telhado de
180 m² recebia o filtro da faixa seguinte, mais caro em R$ 600.

E dois menores: o gráfico de balanço usava 0,35 kg CO₂e/m³ fixo, ignorando o
fator da interface; e o campo de energia da bomba nascia com 0,085, que é o
fator da rede.

---

## 3. O erro que eu mesmo introduzi, e desfiz

Numa etapa intermediária troquei o fator da rede elétrica pela série do
MCTI/SIRENE. Foi erro de grandeza: aquela série é de **CO₂ apenas** e cobre só a
geração, enquanto uma ACV precisa de CO₂-equivalente e de fronteira mais ampla.
Você apontou, e está desfeito. O programa agora carrega bases nomeadas — SIDAC,
CaDI, e os indicadores do seu artigo de 2025 — cada uma com gás e fronteira
declarados, e um teste reprova se o fator da ACV voltar a ficar abaixo do de CO₂
da geração.

---

## 4. Valores que ganharam fonte

| Valor | Antes | Agora | Fonte |
| :--- | ---: | ---: | :--- |
| PEAD, resina | 3,00 | 1,612 | Franklin Associates para o American Chemistry Council (2020) |
| PVC, tubo | 2,80 | 2,36 | EPD Australasia S-P-05503, por kg de tubo instalado |
| PRFV | 4,25 | 3,25 | Composites UK, faixa de 2,5 a 4,0 |
| Aço inox | 2,89 | 3,70 | worldstainless, ponto de 50% de sucata |
| Concreto | 0,14 | 0,14 | corroborado pelo SIDAC |

E as massas, que estavam piores que os fatores:

**Tubos.** O DN 110 estava **47% abaixo** do peso real, o DN 20 estava 36%
acima. Agora vêm de peso de produto da Amanco Wavin para DN 20 a 60, e da
geometria das NBR 5648 e 5688:2018 para os demais. Os seis pesos reais implicam
densidade efetiva de 1,511 g/cm³ com dispersão de apenas 1,504 a 1,516, e é essa
consistência que valida a extensão aos diâmetros sem peso publicado.

**Reservatório em PRFV.** O programa usava densidade constante de 20 kg/m³. O
catálogo Fortlev mostra economia de escala: a constante superestimava um
reservatório de 10.000 L em **46%**.

---

## 5. A NBR 15527:2019, conferida

A Tabela 1 do item 4.6.3 traz **três** parâmetros para todos os usos não
potáveis: *E. coli* < 200/100 mL, turbidez < 5,0 uT e pH de 6,0 a 9,0. Mais o
item 4.6.5, com cloro residual livre de 0,5 a 2,0 mg/L.

**Não há matriz de quatro classes na norma.** A Classe 1 do programa corresponde
ao conjunto normativo; as Classes 2 a 4 passaram a ser apresentadas como
escalonamento de projeto. E o descarte recomendado no item 4.3.5 é de **2 mm**,
não 1 mm como o programa dizia.

---

## 6. Documentação

Cinquenta e seis referências num módulo único, recuperadas do Crossref, do
OpenAlex ou da página do periódico. As catorze páginas técnicas recebem o bloco
de referências automaticamente, nos dois idiomas, e um teste reprova seção
abaixo de três citações.

A conferência achou quatro defeitos na lista anterior: Walsh & Lawler com
título, periódico e páginas errados; Lahdelma com inicial trocada; o artigo da
MIX Sustentável sem autoria nenhuma; e duas datas de acesso no futuro.

Os nove índices agora mostram a equação de cada um. E, atendendo à sua crítica,
reescrevi as passagens que narravam o histórico de edição do programa em vez de
dizer o que o programa usa.

---

## 7. O que continua sem fonte

**Motobombas.** Seis valores, quatro deles extrapolação aritmética. A busca foi
feita e está registrada no código para não se repetir: nem Schneider, nem
Fortlev, nem Bakof publicam massa por modelo, e a literatura de ACV de bombas
trata de equipamentos industriais, cuja fase de operação responde por mais de
99% do impacto — proporção que não vale para uma bomba residencial de meio CV
ligada poucas horas por ano, em que o incorporado chega a um quarto do total.
O código agora declara, por potência, o que é estimativa e o que é extrapolação.

**Massa do reservatório em polietileno.** Fortlev e Bakof publicam dimensões,
não pesos. Especificações de revendedor dão 17 a 21 kg/m³, e um dado de 5.000 L
quebra a tendência, provavelmente por incluir tampa ou embalagem. Os 22 kg/m³ do
programa ficam dentro da faixa observada, mas sem tabela.

**Fator do hipoclorito.** O 1,85 kg CO₂e/kg está atribuído ao Ecoinvent v3.8 sem
nomear o processo nem a geografia. Continua atribuição de base, não de
procedência.

**Coeficientes de lavagem.** Os três *k* estão ancorados no artigo do Maykot como
referência de apoio, e declarados como parâmetros de projeto. Um ajuste de
verdade exigiria os dados brutos.

**Menores:** vida útil de 20 anos, 80 eventos de chuva por ano e turbidez bruta
de 45 NTU.

**Lacuna de apresentação, não de número.** O gerador de relatórios prepara
alguns valores e não os insere no documento: o percentual de dias em que a
demanda pluvial não foi atendida, no relatório executivo, e a dose de cloro, no
ambiental. São informações calculadas e omitidas, e ficam anotadas para uma
próxima passagem.

---

## 8. O aviso do Qt

Não consegui reproduzi-lo: não existe chamada a `setPointSize` no pacote, e nem
a janela principal, nem as dezesseis páginas, nem as vinte e quatro classes de
gráfico o disparam em teste headless. Instalei um capturador que mostra cada
aviso uma só vez e grava a pilha Python em `avisos_qt.log`. Você disse que ele
não apareceu mais; se voltar, o log dirá de onde vem.
