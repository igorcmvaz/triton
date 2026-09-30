"""A informação atravessa o programa conforme se avança pelas etapas.

Este é o teste de fecho da revisão de desconexões. Cada defeito encontrado
naquela varredura era da mesma família: um valor calculado corretamente numa
etapa e descartado antes de chegar a quem devia consumi-lo. Nenhum aparecia em
teste de fórmula, porque cada parte isolada estava certa.

O que se verifica aqui é o percurso, não a fórmula. Uma escolha feita numa
etapa tem de mover um resultado nas seguintes; se deixar de mover, alguma ponte
voltou a se romper.

Três percursos, na ordem do programa:

1. Etapa 1 → chuva carregada → precipitação real chega à qualidade da água;
2. Etapa 2 → escolha de desinfecção → investimento, custeio e emissão;
3. assistente de motobomba → altura manométrica → energia, custo e emissão.
"""

from __future__ import annotations

import sys

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication  # noqa: E402

from netuno.core.economic import run_economic_analysis  # noqa: E402
from netuno.core.environmental import calculate_lca  # noqa: E402
from netuno.core.simulation import SingleTankSimulationResult  # noqa: E402
from netuno.ui.main_window import MainWindow  # noqa: E402


@pytest.fixture(scope="module")
def app():
    inst = QApplication.instance()
    if inst is None:
        inst = QApplication(sys.argv)
    yield inst


@pytest.fixture
def janela(app):
    return MainWindow()


def _simulacao(volume_pluvial_l_dia: float = 330.0) -> SingleTankSimulationResult:
    """Resultado sintético com recalque real.

    `total_pumped_liters` em zero não é neutro: sem volume recalcado não há o
    que a altura manométrica possa encarecer, e a energia dá zero em qualquer
    desnível.
    """
    res = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=volume_pluvial_l_dia,
        avg_potable_consumed_l_day=330.0,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0,
        pct_days_null_satisfaction=5.0,
    )
    res.n_days_simulated = 365
    res.total_pumped_liters = volume_pluvial_l_dia * 365.0
    res.total_pump_cycles = 365
    return res


# ───────── percurso 1: a chuva carregada na Etapa 1 chega à qualidade ──────────

def test_a_precipitacao_carregada_chega_ao_calculo_de_wash_off(janela):
    """Estava fixa em 1.500 mm, de modo que o volume anual de descarte era o
    mesmo em Manaus e em Caxias do Sul."""
    aba = janela.tab_water_quality

    # A janela abre com uma série já carregada, e é dela que a precipitação sai.
    carregada = aba._precipitacao_anual_mm()
    assert carregada != 1500.0, "o valor fixo anterior voltou"
    assert 500.0 < carregada < 4000.0, carregada

    # Duas séries sintéticas de um ano, com totais muito diferentes.
    janela.tab_tanks_simulation.precip_data = [2.0] * 365      # 730 mm/ano
    seca = aba._precipitacao_anual_mm()
    janela.tab_tanks_simulation.precip_data = [8.0] * 365      # 2.920 mm/ano
    umida = aba._precipitacao_anual_mm()

    assert seca == pytest.approx(730.0, rel=0.01)
    assert umida == pytest.approx(2920.0, rel=0.01)
    assert umida > 3 * seca

    # E sem série alguma, o valor de recurso — que é o que a aba usava sempre.
    janela.tab_tanks_simulation.precip_data = None
    assert aba._precipitacao_anual_mm() == pytest.approx(1500.0)


def test_o_volume_simulado_chega_ao_dimensionamento_da_etap(janela):
    """A aba pedia o volume a um atributo que não existe na configuração.

    O `getattr` devolvia sempre 120 m³/ano, e a linha de tratamento era
    dimensionada para esse número qualquer que fosse o projeto.
    """
    from netuno.core.etap_integration import volume_pluvial_anual_m3

    janela.tab_tanks_simulation.last_single_result = _simulacao(1000.0)
    aba = janela.tab_water_quality
    volume = volume_pluvial_anual_m3(janela.config, aba._simulacao_corrente())
    assert volume == pytest.approx(365.25, rel=1e-6)
    assert volume != 120.0


# ────── percurso 2: a escolha de desinfecção move investimento e emissão ───────

