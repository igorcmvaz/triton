# Estruturação da pesquisa — o modelo matemático como contribuição

Documento de desenho de pesquisa. Substitui o eixo do esqueleto anterior: ali a
contribuição era a integração da tríade; aqui é **o modelo matemático**, e a
integração passa a ser consequência dele.

⚠️ **Convenção deste documento.** Marco com **[P]** o que está provado, **[E]** o
que está verificado empiricamente mas não provado, e **[?]** o que é conjectura. Num
artigo de foco matemático, confundir os três é fatal — o revisor confere.

---

## 1. Por que este eixo é mais forte

O esqueleto anterior oferecia uma ferramenta que integra três dimensões. É uma
contribuição de engenharia, e um revisor de Q1 pode responder que integrar módulos
conhecidos não é ciência nova.

O eixo matemático responde outra coisa: **por que o problema tem a estrutura que
tem, e o que decorre disso**. A diferença prática é que os resultados deixam de ser
«no nosso caso deu assim» e passam a ser «isto vale sempre que tais condições
valerem». O segundo tipo sobrevive à revisão; o primeiro é pedido para generalizar.

E há um achado que só aparece neste eixo: **a prática corrente de dimensionamento
não otimiza nada**. Ver §4.3 — é a contribuição mais afiada do trabalho.

---

## 2. O modelo formal

### 2.1 Notação

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `t` | dia, `t = 1 … T` | — |
| `P_t` | precipitação diária | mm |
| `d` | lâmina de descarte da primeira chuva | mm |
| `A` | área de captação | m² |
| `C` | coeficiente de escoamento | — |
| `D_t` | demanda não potável do dia | L |
| `V` | capacidade do reservatório inferior | L |
| `S_t` | volume armazenado ao fim do dia `t` | L |
| `Q_t(d)` | volume captável no dia `t` | L |
| `Y_t` | volume atendido por água de chuva no dia `t` | L |
| `O_t` | extravasamento no dia `t` | L |

### 2.2 O operador de captação e a regra de descarte

A regra de descarte é um **operador** aplicado à precipitação antes da conversão em
volume, e as duas versões do programa usam operadores diferentes:

```
Netuno 5 (subtrativo):   φ_sub(P, d) = max(0, P − d)
Netuno 4 (limiar):       φ_lim(P, d) = P · 1[P ≥ d]
```

E então `Q_t = A · C · φ(P_t, d)`.

**[P] Proposição 1 (ordenação dos operadores).** Para todo `P ≥ 0` e `d > 0`:

```
φ_sub(P, d) ≤ φ_lim(P, d)
```

com igualdade se e somente se `P = 0` ou `P ≥ d` e `d = 0`. A demonstração é
imediata por casos: se `P < d`, ambos valem 0 exceto que φ_lim dá 0 e φ_sub dá 0; se
`P ≥ d`, φ_sub = P − d < P = φ_lim.

**Consequência:** o Netuno 4 capta sempre mais, e a diferença acumulada é
`A·C·d·|{t : P_t ≥ d}|`. **Isto explica e quantifica a divergência entre as versões
sem recorrer a simulação** — é resultado fechado, e é bonito no artigo.

⚠️ E responde a objeção de Perius et al. (2021) que ficou pendente no esqueleto
anterior: o efeito do descarte **não é pequeno em geral**, ele é proporcional ao
número de dias chuvosos. Num regime de muitas chuvas fracas o efeito é grande; num
de poucas chuvas fortes, pequeno. A discordância na literatura é explicável pelo
regime, e você pode mostrar isso analiticamente.

### 2.3 A transição de estado e a ordem das operações

**Convenção YAS (a do Netuno 5):**

```
I_t = min(V, S_{t−1} + Q_t)          (1) armazenamento limitado
O_t = max(0, S_{t−1} + Q_t − V)      (2) extravasamento
Y_t = min(D_t, I_t)                  (3) atendimento
S_t = I_t − Y_t                      (4) estado final
```

**Convenção YBS:** troca a ordem de (1) e (3) — a demanda é retirada antes de o
limite ser aplicado.

**[?] Proposição 2 (dominância do YBS).** Para toda série `{P_t}`, toda demanda
`{D_t}` e todo `V > 0`:

```
Y_t^YBS ≥ Y_t^YAS   para todo t
```

