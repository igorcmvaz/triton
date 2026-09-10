"""
Testes unitários para o módulo core de Análise do Ciclo de Vida (netuno.core.environmental).
"""

import pytest
from netuno.core.environmental import (
    EnvironmentalConfig, PipeInput, PumpInput, calculate_lca, run_environmental_sweep,
    MATERIAL_PRESETS, PIPE_EMISSION_FACTORS_PER_METER, PUMP_EMBEDDED_CO2,
)
from netuno.core.chlorination import Cloracao


def test_calculate_lca_basic():
    config = EnvironmentalConfig(
        lower_material_key="PEAD",
        upper_tank_used=False,
        pipes=[
            PipeInput(diameter_mm=100, length_m=10.0),
        ],
        pump=PumpInput(power_cv=0.50, specific_kwh_per_m3=0.40), # 18 kg CO2e
        system_lifespan_years=20.0,
        grid_co2_factor_kg_kwh=0.085,
        potable_water_co2_kg_m3=0.35,
        chemical_treatment_co2_m3=0.0
    )
    # 5,000 L reservoir (5 m³), saves 100 m³/year pluvial
    res = calculate_lca(5000.0, 100.0, config)

    # Os fatores de emissão vêm de fontes datadas e mudam quando a fonte muda
    # (o do PEAD passou de 3,00 para 1,612 ao ser substituído pelo valor do
    # relatório do American Chemistry Council). Repeti-los aqui como constantes
    # transformaria cada atualização de fonte numa falsa reprovação. O que se
    # verifica é a composição — massa × fator, soma das parcelas —, não o número.
    preset_pead = MATERIAL_PRESETS["PEAD"]
    co2_tubo_por_m = PIPE_EMISSION_FACTORS_PER_METER[100]

    assert res.lower_tank_mass_kg == pytest.approx(5.0 * preset_pead.material_density_kg_per_m3_tank)
    assert res.total_pipes_co2_kg == pytest.approx(10.0 * co2_tubo_por_m)
    # O carbono da motobomba acompanha a QUANTIDADE de bombas do projeto, que
    # por padrao e principal mais reserva. Congelar uma bomba aqui escondia que
    # este padrao divergia do de `NetunoConfig`, onde sempre foram duas.
    assert res.pump_embodied_co2_kg == pytest.approx(
        PUMP_EMBEDDED_CO2[0.50] * config.pump_count
    )

    co2_cisterna = res.lower_tank_mass_kg * preset_pead.co2_factor_kg_per_kg
    assert res.total_embodied_co2_kg == pytest.approx(
        co2_cisterna + res.total_pipes_co2_kg + res.pump_embodied_co2_kg
    )

    # Pumping: 100 m³ * 0.40 kWh/m³ * 0.085 kg CO2/kWh = 3.4 kg CO2e / yr
    assert res.annual_pumping_co2_kg == pytest.approx(3.4)

    # Avoided: 100 m³ * 0.35 kg CO2/m³ = 35.0 kg CO2e / yr
    assert res.annual_avoided_co2_kg == pytest.approx(35.0)

    # Net annual avoided = 35.0 - 3.4 = 31.6 kg CO2e / yr
    assert res.net_annual_avoided_co2_kg == pytest.approx(31.6)

    # Payback ambiental = CO2 incorporado / saldo anual evitado.
    assert res.environmental_payback_years == pytest.approx(
        res.total_embodied_co2_kg / res.net_annual_avoided_co2_kg, abs=0.01
    )

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
    """A massa reportada e de PRODUTO comercial, nao de cloro ativo.

    A distincao nao e cosmetica. A dose e prescrita em mg de cloro ativo por
    litro, mas o que se compra, se transporta e se fabrica e a pastilha, que tem
    65% de cloro ativo. Somar uma dose de cloro ativo a um fator de emissao por
    kg de pastilha subestima em 35%, e era metade da divergencia de 11,7x que
    existia entre o modulo ambiental e o de qualidade.
    """
    config = EnvironmentalConfig(
        upper_tank_used=True,
        pipes=[],
        chlorine_dose_mg_l=2.0,
    )
    result = calculate_lca(5000.0, 100.0, config)

    cloracao = Cloracao(
        dose_mg_por_litro=2.0,
        pureza=config.chlorine_product_purity,
        fator_kg_co2e_por_kg_produto=config.chlorine_co2_kg_per_kg,
    )

    # 100 m3/ano com 2 mg/L dao 0,2 kg de cloro ATIVO; a 65% de pureza, isso
    # exige 0,3077 kg de pastilha.
    assert cloracao.cloro_ativo_kg_por_m3 * 100 == pytest.approx(0.2)
    assert result.annual_chlorine_kg == pytest.approx(0.2 / config.chlorine_product_purity)

    assert result.treatment_co2_kg_per_m3 == pytest.approx(cloracao.co2e_kg_por_m3)
    assert result.annual_treatment_co2_kg == pytest.approx(cloracao.co2e_anual_kg(100.0))


def test_fator_do_cloro_deixou_de_ser_o_custo():
    """Guarda contra o retorno do 25,0.

    O valor 25,0 kg CO2e/kg vinha sem fonte e era identico ao
    `chlorine_cost_per_kg = 25.00` (R$/kg) do costs_database.json. Cloro de rota
    cloro-alcali fica entre 1 e 2 kg CO2e/kg; 25 e implausivel por uma ordem de
    grandeza, e a coincidencia com o preco denuncia a origem do engano.
    """
    config = EnvironmentalConfig()
    assert config.chlorine_co2_kg_per_kg < 5.0, (
        "fator de emissao do cloro implausivel - conferir se nao e o custo em R$/kg"
    )


def test_os_modulos_ambiental_e_de_qualidade_concordam_no_cloro():
    """Os dois usavam bases diferentes e divergiam por 11,7x."""
    from netuno.core.chlorination import (
        FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
        PUREZA_PADRAO,
    )

    config = EnvironmentalConfig()
    assert config.chlorine_co2_kg_per_kg == FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    assert config.chlorine_product_purity == PUREZA_PADRAO


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


def test_a_contagem_de_bombas_e_a_mesma_no_projeto_e_na_acv():
    """Os dois padrões divergiam, e ninguém via.

    `NetunoConfig.pump_count` sempre foi 2 — principal mais reserva, a
    configuração inicial recomendada — e o módulo econômico cobra as duas
    (`pump_unit_cost × pump_count`). `EnvironmentalConfig.pump_count` era 1, de
    modo que a avaliação de ciclo de vida contava o carbono de uma bomba só,
    18 kg CO₂e a menos, para o mesmo sistema que o econômico orçava com duas.

    A divergência só aparecia quando a configuração ambiental era construída sem
    o projeto — geração de relatório e alguns caminhos de otimização.
    """
    from netuno.core.environmental import EnvironmentalConfig
    from netuno.core.parser import NetunoConfig

    assert EnvironmentalConfig().pump_count == NetunoConfig().pump_count


def test_o_carbono_da_bomba_dobra_com_a_bomba_reserva():
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca

    uma = calculate_lca(5000.0, 100.0, EnvironmentalConfig(annual_water_saved_m3=100.0, pump_count=1))
    duas = calculate_lca(5000.0, 100.0, EnvironmentalConfig(annual_water_saved_m3=100.0, pump_count=2))
    assert duas.pump_embodied_co2_kg == pytest.approx(2 * uma.pump_embodied_co2_kg)
    assert duas.total_embodied_co2_kg > uma.total_embodied_co2_kg
