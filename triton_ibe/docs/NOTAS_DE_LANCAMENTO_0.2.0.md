# Triton IBE, Edição Ibérica: notas de lançamento da versão 0.2.0

Versão 0.2.0 (beta), lançada a 11 de novembro de 2026. Este documento diz o que mudou em relação à 0.1.0, o que isso faz aos resultados e como citar. O que a 0.1.0 trouxe, o que não traz e as limitações conhecidas continuam nas [notas da 0.1.0](NOTAS_DE_LANCAMENTO_0.1.0.md); o histórico completo está em [`../CHANGELOG.md`](../CHANGELOG.md); o manual, em [`../manual/Manual-Triton.pdf`](../manual/Manual-Triton.pdf).

**Em resumo: o multicritério passa a ter oito critérios em quatro eixos, relata uma faixa de volumes semelhantes em vez de um volume só e aceita pesos objetivos pelo CRITIC; o programa passa a calcular o peso do sistema.** Antes, eram sete critérios em três eixos, e três deles mediam a mesma água economizada. A ordenação muda, e com ela pode mudar o volume escolhido: no tutorial de Lisboa, com pesos iguais, a maior pontuação do TOPSIS passa de 5 000 L para 3 000 L, numa faixa de escolha de 2 000 a 3 000 L. Para reproduzir um estudo feito com a 0.1.0, use a 0.1.0.

## O que mudou

### Oito critérios em quatro eixos

| Eixo | Critério | Sentido | Definição no programa |
| :--- | :--- | :--- | :--- |
| Técnico | Fiabilidade volumétrica | maximizar | água de chuva consumida ÷ procura de água de chuva (usos não potáveis e rega), em % |
| Técnico | Eficiência de armazenamento | maximizar | água de chuva entregue por dia ÷ volume da cisterna inferior, em % (o giro anual ÷ 365); cai com o volume e trava o sobredimensionamento; não é a ocupação média, que sobe com o volume em clima húmido |
| Económico | Economia financeira líquida | maximizar | o VAL do sistema contra a linha de base sem cisterna (fatura evitada menos investimento e custos de exploração, atualizados) |
| Económico | Custo nivelado da água (LCOW) | minimizar | (investimento + Σ custos de exploração atualizados: energia, manutenção, cloro, linha de tratamento) ÷ Σ água de chuva entregue atualizada, à mesma taxa e no mesmo horizonte do projeto, em €/m³; curva em U; a alternativa sem cisterna recebe o pior LCOW observado + 10% |
| Económico | Período de recuperação descontado | minimizar | como na 0.1.0; quem não se recupera recebe o pior observado + 10% (ao menos mais um ano e ao menos 20 anos) |
| Ambiental | CO₂e de ciclo de vida | minimizar | o CO₂e líquido no fim da vida útil (negativo = evitado), como na 0.1.0 |
| Estrutural | Massa a seco dos materiais | minimizar | massa a seco do sistema (cisternas, tubagem, eletrobomba, acessórios), da calculadora de peso |
| Estrutural | Extravasamento anual | minimizar | volume extravasado por ano, em m³ |

### Pesos

- **Quatro pesos de eixo**, 25% cada por omissão, repartidos dentro de cada eixo pelas **partes no eixo** (por omissão, partes iguais); ou **oito pesos de critério**, um por critério.
- **Três pesos** (projetos e estudos feitos até à 0.1.0) continuam aceites: o eixo estrutural recebe a média dos três, de modo que pesos iguais continuam iguais.
- **Sete valores**, pesos ou partes do modelo anterior, são recusados com a mensagem «O multicritério da versão 0.2.0 tem oito critérios em quatro eixos, e os sete valores do modelo anterior não correspondem a eles. Informe quatro pesos de eixo (técnico, econômico, ambiental, estrutural) ou oito pesos de critério.»
- O TOPSIS, o VIKOR e o PROMETHEE II usam a mesma regra de pesos; o SMAA-VIKOR sorteia oito pesos numa distribuição de Dirichlet com parâmetros (1, 1, 2/3, 2/3, 2/3, 2, 1, 1), com 25% esperado em cada eixo, e informa os pesos centrais agregados nos quatro eixos.

