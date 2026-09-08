from netuno.ui.tab_economic_global_optimizer import TabEconomicGlobalOptimizer


def test_selector_exposes_smaa_vikor_as_one_method_with_simulation_profiles(qapp):
    tab = TabEconomicGlobalOptimizer()

    methods = [tab.combo_mcdm_method.itemData(i) for i in range(tab.combo_mcdm_method.count())]
    assert methods == ["topsis", "smaa_vikor"]

    # Alterna para SMAA-VIKOR
    tab.combo_mcdm_method.setCurrentIndex(1)
    assert tab.combo_smaa_profile.isVisibleTo(tab)
    assert not tab.combo_preset.isVisibleTo(tab)
    assert tab.lbl_profile.text() == "Perfil de simulações:"
    assert tab.combo_smaa_profile.currentData() == 20000
    assert "20.000 simulações" in tab.lbl_weight_validation.text()
    assert "VIKOR v=0.50" in tab.lbl_weight_validation.text()
    assert not tab.spin_w_tech.isVisibleTo(tab)
    assert tab.spin_v_param.isVisibleTo(tab)

    profiles = [tab.combo_smaa_profile.itemData(i) for i in range(tab.combo_smaa_profile.count())]
    assert profiles == [1000, 5000, 10000, 20000, 50000, "custom"]

    # Testa seleção de perfil personalizado
    tab.combo_smaa_profile.setCurrentIndex(tab.combo_smaa_profile.findData("custom"))
    assert tab.spin_smaa_custom_samples.isVisibleTo(tab)
    tab.spin_smaa_custom_samples.setValue(12500)
    assert tab.get_smaa_num_simulations() == 12500
    assert "12.500 simulações" in tab.lbl_weight_validation.text()

    # Testa ajuste do parâmetro v do VIKOR
    tab.spin_v_param.setValue(0.75)
    assert tab.get_vikor_v_param() == 0.75
    assert "VIKOR v=0.75" in tab.lbl_weight_validation.text()

    # Volta para TOPSIS
    tab.combo_mcdm_method.setCurrentIndex(0)
    assert not tab.combo_smaa_profile.isVisibleTo(tab)
    assert tab.combo_preset.isVisibleTo(tab)
    assert tab.lbl_profile.text() == "Perfil de decisão:"
    assert tab.spin_w_tech.isVisibleTo(tab)
    assert not tab.spin_v_param.isVisibleTo(tab)

    tab.close()


def test_vikor_chart_ylim_multiple_of_20_superior_to_max(qapp):
    from unittest.mock import MagicMock
    from netuno.ui.charts import TOPSISComparisonChart

    chart = TOPSISComparisonChart()
    res = MagicMock()
    res.candidates = [MagicMock(lower_tank_vol=1000 * i) for i in range(1, 6)]
    res.best_index = 2
    res.num_simulations = 1000

    # Caso 1: maior valor é 35.0% -> múltiplo imediatamente superior é 40.0
    res.first_rank_acceptabilities = [0.05, 0.12, 0.35, 0.22, 0.08]
    chart.update_chart(smaa_result=res, method="smaa_vikor")
    ax = chart.figure.axes[0]
    assert ax.get_ylim() == (0.0, 40.0)

    # Caso 2: maior valor é 40.0% -> múltiplo estritamente superior é 60.0
    res.first_rank_acceptabilities = [0.05, 0.10, 0.40, 0.20, 0.05]
    chart.update_chart(smaa_result=res, method="smaa_vikor")
    ax = chart.figure.axes[0]
    assert ax.get_ylim() == (0.0, 60.0)

    # Caso 3: maior valor é 57.7% -> múltiplo imediatamente superior é 60.0
    res.first_rank_acceptabilities = [0.10, 0.577, 0.20, 0.05, 0.0]
    chart.update_chart(smaa_result=res, method="smaa_vikor")
    ax = chart.figure.axes[0]
    assert ax.get_ylim() == (0.0, 60.0)

    # Caso 4: maior valor é 100.0% -> múltiplo estritamente superior é 120.0
    res.first_rank_acceptabilities = [0.0, 0.0, 1.0, 0.0, 0.0]
    chart.update_chart(smaa_result=res, method="smaa_vikor")
    ax = chart.figure.axes[0]
    assert ax.get_ylim() == (0.0, 120.0)

