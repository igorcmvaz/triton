# Esqueleto de construção — artigo do Netuno 5

Documento de trabalho para escrever em cima. Cada seção traz **o que ela afirma**,
**com que evidência**, e **o que ainda falta produzir**. As lacunas estão marcadas
com ⚠️ e as decisões que dependem de você, com ❓.

Referências marcadas ✅ foram conferidas no registro do Crossref nesta sessão:
autores, periódico, volume, páginas e ano batem. As marcadas 🔶 vieram de busca no
OpenAlex e têm DOI, mas **não** passaram pela conferência de autoria — faça-a antes
de citar. As marcadas ⚠️ eu não consegui recuperar: você precisa fornecer ou
localizar.

---

## 0. Decisões de configuração

### ❓ Periódico-alvo

Minha recomendação é **Resources, Conservation & Recycling** (Elsevier, Q1, A1).
A razão não é o fator de impacto: é que a revisão sistemática de Semaan et al.
(2020), que é a peça central do seu argumento de lacuna, saiu no *Resources,
Conservation & Recycling X* — o periódico de acesso aberto irmão. Submeter ao RCR
põe o artigo em diálogo direto com a revisão que ele contesta, e o editor reconhece
o problema de imediato.

| Periódico | A favor | Contra |
| :--- | :--- | :--- |
| **Resources, Conservation & Recycling** | diálogo direto com Semaan et al.; aceita tríade técnico-econômico-ambiental; aceita ferramenta com validação | exige que o achado, não o programa, seja a contribuição |
| Journal of Cleaner Production | escopo largo, aceita ACV + econômico; alto volume de publicação em AAC | reputação de escopo difuso; revisão às vezes rasa |
| Water Research | maior prestígio da área | hostil a artigo de ferramenta; exigiria reenquadrar como achado hidrológico puro |
| Journal of Environmental Management | aceita decisão multicritério aplicada | menos leitores de instalações prediais |

**Consequência de estilo:** Elsevier, citação numérica ou autor-data conforme o
periódico. RCR usa autor-data (Harvard). Escrevo o esqueleto nesse pressuposto.

### Configuração assumida

| Item | Valor |
| :--- | :--- |
| Idioma | inglês britânico acadêmico (-ise, -yse, colour, behaviour, programme) |
| Estrutura | IMRaD com Discussão separada dos Resultados |
| Extensão-alvo | 8.000–9.000 palavras (corpo, sem referências) |
| Figuras | 6 a 8; tabelas 3 a 5 |
| Autoria | Igor Catão Martins Vaz; Enedir Ghisi — Grupo de Pesquisa Gestão do Espaço Sustentável, UFSC |

---

## 1. Título

O título precisa carregar a tríade **e** o mecanismo, não só o nome do programa.
Revista Q1 rejeita título que anuncia software.

**Opção A (recomendada) — o achado à frente:**
> Sizing rainwater harvesting systems on one daily balance: integrating technical,
> economic and life-cycle carbon criteria through multi-criteria decision analysis

**Opção B — a lacuna à frente:**
> Beyond single-criterion sizing: a daily-balance framework coupling potable water
> savings, financial return and embodied carbon in building rainwater systems

**Opção C — o contraste metodológico à frente:**
> Why the sizing criterion decides the tank: technical, economic and carbon optima
> diverge in building rainwater harvesting systems

⚠️ **A opção C só é honesta se os três ótimos realmente divergirem nos seus casos.**
Isso é um resultado que você ainda não produziu — ver §5.2. Se divergirem, é o
título mais forte dos três, porque anuncia um achado e não uma ferramenta.

---

## 2. Abstract (250 palavras)

Ordem Nature: problema → lacuna → o que fizemos → **número** → implicação.

