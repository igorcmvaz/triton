# Triton, Edição Brasil (BRL): notas de lançamento da versão 0.2.0

Versão 0.2.0 (beta), lançada em 11 de novembro de 2026. Muda o multicritério: sete critérios em três eixos dão lugar a oito critérios em quatro eixos, o resultado passa a ser uma faixa de volumes de escore semelhante, e não um volume só, e os pesos podem vir do método CRITIC, calculados dos próprios resultados. Este documento diz o que mudou, o que isso faz aos resultados, como reproduzir um estudo da 0.1.0 e como citar. O que a 0.1.0 trouxe, o que não há e as limitações conhecidas que continuam valendo estão nas [notas da 0.1.0](NOTAS_DE_LANCAMENTO_0.1.0.md); o histórico completo, em [`../CHANGELOG.md`](../CHANGELOG.md); o manual, em [`../manual/Manual-Triton.pdf`](../manual/Manual-Triton.pdf).

## O que mudou

**Oito critérios em quatro eixos.** No modelo anterior, três critérios — potencial de economia, extravasamento e consumo de água potável — mediam a mesma água economizada e empurravam a escolha para tanques grandes. O modelo novo reduz essa colinearidade e leva o peso do sistema à decisão.

| Eixo | Critério | Direção | Definição no programa |
| :--- | :--- | :--- | :--- |
| técnico | confiabilidade volumétrica | maximizar | água de chuva consumida ÷ demanda de água de chuva (uso não potável mais irrigação), em % |
| técnico | eficiência de armazenamento | maximizar | água de chuva entregue por dia ÷ volume da cisterna inferior, em % (o giro anual ÷ 365); cai com o volume e freia o superdimensionamento |
| econômico | economia financeira líquida | maximizar | o VPL do sistema contra a linha de base sem cisterna |
| econômico | custo nivelado da água (LCOW) | minimizar | investimento mais custeio anual descontado (energia, operação e manutenção, cloro, linha de tratamento) ÷ água de chuva entregue descontada, à mesma taxa e no mesmo horizonte; em R$/m³ |
| econômico | payback descontado | minimizar | como na 0.1.0; quem não se paga recebe o pior payback observado mais 10% (ao menos um ano a mais e ao menos 20 anos) |
| ambiental | CO₂e de ciclo de vida | minimizar | o CO₂e líquido no fim da vida útil (negativo é carbono evitado), como na 0.1.0 |
| estrutural | massa a seco do sistema | minimizar | da calculadora de peso: cisternas, tubos, motobomba e acessórios |
| estrutural | extravasamento anual | minimizar | volume extravasado por ano, em m³ |

**Pesos.** Quatro pesos de eixo, 25% cada por padrão, repartidos dentro de cada eixo pelas *partes no eixo* (padrão: partes iguais), ou oito pesos diretos, um por critério. TOPSIS, VIKOR e PROMETHEE II usam a mesma regra; o SMAA-VIKOR sorteia oito pesos, com 25% esperado em cada eixo (parâmetros de Dirichlet 1, 1, 2/3, 2/3, 2/3, 2, 1, 1), e informa os pesos centrais agregados nos quatro eixos.

| Onde | Pesos de eixo | Partes no eixo |
| :--- | :--- | :--- |
| aba de decisão | um cartão por eixo (Técnico, Econômico, Ambiental, Estrutural), com o peso em cima, 25% cada; perfis «Equilibrado» e «Priorizar …» (70% no eixo, 10% em cada outro), inclusive «🏗️ Priorizar Leveza e Drenagem», e «📊 Pesos objetivos (CRITIC), calculados dos resultados» | em cada cartão, as partes dos critérios do eixo; embaixo, os botões «Partes iguais» e «⚡ Recalcular» |
| linha de comando | `--weights t,e,a,s`, oito valores ou `critic` | `--criterion-shares`, oito valores (padrão 1,1,1,1,1,1,1,1) |
| arquivo de projeto | `analysis.topsis_weights`, com quatro ou oito valores, ou `"critic"` | `analysis.topsis_criterion_shares`, com oito valores |
| estudo declarativo | `analise.pesos`, com quatro ou oito valores, ou `"critic"` | `analise.partes_no_eixo`, com oito valores |

**Pesos objetivos pelo CRITIC.** Em vez de declarar pesos, pode-se pedir os do método CRITIC (Diakoulaki, D.; Mavrotas, G.; Papayannakis, L., 1995. Determining objective weights in multiple criteria problems: the CRITIC method. *Computers & Operations Research*, 22(7), 763–770. doi:10.1016/0305-0548(94)00059-H). Cada critério é normalizado de 0 (pior valor observado) a 1 (melhor); a informação do critério é o desvio-padrão vezes a soma de (1 − correlação) com os demais, e o peso é a sua parte na informação total. Os pesos saem dos volumes maiores que zero, são recalculados a cada análise e valem para TOPSIS, VIKOR e PROMETHEE II; o SMAA continua sorteando pesos, e na sensibilidade de pesos (`--weight-sensitivity`) sorteiam-se os quatro pesos de eixo. O CRITIC mede contraste e independência dos critérios nos próprios resultados, e não importância: os pesos mudam com o conjunto de volumes avaliado, não expressam a preferência de ninguém, e um critério que varia entre os volumes ganha peso mesmo que importe pouco. É uma escolha de método; o padrão continua 25% por eixo.

