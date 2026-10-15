# Scripts

Ferramentas de linha de comando que acompanham o programa. Nenhuma é importada
por `triton/`: rodam por fora, sobre o projeto. Rode-as a partir desta pasta
(`triton_brl/`). Esta é a pasta da **Edição Brasil**: as outras duas edições levam só
os scripts neutros (`qa_runner.py`, `bench_kernels.py`, `gerar_avisos_de_terceiros.py`)
e os da própria região.

## Base climática CLIMBra

A base compilada é um banco SQLite **por modelo CMIP6**, `data/climbra_<modelo>.db`
(19 arquivos), mais o manifesto `data/climbra_partes.json`. Os bancos estão no Git.

| Script | O que faz |
| :--- | :--- |
| `compilar_base_climbra.py` | CSV do CLIMBra (`climbra_data/`, ~6,5 GB, fora do Git) -> as 19 partes. `--formato unico` gera o `climbra.db` antigo; `--modelo X` compila só um modelo; `--verify-only` confere. |
| `dividir_base_climbra.py` | `data/climbra.db` (banco único, ~820 MB, fora do Git) -> as 19 partes, com verificação byte a byte contra o original. `--verificar` confere as partes que estão em `data/` (hash do arquivo, hash do conteúdo, contagens, limite de tamanho); com o `climbra.db` ao lado, compara cada série com a dele. |

```bash
python scripts/dividir_base_climbra.py                 # climbra.db -> climbra_<modelo>.db (cerca de 10 s)
python scripts/dividir_base_climbra.py --verificar     # confere as partes de data/ (e as compara com o climbra.db, se existir)
python scripts/compilar_base_climbra.py --input climbra_data   # direto dos CSV
```

**Formato de cada parte.** Mesmo esquema do banco único: `climbra_meta` (chave/valor),
`climbra_cities` (as 652 cidades, em todas as partes) com o índice `idx_climbra_cities_norm`, e
`climbra_series (city, model, scenario, count, data)` com chave primária `(city, model, scenario)`.
Cada série é um blob zlib de float16, igual ao do banco único: a série lida de uma parte é
idêntica, valor a valor, à do `climbra.db` (o teste `tests/unit/test_climbra_particionada.py`
confere). A `climbra_meta` de uma parte acrescenta `model`, `scenarios`, `periods` (início, dias e
fim por cenário), `total_series`, `total_cities`, `schema_version` (`2`; o banco único é o 1),
`layout`, `content_sha256` e `created_at`.

**Tamanho.** Medido sobre o `climbra.db` de 22/09/2026: 37.164 séries = 19 modelos x 652 cidades x 3
cenários (1.956 séries por modelo; 12.418 ou 12.419 dias no histórico, 31.410 ou 31.411 nos futuros).
Cada modelo ocupa de 39,98 MB (IPSL-CM6A-LR) a 43,02 MB (KACE), a soma é 785,1 MB, abaixo dos 821,8 MB do
banco único. Os cerca de 37 MB a menos vêm, provavelmente, do espaço ocioso nas páginas do banco único
(inseridas fora da ordem da chave, sem `VACUUM`); cada parte é gravada em ordem e passa por `VACUUM`. As 19
tabelas de cidades repetidas custam menos de 0,5 MB no total. Limites do GitHub: aviso a partir de 50 MB, recusa acima de 100 MB por arquivo; a maior
parte tem 43 MB. Compressão alternativa testada em 300 séries do INM-CM4: nível 9 do zlib ganha 0,9%;
reordenar os bytes do float16 antes do zlib **piora** 4% a 6%; LZMA ganha 5,6% e custa leitura mais lenta e
outro formato. Nenhuma justifica mudar o blob; a divisão por modelo já basta.

**Se uma parte passar do limite.** `dividir_base_climbra.py` divide sozinho o modelo por cenário
(`climbra_<modelo>__HIST.db`, `__SSP245.db`, `__SSP585.db`) quando passa de `--limite-mb` (padrão 95);
`--por-cenario` força. O leitor (`triton/core/climate_database.py`) entende os dois nomes. Com
`--dtype float32` as partes ficam bem maiores e essa divisão passa a valer.

