# Reprodução dos dados de chuva da edição IBE

Estes scripts reproduzem, a partir das fontes públicas, o banco `data/portugal_eobs.db`, a tabela `qualidade` (nível A, B ou C) e as verificações que as sustentam. Estão no Git por exceção (ver `.gitignore`). O programa, o instalador e os testes não dependem deles. Corra-os a partir da pasta `triton_ibe/`.

Todos os caminhos são relativos ao repositório e configuráveis por variável de ambiente (`_caminhos.py` lista-as). Nada aqui depende de uma pasta do computador de quem o escreveu.

## Fontes que tem de obter (fora do Git)

| Fonte | Para quê | Onde colocar (padrão) | Variável |
| :--- | :--- | :--- | :--- |
| E-OBS v33.0e, `rr_ens_mean_0.1deg_reg_v33.0e.nc` (cerca de 3 GB), https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php | a série de chuva | `data/portugal/fontes/` | `TRITON_IBE_FONTES` |
| CAOP 2025, quatro `.gpkg` (Continente, Madeira, Açores central e oriental, Açores ocidental), Direção-Geral do Território | limites dos concelhos | `data/portugal/fontes/caop/` | `TRITON_IBE_FONTES` |
| Iberia01 v1.0 diário, `Iberia01_v1.0_DD_010reg_aa3d_pr.nc` (DIGITAL.CSIC 10261/183071) | comparação do nível de qualidade | `scripts/dados/dados_brutos/iberia01/` | `TRITON_IBE_BRUTOS` |
| ECA&D (série não misturada), GHCN-D, Open-Meteo, CPC | validação contra estações | `scripts/dados/dados_brutos/` | `TRITON_IBE_BRUTOS` |

As licenças e as citações de cada fonte estão em `docs/DADOS.md` e em `resultados/LICENCAS_DOS_DADOS.md`.

## Reproduzir o banco `data/portugal_eobs.db`

```bash
cd triton_ibe
export TRITON_IBE_FONTES=/caminho/para/fontes        # se não estiverem em data/portugal/fontes
python scripts/dados/compilar_base_eobs_portugal.py --saida /tmp/portugal_eobs.db
python scripts/acrescentar_qualidade_ao_banco.py --csv tests/dados_ibe/qualidade_prototipo.csv --db /tmp/portugal_eobs.db
```

O primeiro passo compila as séries por concelho e aplica o critério de completude (mais de 1% de dias sem dado em 1991–2020 deixa o concelho de fora). O segundo acrescenta a tabela `qualidade` e as chaves de identificação do pacote. Sem `--saida`, o primeiro passo escreve em `data/portugal_eobs.db` e **substitui** o banco do repositório: use `--saida` para conferir.

Conferência: o conteúdo da tabela `series` é identificado por `sha256_pacote` (em `metadados`); o ficheiro final tem o SHA-256 indicado em `docs/DADOS.md`. Ver ali o resultado da reprodução.

## Reproduzir o nível de qualidade

`tests/dados_ibe/qualidade_prototipo.csv` (no Git) é a saída de `construir_banco_ibe.py` (diferenças E-OBS menos Iberia01 por concelho, 1971–2000). Para o regenerar:

```bash
python scripts/dados/validar_eobs.py                  # estações ECA&D e GHCN-D -> resultados/resultados_por_concelho.csv
python scripts/dados/construir_banco_ibe.py           # -> prototipo/ibe_prototipo.db, prototipo/ibe_correcao.db, resultados/qualidade_prototipo.csv
python scripts/dados/conferir_reconstrucao.py         # a série reconstruída bate com portugal_eobs.db?
```

A fórmula dos níveis é uma só, em `triton/core/qualidade_chuva.py`; o CSV guarda as diferenças, e o nível e o motivo calculam-se com essa fórmula em `acrescentar_qualidade_ao_banco.py`. Os bancos de protótipo (`prototipo/`, cerca de 95 MB) não vão para o Git.

## Os outros scripts

| Script | O que faz |
| :--- | :--- |
| `coletar_series_publicas.py` | recolhe séries públicas (INE, Eurostat, ERSAR, ERSE e outras) em JSON, com URL e data; as respostas ficam em `dados_automaticos/` (só `capitais_provincia_es.json` está no Git) |
| `comparar_fontes.py` | compara E-OBS, ERA5, ERA5-Land e CERRA com estações GHCN-D, 1991–2020 |
| `ilhas_e_tendencias.py`, `testar_cpc.py`, `global_era5_vs_ghcn.py` | verificações das ilhas, das tendências e do ERA5 |
| `iberia_eobs_vs_iberia01.py` | E-OBS contra Iberia01, célula a célula, em toda a Península |
| `construir_espanha_capitais.py` | ensaio de chuva e nível para as 52 capitais de província de Espanha (`resultados/qualidade_espanha_capitais.csv`); a Espanha não vai no pacote |
| `medir_tamanho.py` | mede o tamanho dos bancos candidatos |

## O que está em `resultados/`

Saídas de verificação, pequenas: `LICENCAS_DOS_DADOS.md`, `ESTRUTURA_DE_DADOS_IBE.md`, `relatorio_prototipo.md`, `qualidade_espanha_capitais.csv`, as comparações com estações (`comparacao_*.csv`, `resultados_por_concelho.csv`, `validacao_global_era5.csv`), `iberia_resumo.csv`, `iberia_tendencias.csv` e `concelhos.csv`.

`concelhos.csv` foi exportado de uma tabela intermédia (`concelhos.pkl`) cuja geração não está registada num script: serve só a `ilhas_e_tendencias.py` e a parte das tendências de `iberia_eobs_vs_iberia01.py`. Não afeta o banco nem o nível de qualidade.

## Limites desta reprodução

- Os scripts de recolha dependem de serviços de terceiros que mudam; o resultado de hoje pode diferir do de 22–23/10/2026.
- Não foi possível confirmar em linha a licença do Iberia01 (o repositório DIGITAL.CSIC bloqueou o pedido automático); ver `docs/DADOS.md`.
