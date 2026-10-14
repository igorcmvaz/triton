# Emissão evitada por m³: procedência de cada rota

A emissão evitada por metro cúbico **não é uma constante do sistema pluvial**. É
propriedade da água que ele deixa de consumir. Substituir água dessalinizada por
via térmica vale trinta vezes mais do que substituir água de manancial tratada
com matriz elétrica limpa, e o programa permite declarar qual é o caso.

**A base do programa é 0,35 kg CO₂e/m³**, da rota `convencional_br`. É o valor de
partida, escolhido por ficar logo abaixo das faixas publicadas para tratamento
convencional tanto com matriz europeia quanto com matriz brasileira, e portanto
ser conservador: subestimar o benefício do sistema pluvial é o erro seguro, já
que uma conclusão de viabilidade obtida assim continua valendo se o número
verdadeiro for maior.

---

## A fronteira, antes dos números

O sistema pluvial substitui água **entregue** na edificação, e não água
**produzida** na estação. Entre uma e outra estão as perdas de distribuição, que
no Brasil são grandes:

| Macrorregião | Perdas | Produzir para entregar 1 m³ |
| :--- | ---: | ---: |
| Sudeste | 33,9% | 1,51 m³ |
| Centro-Oeste | 35,1% | 1,54 m³ |
| Sul | 36,7% | 1,58 m³ |
| Nordeste | 46,7% | 1,88 m³ |
| Norte | 46,9% | 1,88 m³ |

Um valor publicado na porta da estação subestima o benefício do sistema pluvial
em 50 a 88%. É o que separa os 0,236 kg CO₂e/m³ que Vaz et al. (2025) declaram
no texto dos 0,336 a 0,461 por m³ entregue que se obtêm das tabelas do mesmo
artigo. Não são valores discordantes: são a mesma água medida em dois pontos.

Três rotas do catálogo levam `fronteira_incompleta` e a interface avisa ao
selecioná-las. Servem como **limite inferior declarado**, nunca como estimativa
central.

---

## O catálogo

Valores calculados com fator de rede de 0,085 kg CO₂e/kWh onde a rota é
recalculada com a matriz local.

### Tratamento convencional

| Rota | kg CO₂e/m³ | Fonte | Matriz |
| :--- | ---: | :--- | :--- |
| `convencional_br` **(base)** | 0,350 | Adotada pelo programa | — |
| `vaz_2025_sudeste` | 0,336 | Vaz et al. (2025) | Brasil 2022 |
| `vaz_2025_sul` | 0,368 | Vaz et al. (2025) | Brasil 2022 |
| `vaz_2025_centro_oeste` | 0,379 | Vaz et al. (2025) | Brasil 2022 |
| `vaz_2025_brasil` | 0,394 | Vaz et al. (2025) | Brasil 2022 |
| `vaz_2025_norte` | 0,426 | Vaz et al. (2025) | Brasil 2022 |
| `vaz_2025_nordeste` | 0,461 | Vaz et al. (2025) | Brasil 2022 |
| `convencional_garfi` | 0,440 | Garfí et al. (2016) | Espanha |
| `convencional_paquistao_jamil` | 0,450 | Jamil et al. (2023) | Paquistão |
| `eta_matriz_limpa_escocia` | 0,180 | Lui, Lee & Sloan (2025) | Reino Unido |

### Tratamento avançado e dessalinização

| Rota | kg CO₂e/m³ | Fonte |
| :--- | ---: | :--- |
| `dessalinizacao_osmose_reversa` | 0,369 | Vieira et al. (2014), recalculada com a matriz local |
| `convencional_com_osmose_domiciliar` | 0,512 | Garfí et al. (2016), cenário 3 |
| `osmose_reversa_na_eta` | 1,020 | Garfí et al. (2016) |
| `dessalinizacao_termica` | 12,000 | Nagar & Pradeep (2020) |

### Água engarrafada

| Rota | kg CO₂e/m³ |
| :--- | ---: |
| `agua_mineral_vidro` | 60,800 |
| `agua_mineral_pet` | 75,100 |

### Fronteira incompleta — limite inferior, não estimativa