**Estado: conjecturada, não provada.** A intuição é clara — o YBS deixa a água do
dia atender a demanda antes de ser submetida ao limite — mas a demonstração exige
indução sobre o estado, e o estado do YBS pode ficar **menor** que o do YAS depois
de um dia de atendimento, o que abre a possibilidade de o YAS ter mais água guardada
num dia seguinte. **A monotonicidade dia a dia não é óbvia e pode ser falsa.**

⚠️ **Este é um item a resolver, e é interessante justamente por não ser trivial.**
Se a dominância pontual falhar mas a acumulada valer, isso é um resultado por si só.
Recomendo: (a) tentar a prova por indução com hipótese de acoplamento de estados;
(b) se travar, procurar contraexemplo numericamente antes de insistir.

### 2.4 A função de atendimento

Defina o **atendimento anual** como função do volume:

```
Y(V) = (1/n_anos) · Σ_t Y_t(V)
```

e o potencial de economia `E_pot(V) = 100 · Y(V) / Σ_t D_t`.

**[E] Proposição 3 (monotonicidade e concavidade).** `Y(V)` é não decrescente e
**côncava** em `V`.

**Estado: verificada empiricamente, não provada.** Verificação feita nesta sessão:
quatro cidades — Florianópolis, Brasília, Manaus e São Paulo —, quarenta volumes de
500 a 20.000 L, residência unifamiliar de referência. **Ganhos marginais não
crescentes em todos os pontos, zero violações.**

| Cidade | E_pot máximo | Ganho marginal do 1.º passo | do último |
| :--- | ---: | ---: | ---: |
| Florianópolis | 42,1% | 5,691 p.p./500 L | 0,146 |
| Brasília | 27,5% | 2,020 | 0,215 |
| Manaus | 39,0% | 3,008 | 0,260 |
| São Paulo | 41,1% | 5,620 | 0,175 |

A monotonicidade é fácil de provar (mais capacidade nunca reduz o atendimento, por
acoplamento trivial). **A concavidade é a parte difícil e a mais valiosa.**

Intuição da prova: o incremento `Y(V+Δ) − Y(V)` capta apenas água que, com
capacidade `V`, teria extravasado **e** que encontra demanda depois. À medida que
`V` cresce, os eventos de extravasamento aproveitáveis se esgotam dos mais fáceis
para os mais raros. Formalmente, o ganho marginal é o valor esperado do
extravasamento na faixa `[V, V+Δ]` ponderado pela demanda subsequente, e a
distribuição do estado de armazenamento tem cauda superior de densidade não
crescente sob condições a especificar.

⚠️ **Onde a concavidade pode falhar, e você precisa testar.** Em regime fortemente
sazonal com uma única estação chuvosa longa, um reservatório grande o bastante para
atravessar a estiagem pode produzir um **salto** de atendimento — ganho marginal
crescente numa faixa. Brasília é sazonal e não violou, mas quatro cidades não são
prova. **Rode as 652 e conte as violações.** Se houver zero, é evidência forte; se
houver, você descobre a condição, que é um resultado ainda melhor.

---

## 3. Os teoremas de dimensionamento

Aqui está o núcleo do artigo.

### 3.1 O ótimo ambiental

Sejam, ao longo de uma vida útil de `L` anos:

```
G(V) = g₀ + g₁·V            carbono incorporado, afim crescente
Op                          carbono operacional anual
a                           carbono evitado por m³ de água potável substituída
B(V) = G(V) + L·Op(V) − L·a·Y(V)/1000        saldo de carbono
```

**[P] Teorema 1 (existência e unicidade do ótimo interior de carbono).** Se `G` é
afim crescente e `Y` é côncava crescente com `Y'(V) → 0` quando `V → ∞`, então `B` é
**convexa** e admite mínimo único. O mínimo é **interior** se e somente se

```
g₁ < (L·a/1000) · Y'(0⁺)
```

e é `V* = 0` caso contrário.

*Demonstração.* `G` afim ⇒ `G` convexa. `Y` côncava ⇒ `−Y` convexa ⇒ `−L·a·Y/1000`
convexa. Soma de convexas é convexa. A condição de primeira ordem é
`g₁ = (L·a/1000)·Y'(V*)`; como `Y'` é não crescente (concavidade) e tende a zero,
existe solução única sempre que `g₁` estiver abaixo de `Y'(0⁺)` escalado. ∎

**O que isto entrega ao projetista — e é uma regra de bolso publicável:**

> Construa o sistema se e somente se o carbono incorporado por litro de reservatório
> for menor que o carbono evitado, ao longo da vida útil, pelo primeiro litro de
> atendimento. E dimensione onde o carbono incorporado do próximo litro igualar o
> carbono evitado que ele gera.

