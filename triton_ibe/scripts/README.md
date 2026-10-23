# Scripts

> **Ferramentas de desenvolvimento.** Os scripts descritos abaixo ficam no disco do responsável pela manutenção e **não estão no Git** (`.gitignore`). Este ficheiro regista o que cada um faz; o programa, o instalador e os testes não dependem deles.

Ferramentas de linha de comandos que acompanham o código. Nenhuma é importada por `triton/`: correm
por fora, sobre o projeto. Corra-as a partir desta pasta (`triton_ibe/`).

## Dados de Portugal

| Script | O que faz |
| :--- | :--- |
| `compilar_base_eobs_portugal.py` | precipitação diária E-OBS por concelho (fontes brutas E-OBS e CAOP, ~3 GB, fora do Git) -> `data/portugal_eobs.db`, que o instalador leva; `--so-completude` confere o critério na base pronta |
| `acrescentar_qualidade_ao_banco.py` | acrescenta a `data/portugal_eobs.db` a tabela `qualidade` (nível A/B/C e motivo por concelho, da fórmula de `triton/core/qualidade_chuva.py`) e as chaves `pacote_id`, `versao_eobs`, `sha256_pacote`, `qualidade_versao`, `limiares`, `espanha_locais` de `metadados`; entrada: `tests/dados_ibe/qualidade_prototipo.csv`; a série repetida vem do SHA-256 das séries do banco (`--prototipo` confere com as células) |
| `compilar_base_tarifas_fontes.py` | reúne os documentos de terceiros dos tarifários num banco local (`tarifas_portugal/tarifas_portugal_fontes.db`, fora do Git) |
| `gerar_exemplo_portugal.py` | gera os projetos de exemplo (Lisboa, Porto, Funchal). Depende de `gerar_tabelas.py`, do manual-fonte, que fica no disco do mantenedor e fora do Git |

## Verificação e construção

| Script | O que faz |
| :--- | :--- |
| `qa_runner.py` | executa as camadas de verificação (suíte completa e portões; ver `--help`) |
| `bench_kernels.py` | compara o núcleo de referência em Python com o compilado |
| `gerar_avisos_de_terceiros.py` | gera `infos_licenses/AVISOS_DE_TERCEIROS.txt` desta edição (com a atribuição E-OBS e CAOP); o `build_exe.py` corre-o antes de empacotar |
