# 19. Rodar em lote

> **Pergunta que este guia responde:** como rodar cem simulações sem clicar cem
> vezes?

Pela linha de comando. É o mesmo núcleo de cálculo da interface, sem tela.

---

## 19.1. O comando básico

```bash
python -m netuno.cli run projeto.netuno
```

Roda a análise técnica e imprime o resultado. As opções que mais importam:

| Opção | Para quê |
| :--- | :--- |
| `--analysis` | `technical`, `economic`, `environmental`, `topsis` ou `all` |
| `--volume` | força um volume, ignorando o do projeto |
| `--rainfall` | troca a série de chuva do projeto |
| `--set CAMPO=VALOR` | sobrescreve qualquer campo; repetível |
| `--format` | `text`, `json`, `csv`, `html` ou `xlsx` |
| `--output` | arquivo de saída, obrigatório fora do modo texto |
| `--seed` | semente, para análises estocásticas reproduzíveis |

Exemplo de uma varredura de cidades, mantendo o projeto:

```bash
for cidade in Florianopolis1 Brasilia1 Manaus1 SaoPaulo1; do
  python -m netuno.cli run projeto.netuno \
    --rainfall "data/rainfall/${cidade}.csv" \
    --analysis all --format json --output "saida/${cidade}.json"
done
```

---

## 19.2. Os subcomandos

| Subcomando | O que faz |
| :--- | :--- |
| `run` | simula um projeto |
| `analyze` | executa a cadeia completa de análises |
| `validate` | confere a estrutura e as premissas de um projeto |
| `init` | cria um modelo `.netuno` editável |
| `matrix` | combina premissas de edificação com catálogo climático |
| `matrix-projects` | executa vários `.netuno` de uma lista ou pasta |
| `batch` | executa cenários declarados numa planilha CSV ou XLSX |
| `uncertainty` | propaga incertezas por Monte Carlo |

`validate` merece atenção: rode-o antes de qualquer lote. Ele confere a estrutura do
projeto e as premissas, e evita descobrir um erro de cadastro depois de duzentas
simulações.

---

## 19.3. Matriz fatorial

Quando você quer o produto cartesiano de várias premissas — três cidades, quatro
volumes, duas tipologias — use `matrix`:

```bash
python -m netuno.cli matrix --help
```

Ele combina o catálogo de premissas de edificação com o catálogo climático e gera
todas as combinações. É a forma de produzir a base de um artigo.

---

## 19.4. Planilha de cenários

O subcomando `batch` lê uma planilha em que **cada linha é um cenário** e cada
coluna um parâmetro. É o caminho mais simples quando os cenários não formam um
produto cartesiano limpo.

```bash
python -m netuno.cli batch cenarios.csv --output resultados.xlsx
```

Um exemplo de planilha acompanha o programa, em `examples/`.

---

## 19.5. O que a linha de comando não faz

**Cinquenta e cinco dos 103 parâmetros** do projeto são alcançáveis pela linha de
comando. Os outros só existem na interface.

Isso não é limitação de propósito: os parâmetros ausentes são os de detalhamento
fino — materiais de reservatório, comprimentos por diâmetro de tubo, perfis de
modulação diária. Para um estudo em lote, o caminho é montar o `.netuno` **na
interface**, com todo o detalhe, e depois variar pela linha de comando só o que
muda entre os cenários.

O apêndice F traz a referência completa das opções.

---

## 19.6. Reprodutibilidade

Três conselhos que evitam retrabalho:

**Guarde o comando.** Num arquivo de script versionado junto com os resultados, e
não no histórico do terminal.

**Fixe a semente.** Qualquer análise com sorteio — sensibilidade de pesos, Monte
Carlo — precisa de `--seed` para ser reproduzível.

**Grave a saída em JSON.** É o formato que preserva todos os campos. CSV e XLSX são
para leitura humana; JSON é para reprocessar.
