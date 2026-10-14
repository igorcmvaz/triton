# Formulação Matemática e Equações do Balanço Hídrico Diário

Este documento apresenta a formulação matemática canônica adotada no motor de cálculo do **Triton**, fundamentada no modelo comportamental geral de **Latham (1983)** na forma sistematizada por **Fewkes (2000b)**.

---

## 1. Balanço Hídrico Diário (Passo de Tempo $t$)

O balanço hídrico diário em reservatório de aproveitamento de água de chuva (RWH) é regido pelas Equações (1) a (5):

### Equação 1: Afluente Diário Efetivo ($Q_t$)
$$
Q_t = A \cdot C \cdot \max(P_t - F,\, 0) \times 10^{-3}
$$
onde:
- $Q_t$: volume afluente à cisterna no dia $t$ ($\text{m}^3$);
- $A$: área de captação ou telhado ($\text{m}^2$);
- $C$: coeficiente de escoamento superficial (*runoff*), adimensional ($0 \le C \le 1$);
- $P_t$: precipitação pluvial observada no dia $t$ ($\text{mm}$);
- $F$: lâmina de descarte inicial (*first-flush*) ($\text{mm}$).

> **Nota sobre o First-Flush**: No Triton, o descarte inicial é subtraído da lâmina de chuva do dia ($P_t - F$), garantindo que eventos com lâmina superior a $F$ tenham o volume excedente aproveitado.

### Equação 2: Atendimento da Demanda / Consumo Pluvial ($Y_t$)
$$
Y_t = \min\left(D_t,\; V_{t-1} + \phi\, Q_t\right)
$$
onde:
- $Y_t$: volume de água pluvial fornecido para atendimento no dia $t$ (*yield*) ($\text{m}^3$);
- $D_t$: demanda não potável requerida no dia $t$ ($\text{m}^3$);
- $V_{t-1}$: volume armazenado na cisterna ao final do dia anterior ($t-1$) ($\text{m}^3$);
- $\phi$ (a literatura também usa $\theta$): parâmetro do modelo geral de Fewkes (2000b), **opcional e só para reservatório único**:
  - $\phi = 0 \implies$ **YAS estrita** (*Yield After Spillage*): a retirada do dia sai só do que estava guardado na véspera;
  - $\phi = 1 \implies$ **YBS** (*Yield Before Spillage*): a retirada pode usar toda a chuva do dia, antes do extravasamento;
  - $0 < \phi < 1 \implies$ regras intermediárias definidas pelo autor do projeto.

> **Regra do Triton (padrão).** Sem $\phi$, o programa aplica a regra que o manual da 1.0.0 documenta: o extravasamento é calculado antes do consumo, mas a chuva do dia já atende o consumo do dia. Ela fica entre a YAS e a YBS e **não é um ponto da família de $\phi$** (nem $\phi = 0{,}5$ a reproduz). Por isso o campo `phi_operation_rule` vale `None` por padrão, e os números publicados do manual e dos estudos de caso seguem a regra do Triton.

### Equação 3: Volume Armazenado Final ($V_t$)
$$
V_t = \min\left(V_{t-1} + Q_t - Y_t,\; S - (1 - \phi)\, Y_t\right)
$$
onde:
- $V_t$: volume útil armazenado na cisterna ao final do dia $t$ ($\text{m}^3$);
- $S$: capacidade máxima de armazenamento da cisterna ($\text{m}^3$).

### Equação 4: Extravasamento Diário ($O_t$)
$$
O_t = V_{t-1} + Q_t - Y_t - V_t
$$
onde:
- $O_t$: volume extravasado (*overflow*) pelo vertedouro da cisterna no dia $t$ ($\text{m}^3$).

### Equação 5: Complementação pela Rede Pública ($M_t$)
$$
M_t = D_t - Y_t
$$
onde:
- $M_t$: volume complementado pela concessionária de água potável no dia $t$ (*mains backup*) ($\text{m}^3$).

---

## 2. Invariante de Conservação de Massa

Para todo dia $t$, o balanço obedece estritamente ao princípio de conservação de massa:

$$
\Delta V_t + Y_t + O_t - Q_t = 0
$$

onde $\Delta V_t = V_t - V_{t-1}$. Qualquer desvio em relação a zero caracteriza resíduo numérico não admitido pelo sistema de auditoria contínua do Triton (tolerância $\le 10^{-6}\,\text{m}^3$).

---

## 3. Indicadores de Desempenho Consolidados

Ao longo de uma série histórica de $N$ dias de simulação, calculam-se os indicadores adimensionais canônicos (Equações 6 a 10):

### Equação 6: Potencial de Economia de Água Potável ($E$)
$$
E = \frac{\sum_{t=1}^{N} Y_t}{\sum_{t=1}^{N} D_{T,t}} \times 100 \quad [\%]
$$
onde $D_{T,t}$ é a demanda total de água do edifício no dia $t$ (incluindo usos potáveis e não potáveis).

### Equação 7: Confiabilidade Volumétrica ($R_v$)
$$
R_v = \frac{\sum_{t=1}^{N} Y_t}{\sum_{t=1}^{N} D_t} \times 100 \quad [\%]
$$
onde $D_t$ é a demanda específica do subsistema pluvial não potável.

### Equação 8: Confiabilidade Temporal ($R_t$)
$$
R_t = \frac{N_{\mathrm{full}}}{N} \times 100 \quad [\%]
$$
onde $N_{\mathrm{full}}$ é o número de dias em que a demanda pluvial foi atendida em sua totalidade ($Y_t = D_t$).

### Equação 9: Eficiência de Armazenamento ($\eta$)
$$
\eta = \frac{\sum_{t=1}^{N} Y_t}{\sum_{t=1}^{N} Q_t} \times 100 \quad [\%]
$$
Mede a fração do volume captado e afluente que foi efetivamente consumida pelos usuários.

### Equação 10: Razão de Extravasamento ($\varepsilon$)
$$
\varepsilon = \frac{\sum_{t=1}^{N} O_t}{\sum_{t=1}^{N} Q_t} \times 100 \quad [\%]
$$
Mede a fração do volume captado perdida por extravasamento no vertedouro.

---

## 4. Referências Bibliográficas

1. **Latham, B.** (1983). *Rainwater collection systems: a literature review*. MASc thesis, Department of Civil Engineering, University of British Columbia, Vancouver.
2. **Fewkes, A.** (2000b). *Modelling the performance of rainwater collection systems: towards a generalised approach*. Urban Water, 2(4), 323–333.
3. **Jenkins, D., Pearson, F., Moore, E., Sun, J., & Valentine, R.** (1978). *Feasibility of rainwater collection systems in California*. California Water Resources Center, University of California.
4. **Mitchell, V. G.** (2007). *How well do the short-temporal-resolution characteristics of rainwater-harvesting systems predict monthly performance?* Journal of Water Supply: Research and Technology—AQUA, 56(6-7), 409–417.
