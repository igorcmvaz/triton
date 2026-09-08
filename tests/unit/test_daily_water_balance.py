"""
Testes unitários e de integração estruturados utilizando InputRainfall, InputData e Output.
Permite validação diária (balanço hídrico iteração a iteração).
"""

import pytest
from netuno.core.test_framework import (
    InputRainfall,
    InputData,
    Output,
    WaterBalanceTestCase
)


def test_simple_3day_water_balance():
    """
    Exemplo Didático de Balanço Hídrico de 3 dias:
    - Área: 100 m², Coeficiente C: 1.0, Descarte: 0.0 mm
    - Moradores: 4, Demanda per capita: 100 L/hab/dia -> Demanda Total = 400 L/dia
    - Substituição pluvial: 50% -> Demanda Pluvial = 200 L/dia
    - Reservatório inferior: 500 L (inicia vazio = 0 L)
    
    Chuva:
    - Dia 1: 5.0 mm -> Captação = 5 * 100 * 1.0 = 500 L
      - Reservatório recebe 500 L. Consumo pluvial = 200 L. Reservatório final = 300 L.
      - Atendimento: TOTAL (200 L).
    - Dia 2: 0.0 mm -> Captação = 0 L
      - Reservatório inicial = 300 L. Consumo pluvial = 200 L. Reservatório final = 100 L.
      - Atendimento: TOTAL (200 L).
    - Dia 3: 0.0 mm -> Captação = 0 L
      - Reservatório inicial = 100 L. Consumo pluvial = 100 L (limite do reservatório). Reservatório final = 0 L.
      - Atendimento: PARCIAL (100 L).
    """
    test_case = WaterBalanceTestCase(
        test_id="TEST_3DAY_SIMPLE",
        name="Teste Didático 3 Dias",
        input_rainfall=InputRainfall(rainfall_mm=[5.0, 0.0, 0.0]),
        input_data=InputData(
            area=100.0,
            runoff_coeff=1.0,
            discard_mm=0.0,
            residents=4,
            demand_per_capita=100.0,
            rainwater_share=0.5,
            lower_tank_vol=500.0
        )
    )
    
    out = test_case.run()
    
    # Verificação Dia 1
    d1 = out.daily_details[0]
    assert d1.precip_mm == 5.0
    assert d1.harvested_liters == 500.0
    assert d1.pluvial_consumed_liters == 200.0
    assert d1.potable_consumed_liters == 200.0
    assert d1.lower_tank_end_liters == 300.0
    assert d1.satisfaction_type == "TOTAL"

    # Verificação Dia 2
    d2 = out.daily_details[1]
    assert d2.precip_mm == 0.0
    assert d2.harvested_liters == 0.0
    assert d2.pluvial_consumed_liters == 200.0
    assert d2.potable_consumed_liters == 200.0
    assert d2.lower_tank_end_liters == 100.0
    assert d2.satisfaction_type == "TOTAL"

    # Verificação Dia 3
    d3 = out.daily_details[2]
    assert d3.precip_mm == 0.0
    assert d3.harvested_liters == 0.0
    assert d3.pluvial_consumed_liters == 100.0
    assert d3.potable_consumed_liters == 300.0
    assert d3.lower_tank_end_liters == 0.0
    assert d3.satisfaction_type == "PARCIAL"

    # Totais e Médias:
    # Consumo pluvial total = 200 + 200 + 100 = 500 L em 3 dias -> Média = 166.6667 L/dia
    # Demanda total = 400 * 3 = 1200 L -> Potencial = 500 / 1200 = 41.6667%
    assert abs(out.potential_savings_pct - 41.6667) < 0.01
    assert abs(out.avg_pluvial_consumed_l_day - 166.6667) < 0.01
    assert abs(out.pct_days_full_satisfaction - 66.6667) < 0.01  # 2/3 dias
    assert abs(out.pct_days_partial_satisfaction - 33.3333) < 0.01 # 1/3 dias
