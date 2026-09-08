# Relatório de Verificação e Validação — Netuno 5.0.7

**Data da apuração:** 7 de setembro de 2026
**Escopo:** núcleo de cálculo (`netuno.core`), com ênfase no motor de balanço hídrico diário
**Ambiente:** Python 3.13.1, Windows 11, sem `numba` instalado

---

## Nota terminológica

Este documento reporta **verificação**, não validação externa. Seguindo a distinção usual
em modelagem computacional:

- **Verificação** responde *"as equações foram implementadas corretamente?"* — é uma
  pergunta interna ao software, respondida por testes, invariantes e comparação entre
  implementações.
- **Validação** responde *"as equações representam o fenômeno real?"* — exige comparação
  com medições de campo, e não é objeto deste relatório.

Todas as evidências abaixo são de verificação. O software não substitui medição,
certificação, projeto executivo nem revisão profissional das premissas locais.

---

## 1. Sumário executivo

| Dimensão | Resultado |
| :--- | :--- |
| Suíte de testes | 265 testes, 0 falhas, 1 ignorado |
| Cobertura do núcleo de cálculo | 81% das linhas |
| Propriedades científicas verificadas | 9 de 9 aprovadas, em 2 regimes hidrológicos |
| Conservação de massa | fecha exatamente (erro máximo 0,000 L) |
| Defeitos abertos | 1 (repartição interno/irrigação no kernel JIT) |

O motor hidrológico está **correto no caminho de execução efetivamente usado**. O defeito
aberto afeta apenas um caminho alternativo que não está ativo nesta instalação (§4).

---

## 2. Propriedades científicas do motor hidrológico

Um teste de caso pontual verifica um número; uma **propriedade** verifica uma afirmação
válida para toda a família de parametrizações. Uma violação indica erro estrutural no
balanço, não divergência numérica de um cenário isolado.

As nove propriedades abaixo estão implementadas em
[`tests/invariants/test_scientific_properties.py`](../tests/invariants/test_scientific_properties.py)
e executam a cada rodada da suíte.

| # | Propriedade | Formulação | Resultado |
| :-- | :--- | :--- | :--- |
| P1 | Monotonicidade no volume | `V₁ ≤ V₂ ⟹ economia(V₁) ≤ economia(V₂)` | aprovada |
| P2 | Limites físicos | `0 ≤ economia ≤ fração não potável ≤ 100%` | aprovada |
| P2b | Volume nulo | `V = 0 ⟹ economia = 0` | aprovada |
| P3 | Saturação | `economia(V)` converge para teto finito | aprovada |
| P4 | Determinismo | mesma entrada ⟹ saída bit a bit idêntica | aprovada |
| P5 | Monotonicidade na área | `A₁ ≤ A₂ ⟹ economia(A₁) ≤ economia(A₂)` | aprovada |
| P6 | Monotonicidade inversa no descarte | descarte maior ⟹ economia não maior | aprovada |
| P7 | Extravasamento | `V` maior ⟹ extravasamento não maior | aprovada |
| P8 | Conservação de massa em grade | fecha em 12 combinações de `V × A × descarte` | aprovada |
| P9 | Série sem chuva | precipitação nula ⟹ captação, economia e extravasamento nulos | aprovada |

### 2.1 Por que dois regimes hidrológicos

A sensibilidade do modelo depende do regime, e um teste conduzido no regime errado pode
passar sem discriminar nada:

- **Limitado pela demanda** (captação abundante): a economia satura na fração não potável.
  A amplitude de resposta entre o menor e o maior reservatório é de apenas **0,02 pontos
  percentuais** — o regime é quase insensível aos parâmetros.
- **Limitado pela oferta** (captação escassa): a economia satura muito abaixo do teto não
  potável, e a amplitude de resposta é de **3,80 pontos percentuais**, cerca de 190 vezes
  maior.

Cada propriedade é, portanto, executada nos dois regimes. Um erro de balanço que
permanecesse invisível no primeiro regime seria detectado no segundo.

![Resposta do motor hidrológico ao volume do reservatório](figuras/fig01_resposta_do_modelo.png)

*Figura 1 — Resposta do motor ao volume do reservatório inferior nos dois regimes. À
esquerda, o sistema satura em 49,97%, encostando no teto de 50% imposto pela fração não
potável: o fator limitante é a demanda. À direita, satura em 3,86% com o teto em 60% muito
distante: o fator limitante é a captação. Ambas as curvas são monótonas não-decrescentes e
convergem, como exigem P1 e P3.*

