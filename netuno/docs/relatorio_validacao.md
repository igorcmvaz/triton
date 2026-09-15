# RELATÓRIO DE VERIFICAÇÃO TÉCNICA E COMPUTACIONAL — NETUNO 5

**Grupo de Pesquisa Gestão do Espaço Sustentável**  
*Replicação Fiel e Validação da Engenharia do Netuno*  
**Escopo:** evidências automatizadas de regressão e invariantes | **Como reproduzir:** `python -m pytest tests -v`

---

## 1. SUMÁRIO EXECUTIVO

Este relatório descreve evidências automatizadas de **verificação interna** do Netuno 5. Ele não deve ser chamado de validação externa: os testes exercitam equações e regressões do próprio software, mas não substituem comparação independente com medições, certificação, projeto executivo ou revisão profissional das premissas locais.

| Evidência | Caso automatizado | Critério de aceitação | Escopo |
| :--- | :--- | :--- | :--- |
| **Conservação diária de massa** | 100 dias sintéticos, dois reservatórios | resíduo absoluto ≤ `1×10⁻⁷ L` por dia | invariante interno |
| **Comparação opcional com saída legada** | até 20 linhas de `Planilha.csv`, quando o arquivo está disponível | MAE < 3 pontos percentuais no potencial ótimo | regressão amostral, não 4.050 casos |
| **Tarifa em faixas e esgoto** | casos unitários com resultados analíticos | tolerância numérica do `pytest.approx` | verificação de equações |
| **Bomba, CAPEX, O&M, cloro e ACV** | casos unitários e estudo dos três modelos | resíduos exibidos no estudo gerado | verificação de equações/premissas |
| **TOPSIS** | ranking, pesos inválidos, invariância à translação, gaps e renderização | resultados analíticos e faixas `[0,1]` | verificação do método implementado |

---

## 2. METODOLOGIA DE VALIDAÇÃO DO BALANÇO HÍDRICO DIÁRIO

O teste de invariante usa uma série sintética reprodutível de 100 dias e confere, em cada dia, não negatividade, limites dos reservatórios e igualdade entre entradas e saídas. O estudo dos três modelos acrescenta séries longas reais de trabalho e mostra um dia auditado por clima. O teste de regressão com a planilha legada é executado somente quando o conjunto externo necessário está presente; ele amostra até 20 linhas e usa o critério declarado no próprio teste.

### Equações Principais de Conservação de Massa:
1. **Chuva efetiva e volume captável diário** (a lâmina de descarte é subtraída):
   $$P_{\text{ef},t}=\max(0,\,P_t-d_f)\;\text{se a regra se aplica};\quad P_{\text{ef},t}=P_t\;\text{caso contrário}$$
   $$V_{\text{captado},t}=P_{\text{ef},t}\,C_{\text{escoamento}}\,A_{\text{captação}}$$
   O motor subtrai $d_f$ da chuva de cada dia em que a regra se aplica, e um dia com chuva igual ou menor que $d_f$ não produz captação. É uma diferença deliberada em relação ao Netuno 4, que tratava $d_f$ como limiar do evento.
2. **Reservatório inferior no YAS**:
   $$I_t=\min(V_{\text{inf,máx}},S_{t-1}+V_{\text{captado},t});\quad O_t=\max(0,S_{t-1}+V_{\text{captado},t}-V_{\text{inf,máx}})$$
   $$Y_t=\min(D_{\text{pluvial},t},I_t);\quad S_t=I_t-Y_t$$
3. **Invariante dos dois reservatórios** (o recalque é transferência interna):
   $$S_{\text{inf},t-1}+S_{\text{sup},t-1}+V_{\text{captado},t}=S_{\text{inf},t}+S_{\text{sup},t}+Y_t+O_t$$

---

## 3. METODOLOGIA DE VALIDAÇÃO DA ANÁLISE ECONÔMICA

A suíte verifica o modelo financeiro implementado por substituição numérica. As rotinas de referência do Netuno 4 orientam a semântica de tarifas e O&M, enquanto o fluxo robusto atual usa projeção anual explícita.

### 3.1. Estrutura Tarifária Multi-Faixa (Equações 5.1 a 5.4)
O cálculo da conta de água mensal $C_{\text{água}}$ respeita o acumulado por faixas e o esgoto $C_{\text{esgoto}}$:
$$C_{\text{total}} = C_{\text{água}} + C_{\text{esgoto}} + C_{\text{imposto,var}} + C_{\text{imposto,fixo}}$$

### 3.2. Consumo Elétrico da Motobomba (Equações 5.6 a 5.10)
O tempo de operação mensal da bomba $t_{\text{total}}$ considera o recalque contínuo e o tempo de partida $t_{\text{partida}}$:
$$t_{\text{rec}} = \frac{V_{\text{recalque,mês}}}{Q_{\text{bomba}}}$$
$$t_{\text{partida}} = n_{\text{ciclos,mês}} \cdot t_{\text{partida,s}}$$
$$E_{\text{kWh}} = \frac{P_{\text{kW}} \cdot (t_{\text{rec}} + t_{\text{partida}})}{\eta_{\text{bomba}}}$$

### 3.3. Indicadores Financeiros (VPL, TIR e Payback Descontado)
$$\text{VPL} = - \text{CAPEX} + \sum_{t=1}^{N} \frac{\Delta C_{\text{água},t}+\Delta C_{\text{esgoto},t}-C_{\text{bomba},t}-C_{\text{O\&M},t}-C_{\text{cloro},t}}{(1 + i_{\text{TMA}})^t}$$

---

## 4. SUÍTE DE TESTES AUTOMATIZADOS E CRITÉRIOS DE ACEITAÇÃO

Execute `python -m pytest tests -v` no ambiente do projeto para obter a contagem e o resultado atuais. A suíte é organizada por propósito: invariantes de conservação de massa e finanças; testes unitários de simulação, parser, economia, ACV e TOPSIS; integrações de relatórios, cenários e interface. Os casos abaixo são exemplos rastreáveis — o resultado apresentado deve sempre ser o da execução atual.

```text
tests/test_batch_validation.py::test_daily_water_balance_validation_sample PASSED
tests/test_daily_water_balance.py::test_simple_3day_water_balance PASSED
tests/test_economic.py::test_water_bill_multi_tier_calculation PASSED
tests/test_economic.py::test_sewage_fixed_and_water_taxes PASSED
tests/test_economic.py::test_pump_operational_electricity_costs PASSED
tests/test_economic.py::test_additional_operational_costs PASSED
tests/test_economic.py::test_economic_vpl_and_payback_favorable PASSED
tests/test_economic.py::test_economic_unfavorable_scenario_negative_vpl PASSED
tests/test_parser.py::test_parse_float_and_int PASSED
tests/test_parser.py::test_load_precipitation_file PASSED
tests/test_parser.py::test_parse_netuno_project_csv PASSED
tests/test_parser.py::test_export_netuno4_csv_roundtrip PASSED
tests/test_simulation.py::test_zero_rain_simulation PASSED
tests/test_simulation.py::test_extreme_rain_simulation PASSED
tests/test_simulation.py::test_dual_tank_pumping PASSED
tests/test_simulation.py::test_sweep_optimal_volume_determination PASSED
```

---

## 5. CONCLUSÃO E LIMITAÇÃO DA EVIDÊNCIA

Os testes fornecem evidências de que os comportamentos cobertos permanecem estáveis. A aplicação deve ser usada como apoio à decisão: série de chuva, tarifas, orçamento, normas aplicáveis, materiais e dimensionamento final precisam ser revisados por responsável técnico habilitado.
