# Revisão para o lançamento — Triton 1.0.0

Revisão de 21/09/2026 sobre o estado do repositório na véspera do lançamento
público. O objetivo é separar o que **bloqueia** o lançamento do que pode sair
depois, e deixar cada item com dono e com o esforço declarado.

A lista de pendências técnicas de longo prazo continua em
[`pendencias_e_evolucao.md`](pendencias_e_evolucao.md), com vinte itens. Este
documento não a repete: trata do que a revisão desta rodada encontrou e do que
precisa de decisão antes de publicar.

---

## 1. O que a revisão encontrou e já corrigiu

### Empacotamento: três módulos ficariam de fora do executável

O PyInstaller descobre dependências lendo os `import` do topo dos arquivos. Um
`import` escrito dentro de uma função é invisível para ele. O programa usa esse
recurso de propósito, para não carregar módulo pesado antes da hora — e o preço é
que cada módulo assim precisa ser **declarado** nas listas de empacotamento.

Faltavam cinco declarações. Duas são das funções novas desta rodada; três são
anteriores e teriam quebrado no executável, sem quebrar no código-fonte:

| Módulo | O que quebraria no instalador |
| :--- | :--- |
| `triton.core.excel_scenarios` | importar e gerar planilhas de cenários |
| `triton.ui.tab_economic_global_optimizer` | abrir a aba do otimizador econômico global |
| `triton.core.comprimento_de_serie` | a análise de comprimento de série |
| `triton.core.demanda_estocastica` | a demanda sorteada, na linha de comando |
| `triton.ui.dialogs.dialog_comprimento_de_serie` | a janela de resultado da análise |

Os cinco foram declarados em `Triton.spec` e em `build_exe.py`, e
`tests/unit/test_empacotamento.py` passa a recusar qualquer novo import interno
que não seja declarado nas duas listas — que agora também são obrigadas a dizer a
mesma coisa, porque duas listas divergentes produzem dois executáveis diferentes.

==Este era o único achado com potencial de estragar o lançamento: o programa roda
perfeitamente do código-fonte e quebraria na mão do usuário.==

### Versionamento sem estrutura

O histórico de versões era prosa livre. Agora cada versão segue um modelo fixo —
resumo em uma frase, novidades, correções que alteram resultados, correções que
não alteram, documentação — e desse modelo saem três coisas, sem redigitação: o
capítulo do manual, o `CHANGELOG.md` da raiz e a página de versões do site. A
seção 3 deste documento descreve o arranjo.

---

## 2. O que falta decidir antes de publicar

### 2.1 Lâmina de descarte — **decidido: 2 mm** ✔

`TritonConfig.discard` valia 1,0 mm, enquanto o campo da aba Projeto abria vazio
com a dica «Ex: 2,0», o exportador CAD, a linha de comando e o gerador de
relatório assumiam 2,0, e a ABNT NBR 15527:2019, item 4.1.5, recomenda 2 mm na
ausência de dado local. O mesmo projeto descartava o dobro conforme o caminho por
onde entrasse.

Resolvido antes do lançamento, que era a hora: depois dele, a mudança passaria a
quebrar reprodutibilidade de estudo publicado. A lâmina passa a morar em
`triton/core/hydrology_defaults.py`, ao lado do coeficiente de escoamento, que
já tinha tido o mesmo defeito; o campo da tela abre preenchido com 2,0, porque
vazio a prévia lia zero enquanto a simulação descontava a lâmina; e
`tests/unit/test_padroes_hidrologicos.py` recusa qualquer função que volte a
escrever o número à mão. A correção está registrada na seção «correções que
alteram resultados» da 1.0.0.

### 2.2 A linha de comando não acompanha o instalador

O `triton` de linha de comando é registrado pela instalação como pacote Python. O
instalador do Windows entrega só a janela. Quem receber o `.exe` não tem como
rodar `triton series-length`, `triton batch` ou `triton stochastic-demand`.

