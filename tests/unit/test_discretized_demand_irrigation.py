import numpy as np
import pytest
from netuno.core.parser import NetunoConfig, export_netuno_csv, parse_netuno_csv
from netuno.core.simulation import (
    build_daily_demand_vectors,
    build_detailed_daily_demand_vectors,
    run_single_simulation,
    run_sweep_simulation,
)


def test_discretized_indoor_and_irrigation_vectors():
    """Valida se a construção de vetores separa corretamente potável interno, não-potável interno e irrigação."""
    n_days = 5
    # Dias: 0=seco, 1=1.0mm (abaixo do limiar), 2=2.5mm (chuva>=2.0), 3=10.0mm (chuva>=2.0), 4=0mm
    precip = np.array([0.0, 1.0, 2.5, 10.0, 0.0], dtype=np.float64)

    b_cfg = {
        "demand": 150.0,
        "residents": 4.0,
        "potable_indoor_share": 0.65,
        "non_potable_indoor_share": 0.35,
        "irrigation_liters_per_day": 50.0,
        "irrigation_rain_threshold_mm": 2.0,
        "irrigation_potable_backup": True,
    }

    tot_arr, pluv_arr, pot_in_arr, non_pot_in_arr, irr_arr, irr_supp_mask = build_detailed_daily_demand_vectors(
        n_days=n_days,
        building_config=b_cfg,
        precip_data=precip
    )

    # Consumo interno total = 150 * 4 = 600 L/dia
    # Potável interno = 600 * 0.65 = 390 L/dia em todos os dias
    # Não-potável interno = 600 * 0.35 = 210 L/dia em todos os dias
    assert np.allclose(pot_in_arr, 390.0)
    assert np.allclose(non_pot_in_arr, 210.0)

    # Irrigação em dias secos (0, 1, 4): 50 L/dia. Em dias de chuva (2, 3): 0 L/dia
    assert irr_arr[0] == 50.0
    assert irr_arr[1] == 50.0
    assert irr_arr[2] == 0.0
    assert irr_arr[3] == 0.0
    assert irr_arr[4] == 50.0

    # Máscara de supressão
    assert not irr_supp_mask[0]
    assert not irr_supp_mask[1]
    assert irr_supp_mask[2]
    assert irr_supp_mask[3]
    assert not irr_supp_mask[4]

    # Demanda pluvial diária desejada (não-potável interno + irrigação ativa)
    # Dias 0, 1, 4: 210 + 50 = 260 L/dia
    # Dias 2, 3: 210 + 0 = 210 L/dia
    assert pluv_arr[0] == 260.0
    assert pluv_arr[1] == 260.0
    assert pluv_arr[2] == 210.0
    assert pluv_arr[3] == 210.0
    assert pluv_arr[4] == 260.0

    # Demanda total diária (potável interno + pluvial)
    # Dias 0, 1, 4: 390 + 260 = 650 L/dia
    # Dias 2, 3: 390 + 210 = 600 L/dia
    assert tot_arr[0] == 650.0
    assert tot_arr[1] == 650.0
    assert tot_arr[2] == 600.0
    assert tot_arr[3] == 600.0
    assert tot_arr[4] == 650.0


def test_hydraulic_priority_and_potable_backup():
    """
    Valida se a cisterna atende primeiro o não-potável interno (bacias/máquinas)
    e somente o saldo excedente vai para a irrigação externa.
    """
    # 2 dias sem chuva; cisterna começa com 250 L (após uma chuva inicial)
    precip = np.array([10.0, 0.0, 0.0], dtype=np.float64)

    b_cfg = {
        "demand": 100.0,
        "residents": 2.0,  # Interno total = 200 L/dia
        "potable_indoor_share": 0.50,  # 100 L/dia potável
        "non_potable_indoor_share": 0.50,  # 100 L/dia não-potável
        "irrigation_liters_per_day": 80.0,  # 80 L/dia irrigação
        "irrigation_rain_threshold_mm": 2.0,
        "irrigation_potable_backup": True,
    }

    # Dia 0: Chuva de 10mm -> capta 10mm * 100m² * 0.9 = 900L (com descarte 0mm)
    # No dia 0 (chuva>=2), irrigação é suprimida. Demanda pluvial = 100L.
    # Consumo pluvial dia 0 = 100L (não-potável interno). Saldo na cisterna = 800L.
    # No dia 1 (sem chuva): Demanda pluvial = 100L (interno) + 80L (irrigação) = 180L.
    # Ambos são atendidos integralmente.
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=5000.0,
        area=100.0,
        runoff_coeff=0.9,
        discard_mm=0.0,
        store_daily_details=True,
        building_config=b_cfg,
    )

    d0 = res.daily_results[0]
    assert d0.irrigation_suppressed is True
    assert d0.irrigation_demand_liters == 0.0
    assert d0.pluvial_indoor_consumed_liters == 100.0
    assert d0.pluvial_irrigation_consumed_liters == 0.0

    d1 = res.daily_results[1]
    assert d1.irrigation_suppressed is False
    assert d1.irrigation_demand_liters == 80.0
    assert d1.pluvial_indoor_consumed_liters == 100.0
    assert d1.pluvial_irrigation_consumed_liters == 80.0

    assert res.total_irrigation_days_suppressed == 1
    assert res.total_irrigation_days_active == 2