| Onde | Pesos | Partes no eixo |
| :--- | :--- | :--- |
| separador de decisão | quatro cartões, um por eixo (Técnico, Económico, Ambiental, Estrutural; 25% cada), com o peso do eixo em cima; perfis «Equilibrado: 25% em cada eixo», «Priorizar …» (70% num eixo e 10% em cada um dos outros), incluindo «🏗️ Priorizar Leveza e Drenagem», e «📊 Pesos objetivos (CRITIC), calculados dos resultados» | em cada cartão, as partes dos critérios do eixo (Confiabilidade, Eficiência, Economia, LCOW, Payback, CO₂, Massa, Extravasamento); sob os cartões, os botões «Partes iguais» e «⚡ Recalcular» |
| linha de comandos | `--weights t,e,a,s` (ou oito valores, ou `critic`; três ainda aceites) | `--criterion-shares` com oito valores (por omissão, `1,1,1,1,1,1,1,1`) |
| ficheiro de projeto | `analysis.topsis_weights` (quatro ou oito valores, ou `"critic"`) | `analysis.topsis_criterion_shares` (oito) |
| estudo declarativo | `analise.pesos` (quatro ou oito, ou `"critic"`; três aceites) | `analise.partes_no_eixo` (oito) |

### Pesos objetivos pelo CRITIC

Quem não tem consenso sobre os pesos e não quer impor uma preferência pode pedi-los aos resultados. O CRITIC (Diakoulaki, D.; Mavrotas, G.; Papayannakis, L., 1995. Determining objective weights in multiple criteria problems: The CRITIC method. *Computers & Operations Research*, 22(7), 763–770. doi:10.1016/0305-0548(94)00059-H) normaliza cada critério de 0 (pior valor observado) a 1 (melhor) e dá a cada um a informação Cⱼ = σⱼ · Σₖ (1 − rⱼₖ), com σⱼ o desvio-padrão do critério normalizado e rⱼₖ a correlação de Pearson entre critérios; o peso é wⱼ = Cⱼ / Σ C.

- Um critério constante não informa e pesa zero; sem contraste nenhum, os pesos ficam iguais.
- Os pesos saem das alternativas com volume maior que zero (a alternativa sem cisterna entra no TOPSIS com as penalizações do LCOW e do período de recuperação, que inflariam o contraste) e recalculam-se a cada análise.
- Valem para o TOPSIS, o VIKOR e o PROMETHEE II; as partes no eixo não se aplicam; o SMAA continua a sortear os pesos. Na sensibilidade de pesos (`--weight-sensitivity`), com `critic`, sorteiam-se os quatro pesos de eixo.
- **Limites:** os pesos mudam com o conjunto de volumes avaliado, não exprimem a preferência de ninguém, e um critério que varia muito entre os volumes ganha peso mesmo que importe pouco. É uma escolha de método, e não o padrão (25% por eixo). Um estudo que o use di-lo e informa os pesos calculados.

No tutorial de Lisboa, o CRITIC dá 33,8% ao eixo técnico, 23,0% ao económico, 11,5% ao ambiental e 31,7% ao estrutural, e a faixa do TOPSIS passa a 4 000 a 5 000 L.

### Faixa de escolha

Quando vários volumes pontuam quase igual, o multicritério deixa de dizer que um deles é «o melhor»: relata a **faixa de escolha**, os volumes cuja medida, normalizada entre a pior (0) e a melhor (1) dos volumes avaliados, fica a até 5% da amplitude da melhor, e o volume de maior pontuação como informação. A regra vale para o TOPSIS (pontuação), o VIKOR (índice Q, menor é melhor), o PROMETHEE II (fluxo líquido) e o SMAA (aceitabilidade de primeiro lugar). A faixa depende da tolerância e da grade de volumes avaliada: declare as duas.

| Onde | O que mostra ou aceita |
| :--- | :--- |
| separador de decisão | «Faixa TOPSIS», «Faixa VIKOR / SMAA» e «Faixa PROMETHEE II», cada uma com o volume de maior pontuação |
| linha de comandos | `--score-band` (0 a 1; por omissão, 0,05) em todos os comandos que aceitam `--weights`; o texto escreve «TOPSIS: volumes de A a B L com pontuações semelhantes (até 5% da amplitude, a partir da maior) \| maior pontuação em X L» |
| HTML e JSON | o parágrafo «Faixa de escolha (TOPSIS)»; as chaves `topsis.choice_band`, `choice_band_min_volume_l`, `choice_band_max_volume_l` e `smaa_vikor.choice_band` |
| ficheiro de projeto | `analysis.topsis_score_band` |
| estudo declarativo | `analise.tolerancia_faixa`; as métricas `faixa_topsis_min_l` e `faixa_topsis_max_l` |

### Peso do sistema

