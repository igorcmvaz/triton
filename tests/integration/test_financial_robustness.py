"""
Suíte de Testes Financeiros Robustos e Cálculos Massivos do Netuno 5.
Valida:
1. Leitura e Execução de Presets da Planilha CSV (tests/integration/test_financial_presets.csv)
2. Propriedades Matemáticas Invariantes (Monotonicidade, Convergência da TIR, Payback Descontado >= Simples, Balanço de Caixa)
3. Teste Massivo Paramétrico (Monte Carlo / Grid Search com +1000 cenários)
4. Estabilidade da Matriz e Gráfico Teia de Sensibilidade Multivariável em Cenários Extremos
"""

import os
import csv
import math
import pytest
import numpy as np

from netuno.core.economic import (
    run_robust_economic_analysis,
    run_sensitivity_analysis,
    calculate_water_bill,
    run_economic_analysis
)
from netuno.core.parser import NetunoConfig
from netuno.core.simulation import SingleTankSimulationResult


PRESETS_CSV_PATH = os.path.join(os.path.dirname(__file__), "test_financial_presets.csv")


def load_presets_from_csv():
    """Carrega os presets financeiros da planilha CSV."""
    presets = []
    with open(PRESETS_CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            presets.append({
                'preset_id': row['preset_id'],
                'nome_cenario': row['nome_cenario'],
                'investimento_inicial': float(row['investimento_inicial']),
                'volume_agua_m3_ano': float(row['volume_agua_m3_ano']),
                'tarifa_agua_m3': float(row['tarifa_agua_m3']),
                'tarifa_esgoto_m3': float(row['tarifa_esgoto_m3']),
                'modo_esgoto': int(row['modo_esgoto']),
                'reajuste_agua_pct': float(row['reajuste_agua_pct']),
                'reajuste_esgoto_pct': float(row['reajuste_esgoto_pct']),
                'reajuste_energia_pct': float(row['reajuste_energia_pct']),
                'inflacao_pct': float(row['inflacao_pct']),
                'tma_pct': float(row['tma_pct']),
                'custo_om_ano': float(row['custo_om_ano']),
                'periodo_anos': int(row['periodo_anos']),
                'vpl_esperado_min': float(row['vpl_esperado_min']),
                'vpl_esperado_max': float(row['vpl_esperado_max']),
                'payback_simples_max': int(row['payback_simples_max']),
                'tir_esperada_min': float(row['tir_esperada_min'])
            })
    return presets


def test_robust_irr_matches_known_conventional_cash_flow():
    # -1000 no ano zero e 600/ano: TIR de 13,066% em dois anos.
    result = run_robust_economic_analysis(
        initial_investment=1000.0,
        annual_water_saved_m3=600.0,
        water_tariff_per_m3=1.0,
        annual_om_cost_base=0.0,
        pump_power_kw=0.0,
        pump_hours_year=0.0,
        elec_tariff_kwh=0.0,
        analysis_period_years=2,
        discount_rate=0.0,
        water_tariff_escalation_rate=0.0,
        sewage_tariff_escalation_rate=0.0,
        elec_tariff_escalation_rate=0.0,
        inflation_rate=0.0,
    )
    assert result.tir_pct == pytest.approx(13.066, abs=0.01)


@pytest.mark.parametrize("field,value", [
    ("initial_investment", -1.0),
    ("annual_water_saved_m3", float("nan")),
    ("analysis_period_years", 0),
])
def test_robust_economic_rejects_invalid_inputs(field, value):
    params = dict(
        initial_investment=1000.0,
        annual_water_saved_m3=100.0,
        water_tariff_per_m3=5.0,
        analysis_period_years=20,
    )
    params[field] = value
    with pytest.raises(ValueError):
        run_robust_economic_analysis(**params)


# -----------------------------------------------------------------------------
# 1. VALIDAÇÃO DE PRESETS DA PLANILHA CSV
# -----------------------------------------------------------------------------

def test_csv_presets_execution():
    """Testa se todos os presets da planilha CSV executam corretamente dentro das faixas esperadas."""
    presets = load_presets_from_csv()
    assert len(presets) >= 11, "A planilha CSV deve conter pelo menos 11 presets."

    for p in presets:
        res = run_robust_economic_analysis(
            initial_investment=p['investimento_inicial'],
            annual_water_saved_m3=p['volume_agua_m3_ano'],
            water_tariff_per_m3=p['tarifa_agua_m3'],
            sewage_tariff_per_m3=p['tarifa_esgoto_m3'],
            sewage_mode=p['modo_esgoto'],
            water_tariff_escalation_rate=p['reajuste_agua_pct'],
            sewage_tariff_escalation_rate=p['reajuste_esgoto_pct'],
            elec_tariff_escalation_rate=p['reajuste_energia_pct'],
            inflation_rate=p['inflacao_pct'],
            discount_rate=p['tma_pct'],
            annual_om_cost_base=p['custo_om_ano'],
            analysis_period_years=p['periodo_anos']
        )

        # Validações sem erros numéricos
        assert not math.isnan(res.vpl), f"VPL NaN no preset {p['preset_id']}"
        assert not math.isinf(res.vpl), f"VPL Inf no preset {p['preset_id']}"
        assert not math.isnan(res.tir_pct), f"TIR NaN no preset {p['preset_id']}"

        # Validação de intervalo de VPL esperado da planilha
        assert p['vpl_esperado_min'] <= res.vpl <= p['vpl_esperado_max'], (
            f"Preset {p['preset_id']} ({p['nome_cenario']}): VPL {res.vpl:.2f} fora da faixa "
            f"[{p['vpl_esperado_min']}, {p['vpl_esperado_max']}]"
        )

        # Payback simples
        if res.payback_simple_years is not None:
            assert res.payback_simple_years <= p['payback_simples_max']

        # TIR
        if res.vpl > 0:
            assert res.tir_pct >= p['tir_esperada_min']


# -----------------------------------------------------------------------------
# 2. PROPRIEDADES MATEMÁTICAS INVARIANTES
# -----------------------------------------------------------------------------

def test_invariant_monotonicity_volume_and_tariff():
    """Garante que aumentar o volume economizado ou a tarifa DEVE aumentar ou manter o VPL (ceteris paribus)."""
    base_params = {
        'initial_investment': 10000.0,
        'annual_water_saved_m3': 100.0,
        'water_tariff_per_m3': 8.0,
        'sewage_tariff_per_m3': 6.4,
        'sewage_mode': 1,
        'water_tariff_escalation_rate': 0.05,
        'sewage_tariff_escalation_rate': 0.05,
        'elec_tariff_escalation_rate': 0.05,
        'inflation_rate': 0.04,
        'discount_rate': 0.08,
        'annual_om_cost_base': 150.0,
        'analysis_period_years': 20
    }

    res_base = run_robust_economic_analysis(**base_params)

    # 1. Monotonicidade do Volume: 100 m³ -> 150 m³
    params_more_vol = base_params.copy()
    params_more_vol['annual_water_saved_m3'] = 150.0
    res_more_vol = run_robust_economic_analysis(**params_more_vol)
    assert res_more_vol.vpl > res_base.vpl, "VPL deveria aumentar com maior volume economizado"

    # 2. Monotonicidade da Tarifa: R$ 8.00 -> R$ 12.00
    params_higher_tariff = base_params.copy()
    params_higher_tariff['water_tariff_per_m3'] = 12.0
    res_higher_tariff = run_robust_economic_analysis(**params_higher_tariff)
    assert res_higher_tariff.vpl > res_base.vpl, "VPL deveria aumentar com tarifa de água maior"

    # 3. Monotonicidade do Investimento Inicial (CAPEX): R$ 10.000 -> R$ 15.000
    params_higher_capex = base_params.copy()
    params_higher_capex['initial_investment'] = 15000.0
    res_higher_capex = run_robust_economic_analysis(**params_higher_capex)
    assert res_higher_capex.vpl < res_base.vpl, "VPL deveria diminuir com CAPEX maior"


def test_invariant_payback_discounted_gte_simple():
    """Garante que o Payback Descontado é sempre >= Payback Simples."""
    for inv in [5000.0, 15000.0, 50000.0]:
        for vol in [50.0, 150.0, 500.0]:
            for tma in [0.05, 0.10, 0.15]:
                res = run_robust_economic_analysis(
                    initial_investment=inv,
                    annual_water_saved_m3=vol,
                    water_tariff_per_m3=10.0,
                    sewage_tariff_per_m3=8.0,
                    discount_rate=tma,
                    analysis_period_years=25
                )

                if res.payback_simple_years is not None and res.payback_discounted_years is not None:
                    assert res.payback_discounted_years >= res.payback_simple_years, (
                        f"Payback Descontado ({res.payback_discounted_years}) deve ser >= Simples ({res.payback_simple_years})"
                    )


def test_invariant_cash_flow_equation_balance():
    """Garante que Fluxo Líquido = Receita Bruta - Custos OPEX (em todos os anos)."""
    res = run_robust_economic_analysis(
        initial_investment=12000.0,
        annual_water_saved_m3=120.0,
        water_tariff_per_m3=9.0,
        sewage_tariff_per_m3=7.2,
        water_tariff_escalation_rate=0.06,
        inflation_rate=0.04,
        discount_rate=0.09,
        annual_om_cost_base=200.0,
        analysis_period_years=20
    )

    for item in res.annual_cash_flows:
        if item.year == 0:
            assert item.net_cash_flow_nominal_brl == -12000.0
        else:
            expected_net = item.total_gross_savings_brl - item.pump_energy_cost_brl - item.om_cost_brl
            assert math.isclose(item.net_cash_flow_nominal_brl, expected_net, abs_tol=1e-4)


# -----------------------------------------------------------------------------
# 3. TESTE MASSIVO PARAMÉTRICO (+1.000 CENÁRIOS DE STRESS)
# -----------------------------------------------------------------------------

def test_massive_parametric_financial_calculations():
    """
    Executa cálculos massivos testando mais de 1.000 combinações paramétricas financeiras
    para verificar estabilidade matemática, ausência de falhas e consistência global.
    """
    capex_grid = [1000.0, 5000.0, 20000.0, 100000.0]
    vol_grid = [10.0, 50.0, 200.0, 1000.0]
    tariff_grid = [3.0, 8.0, 15.0]
    reajuste_grid = [0.0, 0.05, 0.12]
    tma_grid = [0.04, 0.10, 0.20]
    period_grid = [5, 15, 30]

    count = 0
    err_count = 0

    for capex in capex_grid:
        for vol in vol_grid:
            for tariff in tariff_grid:
                for reajuste in reajuste_grid:
                    for tma in tma_grid:
                        for period in period_grid:
                            count += 1
                            try:
                                res = run_robust_economic_analysis(
                                    initial_investment=capex,
                                    annual_water_saved_m3=vol,
                                    water_tariff_per_m3=tariff,
                                    sewage_tariff_per_m3=tariff * 0.8,
                                    sewage_mode=1,
                                    water_tariff_escalation_rate=reajuste,
                                    sewage_tariff_escalation_rate=reajuste,
                                    elec_tariff_escalation_rate=reajuste,
                                    inflation_rate=0.04,
                                    discount_rate=tma,
                                    annual_om_cost_base=100.0,
                                    analysis_period_years=period
                                )

                                assert not math.isnan(res.vpl)
                                assert not math.isinf(res.vpl)
                                assert len(res.annual_cash_flows) == period + 1

                            except Exception as e:
                                err_count += 1
                                print(f"Erro no cenário massivo #{count}: {e}")

    assert count >= 1000, f"Deveria ter rodado pelo menos 1.000 cenários (rodou {count})."
    assert err_count == 0, f"Ocorreram {err_count} erros durante os cálculos massivos."


# -----------------------------------------------------------------------------
# 4. TESTE DA ANÁLISE DE SENSIBILIDADE MULTIVARIÁVEL EM MASSA
# -----------------------------------------------------------------------------

def test_massive_sensitivity_analysis_stability():
    """Valida a estabilidade do cálculo da curva teia de sensibilidade em 50 cenários variados."""
    presets = load_presets_from_csv()

    for p in presets:
        base_params = {
            'initial_investment': p['investimento_inicial'],
            'annual_water_saved_m3': p['volume_agua_m3_ano'],
            'water_tariff_per_m3': p['tarifa_agua_m3'],
            'sewage_tariff_per_m3': p['tarifa_esgoto_m3'],
            'sewage_mode': p['modo_esgoto'],
            'water_tariff_escalation_rate': p['reajuste_agua_pct'] / 100.0,
            'sewage_tariff_escalation_rate': p['reajuste_esgoto_pct'] / 100.0,
            'elec_tariff_escalation_rate': p['reajuste_energia_pct'] / 100.0,
            'inflation_rate': p['inflacao_pct'] / 100.0,
            'discount_rate': p['tma_pct'] / 100.0,
            'annual_om_cost_base': p['custo_om_ano'],
            'analysis_period_years': p['periodo_anos']
        }

        sens = run_sensitivity_analysis(base_params, variations_pct=[-30.0, -15.0, 0.0, 15.0, 30.0])
        assert len(sens) == 10, "A análise de sensibilidade deve contemplar 10 parâmetros-chave"

        for param_label, curve in sens.items():
            assert len(curve) == 5, f"Curva para {param_label} deve ter 5 pontos"
            for v_pct, vpl_val in curve:
                assert not math.isnan(vpl_val), f"VPL NaN na sensibilidade de {param_label} ({v_pct}%)"
                assert not math.isinf(vpl_val), f"VPL Inf na sensibilidade de {param_label} ({v_pct}%)"
