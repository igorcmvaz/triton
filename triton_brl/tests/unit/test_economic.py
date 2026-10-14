"""
Suíte Completa de Testes de Validação do Motor Econômico do Triton.
Testa:
1. Tarifas de água em faixas (fixas e variáveis) + Esgoto (percentual e fixo) + Impostos
2. Consumo elétrico da motobomba (Potência, Rendimento, Vazão, Partida, Tarifas de Energia, Reserva)
3. Outros custos operacionais (Linhares, Angulares, Periodicidades)
4. Balanço de Fluxo de Caixa Mensal, Inflação, TMA, VPL, TIR e Payback Descontado
5. Cenários desfavoráveis (VPL Negativo e Payback Inexistente)
"""

import pytest

from triton.core.parser import TritonConfig

from triton.core.economic import calculate_water_bill, run_economic_analysis


def test_casan_residential_2026_tariff_example():
    """Confere TFDI, faixas residenciais e esgoto de 100% da CASAN."""
    tariffs = TritonConfig().water_tariffs

    # Água: 46,34 + (5 × 3,08) = 61,74. Esgoto é 100% da tarifa de água.
    assert calculate_water_bill(5000.0, tariffs, sewage_mode=1, sewage_rate=100.0) == pytest.approx(123.48)

    # Água: 46,34 + (10 × 3,08) + (5 × 14,31) = 148,69; com esgoto, 297,38.
    assert calculate_water_bill(15000.0, tariffs, sewage_mode=1, sewage_rate=100.0) == pytest.approx(297.38)


def test_americana_residential_minimum_franchise_tariff():
    """Valida a cobrança com franquia mínima não-cumulativa de Americana (DAE Americana / ARES-PCJ).
    - Até 6 m³: R$ 14,30 fixo de água + 100% esgoto = R$ 28,60 total.
    - 25 m³ (> 6 m³): 25 m³ × R$ 3,49 = R$ 87,25 de água + 100% esgoto = R$ 174,50 total.
    """
    tariffs = [
        (0.0, 6.0, 14.30, -2),
        (6.0, 999999.0, 3.49, 1)
    ]
    # Consumo de 0 m³
    bill_0m3 = calculate_water_bill(0.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_0m3 == pytest.approx(28.60, abs=0.01)

    # Consumo de 4 m³ (dentro do consumo mínimo)
    bill_4m3 = calculate_water_bill(4000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_4m3 == pytest.approx(28.60, abs=0.01)

    # Consumo de 6 m³ (dentro do consumo mínimo)
    bill_6m3 = calculate_water_bill(6000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_6m3 == pytest.approx(28.60, abs=0.01)

    # Consumo de 25 m³ (excede franquia, recalculado desde 0 pelo valor de R$ 3,49/m³)
    bill_25m3 = calculate_water_bill(25000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_25m3 == pytest.approx(174.50, abs=0.01)
