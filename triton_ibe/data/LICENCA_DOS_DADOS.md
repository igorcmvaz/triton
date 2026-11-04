# Licença e uso dos dados desta pasta (Triton, Edição Ibérica, 0.1.0)

Os ficheiros desta pasta **não são o programa**. O código do Triton segue o `LICENSE.md` (licença académica, fonte disponível,
uso não comercial). Os dados abaixo mantêm a licença de quem os produziu. O texto completo das atribuições está em
`infos_licenses/AVISOS_DE_TERCEIROS.txt`; a descrição, a qualidade e as limitações de cada conjunto estão em `docs/DADOS.md`.

| Ficheiros | Conteúdo | Licença | O que se pode fazer |
| :-- | :-- | :-- | :-- |
| `chuva_iberia01_p1..p4.db`, `iberia01_partes.json`, `ibe_unidades.db`, `qualidade_eobs_odbl.db` | Chuva diária por célula do Iberia01 v1.0 (1971–2015), ligação célula–município, pesos e nível de qualidade | **ODbL 1.0** (base derivada do Iberia01) | Usar, copiar e adaptar com atribuição; uma base derivada destes ficheiros fica também sob ODbL e **separada do programa**. Relatórios e gráficos são «Produced Works» e pedem só a atribuição. |
| `chuva_ilhas_era5.db` | Chuva diária ERA5 das Canárias, da Madeira e dos Açores (nível de qualidade C) | **CC BY 4.0** (Open-Meteo / Copernicus C3S) | Usar com atribuição e indicação de alterações. |
| `portugal_eobs.db` (opcional) | Chuva diária E-OBS por concelho | Licença do produto E-OBS: **só uso não comercial** | Investigação e ensino. O uso comercial está bloqueado e avisado a vermelho nos relatórios. |
| `portugal/`, `rainfall/Funchal.csv` | Limites CAOP 2025 (DGT, cc-by); série de exemplo do Funchal (Open-Meteo, CC BY 4.0) | conforme a fonte | Com atribuição. |

## Atribuição a incluir ao usar a chuva do Iberia01

> Contains information from Iberia01, made available under the Open Database License (ODbL 1.0).
> Herrera, S., Cardoso, R. M., Soares, P. M. M., Espírito-Santo, F., Viterbo, P., Gutiérrez, J. M. (2019). Iberia01: a new gridded
> dataset of daily precipitation and temperatures over Iberia. *Earth System Science Data* 11, 1947–1956.
> doi:10.5194/essd-11-1947-2019. Dados: doi:10.20350/digitalCSIC/8641.

Os relatórios do Triton já trazem esta frase quando a chuva vem do Iberia01. Para a chuva ERA5 das ilhas: *Contains modified
Copernicus Climate Change Service information; Hersbach et al. (2020), doi:10.1002/qj.3803; dados Open-Meteo.com (CC BY 4.0).*

## Outros dados da edição (fora desta pasta)

- **Limites de Espanha** (Eurostat/GISCO, LAU 2023): © EuroGeographics, reutilização com atribuição. **INE**: reutilização com citação da fonte.
- **Tarifários de Portugal e de 7 municípios de Espanha** (`triton/data/` e `tarifas_portugal/`): valores públicos regulados, transcritos de
  documentos oficiais com URL, data e SHA-256 em `FONTES.tsv`; os documentos não são redistribuídos. **Os valores de Espanha ainda não
  tiveram a segunda leitura (não conferidos)** e o programa avisa disso nos relatórios. O índice de entidades gestoras vem da ERSAR
  (© ERSAR, todos os direitos reservados; referência ao documento original).

## Limites de uso

A chuva por município é uma média de células de 0,1° e **não substitui** uma série medida no local. O nível de qualidade (A, B ou C) de cada
município está em `ibe_unidades.db` e é mostrado no relatório. Quem publicar resultados deve citar a versão do Triton (DOI
10.5281/zenodo.23402916) e as fontes acima.
