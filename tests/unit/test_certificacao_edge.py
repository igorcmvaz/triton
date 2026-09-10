"""A barra de água do EDGE, e o percurso dela até o relatório.

O EDGE é a certificação mais usada no Brasil em habitação, e é a única da lista
que **não pontua**: mede percentual de economia contra um caso-base local em três
barras independentes — energia, água e energia incorporada nos materiais — e
exige que cada uma cruze 20%.

Fonte dos limiares: IFC, *EDGE Certification Process*,
<https://edgebuildings.com/certify/certification/>, consultado em 10/09/2026.

Os códigos das medidas de água (WEM) foram conferidos contra um relatório de
avaliação EDGE v3.0.0 de projeto residencial certificado. A WEM14 é o sistema de
aproveitamento de água pluvial, e sua entrada no aplicativo é a **área de
captação em m²** — que é justamente o que o Netuno já tem.

O que estes testes guardam, além das faixas: que a área de captação atravessa os
três chamadores até a matriz de créditos. Uma certificação calculada e não
entregue repete o defeito que este projeto persegue.
"""

from __future__ import annotations

import pytest

from netuno.core.edge_certification import (
    LIMIAR_DE_AGUA_PCT,
    LIMIAR_DE_ENERGIA_AVANCADO_PCT,
    MEDIDAS_DE_AGUA,
    avaliar_agua_edge,
    consumo_base_anual_m3,
)
from netuno.core.esg_certifications import calculate_esg_certifications


def _avaliar(pluvial, demanda=250.0, area=180.0, base=None):
    return avaliar_agua_edge(
        volume_pluvial_anual_m3=pluvial,
        demanda_total_anual_m3=demanda,
        area_de_captacao_m2=area,
        consumo_base_anual_m3_declarado=base,
    )


# ──────────────────────────── os limiares publicados ───────────────────────────

def test_o_limiar_das_tres_barras_e_vinte_por_cento():
    assert LIMIAR_DE_AGUA_PCT == 20.0


def test_o_nivel_avancado_pede_quarenta_por_cento_de_energia():
    """EDGE Advanced acrescenta energia, e não água: a barra de água segue em 20%."""
    assert LIMIAR_DE_ENERGIA_AVANCADO_PCT == 40.0
    assert LIMIAR_DE_ENERGIA_AVANCADO_PCT > LIMIAR_DE_AGUA_PCT


@pytest.mark.parametrize(("pct", "atende"), [
    (19.9, False),
    (20.0, True),      # o limiar é inclusivo: «20% ou mais»
    (20.1, True),
])
def test_a_fronteira_dos_vinte_por_cento_e_inclusiva(pct, atende):
    r = _avaliar(pluvial=250.0 * pct / 100.0, demanda=250.0)
    assert r.atende_o_padrao_de_agua is atende


def test_a_margem_diz_quanto_sobra_ou_falta():
    assert _avaliar(75.0).margem_pct == pytest.approx(10.0)     # 30% de 250
    assert _avaliar(25.0).margem_pct == pytest.approx(-10.0)    # 10% de 250


# ─────────────────────── o caso-base, que é a parte delicada ───────────────────

def test_sem_caso_base_declarado_usa_a_demanda_do_projeto_e_avisa():
    r = _avaliar(pluvial=100.0, demanda=400.0)
    assert r.consumo_base_anual_m3 == pytest.approx(400.0)
    assert r.base_declarada_pelo_usuario is False
    assert "piso" in r.ressalva


def test_caso_base_declarado_maior_reduz_o_percentual():
    """Com louças e metais eficientes, o caso-base do EDGE é maior que a demanda.

    O mesmo volume de chuva vale um percentual menor da barra, embora a barra
    total do projeto seja maior. É por isso que o número sem caso-base é piso.
    """
    sem = _avaliar(pluvial=100.0, demanda=400.0)
    com = _avaliar(pluvial=100.0, demanda=400.0, base=600.0)
    assert com.economia_de_agua_pct < sem.economia_de_agua_pct
    assert com.base_declarada_pelo_usuario is True


def test_o_caso_base_converte_de_litros_por_pessoa_dia():
    # 150 L/pessoa·dia, 4 pessoas, 365 dias = 219 m³/ano
    assert consumo_base_anual_m3(150.0, 4) == pytest.approx(219.0)


def test_caso_base_zero_ou_negativo_nao_e_aceito_como_declarado():
    r = _avaliar(pluvial=50.0, demanda=250.0, base=0.0)
    assert r.base_declarada_pelo_usuario is False
    assert r.consumo_base_anual_m3 == pytest.approx(250.0)


def test_demanda_nula_nao_divide_por_zero():
    r = _avaliar(pluvial=50.0, demanda=0.0)
    assert r.economia_de_agua_pct == 0.0
    assert r.atende_o_padrao_de_agua is False


