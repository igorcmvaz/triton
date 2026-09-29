"""
Testes unitários para o assistente de dimensionamento de motobomba e tubulações (Forchheimer).
"""

import pytest
from netuno.ui.dialogs.pump_wizard_dialog import (
    calculate_forchheimer_diameter,
    find_commercial_recalque,
    get_suction_pipe,
    COMMERCIAL_PIPES,
    PUMP_CATALOG,
)


def test_forchheimer_calculation():
    # Vazão de 3.6 m³/h = 0.001 m³/s, operando 2 horas por dia
    q_m3s = 3.6 / 3600.0
    t_h = 2.0
    d_m = calculate_forchheimer_diameter(q_m3s, t_h)
    d_mm = d_m * 1000.0

    # D = 1.3 * (2/24)^0.25 * sqrt(0.001) ~ 0.0221 m = 22.1 mm
    assert 15.0 <= d_mm <= 35.0

    # Seleção de diâmetro comercial
    rec_pipe = find_commercial_recalque(d_m)
    assert rec_pipe["dn"] in [25, 32, 40]
    assert rec_pipe["di_mm"] >= (d_mm * 0.90)


def test_suction_pipe_one_size_above():
    for i in range(len(COMMERCIAL_PIPES) - 1):
        rec_pipe = COMMERCIAL_PIPES[i]
        suc_pipe = get_suction_pipe(rec_pipe)
        expected_suc = COMMERCIAL_PIPES[i + 1]
        assert suc_pipe["dn"] == expected_suc["dn"], f"Para recalque {rec_pipe['dn']}, sucção esperada {expected_suc['dn']}"
        assert suc_pipe["dn"] > rec_pipe["dn"], f"Sucção {suc_pipe['dn']} deve ser maior que recalque {rec_pipe['dn']}"


def test_commercial_pump_catalog_consistency():
    assert len(PUMP_CATALOG) >= 6
    for pump in PUMP_CATALOG:
        assert pump["cv"] > 0
        assert pump["kw"] > 0
        assert pump["flow_lh"] > 0
        assert pump["max_h"] > 0
        assert pump["cost"] > 0
        assert "bocal_suc" in pump and pump["bocal_suc"]
        assert "bocal_rec" in pump and pump["bocal_rec"]
        assert pump["rec_pipe_dn"] in [25, 32, 40, 50, 60, 75]
        assert pump["suc_pipe_dn"] in [25, 32, 40, 50, 60, 75]
        assert pump["rec_pipe_dn"] >= 25
        assert pump["suc_pipe_dn"] >= 32
        assert pump["suc_pipe_dn"] > pump["rec_pipe_dn"], (
            f"Bomba {pump['brand']}: sucção ({pump['suc_pipe_dn']}) deve ser estritamente maior que recalque ({pump['rec_pipe_dn']})"
        )


def test_motobomba_model_governs_pipes_over_forchheimer(qapp):
    from netuno.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
    # Caixa d'água de 350L (volume onde Forchheimer geraria diâmetro teórico inferior a 15mm / DN 20)
    dlg = PumpSelectionWizardDialog(upper_tank_vol=350.0)
    
    # A motobomba deve reger o dimensionamento final
    data = dlg.selected_pump_data
    assert data is not None
    # Recalque deve ser no mínimo 25 mm (regido pela motobomba)
    assert data["recalque_dn"] >= 25
    # Sucção deve ser no mínimo 32 mm e estritamente superior ao recalque
    assert data["suction_dn"] >= 32
    assert data["suction_dn"] > data["recalque_dn"]

    # Ao trocar de motobomba manualmente para BC-21 R (1.0 CV), as tubulações devem acompanhar
    idx_1cv = -1
    for i in range(dlg.combo_pump.count()):
        p = dlg.combo_pump.itemData(i)
        if p and p.get("cv") == 1.0:
            idx_1cv = i
            break
    assert idx_1cv >= 0
    dlg.combo_pump.setCurrentIndex(idx_1cv)
    data_1cv = dlg.selected_pump_data
    assert data_1cv["recalque_dn"] == 40
    assert data_1cv["suction_dn"] == 50


def test_wizard_no_forchheimer_text_and_commercial_pipes():
    from netuno.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
    from netuno.core.cost_estimates import COMMERCIAL_PIPES_CAPEX, _DEFAULT_PIPE_COST_PER_METER
    from netuno.core.parser import NetunoConfig

    # Verifica que todos os diâmetros calculados no wizard estão disponíveis para o CAPEX
    for p in COMMERCIAL_PIPES:
        assert any(cp["dn"] == p["dn"] for cp in COMMERCIAL_PIPES_CAPEX), f"DN {p['dn']} ausente no CAPEX"
        assert p["dn"] in _DEFAULT_PIPE_COST_PER_METER, f"Preço de DN {p['dn']} ausente na tabela de custos"

    # Diâmetros pluviais também presentes
    assert any(cp["dn"] == 100 for cp in COMMERCIAL_PIPES_CAPEX)
    assert any(cp["dn"] == 150 for cp in COMMERCIAL_PIPES_CAPEX)

    # Config salva e recupera comprimentos
    cfg = NetunoConfig()
    cfg.set_pipe_length(20, 12.5)
    assert cfg.get_pipe_length(20) == 12.5
    d = cfg.get_pipe_lengths_dict()
    assert 20 in d and d[20] == 12.5


def test_dialog_other_op_costs_height_and_items(qapp):
    from netuno.ui.dialogs.dialog_economic import DialogOtherOpCosts
    dlg = DialogOtherOpCosts()
    # Altura deve ser pelo menos 600px para acomodar o formulário e a tabela
    assert dlg.minimumHeight() >= 600 or dlg.height() >= 600
    # Tabela com altura mínima dedicada para exibir as 3 rotinas
    assert dlg.table.minimumHeight() >= 150
    # 3 rotinas padrão de manutenção carregadas
    assert dlg.table.rowCount() == 3
    assert len(dlg.op_costs) == 3


def test_dialog_initial_costs_all_commercial_pipes(qapp):
    from netuno.ui.dialogs.dialog_economic import DialogInitialCosts
    from netuno.core.cost_estimates import COMMERCIAL_PIPES_CAPEX
    from netuno.core.parser import NetunoConfig

    cfg = NetunoConfig()
    # Atribui comprimentos a diferentes bitolas comerciais
    cfg.set_pipe_length(25, 10.0)
    cfg.set_pipe_length(32, 12.0)
    cfg.set_pipe_length(110, 8.0)

    dlg = DialogInitialCosts(config=cfg)
    assert hasattr(dlg, "txt_pipes")
    assert len(dlg.txt_pipes) == len(COMMERCIAL_PIPES_CAPEX)

    # Verifica que todos os diâmetros comerciais possuem campos no diálogo
    for p in COMMERCIAL_PIPES_CAPEX:
        dn = p["dn"]
        assert dn in dlg.txt_pipes
        assert dn in dlg.lbl_pipe_costs
        assert hasattr(dlg, f"txt_pipe_{dn}")

    # Verifica valores preenchidos
    assert float(dlg.txt_pipes[25].text().replace(',', '.')) == 10.0
    assert float(dlg.txt_pipes[32].text().replace(',', '.')) == 12.0
    assert float(dlg.txt_pipes[110].text().replace(',', '.')) == 8.0

    # Simula edição de tubo e accept
    dlg.txt_pipes[40].setText("15,0")
    dlg.on_accept()
    assert cfg.get_pipe_length(40) == 15.0


