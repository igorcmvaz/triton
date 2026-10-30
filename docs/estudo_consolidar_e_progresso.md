# `estudo consolidar` e `--progresso`

Dois recursos opcionais da linha de comando `triton estudo`. Nenhum pacote novo entra no instalador, em `requirements.txt`,
em `Triton.spec` ou em `build_exe.py`; os pacotes extras só são usados se estiverem instalados.

## Consolidar vários estudos

```
triton estudo consolidar PASTA [PASTA ...] --saida SAIDA [--idioma auto|pt-BR|pt-PT|en|es|zh] [--motor auto|duckdb|csv]
```

Procura todo `resultados.csv` sob as pastas (saídas de `estudo run` e de `estudo lote`) e grava em `SAIDA`:

- `consolidado.csv`: uma linha por **tipologia** (coluna `grupo`), **caso** (`caso_id`), **métrica** e **unidade**, com as colunas
  `tipologia, caso_id, caso, metrica, rotulo, unidade, estudos, registros, n, minimo, media, mediana, maximo`.
  `n` conta só os casos concluídos (`status` ok) com valor; `registros` conta todas as linhas do grupo. A unidade faz parte da chave:
  moedas ou idiomas diferentes nunca se misturam.
- `consolidado.md`: a mesma tabela em Markdown, com os números no formato do idioma e as casas decimais padrão de cada métrica.

Os números do CSV têm a formatação de `estudo run` (ponto decimal, dez algarismos significativos). A ordem das linhas é estável
(tipologia, caso, métrica, unidade), e os arquivos não levam data nem caminho da máquina: duas execuções dão bytes iguais.

### duckdb opcional, com alternativa

| Caminho | Quando | Como |
| :-- | :-- | :-- |
| `duckdb` | extra `analise` instalado (`pip install -e "triton_int[analise]"`) e `--motor auto` ou `duckdb` | lê todos os arquivos de uma vez e agrupa por SQL |
| `csv` | sem o pacote, ou `--motor csv` | biblioteca padrão |

Os dois caminhos só leem e agrupam; as estatísticas saem do mesmo código (`triton.core.estudo.estatisticas`), então o resultado é
o mesmo byte a byte (há um teste que compara os dois quando o duckdb existe). `--motor duckdb` sem o pacote falha com a mensagem do
extra `analise`; `--motor auto` cai em `csv` sem aviso.

## Progresso em `estudo run` e `estudo lote`

`--progresso {auto,rich,simples}` (padrão `auto`) escolhe como o progresso aparece, sempre na **saída de erro**:

| Modo | Efeito |
| :-- | :-- |
| `simples` | uma linha por caso, `[i/N] id: ok (t s)` (o comportamento de sempre) |
| `rich` | barra de progresso do pacote `rich` (extra `cli`); sem o pacote cai em `simples` com um aviso, uma vez |
| `auto` | `rich` se estiver instalado e a saída de erro for um terminal; senão `simples` |

`--quiet` desliga o progresso. Os arquivos de resultado e a saída padrão são idênticos em bytes em qualquer modo (teste em
`tests/unit/test_progresso.py`). Em executável de janela (sem saída de erro), o modo cai em `simples`.