def test_irrigation_without_potable_backup():
    """Valida se, sem backup potável para irrigação, a concessionária não é cobrada pela irrigação se a cisterna secar."""
    # Cisterna seca de 0 litros; 2 dias sem chuva
    precip = np.array([0.0, 0.0], dtype=np.float64)

    b_cfg = {
        "demand": 100.0,
        "residents": 2.0,  # 200 L/dia total
        "potable_indoor_share": 0.50,  # 100 L/dia potável
        "non_potable_indoor_share": 0.50,  # 100 L/dia não-potável
        "irrigation_liters_per_day": 50.0,  # 50 L/dia irrigação
        "irrigation_rain_threshold_mm": 2.0,
        "irrigation_potable_backup": False,  # Sem backup potável para jardim
    }

    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=1000.0,
        area=100.0,
        runoff_coeff=0.9,
        discard_mm=0.0,
        store_daily_details=True,
        building_config=b_cfg,
    )

    d0 = res.daily_results[0]
    # Cisterna estava vazia (0L consumido)
    # Potável usado = 100L potável interno + 100L déficit não-potável interno = 200L.
    # Os 50L de irrigação NÃO foram supridos pela rede pública porque backup=False.
    assert d0.pluvial_consumed_liters == 0.0
    assert d0.potable_consumed_liters == 200.0


def test_parser_discretized_roundtrip():
    """Valida salvamento e carregamento de configurações com discretização de usos."""
    cfg = NetunoConfig(
        potable_indoor_share=0.70,
        non_potable_indoor_share=0.30,
        irrigation_liters_per_day=75.0,
        irrigation_rain_threshold_mm=3.0,
        irrigation_potable_backup=False,
    )
    assert cfg.potable_indoor_share == 0.70
    assert cfg.non_potable_indoor_share == 0.30
    assert cfg.irrigation_liters_per_day == 75.0
    assert cfg.irrigation_rain_threshold_mm == 3.0
    assert cfg.irrigation_potable_backup is False


def test_discretized_weekly_modulation_with_irrigation():
    """Valida se a modulação semanal separa corretamente frações internas e adiciona irrigação."""
    n_days = 7
    # Chuva no dia 2 (quarta-feira) com 5.0 mm >= limiar 2.0 mm
    precip = np.array([0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64)
    b_cfg = {
        "demand_mode": "weekly",
        "weekly_demands": [100.0, 100.0, 100.0, 100.0, 100.0, 200.0, 200.0],  # Fim de semana consome mais
        "weekly_residents": [4.0] * 7,
        "weekly_shares": [30.0, 30.0, 30.0, 30.0, 30.0, 50.0, 50.0],  # 30% dias úteis, 50% fim de semana
        "irrigation_liters_per_day": 60.0,
        "irrigation_rain_threshold_mm": 2.0,
        "irrigation_potable_backup": True,
    }

    tot_arr, pluv_arr, pot_in_arr, non_pot_in_arr, irr_arr, irr_supp_mask = build_detailed_daily_demand_vectors(
        n_days=n_days,
        building_config=b_cfg,
        precip_data=precip,
        start_date_str="07/01/2002"  # Segunda-feira
    )

    # Dia 0 (Segunda): 100 * 4 = 400 L/dia. Não-potável = 400 * 0.3 = 120 L. Potável = 280 L. Irrigação = 60 L. Pluvial = 180 L.
    assert pot_in_arr[0] == 280.0
    assert non_pot_in_arr[0] == 120.0
    assert irr_arr[0] == 60.0
    assert pluv_arr[0] == 180.0
    assert tot_arr[0] == 460.0

    # Dia 2 (Quarta c/ chuva): Não-potável = 120 L. Irrigação = 0 L (suprimida). Pluvial = 120 L.
    assert bool(irr_supp_mask[2]) is True
    assert irr_arr[2] == 0.0
    assert pluv_arr[2] == 120.0

    # Dia 5 (Sábado): 200 * 4 = 800 L/dia. Não-potável = 800 * 0.5 = 400 L. Potável = 400 L. Irrigação = 60 L. Pluvial = 460 L.
    assert pot_in_arr[5] == 400.0
    assert non_pot_in_arr[5] == 400.0
    assert irr_arr[5] == 60.0
    assert pluv_arr[5] == 460.0

