# Aeroportos de Santa Catarina com voos regulares: municípios da CLIMBra com aeroporto, 19 modelos, 7 recortes

Estudo `sc-aeroportuario` (esquema `triton-estudo`, versão 1), gerado por `scripts/gerar_estudos_sc.py`. Arquétipo: **terminal de passageiros e apoio de aeroporto regional**. Não edite o `estudo.json` à mão sem registrar: o gerador o reescreve.

## Escopo

- Municípios: os **4** com aeroporto de voos regulares e série na CLIMBra. Critério e lista completa (inclusive os excluídos e o motivo) em `../_fontes/aeroportos_sc.json`:

  - SBCH Serafin Enoss Bertaso (Chapecó): 5321 movimentos regulares em 2025, 12 meses com voo; no estudo.
  - SBFL Hercílio Luz (Florianópolis): 36439 movimentos regulares em 2025, 12 meses com voo; no estudo.
  - SBJA Regional Sul (Jaguaruna): 1022 movimentos regulares em 2025, 12 meses com voo; município sem série na CLIMBra: fora do estudo até o autor decidir como representar o clima.
  - SBJV Lauro Carneiro de Loyola (Joinville): 5026 movimentos regulares em 2025, 12 meses com voo; no estudo.
  - SBNF Ministro Victor Konder (Navegantes): 16566 movimentos regulares em 2025, 12 meses com voo; no estudo.
  - SNCP Aeroporto Ricardo Sell Wagner - Regional da Serra Catarinense (Correia Pinto): 134 movimentos regulares em 2025, 5 meses com voo; voos regulares realizados em 5 de 12 meses de 2025.
  - Critério: «com voos regulares»: ao menos um voo regular (VRA da ANAC) realizado em cada um dos 12 meses de 2025, como origem ou destino; sazonais e sem voo regular ficam de fora.
- Clima: CLIMBra (Ballarin et al., 2023, doi:10.1038/s41597-023-01956-z; CC0), **19 modelos** × **7 recortes** (`expansao.recortes`): histórico 1981–2010 e, para SSP2-4.5 e SSP5-8.5, futuro próximo 2021–2050, meados 2041–2070 e fim 2071–2100, os atalhos de `RECORTES_SUGERIDOS`. A série é a da célula de 0,25° do município; o histórico é simulado, não observado.
- Casos: 4 × 19 × 7 = **532** simulações (cada uma varre os volumes do reservatório).
- Análise: `economic`, volume no ótimo técnico, semente 42. Custos: estimativa preliminar do próprio programa (catálogo de preços), tarifas: catálogo municipal do programa.

## Arquétipo (todos os valores: estimativa de arquétipo, a refinar pelo autor)

| Parâmetro | Valor | Origem |
| --- | ---: | --- |
| Área de captação (m²) | 8000 | estimativa de arquétipo, a refinar pelo autor |
| Usuários (passageiros e funcionários presentes por dia, em equivalentes) | 3000 | estimativa de arquétipo, a refinar pelo autor |
| Demanda por usuário (L/dia) | 25 | estimativa de arquétipo, a refinar pelo autor |
| Fração atendível por chuva (%) | 50 | estimativa de arquétipo, a refinar pelo autor |
| Maior volume da varredura (L) | 120000 | estimativa de arquétipo, a refinar pelo autor |
| Passo da varredura (L) | 3000 | estimativa de arquétipo, a refinar pelo autor |
| Reservatório superior (L) | 10000 | estimativa de arquétipo, a refinar pelo autor |
| Categoria tarifária | comercial | escolha de arquétipo; sem tabela coletada para o município, usa a residencial (alerta no resultado) |
| Coeficiente de escoamento, descarte, demais campos | os do modelo da edição | padrão do programa |

Nenhum desses valores é medido nem tirado de norma. Para refinar, edite `padroes.substituicoes` (ou os do script) e cite a fonte de cada um; candidatas de leitura (DOI conferido; nenhum valor foi tirado delas):

- doi:10.3390/w4030607 — Potable Water Savings by Using Rainwater for Non-Potable Uses in Houses (Water, 2012)
- doi:10.3390/w8040110 — Potential for Potable Water Savings in Buildings by Using Stormwater Harvested from Porous Pavements (Water, 2016): setores residencial, público e comercial de Florianópolis
- doi:10.3390/w10040471 — Rainwater Harvesting in Buildings in Brazil: A Literature Review (Water, 2018)
- doi:10.3390/w11112351 — Reduction of Potable Water Consumption and Sewage Generation on a City Scale: A Case Study in Brazil (Water, 2019): Joinville, setores residencial, público e comercial
- doi:10.3390/w12020546 — Assessment of A Rainwater Harvesting System in A Multi-Storey Residential Building in Brazil (Water, 2020): Florianópolis

## Comandos

Na pasta `triton_brl` (edição Brasil):

```powershell
python -m triton.cli estudo validate estudos\santa-catarina\aeroportos\estudo.json
python -m triton.cli estudo run estudos\santa-catarina\aeroportos\estudo.json --saida estudos\santa-catarina\_saida\aeroportos --paralelo 4 --retomar
python -m triton.cli estudo texto estudos\santa-catarina\_saida\aeroportos --modelo estudos\santa-catarina\aeroportos\modelo_texto.md
```

`resultados.csv` é tidy: uma linha por município × modelo × recorte × métrica (colunas `municipio`, `ibge`, `modelo`, `recorte`, `cenario`, `inicio`, `fim`). A pasta `_saida/` não vai para o Git. Veja `../LEIA.md` para o custo da varredura completa.
