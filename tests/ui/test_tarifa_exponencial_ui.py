"""A fórmula exponencial da CORSAN nas duas telas que editam tarifa.

O cálculo é testado em `tests/unit/test_tarifa_exponencial.py`; aqui, que o Gestor
de Tarifas e a etapa econômica mostram, simulam e preservam a tabela exponencial.
"""

from netuno.core.tariffs_structure import EXPOENTE_DE_CONSUMO, PRECO_BASE_EXPONENCIAL

TABELA = [
    (0.0, 0.0, 43.39, -1),
    (0.0, 1000.0, 9.15, PRECO_BASE_EXPONENCIAL),
    (0.0, 10.0, 1.00, EXPOENTE_DE_CONSUMO),
    (10.0, 20.0, 1.05, EXPOENTE_DE_CONSUMO),
    (20.0, 1000.0, 1.10, EXPOENTE_DE_CONSUMO),
    (1000.0, 999999.0, 9.15, 1),
]


def test_o_gestor_mostra_a_formula_e_simula_com_o_motor(qapp):
    from netuno.ui.tab_tariffs_manager import TabTariffsManager

    tab = TabTariffsManager()
    tab.load_city_tariffs("RS", "Alegrete", "residencial")
    assert "Fórmula exponencial" in tab.lbl_disp_callout.text()
    tipos = [tab.table_tiers.item(r, 3).text() for r in range(tab.table_tiers.rowCount())]
    assert "Preço-base (PB × Cⁿ)" in tipos and "Expoente n" in tipos

    # Editar o expoente muda a conta simulada, pela fórmula.
    linha = tipos.index("Expoente n")
    tab.table_tiers.item(linha, 2).setText("1.1000")
    tab.spin_sim_vol.setValue(15.0)
    tab.update_bill_simulation()
    esperado = (43.39 + 9.15 * 15 ** 1.1) * 1.70
    assert f"Total: R$ {esperado:.2f}/mês" in tab.lbl_sim_result.text()
    assert "PB × Cⁿ" in tab.lbl_sim_result.text()
    assert tab._faixas_da_tabela()[linha] == [0.0, 1000.0, 1.1, EXPOENTE_DE_CONSUMO]


def test_a_etapa_economica_preserva_a_tabela_exponencial(qapp):
    from netuno.core.parser import NetunoConfig
    from netuno.ui.dialogs.dialog_economic import DialogTariffs

    cfg = NetunoConfig()
    cfg.water_tariffs = list(TABELA)
    dialogo = DialogTariffs(config=cfg)
    dialogo.populate_table_from_tariffs(TABELA)
    dialogo.on_accept()
    assert cfg.water_tariffs == TABELA