### 2.2 Conservação de massa

A conservação é verificada dia a dia, e não apenas no agregado anual:

```
estoque(t−1) + captado(t) = estoque(t) + consumido(t) + extravasado(t)
```

Em 12 combinações de volume, área de captação e lâmina de descarte, ao longo de 1.825 dias
cada, o **erro máximo de fechamento foi 0,000 L** — igualdade exata em ponto flutuante, não
apenas dentro de tolerância. O recalque para o reservatório superior é transferência
interna e cancela no balanço combinado.

---

## 3. Cobertura de testes

![Cobertura de testes por módulo](figuras/fig03_cobertura_por_modulo.png)

*Figura 2 — Cobertura de linhas por módulo do núcleo. A cobertura total é de 81%. Três
módulos estão abaixo de 50%.*

A cobertura agregada de 81% é adequada, mas a distribuição é desigual e a leitura por
módulo é mais informativa que o total:

| Faixa | Módulos | Leitura |
| :--- | :--- | :--- |
| ≥ 90% | `report_service`, `topsis`, `mcdm_methods`, `environmental`, `cad_exporter`, `esg_certifications` | núcleo decisório bem coberto |
| 63–87% | `economic`, `parser`, `report_generator`, `climate_database`, `simulation`, `cost_estimates` | lacunas concentradas em ramos de exceção |
| < 50% | `scenarios` (33%), `change_detector` (24%), `excel_scenarios` (14%) | risco concentrado |

Os 70% de `simulation.py` são explicados em §4: 167 linhas correspondem aos kernels JIT,
que não existem neste ambiente e que a ferramenta de cobertura não consegue instrumentar
mesmo quando existem.

---

## 4. Defeito aberto: repartição interno/irrigação no kernel JIT

### 4.1 Contexto

`netuno.core.simulation` mantém **duas implementações independentes** do balanço diário. A
seleção é implícita e ocorre em tempo de importação:

```python
if HAS_NUMBA and not store_daily_details:   # kernel JIT compilado
else:                                       # kernel Python de referência
```

Três circunstâncias tornam isso frágil:

1. `numba` **não está declarado** em `pyproject.toml` nem em `requirements.txt`. Qual kernel
   roda depende do que houver instalado na máquina — dois usuários podem obter resultados
   diferentes do mesmo projeto sem nenhum aviso.
2. Os kernels usam `@numba.njit(fastmath=True)`. `fastmath` autoriza reassociação de
   operações de ponto flutuante, dispensando o compilador da aritmética IEEE estrita.
3. `test_mass_conservation.py` usa `store_daily_details=True`, condição que **força o kernel
   Python**. O invariante mais forte do sistema, portanto, nunca alcançava o caminho JIT.

### 4.2 O defeito

Em ambiente isolado com `numba` 0.67.0 e `numpy` 2.5.3, os dois kernels foram comparados
em 3 cenários × 3 volumes × 8 indicadores. **Sem irrigação configurada, concordam em todos
os 72 pontos** dentro de tolerância relativa de 1×10⁻⁹.

Com irrigação configurada, divergem na repartição do consumo:

![Divergência entre kernels](figuras/fig02_divergencia_kernels.png)

*Figura 3 — Repartição do consumo pluvial entre uso interno e irrigação. O total aproveitado
é idêntico nos dois kernels; apenas a divisão entre as duas parcelas diverge, em até 26,3%
na componente de irrigação.*

**Causa raiz.** O kernel Python acumula o mínimo dia a dia
([`simulation.py:788-791`](../netuno/core/simulation.py)):

```python
c_pluv_in  = min(v_c, non_pot_in_day)                  # por dia
c_pluv_irr = min(max(0.0, v_c - c_pluv_in), irr_day)   # por dia
total_pluvial_indoor_consumed += c_pluv_in             # acumula
```

O kernel JIT aplica o mesmo `min()` sobre os **totais anuais**
([`simulation.py:638-639`](../netuno/core/simulation.py)):

```python
pluv_in_est  = min(tot_pluv, tot_non_pot_demand)       # sobre o total!
pluv_irr_est = min(tot_pluv - pluv_in_est, sum(irr_arr))
```

