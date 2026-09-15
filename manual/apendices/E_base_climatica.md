# Base climática

---

## O que a base contém

<!-- tabela: Conteúdo da base climática nacional -->
| O que a base traz | Quantidade |
| :--- | ---: |
| cidades brasileiras | 652 |
| modelos climáticos do CMIP6 | 19 |
| cenários de emissão | 3 |
| janelas temporais | 3 |
| tamanho aproximado | 6,5 GB |
| arquivos | cerca de 37 mil |

Cada arquivo é uma série diária de precipitação, em milímetros, para uma combinação
de cidade, modelo, cenário e janela.

---

## Por que é distribuída à parte

Seis vírgula cinco gigabytes não cabem numa distribuição de programa. A base é
obtida separadamente e instalada no diretório que o programa indica.

**Sem ela**, a aba de Projeto oferece apenas o carregamento de arquivo próprio, as
abas dependentes avisam, e os testes que a exigem são pulados em vez de falharem. O
programa continua inteiramente funcional com séries do usuário.

---

## Os cenários

As *Shared Socioeconomic Pathways* do CMIP6:

As três trajetórias estão desenhadas na seção {{n:15}}: o SSP1-2.6 supõe emissões em queda rápida, o SSP2-4.5 é a trajetória intermediária e o SSP5-8.5 supõe emissões altas sem mitigação.


---

## As séries históricas que acompanham o programa

Independentes da base CMIP6, quatro séries históricas longas acompanham a
instalação, na pasta `data
ainfall` do programa:

<!-- tabela: Séries históricas de precipitação distribuídas com o programa -->
| Cidade | Arquivos |
| :--- | ---: |
| Florianópolis | 3 |
| Brasília | 3 |
| Manaus | 3 |
| São Paulo | 3 |

A série de Florianópolis usada no tutorial tem 86 anos; os trinta primeiros anos
somam 1.795 mm anuais médios, com chuva em 46% dos dias.

---

## O que declarar num estudo

- **modelo ou modelos**, pelo nome, e o critério de seleção;
- **cenário** SSP;
- **janela temporal**, com os anos;
- a **série histórica** usada como referência;
- se houve *downscaling* ou correção de viés, e qual;
- a **procedência e a versão** da base.

A seção {{n:15}} trata da condução do estudo com cenários futuros, e alerta para o erro de
escolher o modelo pelo resultado.