**Faixa de escolha.** Quando vários volumes pontuam parecido, o programa não diz «o melhor volume»: relata os volumes cujo escore, normalizado entre o pior (0) e o melhor (1) dos volumes avaliados, fica a até 5% da amplitude do maior, e informa o de maior escore ao lado. Vale para TOPSIS (escore), VIKOR (índice Q), PROMETHEE II (fluxo líquido) e SMAA (aceitabilidade de 1º lugar). A tolerância muda com `--score-band` (de 0 a 1), `analysis.topsis_score_band` ou `analise.tolerancia_faixa`; o JSON traz `topsis.choice_band` e `smaa_vikor.choice_band`, e o estudo declarativo, as métricas `faixa_topsis_min_l` e `faixa_topsis_max_l`. A faixa depende da grade de volumes e da tolerância: declare as duas.

**Peso do sistema.** `triton analyze` com `--analysis system_weight` (ou `all`) informa a massa a seco, a carga de água e a carga em operação, em kg e kN, separadas em subsolo ou nível inferior, cobertura ou nível superior, e prumadas e rede. O texto do terminal, o HTML e o XLSX mostram o bloco; no XLSX, a aba `system_weight` traz o resumo do volume escolhido, e os valores por volume ficam na aba `alternatives`. Quatro alertas pedem confirmação com o projeto estrutural ou de fundações: mais de 500 kg na cobertura com o reservatório cheio, reservatório superior acima de 1.500 L, cisterna acima de 3.000 kg a seco e cisterna de concreto. São limiares de atenção do programa, e não de norma.

## O que isso faz aos resultados

O escore e o volume escolhido do TOPSIS, do VIKOR, do PROMETHEE II e do SMAA-VIKOR mudam. No tutorial do manual (residência em Florianópolis, cisterna de polietileno, sete volumes candidatos), com pesos iguais, o TOPSIS indicava 4.000 L; agora a faixa de escolha vai de 2.000 a 3.000 L, com o maior escore em 2.000 L, e 4.000 L ficam em terceiro. Com 70% num eixo e 10% em cada outro, a faixa é 1.000 L no técnico, de 2.000 a 4.000 L no econômico, de 1.000 a 3.000 L no ambiental e de 3.000 a 4.000 L no estrutural (maior escore em 4.000 L). Os pesos do CRITIC dão 34,4% ao eixo técnico, 26,6% ao econômico, 10,0% ao ambiental e 29,0% ao estrutural, e a faixa de 3.000 a 4.000 L. O SMAA-VIKOR, com 25% esperado por eixo, dá a 2.000 L 44% dos primeiros lugares, a 3.000 L 25% e a 4.000 L 18%. O eixo técnico equilibra a confiabilidade, que sobe com o volume, e a eficiência de armazenamento, que cai; por isso o peso técnico dominante leva ao menor volume, enquanto o critério hidráulico do manual (limiar de ganho marginal de 1 %/m³) continua indicando 4.000 L. O manual, na seção «Qual volume escolher, afinal», mostra o que os 4.000 L cedem e quando o volume menor é a escolha defensável.

A simulação, a análise econômica e a avaliação ambiental não mudam: só a ordenação multicritério.

## Projetos e estudos da 0.1.0

- **Três pesos** (técnico, econômico, ambiental) continuam aceitos, na interface, na linha de comando, no arquivo de projeto e no estudo declarativo: o eixo estrutural recebe a média dos três, e pesos iguais continuam iguais. O resultado muda mesmo assim, porque os critérios mudaram.
- **Sete valores**, de pesos ou de partes do modelo anterior, são recusados com a mensagem: «O multicritério da versão 0.2.0 tem oito critérios em quatro eixos, e os sete valores do modelo anterior não correspondem a eles. Informe quatro pesos de eixo (técnico, econômico, ambiental, estrutural) ou oito pesos de critério.»
- **Para reproduzir um estudo feito na 0.1.0, use a 0.1.0**, pelo DOI daquela versão, 10.5281/zenodo.23402916.

## Instalar

| | |
| :--- | :--- |
| Instalador para Windows | No registro do Zenodo. O DOI 10.5281/zenodo.23402915 reúne todas as versões e aponta sempre para a mais recente; a 0.1.0 continua no DOI 10.5281/zenodo.23402916. Não precisa de Python. |
| A partir do código | Python 3.12 ou superior; `pip install -r requirements.txt`; `python main.py` (interface) ou `python -m triton.cli --help` (linha de comando) |

## Limitações conhecidas

- A massa a seco vem de pesos de referência dos componentes, e não substitui o cálculo estrutural; os alertas de carga são limiares de atenção do programa.
- No multicritério da interface e da linha de comando, a massa sai da configuração do projeto; nas tabelas do manual, da configuração padrão da calculadora. A diferença é uma parcela que não muda com o volume, e a ordem do TOPSIS é a mesma.
- As limitações da 0.1.0 continuam valendo ([notas da 0.1.0](NOTAS_DE_LANCAMENTO_0.1.0.md)).

## Relatar um problema

Descreva a versão (0.2.0), a edição, os passos e anexe o arquivo `.triton`. Contato: igorcmvaz@gmail.com. O manual, na seção «Relatar um problema», diz o que anexar.

## Como citar

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações* (versão 0.2.0). Universidade Federal de Santa Catarina (UFSC). https://doi.org/10.5281/zenodo.23402915

O DOI 10.5281/zenodo.23402915 reúne todas as versões e aponta para a mais recente; declare no texto a versão usada. Um estudo feito na 0.1.0 cita a 0.1.0, pelo DOI 10.5281/zenodo.23402916. Para a base climática, cite também Ballarin et al. (2023), *Scientific Data* 10, 47, doi:10.1038/s41597-023-01956-z.