Como `Σᵢ min(aᵢ, bᵢ) ≤ min(Σᵢ aᵢ, Σᵢ bᵢ)`, o erro tem **direção constante**: o kernel JIT
superestima sistematicamente o consumo interno e subestima a irrigação. Não é ruído de
arredondamento nem efeito de `fastmath` — é uma diferença algorítmica.

### 4.3 Severidade

O total de água aproveitada e a economia de água potável — os indicadores principais —
permanecem **exatos**. O erro afeta apenas a repartição. Contudo, a repartição não é
cosmética: **LEED v4 pontua uso externo (WEc1) e uso interno (WEc2) em créditos separados**,
de modo que um erro de 26% na componente de irrigação pode alterar o enquadramento em
certificação ainda que a economia total esteja correta.

**Situação nesta instalação:** dormente. Sem `numba` instalado, o kernel Python é sempre
usado e todos os resultados estão corretos.

### 4.4 Rastreamento

O defeito está registrado como teste de regressão em
[`tests/invariants/test_numba_python_parity.py`](../tests/invariants/test_numba_python_parity.py),
marcado `xfail` com a causa documentada. Em ambiente sem `numba` o teste é ignorado; em
ambiente com `numba` ele falha de forma controlada, sem quebrar a suíte. Quando o defeito
for corrigido, o teste passa a `XPASS` e sinaliza a correção.

### 4.5 Opções de correção

| Opção | Efeito | Custo |
| :--- | :--- | :--- |
| **A. Acumular a repartição dentro dos kernels JIT** | corrige mantendo o desempenho | altera código JIT; exige ambiente com `numba` para testar |
| **B. Declarar `numba` como dependência e corrigir** | torna o caminho rápido determinístico e suportado | adiciona dependência pesada (~200 MB com LLVM) |
| **C. Remover os kernels JIT** | elimina a classe inteira de risco; −167 linhas | perde o caminho acelerado |

A opção **C** merece consideração séria: o caminho JIT nunca esteve ativo nesta instalação,
não é declarado, não é testado por padrão e já demonstrou divergir do kernel de referência.

---

## 5. Correção aplicada nesta apuração

`tests/test_tariffs_database.py` rejeitava a faixa tarifária `[0.0, 6.0, 14.3, −2]` de
**SP/Americana (DAE Americana)**, por asseverar `is_fix ∈ [−1, 1]`.

A investigação mostrou que `−2` é semântica **deliberada e suportada**: `economic.py:149`
a documenta como *"franquia de consumo mínimo com taxa fixa inclusa"* e o comentário cita
literalmente o caso da DAE Americana. Os dados tarifários são de 26–31/08/2026, anteriores
à apuração. **O dado estava correto; a asserção é que não fora atualizada** quando `−2` foi
introduzido. A asserção passou a `[−2, −1, 1]`, com comentário explicativo.

Distribuição no catálogo das 652 cidades: `is_fix = 1` em 3.510 faixas, `−1` em 486, `−2` em 1.

---

## 6. Limitações desta verificação

Registradas explicitamente para que o relatório não seja lido além do que sustenta:

1. **Séries sintéticas.** As propriedades usam chuva exponencial pseudoaleatória, não séries
   observadas. Elas verificam coerência estrutural, não realismo hidrológico.
2. **Sem validação de campo.** Nenhuma comparação com medições de sistemas reais.
3. **Kernel JIT parcialmente verificado.** A paridade foi medida em 3 cenários; cenários com
   modulação semanal/mensal de demanda e com reservatório superior sob irrigação não foram
   comparados.
4. **Cobertura ≠ correção.** 81% de linhas executadas não implica 81% do comportamento
   verificado; ramos de exceção em `scenarios` e `excel_scenarios` permanecem pouco exercitados.
5. **Módulos econômicos e ambientais** foram verificados por testes de caso e invariantes
   financeiros, mas não pelo método de propriedades aplicado ao motor hidrológico.

---

## 7. Como reproduzir

```bash
# suíte completa com cobertura
python -m pytest --cov=netuno.core --cov-report=term-missing

# apenas as propriedades científicas
python -m pytest tests/invariants/ -v

# regerar as figuras deste relatório
python docs/gerar_figuras.py
```

Para exercitar o kernel JIT é necessário um ambiente com `numba`, preferencialmente
isolado, para não alterar as versões de `numpy` da instalação principal:

```bash
python -m venv venv_numba
venv_numba/Scripts/pip install numba pytest matplotlib
venv_numba/Scripts/python -m pytest tests/invariants/test_numba_python_parity.py -v
```
