# Séries de chuva de exemplo (IBE)

| Ficheiro | Local | Período | Fonte |
|---|---|---|---|
| `Funchal.csv` | Funchal (32,65 N, 16,90 O, grelha a 323 m de altitude) | 01/01/1991 a 31/12/2020, 10.958 dias | Open-Meteo, reanálise ERA5 |

Formato: um valor por linha, precipitação diária em milímetros, sem data (a data inicial vem do projeto: 01/01/1991).

O Funchal não tem série E-OBS utilizável (22% de dias sem dados no período, acima do limite de 1%); por isso o exemplo usa a reanálise ERA5. A média anual da reanálise (cerca de 538 mm) vem de uma célula de grelha de 9 km a 323 m de altitude e pode diferir da média medida na estação do Funchal; para um projeto real, use a série medida.

Lisboa, Porto, Madrid e Palma usam o Iberia01 por município (`data/chuva_iberia01_p*.db`), sem ficheiro de série; o exemplo do Funchal usa a mesma ERA5 pela base das ilhas (`data/chuva_ilhas_era5.db`, 1986–2015).

Atribuição: dados meteorológicos de Open-Meteo.com (licença CC BY 4.0), baseados na reanálise ERA5 do ECMWF (Copernicus Climate Change Service: Hersbach et al., 2020, *Q. J. R. Meteorol. Soc.* 146, 1999-2049). Obtidos em 14/10/2026 pela API de arquivo (`archive-api.open-meteo.com`).