def test_escolher_ultravioleta_atravessa_ate_o_economico_e_a_acv(janela):
    """Era a maior desconexão: a escolha ficava guardada e era ignorada.

    O percurso completo, e não só o núcleo: a aba grava na configuração, e os
    dois módulos leem dela.
    """
    aba = janela.tab_water_quality

    idx = aba.combo_disinf.findData("cloro")
    aba.combo_disinf.setCurrentIndex(idx)
    aba.on_disinfection_changed()
    assert janela.config.water_quality_disinfection == "cloro"
    econ_cloro = run_economic_analysis(janela.config, _simulacao())

    idx = aba.combo_disinf.findData("uv")
    aba.combo_disinf.setCurrentIndex(idx)
    aba.on_disinfection_changed()
    assert janela.config.water_quality_disinfection == "uv"
    econ_uv = run_economic_analysis(janela.config, _simulacao())

    assert econ_uv.capex_total > econ_cloro.capex_total
    assert econ_uv.annual_etap_opex_brl > econ_cloro.annual_etap_opex_brl
    assert econ_uv.vpl < econ_cloro.vpl


def test_o_filtro_de_polimento_atravessa_a_partir_da_caixa_de_selecao(janela):
    """O campo existia e nunca era escrito: marcar o filtro não mudava nada."""
    aba = janela.tab_water_quality

    aba.chk_polishing.setChecked(False)
    aba.on_polishing_changed()
    sem = run_economic_analysis(janela.config, _simulacao()).capex_total

    aba.chk_polishing.setChecked(True)
    aba.on_polishing_changed()
    assert janela.config.water_quality_polishing is True
    com = run_economic_analysis(janela.config, _simulacao()).capex_total

    assert com > sem


def test_a_dose_digitada_atravessa_ate_a_massa_anual(janela):
    """A dose digitada na Etapa 2 não chegava à configuração.

    O econômico e a ACV seguiam com a dose padrão enquanto a tela mostrava
    outra.
    """
    aba = janela.tab_water_quality
    aba.txt_cl_dose.setText("3,0")
    aba.recalculate_all()

    assert janela.config.chlorine_dose_mg_l == pytest.approx(3.0)
    econ = run_economic_analysis(janela.config, _simulacao())

    aba.txt_cl_dose.setText("1,5")
    aba.recalculate_all()
    metade = run_economic_analysis(janela.config, _simulacao())

    assert econ.annual_chlorine_kg == pytest.approx(2 * metade.annual_chlorine_kg, rel=1e-6)


# ───────── percurso 3: o assistente de motobomba chega à energia ───────────────

def test_a_altura_do_assistente_atravessa_ate_a_emissao(janela):
    """O assistente calculava a altura manométrica e a descartava no retorno.

    Uma casa térrea e um sobrado davam a mesma emissão de bombeamento.
    """
    from netuno.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog

    emissoes = []
    for altura in (4.0, 30.0):
        assistente = PumpSelectionWizardDialog(upper_tank_vol=500.0)
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        dados = assistente.selected_pump_data

        cfg = janela.config
        cfg.pump_power_kw = dados["kw"]
        cfg.pump_flow_rate = dados["flow_lh"]
        cfg.pump_efficiency = float(dados["efficiency"])
        cfg.pump_manometric_head_m = float(dados["manometric_head_m"])

        lca = calculate_lca(5000.0, 120.0, _config_ambiental(cfg))
        emissoes.append(lca.annual_pumping_co2_kg)

    assert emissoes[1] > 3 * emissoes[0], emissoes


def _config_ambiental(cfg):
    from netuno.core.environmental import EnvironmentalConfig
    from netuno.core.pump_energy import compute_annual_pump_energy

    energia = compute_annual_pump_energy(cfg, _simulacao(), upper_tank_used=True)
    return EnvironmentalConfig(
        annual_water_saved_m3=120.0,
        annual_pump_kwh=energia.annual_kwh,
    )


# ──────────────── nenhuma ponte se rompe em silêncio ao recalcular ─────────────

def test_recalcular_a_qualidade_nao_apaga_a_escolha_do_usuario(janela):
    """Recalcular reescreve campos, e um `recalculate` distraído já apagou escolha
    antes. O teste guarda a idempotência."""
    aba = janela.tab_water_quality
    idx = aba.combo_disinf.findData("ozonio")
    aba.combo_disinf.setCurrentIndex(idx)
    aba.on_disinfection_changed()
    aba.chk_polishing.setChecked(True)
    aba.on_polishing_changed()
    aba.txt_cl_dose.setText("2,5")

    for _ in range(3):
        aba.recalculate_all()

    assert janela.config.water_quality_disinfection == "ozonio"
    assert janela.config.water_quality_polishing is True
    assert janela.config.chlorine_dose_mg_l == pytest.approx(2.5)
