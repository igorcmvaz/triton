"""
Testes de verificação introduzidos na versão 5.0.7:
1. Coerência da versão declarada
2. Paybacks simples e descontados calculados com precisão mensal
3. Cloração uniforme do reservatório superior nas varreduras
4. Sincronização e integridade do módulo ambiental
"""

import pytest
import numpy as np
from netuno import __version__
from netuno.core.economic import run_robust_economic_analysis, calculate_economic_indicators
from netuno.core.environmental import (
    EnvironmentalConfig, calculate_lca, run_environmental_sweep
)


def test_versao_declarada_e_coerente():
    """A versao e declarada num lugar so e segue versionamento semantico.

    Fixar o numero exato aqui faria o teste reprovar a cada release, sem
    detectar defeito nenhum. O que se verifica e a forma e a coerencia entre
    netuno/__init__.py e pyproject.toml, que e onde o engano acontece.
    """
    import os
    import re

    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__), __version__

    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    caminho = os.path.join(raiz, "pyproject.toml")
    if not os.path.isfile(caminho):
        pytest.skip("pyproject.toml nao distribuido nesta copia")

    with open(caminho, encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    declarada = re.search(r'^version\s*=\s*"([^"]+)"', conteudo, re.M)
    assert declarada, "pyproject.toml sem declaracao de versao"
    assert declarada.group(1) == __version__, (
        f"pyproject.toml diz {declarada.group(1)}, netuno/__init__.py diz {__version__}"
    )


def test_monthly_precision_payback_simple():
    """Valida se o payback simples é fracionário com precisão mensal."""
    # Investimento: 12.000, Economia líquida: 1.000/mês -> 12.000/ano
    # Payback deve ser exatamente 1.0 ano (12 meses).
    # Com economia de 1.500/mês -> 18.000/ano -> 8 meses -> 0.67 anos
    res = run_robust_economic_analysis(
        initial_investment=12000.0,
        annual_water_saved_m3=1800.0,
        water_tariff_per_m3=10.0,
        sewage_tariff_per_m3=0.0,
        sewage_mode=0,
        water_tariff_escalation_rate=0.0,
        sewage_tariff_escalation_rate=0.0,
        elec_tariff_escalation_rate=0.0,
        inflation_rate=0.0,
        discount_rate=0.0,
        annual_om_cost_base=0.0,
        pump_power_kw=0.0,
        pump_hours_year=0.0,
        elec_tariff_kwh=0.0,
        analysis_period_years=5,
        annual_chlorine_cost=0.0,
    )
    # 18.000/ano = 1.500/mês -> Mês 8 = 12.000
    assert res.payback_simple_years == pytest.approx(8.0 / 12.0, rel=1e-3)
    assert res.payback_discounted_years == pytest.approx(8.0 / 12.0, rel=1e-3)


def test_monthly_precision_payback_discounted():
    """Valida se o payback descontado é calculado mês a mês com taxa de desconto."""
    res = run_robust_economic_analysis(
        initial_investment=10000.0,
        annual_water_saved_m3=1000.0,
        water_tariff_per_m3=5.0,  # 5.000/ano bruto
        sewage_tariff_per_m3=0.0,
        sewage_mode=0,
        water_tariff_escalation_rate=0.0,
        discount_rate=0.10,  # 10% a.a., como fração
        annual_om_cost_base=0.0,
        pump_power_kw=0.0,
        analysis_period_years=10,
    )
    assert res.payback_simple_years == pytest.approx(2.0, rel=1e-2)
    # Payback descontado deve ser maior que o simples devido ao valor do dinheiro no tempo
    assert res.payback_discounted_years is not None
    assert res.payback_discounted_years > res.payback_simple_years
    # Deve ser um valor fracionário não inteiro
    assert res.payback_discounted_years > 2.0


def test_upper_tank_chlorination_uniform_in_environmental_sweep():
    """Valida se a cloração da caixa d'água superior é uniforme entre volumes na varredura ambiental."""
    cfg = EnvironmentalConfig(
        upper_tank_used=True,
        upper_tank_vol_liters=500.0,
        annual_water_saved_m3=120.0,
        chlorine_dose_mg_l=2.0,
        chlorine_co2_kg_per_kg=25.0
    )

    volume_map = [
        (0.0, 0.0),
        (1000.0, 50.0),
        (3000.0, 80.0),
        (5000.0, 100.0),
        (10000.0, 120.0),
    ]

    sw_res = run_environmental_sweep(volume_map, cfg)
    assert len(sw_res.sweep_details) == 5

    # Para V=0 (sem sistema), emissão e massa de cloro são 0
    assert sw_res.sweep_details[0]["lca_result"].annual_chlorine_kg == 0.0
    assert sw_res.sweep_details[0]["lca_result"].annual_treatment_co2_kg == 0.0

    # Para todos os volumes V > 0, massa e emissão de cloro devem ser iguais e uniformes
    cl_masses = [d["lca_result"].annual_chlorine_kg for d in sw_res.sweep_details[1:]]
    cl_co2s = [d["lca_result"].annual_treatment_co2_kg for d in sw_res.sweep_details[1:]]

    # Todos os valores devem ser iguais entre si
    assert len(set(round(m, 4) for m in cl_masses)) == 1
    assert len(set(round(c, 4) for c in cl_co2s)) == 1
    assert cl_masses[0] > 0.0


def test_calculate_lca_without_upper_tank_keeps_chlorination():
    """Sem caixa superior, a cloração continua no inventário: ela acompanha o tratamento."""
    cfg = EnvironmentalConfig(
        upper_tank_used=False,
        chlorine_dose_mg_l=2.0,
        chlorine_co2_kg_per_kg=25.0
    )
    lca = calculate_lca(5000.0, 100.0, cfg)
    assert lca.annual_chlorine_kg > 0.0
    assert lca.annual_treatment_co2_kg > 0.0