| Movimento | Conteúdo | Evidência |
| :--- | :--- | :--- |
| 1 frase — contexto | dimensionamento de reservatório decide desempenho e custo | Semaan et al. 🔶 |
| 2 frases — lacuna | literatura otimiza por um critério de cada vez; ACV raramente entra no dimensionamento | Semaan et al. 🔶; Amos et al. 🔶 |
| 1 frase — o que fizemos | motor de balanço diário YAS com varredura de volumes acoplada a ACV de triagem, análise econômica e TOPSIS/SMAA | ✅ implementado |
| 3–4 frases — resultados | ⚠️ **os números ainda não existem** — ver §5 | — |
| 1 frase — implicação | o critério escolhido muda o volume recomendado; declarar o critério passa a ser obrigatório | decorre de §5.2 |

⚠️ Escrever **por último**, quando os números de §5 existirem.

---

## 3. Introduction (~1.200 palavras)

Quatro parágrafos curtos. Sem "water is essential for life".

### 3.1 Abertura — o dimensionamento é a decisão que importa

**Afirma:** o volume do reservatório é a variável de projeto que governa
simultaneamente o desempenho hídrico, o custo e o material empregado; subdimensionar
entrega confiabilidade insuficiente e superdimensionar gasta capital e carbono sem
retorno proporcional.

**Evidência:** Semaan et al. 🔶 (diz isto explicitamente no abstract); Campisano et
al. 🔶 (revisão de referência, 762 citações).

### 3.2 O estado do método — e por que ele se fragmenta

**Afirma:** a literatura desenvolveu métodos maduros de dimensionamento, mas cada
família otimiza uma dimensão de cada vez.

**Evidência a articular:**

- Semaan et al. 🔶 — «Sizing of storage is identified as the most important
  objective of optimization, yet sizing for cost is the most frequently implemented
  outcome» e «Optimizing for a local maximum is often favored over simulation-based
  optimization methods that produce global maxima». **Esta é a frase que sustenta
  metade do seu argumento.** Leia o artigo inteiro e cite o trecho com página.
- Amos et al. 🔶 — «Most of the economic analyses have ignored the full benefits
  that a RWH system can offer» e «there is a need to standardize the methods of
  economic analysis». Sustenta a outra metade.
- Ghimire et al. 🔶 — ACV de sistema de AAC, mas sem acoplamento ao dimensionamento.
  Exemplo de que a dimensão ambiental existe na literatura **separada** do
  dimensionamento.

⚠️ **Você precisa fazer a contagem que sustenta a afirmação.** Uma frase do tipo
«de N estudos de dimensionamento publicados entre 2015 e 2025, X otimizam por
critério técnico, Y por econômico, Z por ambiental e apenas W pelos três» é o que
transforma uma impressão em evidência. Sem ela, o revisor vai pedir. Sugestão: faça
uma tabela de triagem sobre a amostra de Semaan et al. estendida até 2025.

### 3.3 A lacuna, dita sem exagero

**Afirma:** não localizamos estudo que dimensione o reservatório avaliando as três
dimensões **sobre o mesmo balanço diário** e com decisão multicritério explícita.

**Evidência:** teste de duplicação executado nesta sessão — os vizinhos conceituais
mais próximos são revisões (Teston et al. 🔶; Yannopoulos et al. 🔶) ou estudos de
dimensão única (Maykot & Ghisi 🔶, econômico; Ghimire et al. 🔶, ambiental).

⚠️ **Cuidado com a formulação.** Ausência numa busca não é prova de inexistência.
Escreva «we did not identify» e não «no study has». O revisor que conhecer um
contraexemplo derruba a afirmação forte e fica com má impressão do resto.

### 3.4 Objetivo e contribuições

Três contribuições, nesta ordem de força:

1. um arcabouço que resolve as três dimensões sobre a mesma varredura de volumes,
   com TOPSIS e SMAA para tornar explícito o peso de cada critério;
2. ⚠️ a demonstração de que o critério escolhido **muda o volume recomendado** —
   ver §5.2, que é o resultado ainda por produzir;
3. o comprimento representativo da série como função do projeto, e não da cidade.

---

## 4. Materials and methods (~2.500 palavras)

### 4.1 Daily water balance and the YAS convention (~700 palavras)

**Esta é a seção que o revisor de Q1 vai ler com mais atenção.**

