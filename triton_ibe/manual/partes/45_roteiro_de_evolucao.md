# Roteiro de evolução

> Para onde o programa deve ir, e com que evidência. Um roteiro que separa o que está decidido do
> que é intenção permite ao utilizador planear o estudo com a versão que tem hoje, e não com a que
> gostaria de ter.

Esta secção resume o `ROADMAP.md` da raiz do repositório do Triton, que vale para as três edições e
reflete o estado da versão beta 0.1.0. Nada do que está abaixo da linha «Estável» existe nesta
versão: são intenções do grupo de investigação, sem data de entrega. Quando um item é
implementado, sai daqui e entra no histórico de versões, com a indicação de se muda os resultados
de estudos já feitos.

A direção vem de duas fontes. A primeira é a revisão sistemática da literatura que o grupo conduz
sobre a simulação do aproveitamento de águas pluviais; mostra onde os estudos publicados omitem a
regra de operação, a definição de fiabilidade e os parâmetros económicos. A segunda é o registo de
pendências do próprio programa, descrito na secção «Limitações conhecidas».

---

## O que já é estável na 0.1.0

**Série climática.** Chuva diária do Iberia01 por município (Portugal, Espanha e Baleares; normal 1986–2015), a E-OBS opcional (278 concelhos, 1950 a
2025), a reanálise ERA5 das ilhas (nível C) e séries diárias fornecidas pelo utilizador. **Tarifas.** Os
tarifários transcritos de Lisboa, do Porto e do Funchal, e estruturas introduzidas pelo utilizador,
com escalões progressivos, partes fixas e atualização. **Balanço hídrico.** Simulação diária pela
regra do Triton, com a YAS estrita, a YBS e o parâmetro φ de Fewkes (2000b) como opções para
reservatório único. **Decisão.** Multicritério por TOPSIS e por SMAA-VIKOR. **Incerteza.**
Modulação probabilística das premissas (secção «O que é a modulação probabilística»).
**Edição.** Portugal.

A versão 1.0 será a primeira versão oficial, depois dos ajustes das versões 0.x.

---

## Versão 1.1: consolidação e fiabilidade

Os três primeiros itens vêm do roteiro comum e dizem respeito sobretudo à Edição Internacional.

<!-- tabela: Itens previstos para a versão 1.1 -->
| Eixo | Item | Método |
| :--- | :--- | :--- |
| Dados e tarifas | Fornecedores globais de chuva | Reanálises ERA5-Land e NOAA GHCN-Daily |
| Dados e tarifas | Unidades métricas e imperiais | Conversão sem resíduo, com a conservação de massa conferida nas duas |
| Dados e tarifas | Tarifas sazonais e de escassez | Escalões dinâmicos, sobretaxa de seca, saneamento separado |
| Decisão multicritério | Ordenação completa com plano GAIA | PROMETHEE II |
| Decisão multicritério | Limiares de veto e classes de viabilidade | ELECTRE Tri |
| Decisão multicritério | Pesos mais consistentes | Best-Worst Method (BWM) |
| Probabilidade e risco | Dependência entre chuva e procura | Cópulas bivariadas (Clayton, Gumbel) |
| Probabilidade e risco | Que variáveis governam o resultado | Índices de Sobol de primeira ordem e totais |
| Probabilidade e risco | Chuva sintética | Bootstrap em blocos, com os dias secos consecutivos preservados |
| Custos e engenharia | Custo de instalação por material e por solo | Curvas paramétricas por tecnologia e por classe de solo |
| Custos e engenharia | Custo de exploração detalhado | Filtros, desinfeção, curva de degradação da bomba |

## Versão 2.0: fronteira metodológica

<!-- tabela: Itens previstos para a versão 2.0 -->
| Eixo | Item | Método |
| :--- | :--- | :--- |
| Física do sistema | Passo de tempo horário | Modelo horário com dados de udógrafo |
| Física do sistema | Balanço hídrico na zona radicular | FAO-56 Penman-Monteith, para a rega |
| Física do sistema | Coeficiente de escoamento variável | Depende da lâmina e da estiagem antecedente |
| Territorial | Escala de bacia urbana | Vetores GeoJSON |

---

## Como ler este roteiro

**A ordem não é um compromisso de datas.** A ordem segue a consequência sobre o resultado de um
estudo. O passo horário, por exemplo, só chega na 2.0 porque exige dados de udógrafo que a maioria
dos concelhos não tem.

**Um item entra pela evidência.** Cada método listado responde a uma lacuna medida na revisão da
literatura, e não a uma preferência de implementação.

**Uma alteração que muda resultados é declarada.** Quem publica com o programa tem de registar a
versão usada. Por isso o histórico de versões separa a correção que muda um número de um estudo
já feito da que muda só a interface.
