"""Sem catálogo de preços, o preço da cisterna inferior é um campo editável na moeda do projeto."""
from triton.core.parser import TritonConfig
from triton.core.cost_estimates import banco_tem_precos, precos_de_catalogo


def test_preco_da_cisterna_digitado_vai_para_a_tabela_e_para_o_projeto(qapp):
    from triton.ui.dialogs.dialog_economic import DialogInitialCosts
    cfg = TritonConfig()
    dlg = DialogInitialCosts(config=cfg, evaluated_volumes=[0, 1000, 2000])
    if precos_de_catalogo(cfg) and banco_tem_precos():
        assert not dlg._lower_cost_is_typed()
        return
    assert dlg._lower_cost_is_typed()
    dlg.txt_lower.setText("1500,50")
    assert dlg._lower_cost_of(0) == 0.0
    assert dlg._lower_cost_of(1000) == 1500.5
    assert "1.500,50" in dlg.table_lower_costs.item(1, 1).text()
    dlg.on_accept()
    assert cfg.cost_lower_tank == 1500.5


def test_preco_da_cisterna_com_custo_por_m3(qapp):
    from triton.ui.dialogs.dialog_economic import DialogInitialCosts
    from triton.core.cost_estimates import preco_da_cisterna_do_volume
    cfg = TritonConfig()
    cfg.precos_de_catalogo = False
    cfg.cost_lower_tank = 1000.0
    cfg.cost_lower_tank_per_m3 = 500.0

    # Volume 0 -> 0.0
    assert preco_da_cisterna_do_volume(cfg, 0.0) == 0.0
    # Volume 1.000 L -> 1000 + 1 * 500 = 1500.0
    assert preco_da_cisterna_do_volume(cfg, 1000.0) == 1500.0
    # Volume 5.000 L -> 1000 + 5 * 500 = 3500.0
    assert preco_da_cisterna_do_volume(cfg, 5000.0) == 3500.0

    dlg = DialogInitialCosts(config=cfg, evaluated_volumes=[0, 1000, 3000])
    assert dlg._lower_cost_of(0) == 0.0
    assert dlg._lower_cost_of(1000) == 1500.0
    assert dlg._lower_cost_of(3000) == 2500.0