**Afirma:** o motor resolve o balanço diário pela convenção *yield after spillage*
(YAS), em que o armazenamento é limitado e o extravasamento ocorre **antes** da
retirada da demanda.

**As equações, na ordem que importa:**

```
I_t = min(V, S_{t-1} + Vcap_t)          armazenamento limitado
O_t = max(0, S_{t-1} + Vcap_t − V)      extravasamento
Y_t = min(D_t, I_t)                      retirada da demanda
S_t = I_t − Y_t                          estado final do dia
```

**Por que YAS e não YBS — o argumento a desenvolver:**

A diferença entre YAS e YBS é a ordem de duas operações, e a consequência é
sistemática, não aleatória: o YBS permite que a água que chega no dia atenda a
demanda **antes** de ser submetida ao limite do reservatório, o que faz um
reservatório pequeno se comportar como se fosse maior. O viés é para cima, e cresce
quando o reservatório é pequeno em relação à chuva diária.

**Evidência:**

- ✅ **Fewkes & Butler (2000)** — *Simulating the performance of rainwater
  collection and reuse systems using behavioural models*, Building Services
  Engineering Research and Technology 21(2), 99–106, DOI
  `10.1177/014362440002100204`. (Note o título exato: é «collection **and reuse**».)
- ✅ **Mitchell (2007)** — *How important is the selection of computational analysis
  method to the accuracy of rainwater tank behaviour modelling?*, Hydrological
  Processes 21(21), 2850–2861, DOI `10.1002/hyp.6499`. **É o artigo que quantifica o
  efeito da escolha do método.** Leia e cite o número, não só a conclusão.
- ⚠️ **Jenkins, Pearson & Fletcher (1978)** — origem das convenções YAS/YBS. Não
  consegui recuperá-la: provavelmente é relatório técnico da Universidade da
  Califórnia, não indexado no Crossref. Você precisa localizar a referência primária
  ou citar por meio de Fewkes & Butler.

**Evidência empírica de que o YAS é a prática corrente:** o Tangki NAHRIM 2.0
(Malásia) 🔶 e o estudo da Universidade da Cidade do Cabo 🔶 declaram YAS
explicitamente. Serve para mostrar que a escolha não é idiossincrática.

⚠️ **Oportunidade que eu recomendo agarrar.** Você tem o motor. Rodar a mesma
varredura sob YAS e sob YBS nas quatro cidades e publicar a diferença em pontos
percentuais de potencial de economia seria **um resultado próprio**, não uma
citação. Custo baixo, valor alto: transforma uma escolha de método em contribuição.

### 4.2 From Netuno 4 to Netuno 5 (~500 palavras)

**Afirma:** o motor foi reescrito, e a comparação com a versão anterior é
quantificada, com uma divergência de método isolada e declarada.

**A divergência, dita com precisão:**

| | Netuno 4 | Netuno 5 |
| :--- | :--- | :--- |
| Lâmina de descarte `d_f` | **limiar de evento**: o dia capta tudo se `P_t ≥ d_f`, e nada caso contrário | **subtraída**: chuva efetiva é `P_t − d_f`, e zero se `P_t ≤ d_f` |

**Evidência:** ✅ replicação do estudo climático nacional do grupo — com a regra de
limiar emulada (`np.where(serie >= d, serie + d, 0)`), a divergência máxima fica em
**0,11 ponto percentual**. Registrada em `docs/replicacao_dos_artigos.md`.

**Por que isso importa para o leitor:** qualquer estudo publicado com o Netuno 4
permanece reproduzível, desde que a regra de descarte seja declarada. É um argumento
de continuidade científica, não de superioridade de versão — escreva assim.

⚠️ **Contraste a enfrentar, e é o mais perigoso do artigo.** Perius et al. (2021) 🔶
concluem que «the RWH efficiency was not significantly affected by the first-flush».
Se o descarte não afeta o resultado, por que a diferença Netuno 4 → 5 importa? Você
precisa responder. Caminhos possíveis: (a) o efeito depende do regime pluviométrico
e da frequência de chuvas fracas, e as cidades diferem; (b) o efeito é pequeno na
média anual mas não no dimensionamento do reservatório de descarte, que tem custo
próprio. **Não deixe essa objeção para o revisor levantar.**

