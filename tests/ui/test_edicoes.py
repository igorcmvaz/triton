"""A Edição Brasil traz os dados brasileiros; a Internacional, o núcleo neutro."""

import pytest

from netuno.core.edition import neutralizar_para_a_internacional, rotulo_da_edicao
from netuno.core.parser import NetunoConfig


@pytest.fixture
def internacional(monkeypatch):
    monkeypatch.setenv("NETUNO_EDITION", "INT")


@pytest.fixture
def brasil(monkeypatch):
    monkeypatch.setenv("NETUNO_EDITION", "BRL")


def test_o_rotulo_identifica_a_edicao(brasil, monkeypatch):
    assert rotulo_da_edicao() == "Edição Brasil (BRL)"
    monkeypatch.setenv("NETUNO_EDITION", "INT")
    assert rotulo_da_edicao() == "International Edition (INT)"
    assert rotulo_da_edicao(curto=True) == "INT"


def test_projeto_novo_da_internacional_nao_traz_precos_brasileiros():
    cfg = NetunoConfig()
    neutralizar_para_a_internacional(cfg)
    assert cfg.water_tariffs == [] and cfg.elec_tariff == 0 and cfg.pump_unit_cost == 0
    assert cfg.chlorine_cost_per_kg == 0 and cfg.iptu_green_enabled is False
    assert cfg.capex_do_arranjo is False and cfg.mao_de_obra_automatica is False
    assert cfg.op_costs and all(fixo == 0 and variavel == 0 for _, _, fixo, variavel in cfg.op_costs)


def test_janela_da_internacional(qapp, internacional):
    from netuno.ui.main_window import MainWindow

    janela = MainWindow()
    try:
        assert janela.sidebar.lbl_edicao.text() == "International Edition (INT)"
        assert not any("Tarif" in b.text() for b in janela.sidebar.btn_group.buttons())
        assert janela.tab_tanks_simulation.get_currency_symbol() == "$"
        assert janela.config.water_tariffs == [] and janela.config.capex_do_arranjo is False
        ambiental = janela.tab_environmental
        assert ambiental.faltam_fatores_do_pais()            # sem fator do país, sem ACV
        assert ambiental.get_config().grid_co2_factor_kg_kwh == 0.0
        assert not ambiental.card_aqua.isVisibleTo(janela) and not ambiental.card_casa_azul.isVisibleTo(janela)
        assert "Casa Azul" not in ambiental._get_esg_methodology_html(False)
        assert "AQUA" not in ambiental._get_esg_methodology_html(False)
        assert not janela.tab_project.rb_source_national.isVisibleTo(janela)
        ambiental.txt_grid_co2.setText("0.4")
        ambiental.txt_potable_co2.setText("0.3")
        assert not ambiental.faltam_fatores_do_pais()
    finally:
        janela.close()


def test_janela_da_brasil_continua_como_era(qapp, brasil):
    from netuno.ui.main_window import MainWindow

    janela = MainWindow()
    try:
        assert janela.sidebar.lbl_edicao.text() == "Edição Brasil (BRL)"
        assert any("Tarif" in b.text() for b in janela.sidebar.btn_group.buttons())
        assert janela.tab_tanks_simulation.get_currency_symbol() == "R$"
        assert janela.config.water_tariffs and janela.config.capex_do_arranjo is True
        ambiental = janela.tab_environmental
        assert not ambiental.faltam_fatores_do_pais()
        assert ambiental.get_config().grid_co2_factor_kg_kwh > 0
        assert "Casa Azul" in ambiental._get_esg_methodology_html(False)
    finally:
        janela.close()


def test_relatorios_e_prancha_trazem_a_edicao(internacional):
    from netuno.core.schematic_3d import generate_schematic_3d_svg
    from netuno.core.study_layout import generate_study_layout

    dados = dict(generate_study_layout({}), project_name="t")
    assert "International Edition (INT)" in generate_schematic_3d_svg(dados)


def test_instalador_por_edicao():
    from pathlib import Path

    iss = (Path(__file__).resolve().parents[2] / "setup_script.iss").read_text(encoding="utf-8")
    assert '#if Edition == "INT"' in iss
    assert iss.count("#define AppGuid") == 2   # AppIds distintos: instalam-se lado a lado
    assert 'Source: "{#DistDir}\\*"' in iss