`triton analyze … --analysis all` (e `--analysis system_weight`) traz o bloco `system_weight`: a massa a seco, a carga de água e a carga em operação, em kg e kN, separadas em subsolo ou nível inferior, cobertura ou nível superior, e prumadas e rede. O relatório HTML, o XLSX (folha `system_weight` com o resumo do volume escolhido; os valores por volume ficam na folha `alternatives`) e o texto do terminal mostram o bloco.

Os alertas usam limiares de atenção do **programa**, que não vêm de nenhuma norma: 500 kg sobre a cobertura com o reservatório cheio, reservatório superior acima de 1 500 L, cisterna acima de 3 000 kg a seco e qualquer cisterna de betão. Pedem a confirmação do projeto estrutural ou de fundações; não o substituem.

## O que isto faz aos resultados

- **Mudam:** a ordenação do TOPSIS, do VIKOR, do PROMETHEE II e do SMAA-VIKOR, e os volumes que cada um aponta. No tutorial de Lisboa do manual (sete volumes de 1 000 a 12 000 L, cisterna de polietileno), com os quatro eixos a 25%, a faixa de escolha do TOPSIS vai de 2 000 a 3 000 L, com a maior pontuação em 3 000 L, à frente de 2 000 L por 0,0004; com 70% num eixo e 10% nos outros, a faixa fica em 1 000 L (técnico), 2 000 a 4 000 L (económico), 1 000 a 3 000 L (ambiental) e 3 000 a 4 000 L (estrutural). Na 0.1.0, com pesos iguais, o TOPSIS escolhia 5 000 L.
- **O SMAA-VIKOR sorteia os pesos com 25% esperado em cada eixo**, e as aceitabilidades mudam: no tutorial, 3 000 L ficam em primeiro lugar em 24,1% dos sorteios, 5 000 L em 20,5% e 2 000 L em 18,2%.
- **Não mudam no manual:** regeneradas com a 0.2.0, as tabelas da simulação diária, da economia, do ciclo de vida e do volume ideal são iguais às da 0.1.0; só mudaram as do multicritério e as da modulação probabilística, que escolhe o volume de referência pelo TOPSIS (no exemplo do tutorial, passou de 20 000 L para 2 000 L). O tutorial continua com os 5 000 L do critério hidráulico, e a secção «Que volume escolher, afinal» diz o que essa escolha cede em relação à faixa de 2 000 a 3 000 L do multicritério.
- **Para reproduzir um estudo feito com a 0.1.0, use a 0.1.0** (DOI 10.5281/zenodo.23402916). Declare num estudo novo os quatro pesos de eixo e as partes no eixo (ou que usou o CRITIC, com os pesos calculados), os volumes candidatos e a faixa de escolha com a tolerância: o resultado do TOPSIS depende do conjunto avaliado.

## O que continua igual

Os dados, as licenças e a cobertura da 0.1.0 ([`DADOS.md`](DADOS.md)). Em Espanha, as tarifas continuam a ser a média regional do INE (indicativa), com 7 municípios de tarifa transcrita ainda não conferida (segunda leitura pendente); em Portugal, só Lisboa, Porto e Funchal têm tarifário transcrito. Os preços de obra e o fator de emissão da rede continuam a partir de zero.

## Limitações conhecidas desta versão

- O resultado do TOPSIS depende do conjunto de candidatos: no tutorial, sete candidatos dão a faixa de 2 000 a 3 000 L, e a varredura de 1 a 20 m³ só 1 000 L.
- A faixa de escolha não é um intervalo de confiança: depende da tolerância declarada e da grade de volumes avaliada.
- Os pesos do CRITIC dependem dos resultados do próprio estudo e mudam com o conjunto de volumes avaliado.
- As limitações da 0.1.0 que não constam do histórico como resolvidas continuam válidas ([notas da 0.1.0](NOTAS_DE_LANCAMENTO_0.1.0.md)).

## Comunicar um problema

Indique a versão (0.2.0), a edição, os passos e anexe o ficheiro `.triton`. Contacto: igorcmvaz@gmail.com.

## Como citar

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações* (versão 0.2.0). Universidade Federal de Santa Catarina (UFSC). https://doi.org/10.5281/zenodo.23402915

O DOI 10.5281/zenodo.23402915 reúne todas as versões e aponta sempre para a mais recente; a 0.2.0 ainda não tem DOI próprio. A 0.1.0 tem o DOI 10.5281/zenodo.23402916. Para a chuva, cite também a fonte usada, como nas [notas da 0.1.0](NOTAS_DE_LANCAMENTO_0.1.0.md#como-citar).