### 4.3 Life-cycle carbon module (~400 palavras)

**Afirma:** ACV de triagem acoplada à mesma varredura, com fronteira declarada.

**Componentes:** carbono incorporado por material de reservatório, tubulação e
motobomba; carbono operacional (bombeamento + tratamento); carbono evitado da água
potável substituída; saldo em 20 anos e payback ambiental.

⚠️ **Declare a limitação antes que perguntem.** É ACV de **triagem**, não inventário
completo conforme a ISO 14040. Vários fatores de emissão ainda não têm fonte
primária com versão, geografia e fronteira declaradas — isso está levantado em
`docs/revisao_de_lancamento.md`. Para um artigo Q1, **os fatores usados nos casos do
artigo precisam de procedência completa**, ainda que os demais permaneçam como
triagem. Esse é provavelmente o maior trabalho pendente antes da submissão.

### 4.4 Economic module (~300 palavras)

CAPEX, OPEX, VPL, TIR, payback simples e descontado; base tarifária de 652
municípios. Declarar a TMA adotada e a razão.

⚠️ Amos et al. 🔶 criticam justamente a falta de padronização nas análises
econômicas de AAC. Use a crítica a seu favor: declare explicitamente o horizonte, a
taxa, o que entra no CAPEX e o que fica de fora.

### 4.5 Multi-criteria decision analysis (~400 palavras)

TOPSIS com 7 critérios; SMAA sobre o simplex de pesos.

**Afirma:** o TOPSIS entrega um ranking para um vetor de pesos; o SMAA responde a
pergunta mais útil — *para que fração do espaço de pesos este volume continua sendo
o escolhido?*

⚠️ **Declare a variante.** A normalização do programa translada por `x − min(x)`
antes da normalização vetorial de Hwang & Yoon, para admitir VPL negativo. Isso é
uma variante deliberada e **precisa ser apresentada como variante**, com
justificativa — não como TOPSIS canônico. Um revisor de decisão multicritério
percebe.

⚠️ **Referências a recuperar e verificar:** Hwang & Yoon (1981) para TOPSIS;
Opricovic & Tzeng para VIKOR; Lahdelma, Hokkanen & Salminen (1998) e Tervonen &
Figueira (2008) para SMAA e SMAA-2. Nenhuma delas foi verificada nesta sessão.

### 4.6 Case studies and climate data (~200 palavras)

Base CLIMBra: 652 municípios, 19 GCMs do CMIP6, SSP2-4.5 e SSP5-8.5, corrigida de
viés por *Quantile Delta Mapping*.

- ✅ **Ballarin, A. S.; Sone, J. S.; Gesualdo, G. C.; Schwamback, D.; Reis, A.;
  Almagro, A.; Wendland, E. C.** (2023). *CLIMBra — Climate Change Dataset for
  Brazil*. Scientific Data 10(1), art. 47. DOI `10.1038/s41597-023-01956-z`.
  **Atenção:** a lista de autores que circulava internamente estava errada; esta é a
  conferida no Crossref.
- ✅ **Xavier, A. C.; King, C. W.; Scanlon, B. R.** (2016). *Daily gridded
  meteorological variables in Brazil (1980–2013)*. International Journal of
  Climatology 36(6), 2644–2659. DOI `10.1002/joc.4518`.

❓ **Quantas cidades no artigo?** Quatro casos permitem discussão profunda de cada
um; as 652 permitem generalização estatística. Minha recomendação: **quatro casos em
profundidade no corpo, e a varredura nacional como uma figura de generalização** —
é o desenho que sustenta os dois tipos de afirmação sem inchar o artigo.

---

## 5. Results (~2.000 palavras)

### 5.1 Technical, economic and carbon performance across volumes

**Afirma:** as três curvas de desempenho sobre a mesma varredura.

**Evidência:** ✅ o motor produz. ⚠️ Os casos do artigo ainda não foram rodados e
tabulados.