def test_o_percentual_nunca_passa_de_cem():
    assert _avaliar(pluvial=900.0, demanda=250.0).economia_de_agua_pct == 100.0


# ────────────────────────────── as medidas de água ─────────────────────────────

def test_a_wem14_e_a_medida_que_este_programa_dimensiona():
    wem14 = [m for m in MEDIDAS_DE_AGUA if m.codigo == "WEM14"]
    assert len(wem14) == 1
    assert wem14[0].modelada_pelo_netuno is True
    assert "pluvial" in wem14[0].nome.lower()


def test_as_medidas_fora_do_escopo_estao_declaradas_como_tal():
    """Honestidade sobre o que não se modela vale mais que cobertura aparente."""
    fora = [m for m in MEDIDAS_DE_AGUA if not m.modelada_pelo_netuno]
    assert {m.codigo for m in fora} == {"WEM13", "WEM15"}
    for m in fora:
        assert m.observacao


# ──────────────────── o percurso até a matriz de créditos ──────────────────────

def _esg(area=180.0, pluvial=95.0, potavel=155.0):
    return calculate_esg_certifications(
        potable_savings_pct=pluvial / (pluvial + potavel) * 100.0,
        annual_pluvial_consumed_m3=pluvial,
        annual_potable_consumed_m3=potavel,
        net_co2e_saved_kg_lifetime=1200.0,
        catchment_area_m2=area,
    )


def test_o_edge_chega_ao_relatorio_consolidado():
    assert _esg().edge.economia_de_agua_pct > 0.0


def test_a_area_de_captacao_atravessa_ate_a_matriz():
    """Era o percurso em risco: sem ela, o campo da WEM14 sairia zerado."""
    linha = [c for c in _esg(area=240.0).credit_details if c.credit_code == "WEM14"]
    assert len(linha) == 1
    assert "240" in linha[0].notes


def test_a_matriz_diz_que_o_edge_nao_pontua():
    linha = [c for c in _esg().credit_details if c.credit_code == "WEM14"][0]
    assert "não atribui pontos" in linha.notes
    assert "pts" not in linha.points_or_level


def test_a_sintese_executiva_menciona_o_edge():
    assert "EDGE" in _esg().esg_summary_text


def test_mais_chuva_aproveitada_move_a_barra_de_agua():
    """Se a barra não se mexesse com a simulação, seria enfeite."""
    pouco = _esg(pluvial=30.0, potavel=220.0).edge.economia_de_agua_pct
    muito = _esg(pluvial=120.0, potavel=130.0).edge.economia_de_agua_pct
    assert muito > pouco


def test_o_edge_e_independente_da_pontuacao_leed():
    """São réguas diferentes: uma mede percentual, a outra soma pontos."""
    r = _esg(pluvial=60.0, potavel=190.0)
    assert r.edge.atende_o_padrao_de_agua is True     # 24% da demanda
    assert r.leed.total_leed_we_points >= 0            # o LEED tem sua própria faixa


# ─────────────────── o caso-base declarado tem campo e sobrevive ───────────────

def test_o_caso_base_e_um_campo_do_projeto_e_volta_ao_reabrir(tmp_path):
    """Parâmetro sem onde ser informado é o defeito que esta rodada corrigiu."""
    from netuno.core.parser import NetunoConfig, export_netuno_json, load_netuno_project

    cfg = NetunoConfig()
    assert hasattr(cfg, "edge_base_case_l_person_day")
    cfg.edge_base_case_l_person_day = 165.0

    caminho = str(tmp_path / "projeto.netuno")
    export_netuno_json(cfg, caminho)
    pacote = load_netuno_project(caminho)
    lido = pacote["config"] if isinstance(pacote, dict) else pacote
    assert lido.edge_base_case_l_person_day == pytest.approx(165.0)


def test_o_campo_da_tela_chega_ao_calculo(qapp):
    """Percurso tela → cálculo: o campo converte L/pessoa·dia em m³/ano."""
    pytest.importorskip("PySide6")
    from netuno.core.parser import NetunoConfig
    from netuno.ui.tab_environmental import TabEnvironmental

    aba = TabEnvironmental()
    assert aba._edge_base_case_annual_m3() is None      # em branco, não declarado

    aba.txt_edge_base.setText("150")
    janela = aba.window()
    janela.config = NetunoConfig()
    janela.config.residents_count = 4
    janela.config.num_economias = 1
    assert aba._edge_base_case_annual_m3() == pytest.approx(219.0)


def test_valor_ilegivel_no_campo_nao_derruba_a_tela(qapp):
    pytest.importorskip("PySide6")
    from netuno.ui.tab_environmental import TabEnvironmental

    aba = TabEnvironmental()
    for texto in ("abc", "-5", "0"):
        aba.txt_edge_base.setText(texto)
        assert aba._edge_base_case_annual_m3() is None
