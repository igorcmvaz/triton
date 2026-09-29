"""O filtro de polimento é escolha do usuário, e o padrão é não usar.

Dois defeitos na mesma caixa de seleção, e o segundo é o mais grave.

**A escolha não valia.** Para as classes 2 a 4 a conta era
`include_polishing_filter or target_class.exige_filtracao_fina`, de modo que a
classe sobrepunha a escolha em silêncio: a caixa aparecia desmarcada e o filtro
entrava assim mesmo, com R$ 380 a R$ 550 de investimento e 4 a 8 kg CO₂e/ano que
o usuário acabara de recusar. Um controle que mente sobre o próprio estado é pior
que um controle ausente.

**A escolha não chegava.** Havia dois motores econômicos: `run_economic_analysis`,
no núcleo, que recebeu a linha de tratamento na versão passada, e o da aba
econômica integrada, que soma o investimento à mão e monta o próprio fluxo de
caixa — e não a recebeu. Ligar só o primeiro repetiu, com outro nome, o defeito
que a revisão inteira persegue: o valor chega a quem calcula e não chega a quem
exibe.

As classes 2 a 4 são declaradas «adaptada, não normativa» pelo próprio programa.
A exigência de filtração fina é recomendação dele, não da NBR 15527:2019, e
recomendação se apresenta, não se impõe.
"""

from __future__ import annotations

import pytest

from netuno.core.etap_integration import (
    capex_incremental_da_etap,
    opex_anual_incremental_da_etap,
)
from netuno.core.parser import NetunoConfig
from netuno.core.water_quality import WATER_QUALITY_CLASSES, size_etap

CLASSES_QUE_RECOMENDAM = tuple(
    c for c, v in WATER_QUALITY_CLASSES.items() if v.exige_filtracao_fina
)


# ─────────────────────────────── o padrão é não usar ───────────────────────────

def test_o_padrao_da_configuracao_e_nao_usar_polimento():
    assert NetunoConfig().water_quality_polishing is False


def test_a_classe_padrao_nem_sequer_recomenda_polimento():
    """A classe 1 é a dos parâmetros mínimos da NBR 15527:2019."""
    padrao = NetunoConfig().water_quality_target_class
    assert WATER_QUALITY_CLASSES[padrao].exige_filtracao_fina is False


def test_sem_polimento_o_dimensionamento_nao_cobra_filtro():
    r = size_etap(include_polishing_filter=False)
    assert r.polishing_capex == 0.0
    assert r.polishing_annual_opex == 0.0


# ────────────────────── a escolha do usuário é que vale ────────────────────────

def test_desmarcar_surte_efeito_em_todas_as_classes():
    """Era o defeito principal: nas classes 2 a 4 desmarcar não fazia nada."""
    assert CLASSES_QUE_RECOMENDAM, "nenhuma classe recomenda filtração fina"
    for classe in CLASSES_QUE_RECOMENDAM:
        sem = size_etap(target_class_id=classe, include_polishing_filter=False)
        com = size_etap(target_class_id=classe, include_polishing_filter=True)

        assert sem.polishing_capex == 0.0, classe
        assert sem.polishing_annual_opex == 0.0, classe
        assert com.polishing_capex > 0.0, classe
        assert com.total_etap_capex > sem.total_etap_capex, classe
        assert com.total_etap_annual_opex > sem.total_etap_annual_opex, classe
        assert com.total_etap_co2e_kg_yr > sem.total_etap_co2e_kg_yr, classe


def test_a_recusa_da_recomendacao_fica_registrada():
    """Não é erro, e não é silêncio: o relatório precisa poder declarar a escolha."""
    for classe in CLASSES_QUE_RECOMENDAM:
        recusado = size_etap(target_class_id=classe, include_polishing_filter=False)
        aceito = size_etap(target_class_id=classe, include_polishing_filter=True)
        assert recusado.polishing_recommended_but_declined is True, classe
        assert aceito.polishing_recommended_but_declined is False, classe
        assert "dispensada" in recusado.polishing_filter_type


def test_a_classe_1_nunca_marca_recusa():
    """Ela não recomenda, então não há o que recusar."""
    for incluir in (False, True):
        r = size_etap(target_class_id="classe_1", include_polishing_filter=incluir)
        assert r.polishing_recommended_but_declined is False


def test_a_classe_4_leva_carvao_ativado_e_as_demais_areia():
    """O tipo de filtro muda com a classe, e o custo com ele."""
    carvao = size_etap(target_class_id="classe_4", include_polishing_filter=True)
    areia = size_etap(target_class_id="classe_2", include_polishing_filter=True)
    assert "Carvão" in carvao.polishing_filter_type
    assert carvao.polishing_capex > areia.polishing_capex


# ──────────────── a escolha chega aos dois motores econômicos ──────────────────

def _config(polimento: bool, classe: str = "classe_4") -> NetunoConfig:
    cfg = NetunoConfig()
    cfg.water_quality_target_class = classe
    cfg.water_quality_polishing = polimento
    return cfg


def test_o_polimento_move_o_investimento_incremental():
    sem = capex_incremental_da_etap(_config(False))
    com = capex_incremental_da_etap(_config(True))
    assert com > sem
    esperado = size_etap(target_class_id="classe_4", include_polishing_filter=True).polishing_capex
    assert com - sem == pytest.approx(esperado)


def test_o_polimento_move_o_custeio_incremental():
    sem = opex_anual_incremental_da_etap(_config(False))
    com = opex_anual_incremental_da_etap(_config(True))
    esperado = size_etap(target_class_id="classe_4", include_polishing_filter=True).polishing_annual_opex
    assert com - sem == pytest.approx(esperado)