**Figura 1** — três painéis (a) potencial de economia, (b) VPL, (c) saldo de carbono
em 20 anos, todos contra o volume do reservatório, para as quatro cidades.
Padrão ABNT: sem título dentro da figura, (a)/(b)/(c), eixos em números redondos.

### 5.2 ⚠️ The optima diverge — **o resultado central, ainda por produzir**

**Afirma (hipótese a testar):** o volume que maximiza o potencial técnico, o que
maximiza o VPL e o que minimiza o carbono **não são o mesmo volume**, e a distância
entre eles é material.

**Isto é o coração do artigo.** Se os três ótimos coincidirem, a tese da tríade
perde força e o artigo vira uma descrição de ferramenta — publicável em SoftwareX,
não em RCR. Se divergirem, você tem um achado que justifica sozinho um Q1.

**Tabela 1** — por cidade: volume ótimo técnico, volume ótimo econômico, volume de
menor carbono, e o volume eleito pelo TOPSIS com pesos iguais. Mais a penalidade de
adotar um critério quando outro seria o correto.

**Figura 2** — SMAA: para cada volume, a fração do espaço de pesos em que ele é o
primeiro colocado. É a figura que mostra se a recomendação é robusta ou se depende
de uma ponderação específica.

### 5.3 How long must the rainfall series be?

**Afirma:** o comprimento representativo é propriedade do projeto — muda com a
fração atendível e a demanda —, e não da cidade.

**Evidência:** ✅ implementado e replicado em quatro cidades pelo método de Geraldi e
Ghisi.

⚠️ **Referência a fornecer.** Não consegui recuperar o artigo de Geraldi e Ghisi
sobre comprimento de série nas buscas. Você precisa dar a referência completa — é a
base do método e não pode ficar sem citação.

**Contexto a engatar:** Fioramonte et al. (2022) 🔶 documentam que **30 anos** é o
comprimento mais usado na literatura, tomado como convenção. Se o seu resultado
mostra que o requisito varia por projeto, você está contestando uma convenção — o
que é exatamente o tipo de afirmação que um Q1 quer. Perius et al. (2021) 🔶 também
observaram que o comprimento da série influencia o dimensionamento de volumes
maiores; convergente com o seu achado e vale citar como apoio independente.

### 5.4 Demand uncertainty: level, not noise

**Afirma:** o ruído diário do consumo se cancela ao longo de 30 anos; o que desloca
o resultado é a incerteza sobre o **nível médio** do consumo — e apenas em regime
limitado pela oferta.

**Evidência:** ✅ implementado e demonstrado.

**Por que vale publicar:** Semaan et al. 🔶 recomendam explicitamente que estudos
futuros incorporem «greater variation in water demands». Seu resultado responde a
essa recomendação e a **qualifica**: mostra que variar a demanda diária é gastar
esforço no lugar errado. É um achado contra-intuitivo, que é o tipo que sobrevive à
revisão.

---

## 6. Discussion (~1.800 palavras)

### 6.1 The sizing criterion is a declaration, not a detail

Retoma §5.2. Se os ótimos divergem, então todo estudo publicado que dimensionou por
um critério só recomendou um volume que outro critério recusaria — e a maioria não
declara o critério como escolha.

### 6.2 What the YAS/YBS choice costs

Retoma §4.1. Com o experimento sugerido, aqui entra o número próprio.

### 6.3 Continuity with Netuno 4, and the discard rule

Retoma §4.2, incluindo a resposta a Perius et al. 🔶.

### 6.4 Limitations — escreva esta seção antes da conclusão, e com honestidade

- ACV de triagem, não ISO 14040 completa;
- fatores de emissão com procedência desigual (§4.3);
- variante de normalização do TOPSIS (§4.5);
- tarifas e custos de um único país;
- ⚠️ **a lacuna foi estabelecida por busca, não por revisão sistemática** — declare
  o protocolo de busca ou apresente-a como «we did not identify».

### 6.5 Reproducibility as a design decision

**Afirma:** o programa, o manual e os números publicados saem da mesma fonte, com
verificação automática — mais de 1.100 testes, e cada número do manual tem
verificação correspondente.