| Rota | kg CO₂e/m³ | O que falta |
| :--- | ---: | :--- |
| `rede_publica_brasil_snis` | 0,147 | Parte de um indicador de energia; sem inventário próprio de químicos, infraestrutura e lodo |
| `eta_matriz_limpa_escocia`* | 0,180 | Tratamento apenas, sem distribuição |
| `vaz_2025_porta_da_eta` | 0,236 | Por m³ produzido, antes das perdas |
| `abastecimento_urbano_china` | 0,213 | Somente eletricidade |

\* a rota escocesa não leva a marca, porque a fonte separa tratamento de
distribuição por desenho, e o valor é usável dentro dessa leitura.

---

## Por que a rota do SNIS não é o padrão

O indicador IN058 do SNIS mede consumo de energia elétrica em sistemas de
abastecimento: 0,67 kWh/m³ no Brasil em 2022. Com a matriz nacional, isso dá
cerca de 0,057 kg CO₂e/m³, e somando uma parcela não energética deduzida por
proporção chega-se a 0,147.

O problema não é o número, é o método. **Uma avaliação de ciclo de vida é mais do
que energia**: produtos químicos, infraestrutura da rede, lodo, construção da
estação. Uma rota montada a partir de um indicador energético omite parcelas que
existem, e por construção subestima.

Adotá-la como padrão levaria o payback ambiental de 8,5 para 32,6 anos e o saldo
de 20 anos de +379 para −109 kg num sistema de 5.000 L com 100 kWh/ano de
recalque, e o faria com uma fronteira que se sabe incompleta. Continua no
catálogo porque o limite inferior é informação, e sinalizada porque um limite
inferior apresentado como estimativa central é desinformação.

---

## Referências

- **Garfí, M., Cadena, E., Sanchez-Ramos, D. & Ferrer, I.** (2016). Life cycle
  assessment of drinking water: comparing conventional water treatment,
  reverse osmosis and mineral water in glass and plastic bottles. *Journal of
  Cleaner Production*. DOI [10.1016/j.jclepro.2016.07.218](https://doi.org/10.1016/j.jclepro.2016.07.218)
- **Jamil, S., Pervez, S. & Sarwar, F.** (2023). Lifecycle assessment of two
  urban water treatment plants of Pakistan. *Sustainability*, 15(23), 16172.
  DOI [10.3390/su152316172](https://doi.org/10.3390/su152316172)
- **Lui, J., Lee, S. & Sloan, W. T.** (2025). Life cycle assessment of drinking
  water and wastewater treatment works in mainland Scotland. *Science of the
  Total Environment*, 958, 177989.
  DOI [10.1016/j.scitotenv.2024.177989](https://doi.org/10.1016/j.scitotenv.2024.177989)
- **Nagar, A. & Pradeep, T.** (2020). Clean water through nanotechnology: needs,
  gaps, and fulfillment. *ACS Nano*, 14(6), 6420–6435.
  DOI [10.1021/acsnano.9b01730](https://doi.org/10.1021/acsnano.9b01730)
- **Smith, K. & Liu, S.** (2015). Contribution of urban water supply to
  greenhouse gas emissions in China. *Journal of Industrial Ecology*, 20(4),
  792–802. DOI [10.1111/jiec.12290](https://doi.org/10.1111/jiec.12290)
- **Vaz, I. C. M., Ghisi, E., Scolaro, T. P. & Schaefer, A.** (2025).
  Understanding the environmental impacts of residential water consumption in
  Brazil: integrating the building stock with life cycle assessment. *Building
  and Environment*, 279, 113085.
  DOI [10.1016/j.buildenv.2025.113085](https://doi.org/10.1016/j.buildenv.2025.113085)
- **Vieira, A. S., Beal, C. D., Ghisi, E. & Stewart, R. A.** (2014). Energy
  intensity of rainwater harvesting systems: a review. *Renewable and
  Sustainable Energy Reviews*.
  DOI [10.1016/j.rser.2014.03.012](https://doi.org/10.1016/j.rser.2014.03.012)
- **SNIS** (2023). *Diagnóstico Temático dos Serviços de Água e Esgoto*,
  ano-base 2022. Ministério das Cidades, Brasília.
