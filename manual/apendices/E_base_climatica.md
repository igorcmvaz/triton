# Base climática

![Logotipo do conjunto de dados CLIMBra](../figuras/CLIMBra.jpg)

---

## O que a base contém

<!-- tabela: Conteúdo da base climática nacional -->
| O que a base traz | Quantidade |
| :--- | ---: |
| cidades brasileiras | 652 |
| modelos climáticos do CMIP6 | 19 |
| cenários de emissão | 2, SSP2-4.5 e SSP5-8.5 |
| simulações por cidade e modelo | 3: histórica, SSP2-4.5 e SSP5-8.5 |
| total de séries temporais | 37.164 séries |
| formato original descompactado | ~6,5 GB (CSVs) |
| formato compilado do Netuno 5 | Banco SQLite comprimido (`climbra.db`) |

Cada série é um registro diário contínuo de precipitação, em milímetros, para uma combinação de
cidade, modelo e simulação: 652 cidades × 19 modelos × 3 simulações dão as 37.164
séries. As séries vêm do **CLIMBra** (Ballarin et al., 2023, [*Scientific Data / Nature*](https://www.nature.com/articles/s41597-023-01956-z), [doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z); repositório [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316), [doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)), corrigidas de viés por
*Quantile Delta Mapping* contra a grade diária de Xavier, King e Scanlon (2016), com
resolução de 0,25°. A histórica cobre de 1980 a 2013 (12.419 dias) e as futuras, de 2015 a 2100 (31.411 dias); as
janelas de estudo são recortes livres dessas séries. Todas estão em calendário
gregoriano. Os modelos HadGEM3-GC31-LL, KACE e UKESM1-0-LL, que usam originalmente anos
de 360 dias, têm um dia a menos no fim de cada série, o que não afeta o recorte.

---

## Embarque no executável e formato otimizado

Para evitar a manipulação morosa de dezenas de milhares de arquivos de texto e viabilizar
a distribuição direta no instalador e executável do Netuno 5, as 37.164 séries foram
compiladas e indexadas em um banco de dados **SQLite de alta eficiência** (`climbra.db`), com
compressão binária por série via `zlib`.

- **Velocidade de acesso:** O acesso indexado no banco leva **menos de 1 milissegundo** por série, contra dezenas de milissegundos na abertura e parse de arquivos CSV em disco.
- **Transparência:** O motor de dados climáticos do Netuno 5 prioriza o banco compilado e recorre automaticamente à pasta de arquivos `.csv` soltos se o banco não for encontrado.
- **Portabilidade:** Permite ao instalador do Netuno 5 fornecer a base nacional pronta para uso sem exigir download manual e descompactação de 6,5 GB pelo usuário.

---

## Os cenários

As duas trajetórias socioeconômicas compartilhadas do CMIP6 disponíveis na base, as *Shared Socioeconomic Pathways*, estão desenhadas na seção {{n:15}}: o SSP2-4.5 é a trajetória intermediária e o SSP5-8.5 supõe emissões altas sem mitigação. O CLIMBra não inclui cenários de mitigação forte, como o SSP1-2.6.


---

## As séries históricas que acompanham o programa

Independentes da base CMIP6, quatro séries históricas longas acompanham a
instalação, na pasta `data/rainfall` do programa:

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