def test_a_regra_incremental_tem_uma_definicao_so():
    """Havia dois motores econômicos, e só um recebia a linha de tratamento.

    O núcleo tem de devolver exatamente o que o auxiliar compartilhado calcula:
    se divergirem, a aba econômica e o relatório mostram números diferentes para
    o mesmo projeto, que foi como o cloro chegou a ter cinco convenções.
    """
    from netuno.core.economic import run_economic_analysis
    from netuno.core.simulation import SingleTankSimulationResult

    sim = SingleTankSimulationResult(
        lower_tank_vol=5000.0, potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=330.0, avg_potable_consumed_l_day=330.0,
        avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0,
    )
    for polimento in (False, True):
        cfg = _config(polimento)
        econ = run_economic_analysis(cfg, sim)
        anual = sim.annual_pluvial_consumed_m3
        assert econ.etap_capex_brl == pytest.approx(capex_incremental_da_etap(cfg, anual, sim))
        assert econ.annual_etap_opex_brl == pytest.approx(
            opex_anual_incremental_da_etap(cfg, anual, sim)
        )


def test_desligar_a_etap_zera_o_incremental():
    cfg = _config(True)
    cfg.etap_enabled = False
    assert capex_incremental_da_etap(cfg) == 0.0
    assert opex_anual_incremental_da_etap(cfg) == 0.0


def test_a_verba_ja_prevista_em_acessorios_e_descontada_uma_vez_so():
    """O desconto vale para a linha inteira, e não por estágio.

    Descontá-lo duas vezes faria o filtro de polimento parecer mais barato do que
    é quando há acessórios orçados.
    """
    from netuno.core.cost_estimates import verba_generica_de_tratamento_brl

    verba = verba_generica_de_tratamento_brl("UTI")
    sem_acessorios, com_acessorios = _config(True), _config(True)
    com_acessorios.cost_accessories = 800.0
    assert capex_incremental_da_etap(sem_acessorios) - capex_incremental_da_etap(
        com_acessorios
    ) == pytest.approx(verba)


# ───────────── o que o professor vê na tela é o que muda de fato ───────────────

@pytest.fixture
def janela(qapp):
    pytest.importorskip("PySide6")
    from netuno.core.simulation import SingleTankSimulationResult
    from netuno.ui.main_window import MainWindow

    win = MainWindow()
    sim = SingleTankSimulationResult(
        lower_tank_vol=5000.0, potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=330.0, avg_potable_consumed_l_day=330.0,
        avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0,
    )
    sim.n_days_simulated = 365
    sim.total_pumped_liters = 330.0 * 365
    sim.total_pump_cycles = 365
    win.tab_tanks_simulation.last_single_result = sim
    win.tab_tanks_simulation._is_technical_only = False
    return win


def _reais(texto: str) -> float:
    return float(texto.replace("R$", "").replace(".", "").replace(",", ".").strip() or 0.0)


def test_a_caixa_comeca_desmarcada(janela):
    """O professor pediu que o padrão fosse não utilizar."""
    aba = janela.tab_water_quality
    assert aba.chk_polishing.isChecked() is False
    assert janela.config.water_quality_polishing is False


def test_trocar_de_classe_recomenda_mas_nao_marca_a_caixa(janela):
    """Marcar sozinho fazia o polimento parecer obrigatório."""
    aba = janela.tab_water_quality
    for classe in CLASSES_QUE_RECOMENDAM:
        aba.combo_class.setCurrentIndex(aba.combo_class.findData(classe))
        aba.on_class_changed()
        assert aba.chk_polishing.isChecked() is False, classe
        assert aba.lbl_polishing_reco.text(), f"{classe} não mostrou a recomendação"

    aba.combo_class.setCurrentIndex(aba.combo_class.findData("classe_1"))
    aba.on_class_changed()
    assert aba.lbl_polishing_reco.text() == ""


def test_o_investimento_e_a_manutencao_exibidos_acompanham_a_caixa(janela):
    """Era o sintoma relatado: marcar ou desmarcar não mexia nos dois valores.

    A aba econômica integrada soma o investimento à mão e monta o próprio fluxo
    de caixa, e não recebia a linha de tratamento. Ligar só o motor do núcleo
    deixava o número certo fora da tela.
    """
    aba, tab = janela.tab_water_quality, janela.tab_economic
    aba.combo_class.setCurrentIndex(aba.combo_class.findData("classe_4"))
    aba.on_class_changed()

    medidas = {}
    for estado in (False, True):
        aba.chk_polishing.setChecked(estado)
        aba.on_polishing_changed()
        tab.calculate_economics(force=True)
        tabela = tab.table_cashflow
        medidas[estado] = (
            _reais(tabela.item(0, 1).text()),   # investimento, ano 0
            _reais(tabela.item(1, 9).text()),   # O&M, ano 1
        )

    esperado = size_etap(target_class_id="classe_4", include_polishing_filter=True)
    assert medidas[True][0] - medidas[False][0] == pytest.approx(esperado.polishing_capex)
    assert medidas[True][1] - medidas[False][1] == pytest.approx(esperado.polishing_annual_opex)


def test_o_payback_exibido_piora_com_o_filtro(janela):
    """Se o investimento sobe e a economia não, o retorno tem de demorar mais."""
    aba, tab = janela.tab_water_quality, janela.tab_economic
    aba.combo_class.setCurrentIndex(aba.combo_class.findData("classe_4"))
    aba.on_class_changed()

    textos = {}
    for estado in (False, True):
        aba.chk_polishing.setChecked(estado)
        aba.on_polishing_changed()
        tab.calculate_economics(force=True)
        textos[estado] = tab.lbl_val_payback.text()

    assert textos[True] != textos[False]
