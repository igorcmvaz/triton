"""
Testes unitários para o módulo core de Análise do Ciclo de Vida (netuno.core.environmental).
"""

import pytest
from netuno.core.environmental import (
    EnvironmentalConfig, PipeInput, PumpInput, calculate_lca, run_environmental_sweep, MATERIAL_PRESETS
)


def test_calculate_lca_basic():
    config = EnvironmentalConfig(
        lower_material_key="PEAD",
        upper_tank_used=False,
        pipes=[
            PipeInput(diameter_mm=100, length_m=10.0), # 10m * 3.92 kg CO2/m = 39.2 kg CO2e
        ],
        pump=PumpInput(power_cv=0.50, specific_kwh_per_m3=0.40), # 18 kg CO2e
        system_lifespan_years=20.0,
        grid_co2_factor_kg_kwh=0.085,
        potable_water_co2_kg_m3=0.35,
        chemical_treatment_co2_m3=0.0
    )
    # 5,000 L reservoir (5 m³), saves 100 m³/year pluvial
    res = calculate_lca(5000.0, 100.0, config)

    # 5 m³ * 22 kg/m³ = 110 kg PEAD * 3.0 kg CO2e/kg = 330 kg CO2e cisterna
    assert res.lower_tank_mass_kg == pytest.approx(110.0)
    assert res.total_pipes_co2_kg == pytest.approx(39.2)
    assert res.pump_embodied_co2_kg == pytest.approx(18.0)
    # Total embodied = 330 + 39.2 + 18.0 = 387.2 kg CO2e
    assert res.total_embodied_co2_kg == pytest.approx(387.2)

    # Pumping: 100 m³ * 0.40 kWh/m³ * 0.085 kg CO2/kWh = 3.4 kg CO2e / yr
    assert res.annual_pumping_co2_kg == pytest.approx(3.4)

    # Avoided: 100 m³ * 0.35 kg CO2/m³ = 35.0 kg CO2e / yr
    assert res.annual_avoided_co2_kg == pytest.approx(35.0)

    # Net annual avoided = 35.0 - 3.4 = 31.6 kg CO2e / yr
    assert res.net_annual_avoided_co2_kg == pytest.approx(31.6)

    # Payback = 387.2 / 31.6 = ~12.253 years
    assert res.environmental_payback_years == pytest.approx(387.2 / 31.6, abs=0.01)

    # Inventory items should contain expected breakdown
    assert len(res.inventory_items) >= 4
    assert res.is_environmentally_viable is True


def test_materials_comparison():
    config_pead = EnvironmentalConfig(lower_material_key="PEAD")
    config_conc = EnvironmentalConfig(lower_material_key="CONCRETO")

    lca_pead = calculate_lca(10000.0, 200.0, config_pead)
    lca_conc = calculate_lca(10000.0, 200.0, config_conc)

    # Concrete should have a higher embodied carbon footprint than PEAD
    assert lca_conc.total_embodied_co2_kg > lca_pead.total_embodied_co2_kg
    assert lca_pead.environmental_payback_years < lca_conc.environmental_payback_years


def test_prfv_alias_uses_fiberglass_preset_and_zero_is_no_system_baseline():
    alias = calculate_lca(5000.0, 100.0, EnvironmentalConfig(lower_material_key="PRFV"))
    canonical = calculate_lca(5000.0, 100.0, EnvironmentalConfig(lower_material_key="FIBRA"))
    assert alias.lower_tank_mass_kg == pytest.approx(canonical.lower_tank_mass_kg)
    assert alias.total_embodied_co2_kg == pytest.approx(canonical.total_embodied_co2_kg)

    baseline = calculate_lca(0.0, 0.0, EnvironmentalConfig())
    assert baseline.total_embodied_co2_kg == pytest.approx(0.0)
    assert baseline.lifetime_net_co2_saved_kg == pytest.approx(0.0)


def test_chlorine_mass_and_emissions_are_calculated_from_dose():
    config = EnvironmentalConfig(
        upper_tank_used=True,
        pipes=[],
        chlorine_dose_mg_l=2.0,
        chlorine_co2_kg_per_kg=25.0,
    )
    result = calculate_lca(5000.0, 100.0, config)

    # 100 m³/ano = 100.000 L/ano; 2 mg/L = 0,2 kg Cl2/ano.
    assert result.annual_chlorine_kg == pytest.approx(0.2)
    assert result.treatment_co2_kg_per_m3 == pytest.approx(0.05)
    assert result.annual_treatment_co2_kg == pytest.approx(5.0)
    chlorine_item = next(item for item in result.inventory_items if "Dosagem Qu" in item.category)
    assert "0.200 kg Cl2/ano" in chlorine_item.quantity_str


def test_environmental_sweep():
    sweep_map = [
        (1000.0, 50.0),
        (2000.0, 80.0),
        (5000.0, 120.0),
        (10000.0, 140.0),
        (20000.0, 150.0),
    ]
    config = EnvironmentalConfig(lower_material_key="PEAD")
    res = run_environmental_sweep(sweep_map, config)

    assert res.best_lifetime_co2_vol_liters > 0
    assert len(res.sweep_details) == 5
    assert res.min_payback_years < 999.0


def test_environmental_sweep_uses_pump_energy_of_each_volume():
    config = EnvironmentalConfig(
        lower_material_key="PEAD",
        grid_co2_factor_kg_kwh=1.0,
        chlorine_dose_mg_l=0.0,
    )
    result = run_environmental_sweep([
        (1000.0, 100.0, 10.0),
        (2000.0, 100.0, 30.0),
    ], config)
    assert result.sweep_details[0]["lca_result"].annual_pumping_co2_kg == pytest.approx(10.0)
    assert result.sweep_details[1]["lca_result"].annual_pumping_co2_kg == pytest.approx(30.0)


def test_tab_environmental_charts_dynamic_sizing(qapp):
    from netuno.ui.tab_environmental import TabEnvironmental
    tab = TabEnvironmental()

    # Inicialmente na aba 0 (Otimização de volume): altura máxima confortável <= 530px
    assert tab.tab_charts_env.maximumHeight() <= 530

    # Mudança para aba 1 (Balanço acumulado): permanece confortável <= 530px
    tab.tab_charts_env.setCurrentIndex(1)
    assert tab.tab_charts_env.maximumHeight() <= 530

    # Mudança para aba 2 (Certificações ESG): expande para acomodar cards, matriz e texto
    tab.tab_charts_env.setCurrentIndex(2)
    assert tab.tab_charts_env.maximumHeight() > 10000
    assert tab.tab_charts_env.minimumHeight() >= 650

    # Retorno para aba 0: encolhe novamente para a altura das abas de gráficos
    tab.tab_charts_env.setCurrentIndex(0)
    assert tab.tab_charts_env.maximumHeight() <= 530