**[E] Verificação numérica já feita.** Residência de referência, Florianópolis: o
saldo em 20 anos é −152, −206, −215 e −189 kg CO₂e para 1.000, 2.000, 3.000 e
5.000 L. **Mínimo interior em 3.000 L, e piora depois** — exatamente o previsto pelo
Teorema 1.

### 3.2 O ótimo econômico

Mesma estrutura: CAPEX afim em `V`, economia anual proporcional a `Y(V)` côncava.

**[P] Teorema 2.** O valor presente líquido `VPL(V)` é **côncavo** e admite máximo
único; interior sob a condição análoga à do Teorema 1.

⚠️ **Cuidado com uma hipótese.** O CAPEX de reservatórios reais **não é afim** — tem
degraus, porque reservatórios vêm em tamanhos comerciais. O teorema vale para a
envoltória afim; para a função em degraus, o ótimo é o do conjunto discreto de
tamanhos disponíveis. **Declare isso**, e apresente a versão discreta como corolário.

### 3.3 O corolário que critica a prática corrente

Esta é, na minha leitura, **a contribuição mais afiada do trabalho**.

O dimensionamento convencional — inclusive o do Netuno 4 e o do próprio Netuno 5 —
define o «volume ideal» por uma **regra de parada por ganho marginal**:

```
V_ideal = min { V : ΔE_pot/ΔV < ε }
```

**[P] Corolário 1.** A regra de parada sempre termina, porque `Y` é côncava com
`Y' → 0`. Mas `V_ideal` **não é o argmin nem o argmax de nenhuma função objetivo**:
é o ponto em que uma derivada cruza um limiar `ε` arbitrário, sem unidade física e
sem interpretação econômica ou ambiental.

**Em contraste**, `V*` dos Teoremas 1 e 2 são ótimos genuínos, com condição de
primeira ordem interpretável: *marginal incorrido igual a marginal evitado*.

**A frase que o artigo pode dizer, e que é forte:**

> O «volume ideal» amplamente adotado na literatura de aproveitamento de água de
> chuva é uma heurística de parada, não um ótimo. Duas escolhas de `ε` produzem dois
> volumes, ambos chamados de ideais, sem que nenhum critério externo distinga entre
> eles.

⚠️ **Isto critica o próprio Netuno, inclusive o 4, que é do seu grupo.** Minha
recomendação é enfrentar de frente: apresentar como evolução do próprio trabalho,
não como crítica a terceiros. É mais honesto e desarma o revisor.

### 3.4 O comprimento de série, reenquadrado

O resultado de comprimento representativo deixa de ser empírico e vira uma pergunta
de **convergência**: a partir de quantos anos `Ŷ_n(V)` — estimador com `n` anos —
está a `δ` de `Y(V)`, com confiança `1−α`?

**[?]** Sob estacionariedade e mistura fraca da série de chuva, vale um teorema
central do limite e `|Ŷ_n − Y| = O_p(n^{−1/2})`. Isso **prediz** que o comprimento
necessário cresce com `δ^{−2}`, e que depende de `V` através da variância de `Y`.

⚠️ **Testável e valioso.** Se o comprimento observado nas suas quatro cidades seguir
`n ∝ δ^{−2}`, você confirmou a taxa. Se não seguir, a série viola alguma hipótese —
provavelmente estacionariedade — e isso é um achado sobre clima, não sobre método.

---

## 4. Perguntas de pesquisa e hipóteses

| # | Pergunta | Hipótese | Como se responde |
| :--- | :--- | :--- | :--- |
| Q1 | A função de atendimento é côncava em toda parte? | H1: sim, sob demanda constante | prova + varredura das 652 cidades contando violações |
| Q2 | O ótimo de carbono é interior? | H2: sim, se `g₁ < L·a·Y'(0⁺)/1000` | Teorema 1 + verificação numérica |
| Q3 | Os ótimos técnico, econômico e ambiental coincidem? | H3: não, e a distância cresce com a razão CAPEX/tarifa | varredura nacional |
| Q4 | Qual o efeito do operador de descarte? | H4: diferença proporcional ao n.º de dias chuvosos | Proposição 1 + verificação |
| Q5 | YBS domina YAS pontualmente? | H5: sim | prova ou contraexemplo |
| Q6 | O comprimento de série converge a `n^{−1/2}`? | H6: sim, sob estacionariedade | ajuste da taxa observada |

---

## 5. Desenho experimental

### 5.1 Unidade e variação

