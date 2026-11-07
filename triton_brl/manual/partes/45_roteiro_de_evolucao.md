# Roteiro de evolução

> Para onde o programa deve ir, e com que evidência. Um roteiro que separa o que está
> decidido do que é intenção deixa o usuário planejar o estudo com a versão que tem hoje,
> e não com a que gostaria de ter.

Esta seção resume o `ROADMAP.md` da raiz do repositório Triton, que vale para as três edições e reflete o estado da versão
0.1.0 (beta). Nada do que está abaixo da linha «Estável» existe nesta versão: são intenções do
grupo de pesquisa, sem data de entrega. Quando um item é implementado, ele sai daqui e
entra no histórico de versões, com a indicação de se muda o resultado de estudos já
feitos.

A direção vem de duas fontes. A primeira é a revisão sistemática da literatura que o grupo
conduz: 762 estudos quantitativos sobre a simulação do aproveitamento de água de chuva, dos
quais 56 usam o Triton. Ela mostra onde os estudos publicados omitem a regra de operação, a
definição de confiabilidade e os parâmetros econômicos. A segunda é o registro de pendências
do próprio programa, descrito na seção «Limitações conhecidas».

---

## O que já é estável na 0.1.0 (beta)

**Série climática.** 652 municípios brasileiros com séries contínuas projetadas (base
CLIMBra, CMIP6). **Tarifas.** 652 municípios com catálogo de tarifas transcritas de fontes
oficiais. **Balanço hídrico.** Simulação diária pela regra do Triton, com a YAS estrita, a
YBS e o parâmetro φ de Fewkes (2000b) como opções para reservatório único. **Decisão.**
Multicritério por TOPSIS e por SMAA-VIKOR. **Incerteza.** Modulação probabilística das
premissas (seção «O que é a modulação probabilística»). **Edições.** Brasil, Internacional
e Portugal.

---

## Versão 1.1: consolidação e confiabilidade

<!-- tabela: Itens previstos para a versão 1.1 -->
| Eixo | Item | Método |
| :--- | :--- | :--- |
| Edição Internacional | Provedores globais de chuva | Reanálises ERA5-Land e NOAA GHCN-Daily |
| Edição Internacional | Unidades métricas e imperiais | Conversão sem resíduo, com a conservação de massa conferida nas duas |
| Edição Internacional | Tarifas sazonais e de escassez | Blocos dinâmicos, sobretaxa de seca, esgoto separado |
| Decisão multicritério | Ordenação completa com plano GAIA | PROMETHEE II |
| Decisão multicritério | Limiares de veto e classes de viabilidade | ELECTRE Tri |
| Decisão multicritério | Pesos mais consistentes | Best-Worst Method (BWM) |
| Probabilidade e risco | Dependência entre chuva e demanda | Cópulas bivariadas (Clayton, Gumbel) |
| Probabilidade e risco | Quais variáveis governam o resultado | Índices de Sobol de primeira ordem e totais |
| Probabilidade e risco | Chuva sintética | Bootstrap em blocos, com os dias secos consecutivos preservados |
| Custos e engenharia | Custo de implantação por material e por solo | Curvas paramétricas por tecnologia e por classe de solo |
| Custos e engenharia | Custo de operação detalhado | Filtros, desinfecção, curva de degradação da bomba |

## Versão 2.0: fronteira metodológica

<!-- tabela: Itens previstos para a versão 2.0 -->
| Eixo | Item | Método |
| :--- | :--- | :--- |
| Física do sistema | Passo de tempo horário | Modelo horário com dados de pluviógrafo |
| Física do sistema | Balanço hídrico na zona radicular | FAO-56 Penman-Monteith, para irrigação |
| Física do sistema | Coeficiente de escoamento variável | Dependente da lâmina e da estiagem antecedente |
| Territorial | Escala de bacia urbana | Vetores GeoJSON |

---

## Como ler este roteiro

**A ordem não é um compromisso de data.** A ordem segue a consequência sobre o resultado de
um estudo. O passo horário, por exemplo, só chega na 2.0 porque exige dados de pluviógrafo
que a maioria dos municípios não tem.

**Um item entra pela evidência.** Cada método listado responde a uma lacuna medida na
revisão da literatura, e não a uma preferência de implementação.

**Uma mudança que altera resultados é declarada.** Quem publica com o programa precisa
registrar a versão usada. Por isso o histórico de versões separa a correção que muda um
número de estudo já feito da que muda só a interface.