⚠️ **Não transforme isto numa seção de propaganda.** Em Q1, reprodutibilidade
convence quando vem como *método*, em uma ou duas frases na seção de métodos, mais
uma declaração de disponibilidade de código e dados no fim. Uma seção inteira sobre
a suíte de testes soa defensiva. Minha sugestão: reduza a dois parágrafos aqui e
mova o essencial para uma *Data availability statement*.

---

## 7. Conclusions (~400 palavras)

Três a cinco frases-tese, cada uma com número. Sem «future work will...» genérico.

---

## 8. Mapa de evidências — consolidado

| # | Afirmação | Evidência | Estado |
| :--- | :--- | :--- | :--- |
| 1 | Dimensionamento governa desempenho e custo | Semaan et al.; Campisano et al. | 🔶 verificar autoria |
| 2 | A literatura otimiza por um critério de cada vez | Semaan et al.; Amos et al. | 🔶 + ⚠️ falta a contagem própria |
| 3 | Ninguém integra os três sobre o mesmo balanço | teste de duplicação | ⚠️ formular como «not identified» |
| 4 | YAS é conservador; YBS superestima | Fewkes & Butler; Mitchell | ✅ + ⚠️ origem (Jenkins et al.) |
| 5 | Netuno 4 e 5 divergem só na regra de descarte | replicação, 0,11 p.p. | ✅ |
| 6 | Os três ótimos divergem | — | ⚠️ **não produzido — é o artigo** |
| 7 | Comprimento da série é do projeto | quatro cidades | ✅ + ⚠️ falta ref. Geraldi & Ghisi |
| 8 | Incerteza de nível, não de ruído | demonstrado | ✅ |
| 9 | Fatores de ACV com procedência | parcial | ⚠️ maior pendência técnica |

---

## 9. Referências recuperadas

### Conferidas no Crossref ✅

- **Fewkes, A.; Butler, D.** (2000). Simulating the performance of rainwater
  collection and reuse systems using behavioural models. *Building Services
  Engineering Research and Technology*, 21(2), 99–106. `10.1177/014362440002100204`
- **Mitchell, V. G.** (2007). How important is the selection of computational
  analysis method to the accuracy of rainwater tank behaviour modelling?
  *Hydrological Processes*, 21(21), 2850–2861. `10.1002/hyp.6499`
- **Ballarin, A. S.; Sone, J. S.; Gesualdo, G. C.; Schwamback, D.; Reis, A.;
  Almagro, A.; Wendland, E. C.** (2023). CLIMBra — Climate Change Dataset for
  Brazil. *Scientific Data*, 10(1), art. 47. `10.1038/s41597-023-01956-z`
- **Xavier, A. C.; King, C. W.; Scanlon, B. R.** (2016). Daily gridded
  meteorological variables in Brazil (1980–2013). *International Journal of
  Climatology*, 36(6), 2644–2659. `10.1002/joc.4518`

### Recuperadas no OpenAlex, autoria por conferir 🔶

| Referência | DOI | Papel no artigo |
| :--- | :--- | :--- |
| Semaan et al. (2020), *Resour. Conserv. Recycl. X* | `10.1016/j.rcrx.2020.100033` | **peça central da lacuna** |
| Campisano et al. (2017), *Water Research* | `10.1016/j.watres.2017.02.056` | revisão de referência (762 cit.) |
| Amos et al. (2016), *Water* 8(4):149 | `10.3390/w8040149` | crítica à análise econômica |
| Teston et al. (2018), *Water* 10(4):471 | `10.3390/w10040471` | contexto brasileiro |
| Fioramonte et al. (2022), *AQUA* 71(7) | `10.2166/aqua.2022.034` | convenção dos 30 anos |
| Perius et al. (2021), *RBRH* | `10.1590/2318-0331.262120210067` | **contraste sobre o descarte** |
| Ghimire et al. (2019), *Resour. Conserv. Recycl.* | `10.1016/j.resconrec.2019.01.043` | ACV desacoplada |
| Maykot & Ghisi (2020), *Water* 12(2):546 | `10.3390/w12020546` | Netuno 4, econômico |
| Ghisi & Freitas (2024), *Water* 16(11):1580 | `10.3390/w16111580` | trabalho recente do grupo |
| Silva, Teston, Vaz et al. (2025), *Water* 17(18):2748 | `10.3390/w17182748` | seu trabalho recente com Netuno 4 |
| Raimondi et al. (2023), *Water* 15:1518 | `10.3390/w15081518` | estado da arte |