- **Unidade fixa:** uma residência unifamiliar de referência, declarada com precisão
  de reprodução (área, moradores, consumo per capita, fração não potável, arranjo).
- **Variação:** o clima. Quatro cidades em profundidade e as 652 para generalização.
- **Rationale:** com a tipologia constante, o regime pluviométrico fica isolado como
  única variável — é o desenho que dá poder estatístico sem confundimento.

### 5.2 Experimentos, em ordem de execução

| # | Experimento | Responde | Esforço |
| :--- | :--- | :--- | :--- |
| 1 | Varredura de `Y(V)` nas 652 cidades; contagem de violações de concavidade | Q1 | médio — já implementado, é rodar |
| 2 | Curvas `B(V)` e `VPL(V)`; localização dos três ótimos | Q2, Q3 | médio |
| 3 | `φ_sub` contra `φ_lim` na mesma série; regressão da diferença contra o n.º de dias chuvosos | Q4 | baixo — ✅ já emulado |
| 4 | YAS contra YBS; busca de contraexemplo à dominância pontual | Q5 | baixo |
| 5 | Comprimento representativo contra `δ`; ajuste do expoente | Q6 | ✅ implementado |

⚠️ **O experimento 1 é o mais importante e o menos glamouroso.** Zero violações em
652 cidades transforma a Proposição 3 de conjectura em fato empírico robusto, e é o
que sustenta os dois teoremas. Faça-o primeiro.

---

## 6. Estrutura do artigo

| Seção | Conteúdo | Palavras |
| :--- | :--- | :--- |
| 1. Introduction | a lacuna: dimensionamento sem teoria de otimização | 1.000 |
| 2. Model formulation | §2 deste documento: operadores, transição, `Y(V)` | 1.600 |
| 3. Properties and optimality | §3: Proposições 1–3, Teoremas 1–2, Corolário 1 | 1.800 |
| 4. Implementation | o Netuno 5 como realização do modelo; verificação | 900 |
| 5. Numerical experiments | §5.2 | 1.800 |
| 6. Discussion | o que muda na prática; a crítica à regra de parada | 1.200 |
| 7. Conclusions | | 400 |

**O lançamento da ferramenta cabe na §4, e não no título.** Num artigo de foco
matemático o programa é a implementação de referência — o que, paradoxalmente, dá
mais credibilidade à ferramenta do que anunciá-la.

### Títulos possíveis

> On the concavity of rainwater yield and the existence of interior optima for tank
> sizing

> Rainwater tank sizing is not an optimisation problem — and what it becomes when it
> is

> Marginal-gain stopping rules versus true optima in rainwater harvesting tank design

---

## 7. Periódico

O foco matemático desloca o alvo. **Environmental Modelling & Software** passa a ser
a recomendação: aceita formulação com teoremas acompanhada de implementação, e é
exatamente o perfil «modelo + ferramenta» que você descreveu. **Water Research**
volta a ser viável, porque a contribuição deixa de ser uma ferramenta. O **Journal
of Hydrology** aceita a formulação, mas tem menos interesse na parte econômica e
ambiental.

---

## 8. Riscos

| Risco | Gravidade | Mitigação |
| :--- | :--- | :--- |
| A concavidade falhar em algum regime | **alta** — derruba os dois teoremas na forma geral | achar a condição e enunciar os teoremas sob ela; a falha vira resultado |
| A dominância YBS ≥ YAS ser falsa | média | vira resultado negativo, que é publicável se bem explicado |
| Revisor pedir prova da concavidade | **alta** | ou provar, ou enunciar explicitamente como hipótese verificada e restringir os teoremas |
| A crítica à regra de parada soar como ataque ao próprio grupo | baixa | enquadrar como evolução do próprio trabalho |

⚠️ **O risco maior é o terceiro.** Num artigo de foco matemático, «verificamos em
652 cidades» não substitui uma prova, e o revisor pode exigi-la. Duas saídas
honestas: provar a concavidade sob hipóteses declaradas, ou enunciar os teoremas
como **condicionais à concavidade** e apresentar a verificação como evidência de que
a condição vale na prática. A segunda é aceitável e comum; a primeira é melhor.

---

## 9. O que fazer primeiro

1. **Rodar o experimento 1** — 652 cidades, contagem de violações de concavidade.
   Tudo depende disso.
2. **Tentar a prova da concavidade**, ou delimitar as hipóteses sob as quais ela
   vale.
3. **Rodar o econômico** para fechar a tabela dos três ótimos.
4. Resolver a Proposição 2 — prova ou contraexemplo.