**Decisão sua**, entre três: aceitar e documentar (é o que o manual faz hoje);
empacotar um segundo executável de console no mesmo instalador; ou publicar o
pacote no PyPI, que resolve para quem já usa Python.

### 2.3 O instalador não leva a base climática de 652 cidades

São 6,4 GB, e o instalador tem 200 MB. Hoje a base é um download à parte, e o
manual explica onde pô-la. É a solução certa; fica registrado porque é a pergunta
que o primeiro usuário vai fazer.

### 2.4 Numeração desta rodada — **decidido: tudo é 1.0.0** ✔

A análise de comprimento de série, a demanda sorteada e a correção da lâmina
foram escritas depois de a 1.0.0 ser fechada e etiquetada, e antes de o
repositório ser publicado. Ficam todas na 1.0.0, que ainda não circulou: a
etiqueta `v1.0.0` foi remarcada no topo. A numeração por versão passa a valer
quando o professor disser — daí em diante, cada lançamento ganha entrada própria
e a etiqueta acompanha o commit que a fecha.

---

## 3. O versionamento, agora

### O modelo de uma entrada

```markdown
## Versão 5.1.0 — 30 de setembro de 2026

> **Em uma frase.** o resumo que aparece no panorama e no site

### Novidades
### Correções que alteram resultados
### Correções que não alteram resultados
### Documentação
```

Seções vazias simplesmente não aparecem. A entrada mais recente vem primeiro, e
um teste recusa ordem trocada, entrada sem data, entrada sem resumo e seção fora
do modelo.

### O que sai dela

| Destino | Como | O que mostra |
| :--- | :--- | :--- |
| Capítulo do manual | escrito à mão, é a fonte | o texto completo de cada versão |
| Panorama do capítulo | `_tabelas/cap38_versoes.md`, gerado | uma linha por versão: número, data, resumo e quantas correções alteram resultados |
| `CHANGELOG.md` | gerado por `manual/gerar_changelog.py` | o mesmo texto, para quem acompanha pelo código |
| Página de versões do site | `#/versoes`, gerada na montagem | um cartão por versão, com as seções recolhíveis e a contagem de correções |

O selo da versão na barra do site leva à página; o número na página inicial e no
rodapé também. Quem abre a documentação sabe, em um clique, de que versão ela
fala e o que mudou desde a anterior.

### Como lançar

O procedimento está em `manual/README.md`: escrever a entrada, trocar
`__version__`, regerar e rodar a suíte. Três verificações automáticas sustentam
o procedimento — o changelog fora de dia, a versão sem entrada e a data diferente
da do `CITATION.cff` fazem a suíte falhar.

---

## 4. Estado da verificação

- A suíte tem 81 arquivos de teste de unidade, mais integração, invariantes,
  interface e comparação com o Netuno 4.
- Os números publicados no manual têm verificação automática correspondente.
- A comparação com o Netuno 4 está documentada com a diferença de método do
  descarte isolada, e a replicação do estudo climático nacional confere com o
  motor do Triton dentro de 0,11 ponto percentual, como registra
  [`replicacao_dos_artigos.md`](replicacao_dos_artigos.md).

## 5. O que eu faria depois do lançamento, nesta ordem

1. **Varredura com passo variável e teto maior**, que é a diferença de prática
   entre o programa e os artigos do grupo (esforço baixo).
2. **Quebrar os cinco módulos de mais de 2.000 linhas** — `report_generator.py`,
   `dialog_economic.py`, `cli.py`, `translation.py` e `tab_documentation.py` —,
   que é onde a manutenção dói primeiro.
3. **Fechar as pendências de dado externo** da lista de pendências: os quatro
   municípios sem tarifa de excedente e os cinco com tarifa decrescente.
4. **Indicadores de período seco** ligados ao desempenho, que os artigos do grupo
   apontam como os mais explicativos.
