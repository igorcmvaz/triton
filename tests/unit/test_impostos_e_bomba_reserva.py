"""Os quatro impostos existem em tela, e a contagem de bombas volta como foi escolhida.

O quadro de ligações desta rodada mostrou quatro campos numa situação estranha:
`water_tax_fixed`, `water_tax_var`, `elec_tax_fixed` e `elec_tax_var` chegam ao
motor econômico e à linha de comando, e não tinham campo em tela nenhuma.

O motivo era pior do que a ausência. As duas caixas de diálogo que tratam do
assunto atribuíam `0.0` aos quatro ao fechar, incondicionalmente — de modo que um
projeto que declarasse imposto perdia o valor no primeiro OK, sem aviso. É a
mesma família de defeito que perseguimos desde o início: valor correto que não
chega a quem deveria consumi-lo, aqui apagado pela travessia da tela.

O bombeamento é o único custo operacional recorrente do sistema. No Brasil a
fatura de energia carrega ICMS mais PIS/COFINS, entre 25% e 30% em boa parte dos
estados, e zerar isso subestima o OPEX.

Na mesma tela, a caixa «considerar motobomba de reserva» era marcada por
`True if pump_count >= 1 else True` — verdadeiro nos dois ramos. Abria sempre
marcada, e o OK devolvia `pump_count = 2`. Quem escolhesse bomba única recebia
duas de volta, com o CAPEX e a emissão incorporada que vêm junto.
"""

from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from netuno.core.economic import calculate_water_bill  # noqa: E402
from netuno.core.parser import NetunoConfig  # noqa: E402
from netuno.ui.dialogs.dialog_economic import DialogElectricity, DialogTariffs  # noqa: E402

TARIFA_SIMPLES = [(0.0, 10.0, 3.08, 1), (10.0, 999999.0, 6.81, 1)]


def _config(**trocas):
    cfg = NetunoConfig()
    cfg.water_tariffs = list(TARIFA_SIMPLES)
    cfg.sewage_mode, cfg.sewage_rate = 1, 100.0
    for k, v in trocas.items():
        setattr(cfg, k, v)
    return cfg


# ───────────────────────── a tela oferece os quatro campos ─────────────────────

def test_a_tela_de_tarifas_tem_campo_para_os_dois_impostos_da_agua(qapp):
    d = DialogTariffs(config=_config())
    assert hasattr(d, "txt_tax_fix")
    assert hasattr(d, "txt_tax_var")


def test_a_tela_de_energia_tem_campo_para_os_dois_impostos_da_energia(qapp):
    d = DialogElectricity(config=_config())
    assert hasattr(d, "txt_elec_tax_fix")
    assert hasattr(d, "txt_elec_tax_var")


# ─────────────────── o valor declarado sobrevive à travessia ───────────────────

def test_o_imposto_da_agua_nao_e_zerado_ao_fechar(qapp):
    """Antes, `on_accept` atribuía 0.0 aos dois, apagando o que viesse do arquivo."""
    cfg = _config(water_tax_fixed=4.75, water_tax_var=12.5)
    d = DialogTariffs(config=cfg)
    d.on_accept()
    assert cfg.water_tax_fixed == pytest.approx(4.75)
    assert cfg.water_tax_var == pytest.approx(12.5)


def test_o_imposto_da_energia_nao_e_zerado_ao_fechar(qapp):
    cfg = _config(elec_tax_fixed=9.20, elec_tax_var=29.5)
    d = DialogElectricity(config=cfg)
    d.on_accept()
    assert cfg.elec_tax_fixed == pytest.approx(9.20)
    assert cfg.elec_tax_var == pytest.approx(29.5)


def test_o_que_o_usuario_digita_e_o_que_chega_ao_config(qapp):
    """Vírgula decimal, como o resto do programa aceita."""
    cfg = _config()
    d = DialogTariffs(config=cfg)
    d.txt_tax_fix.setText("3,40")
    d.txt_tax_var.setText("7,25")
    d.on_accept()
    assert cfg.water_tax_fixed == pytest.approx(3.40)
    assert cfg.water_tax_var == pytest.approx(7.25)


def test_campo_vazio_ou_ilegivel_nao_derruba_a_tela(qapp):
    cfg = _config(water_tax_fixed=1.0)
    d = DialogTariffs(config=cfg)
    d.txt_tax_fix.setText("")
    d.txt_tax_var.setText("abc")
    d.on_accept()
    assert cfg.water_tax_fixed == 0.0
    assert cfg.water_tax_var == 0.0


# ───────────────── e move o resultado, que é o que importa ─────────────────────

def test_o_imposto_da_agua_move_a_conta():
    """Percurso fechado: se o campo não mudasse a conta, o campo seria decorativo."""
    sem = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 0.0, 0.0)
    com = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 5.0, 10.0)
    assert com > sem
    assert com - sem > 5.0        # o fixo entra inteiro, mais o percentual


def test_o_imposto_fixo_e_o_variavel_agem_por_caminhos_diferentes():
    base = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 0.0, 0.0)
    so_fixo = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 7.0, 0.0)
    so_var = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 0.0, 20.0)
    assert so_fixo - base == pytest.approx(7.0)          # não escala com o consumo
    assert so_var > base                                  # escala com o consumo


# ─────────────────────────── a bomba de reserva ────────────────────────────────

@pytest.mark.parametrize("quantas", [1, 2])
def test_a_contagem_de_bombas_volta_como_foi_escolhida(qapp, quantas):
    """A caixa era marcada por um ternário que devolvia True nos dois ramos."""
    cfg = _config(pump_count=quantas, pump_power_kw=0.37, pump_efficiency=60.0,
                  pump_flow_rate=3000.0)
    d = DialogElectricity(config=cfg)
    assert d.chk_backup_pump.isChecked() is (quantas >= 2)
    d.on_accept()
    assert cfg.pump_count == quantas


def test_desmarcar_a_reserva_deixa_uma_bomba(qapp):
    cfg = _config(pump_count=2, pump_power_kw=0.37, pump_efficiency=60.0,
                  pump_flow_rate=3000.0)
    d = DialogElectricity(config=cfg)
    d.chk_backup_pump.setChecked(False)
    d.on_accept()
    assert cfg.pump_count == 1