**Peso no repositório.** As 19 partes somam ~785 MB. Cada vez que uma parte é regerada, o Git guarda outra
cópia dela (o blob já é comprimido, o Git não reduz). Por isso: gere uma vez, versione, e só regere um modelo
se o dado mudar. Alternativa, se o limite do repositório pesar: Git LFS para `data/climbra_*.db` (uma
linha em `.gitattributes`: `data/climbra_*.db filter=lfs diff=lfs merge=lfs -text`) ou publicar as partes
como arquivos da release/Zenodo e deixar de versioná-las (`.gitignore`).

**Onde o programa as procura.** `triton/core/climate_database.py` varre, nesta ordem: a variável
`TRITON_CLIMBRA_DIR` (pasta), `TRITON_CLIMBRA_DB`/`TRITON_CLIMATE_DB` (arquivo ou pasta), a pasta `data/` do
executável instalado (`_internal/data/`), do código e do diretório atual. Vale a primeira pasta que tiver
bancos. Se existirem partes e o `climbra.db` antigo, vale a parte do modelo e o antigo cobre o que faltar.

## Tarifas e custos (Brasil)

| Script | O que faz |
| :--- | :--- |
| `update_all_tariffs.py` | atualização das 652 estruturas a partir das fontes (usa a rede) |
| `audit_tariffs.py` | auditoria da base tarifária |
| `reconciliar_tarifas.py` | conciliação entre a coleta e a evidência primária |
| `completar_tarifas_faltantes.py` | preenche municípios sem estrutura |
| `aplicar_categorias_casan.py`, `aplicar_categorias_corsan.py`, `aplicar_tarifa_exponencial.py` | gravam categorias e fórmulas de prestadores específicos |
| `compilar_base_tarifas_fontes.py` | reúne os documentos de terceiros das tarifas num banco local (`tarifas/tarifas_fontes.db`, fora do Git) |
| `generate_uf_tariffs_breakdown.py`, `plot_tariff_tiers_summary.py` | figuras e quadros da estrutura tarifária |
| `verificar_custos_calibrados.py` | imprime o CAPEX e o OPEX calibrados por tipologia e UF, para conferência visual (sem asserções) |

## Verificação e estudos

| Script | O que faz |
| :--- | :--- |
| `qa_runner.py` | executa as camadas de verificação; `--layer replicacao` roda a comparação completa contra o Netuno 4 |
| `run_batch_validation.py`, `run_mass_simulations.py` | validação em lote e simulações em massa (saídas em `data/simulation_outputs/`) |
| `comparar_exportacao_netuno4.py` | confronta uma exportação com a do Netuno 4 |
| `generate_reference_case_studies.py` | casos de referência (Florianópolis, Brasília, Manaus) |
| `gerar_relatorios_exemplo.py` | regera os laudos de `reports/exemplos/` pela própria interface |
| `bench_kernels.py` | desempenho do kernel Python contra o compilado |
| `replicacao/` | cenários climáticos e comprimento de série usados na replicação dos artigos do grupo |

## Build

| Script | O que faz |
| :--- | :--- |
| `gerar_avisos_de_terceiros.py` | gera `infos_licenses/AVISOS_DE_TERCEIROS.txt` da edição (a CLIMBra só na Brasil); o `build_exe.py` o roda antes de empacotar |

## Legado

`split_climates.py` e `split_climates_vaz.py` recortavam as séries do CLIMBra em horizontes fixos
(futuro próximo e distante) para estudos antigos. O programa não usa mais janelas fixas (o usuário
recorta o período que quiser), e a base compilada traz as séries inteiras. Ficam só como registro;
se não houver estudo antigo a repetir, podem sair.

## Estudos e artigos

Os scripts que produzem os dados e as figuras dos artigos não ficam aqui. Estão na
pasta `Estudos/`, ao lado deste repositório, junto dos dados de cada estudo.