### A localizar ⚠️

- **Jenkins, Pearson & Fletcher (1978)** — origem das convenções YAS/YBS
- **Geraldi & Ghisi** — comprimento representativo da série
- **Hwang & Yoon (1981)** — TOPSIS
- **Opricovic & Tzeng** — VIKOR
- **Lahdelma, Hokkanen & Salminen (1998)**; **Tervonen & Figueira (2008)** — SMAA

---

## 10. Contra o que comparar

Antes da lista de programas, um argumento de método que muda o desenho do
experimento.

### 10.1 Comparar métodos vale mais do que comparar programas

Comparar o Netuno 5 com outro programa mede **três coisas ao mesmo tempo**: o
algoritmo, os valores padrão de cada um e os dados de entrada que cada um aceita.
Quando o resultado difere, a diferença não é atribuível — o revisor pergunta se o
Netuno acertou ou se o outro programa estava com outro coeficiente de escoamento,
e você não tem como responder.

Comparar **métodos dentro do mesmo motor** isola a causa. Você roda a mesma série,
a mesma área, a mesma demanda e o mesmo coeficiente, e troca só a regra. A
diferença que sai é do método, e de mais nada.

Minha recomendação, portanto: **o núcleo do artigo deve ser comparação de métodos
no Netuno 5**, e a comparação com programas de terceiros entra como verificação
externa — para mostrar que o motor não está deslocado —, não como resultado
principal.

### 10.2 Comparações de método, dentro do próprio motor

Estas são as que eu rodaria, em ordem de valor:

| # | Comparação | O que revela | Esforço |
| :--- | :--- | :--- | :--- |
| 1 | **Métodos simplificados da ABNT NBR 15527 contra a simulação diária** — Rippl, Azevedo Neto, Prático Alemão, Prático Inglês, Prático Australiano | É a crítica dos valores médios feita número. O engenheiro brasileiro usa estes métodos; mostrar por quanto eles erram é o resultado de maior alcance prático do artigo | baixo — são fórmulas fechadas |
| 2 | **YAS contra YBS** | Quantifica o viés da convenção. Fecha a discussão de §4.1 com número próprio em vez de citação | baixo — é trocar a ordem de duas linhas |
| 3 | **Netuno 4 contra Netuno 5** | Continuidade e a regra de descarte | ✅ já feito |
| 4 | **Passo diário contra passo mensal** | Sustenta a escolha do passo; muitos estudos ainda usam médias mensais | baixo |
| 5 | **Percentil de base do R95p: série inteira contra 1961–1990** | Relevante se os índices pluviométricos entrarem no artigo | médio |

A comparação 1 é, na minha leitura, a de maior retorno: ela liga o artigo
diretamente à prática normativa brasileira e dá um resultado que o revisor
internacional entende sem conhecer a NBR.

### 10.3 Programas de terceiros — o que a literatura mostra usando

Distingo o que recuperei em registro do que sei de memória, porque a diferença
importa.

**Recuperados e confirmados em uso na literatura 🔶**

