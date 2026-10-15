# Séries de chuva de exemplo (INT)

| Arquivo | Local | Período | Fonte |
|---|---|---|---|
| `NewYork.csv` | Nova York (ponto de grade de Manhattan, 40,81 N, 74,02 O) | 01/01/1991 a 31/12/2020, 10.958 dias | Open-Meteo, reanálise ERA5 |
| `London.csv` | Londres (51,49 N, 0,16 O) | idem | idem |
| `CapeTown.csv` | Cidade do Cabo (33,99 S, 18,43 L) | idem | idem |

Formato: um valor por linha, precipitação diária em milímetros, sem data (a data inicial vem do projeto: 01/01/1991).

São dados de **reanálise** (ponto de grade de cerca de 9 km), não de pluviógrafo: servem de exemplo e de ponto de partida; para um projeto real, use a série medida do local.

Atribuição: dados meteorológicos de Open-Meteo.com (licença CC BY 4.0), baseados na reanálise ERA5 do ECMWF (Copernicus Climate Change Service: Hersbach et al., 2020, *Q. J. R. Meteorol. Soc.* 146, 1999-2049). Obtidos em 14/10/2026 pela API de arquivo (`archive-api.open-meteo.com`).