| Programa | Origem | Convenção | Por que serve de comparação | Evidência |
| :--- | :--- | :--- | :--- | :--- |
| **Netuno 4** | UFSC, Brasil | limiar de descarte | antecessor direto; base dos estudos do grupo | Maykot & Ghisi (2020); Silva, Teston, Vaz et al. (2025) |
| **RainCycle** | Reino Unido | balanço diário com custeio de ciclo de vida | **o comparador mais próximo na dimensão econômica** — faz análise de custo de ciclo de vida, que é metade da sua tríade | Gao, Kim & Lee (2014), *J. Korean Housing Assoc.*, `10.6107/jkha.2014.25.3.053`; Doncaster et al. (2012), relatório de Bradford |
| **Tangki NAHRIM 2.0** | NAHRIM, Malásia | **YAS declarado** | aplicação web gratuita, YAS explícito, base própria de chuva; comparador metodologicamente alinhado | Mat Daud et al. (2021), `10.1088/1755-1315/920/1/012035`; Mat Daud et al. (2023), `10.17576/jkukm-2023-35(6)-21` |
| **SS STORM (modificado)** | EUA | planilha de armazenamento, tratamento e extravasamento | usado com índice de sustentabilidade; comparador na dimensão de confiabilidade | Park & Um (2018), `10.3390/su10010280` |

**De memória, a verificar antes de citar ⚠️**

Estes eu não recuperei em registro nesta sessão. Existem, mas **confirme a
referência e a disponibilidade atual antes de incluir**: SimTanka (Índia),
Aquacycle e UrbanBEATS (Austrália), Plugrisost (Espanha, acoplado a ACV), o módulo
de aproveitamento do EPA SWMM, e as calculadoras normativas do BS 8515 (Reino
Unido) e da DIN 1989 (Alemanha).

⚠️ **Cuidado com o Plugrisost em particular.** Se ele de fato acopla ACV ao
dimensionamento, é o **concorrente mais direto da sua tese de lacuna** — e você
precisa saber disso antes do revisor. Verifique-o primeiro.

### 10.4 O desenho de comparação que eu proporia

Três camadas, com propósitos distintos:

1. **Camada de método** (o resultado): as comparações de §10.2, todas no Netuno 5,
   sobre as mesmas quatro cidades. Isola a causa e produz os números do artigo.
2. **Camada de verificação externa** (a confiança): mesmos casos no Netuno 4 e no
   Tangki NAHRIM 2.0. Se o Netuno 5 ficar próximo do NAHRIM — que declara YAS — e
   se afastar do Netuno 4 no descarte, você demonstra que o motor está alinhado com
   a prática internacional e que a divergência com a versão anterior tem causa
   conhecida.
3. **Camada de escopo** (a lacuna): uma tabela de funcionalidades comparando quais
   programas resolvem técnico, econômico e ambiental, e quais fazem decisão
   multicritério. **Esta tabela é o argumento de lacuna em forma visual**, e vale
   mais que um parágrafo de prosa.

⚠️ **A tabela da camada 3 precisa ser justa.** Liste também o que os outros fazem e
o Netuno 5 não — por exemplo, gestão de escoamento superficial e qualidade
microbiológica dinâmica. Uma tabela em que a sua ferramenta ganha em todas as
colunas não convence ninguém e sinaliza viés.

### 10.5 Obstáculo prático a antecipar

Comparar com programa de terceiros exige **entrar com os mesmos dados**, e cada um
aceita um formato de série de chuva diferente. Reserve tempo para isso, e **declare
no artigo exatamente quais parâmetros foram igualados** — área, coeficiente,
demanda, lâmina de descarte, passo, período da série. Sem essa declaração, a
comparação não é reprodutível e o revisor tem razão em desconfiar.

---
## 11. O que fazer antes de escrever

Em ordem de importância:

1. ⚠️ **Rodar os casos e testar se os três ótimos divergem** (§5.2). Sem isso não há
   artigo Q1 — há artigo de ferramenta.
2. ⚠️ **Dar procedência aos fatores de ACV** usados nos casos do artigo (§4.3).
3. ⚠️ **Fazer a contagem que sustenta a lacuna** (§3.2): N estudos, quantos por
   critério.
4. ⚠️ **Rodar YAS contra YBS** nas quatro cidades (§4.1) — resultado próprio, custo
   baixo.
5. ⚠️ **Fornecer as cinco referências faltantes** (§9).
6. ⚠️ **Preparar a resposta a Perius et al.** sobre o descarte (§4.2).
7. ❓ Decidir periódico e número de casos.

Os itens 1 e 2 são os que separam uma submissão de uma rejeição em triagem.
