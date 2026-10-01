"""Os controles da tela de parâmetros da ACV chegam ao cálculo.

Um controle que não alimenta o motor repete exatamente o defeito que existe
para corrigir: valor escolhido na interface e ignorado no resultado. Estes
testes fecham o percurso de cada um dos quatro que entraram nesta versão.

Também fixam duas justificativas que estavam implementadas e não eram chamadas
em lugar nenhum — tubulação e motobomba eram os únicos parâmetros do módulo
ambiental sem procedência visível ao usuário, e são os dois que mais mudaram.
"""

from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from netuno.core.chlorination import PUREZA_PADRAO  # noqa: E402
from netuno.core.environmental import (  # noqa: E402
    EnvironmentalConfig,
    calculate_lca,
    pump_embodied_co2_is_extrapolated,
)
from netuno.core.environmental_justifications import (  # noqa: E402
    get_operational_justification,
    get_pipe_justification,
    get_pump_justification,
)
from netuno.core.grid_emission_factors import (  # noqa: E402
    BASE_PADRAO,
    bases_disponiveis,
    fator_co2eq,
    procedencia_da_base,
)


# ─────────────────────────── justificativas antes órfãs ────────────────────────

def test_a_tubulacao_tem_justificativa_para_os_diametros_documentados():
    for dn in (50, 75, 100, 150):
        just = get_pipe_justification(dn)
        assert just is not None, dn
        assert just.title


def test_a_motobomba_tem_justificativa_nas_seis_potencias_comerciais():
    for cv in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0):
        assert get_pump_justification(cv) is not None, cv


def test_a_motobomba_nao_tem_mais_valor_extrapolado():
    """Quatro dos seis valores eram escalonamento aritmético do de meio cavalo.

    Agora cada potência é massa de catálogo vezes a intensidade por quilo de uma
    EPD, e nenhuma é extrapolada. A função continua existindo para que a
    interface volte a sinalizar se uma potência sem fonte for acrescentada.
    """
    from netuno.core.environmental import PUMP_EMBEDDED_CO2, PUMP_MASS_KG, PUMP_KG_CO2E_POR_KG
    assert PUMP_KG_CO2E_POR_KG == pytest.approx(10.4 / 2.179)
    for cv, massa in PUMP_MASS_KG.items():
        assert not pump_embodied_co2_is_extrapolated(cv), cv
        assert PUMP_EMBEDDED_CO2[cv] == pytest.approx(massa * PUMP_KG_CO2E_POR_KG, abs=0.05)
    # A massa, e portanto a emissão, cresce com a potência.
    valores = [PUMP_EMBEDDED_CO2[cv] for cv in sorted(PUMP_EMBEDDED_CO2)]
    assert valores == sorted(valores)


def test_a_pureza_tem_justificativa_propria():
    """Passou a ser editável, e todo campo editável daquela tela é justificado."""
    just = get_operational_justification("chlorine_purity")
    assert just is not None
    assert "pureza" in just.calculation_basis.lower()


# ────────────────────────────── base do fator da rede ──────────────────────────

def test_cada_base_nomeada_declara_gas_e_fronteira():
    """Sem isso as bases pareceriam intercambiáveis, e não são.

    A série do MCTI contabiliza CO2 apenas, e apenas da geração; as demais são
    CO2-equivalente com fronteira mais larga. Trocar uma pela outra sem dizer
    qual é qual foi o que produziu a divergência entre módulos.
    """
    bases = bases_disponiveis()
    assert len(bases) >= 3
    for chave in bases:
        proc = procedencia_da_base(chave)
        assert proc.get("fonte"), chave
        assert proc.get("gas"), chave
        assert proc.get("fronteira"), chave


def test_escolher_a_base_muda_o_resultado_da_acv():
    valores = {c: fator_co2eq(c) for c in bases_disponiveis()}
    assert len(set(valores.values())) > 1, "bases idênticas não seriam escolha"

    menor = min(valores, key=valores.get)
    maior = max(valores, key=valores.get)
    base = dict(annual_water_saved_m3=120.0, annual_pump_kwh=200.0)
    r_menor = calculate_lca(5000.0, 120.0, EnvironmentalConfig(
        grid_co2_factor_kg_kwh=valores[menor], grid_co2_factor_basis=menor, **base))
    r_maior = calculate_lca(5000.0, 120.0, EnvironmentalConfig(
        grid_co2_factor_kg_kwh=valores[maior], grid_co2_factor_basis=maior, **base))
    assert r_maior.annual_pumping_co2_kg > r_menor.annual_pumping_co2_kg


def test_a_base_padrao_existe_e_e_nomeada():
    assert BASE_PADRAO in bases_disponiveis()
    assert EnvironmentalConfig().grid_co2_factor_basis == BASE_PADRAO


# ─────────────────────────────── pureza do produto ─────────────────────────────

def test_a_pureza_muda_a_massa_de_produto_na_acv():
    """O efeito é de 1/pureza, e a pureza não era editável.

    Quem clora com água sanitária (cerca de 10% de cloro ativo) precisa de seis
    vezes mais produto que quem usa pastilha, e via o mesmo número.
    """
    def massa(pureza: float) -> float:
        cfg = EnvironmentalConfig(
            annual_water_saved_m3=120.0,
            chlorine_product_purity=pureza,
            etap_enabled=False,   # isola o efeito da pureza no termo de cloração
        )
        return calculate_lca(5000.0, 120.0, cfg).annual_chlorine_kg

    assert massa(0.325) == pytest.approx(2 * massa(0.65), rel=1e-9)
    assert massa(PUREZA_PADRAO) == pytest.approx(massa(0.65), rel=1e-9)


# ──────────────────────── o diálogo entrega o que o usuário escolheu ───────────

@pytest.fixture
def aba(qapp):
    from netuno.ui.tab_environmental import TabEnvironmental
    return TabEnvironmental()


def test_a_aba_entrega_a_pureza_e_a_base_escolhidas(aba):
    """O diálogo grava as duas no estado da aba, e `get_config` as lê.

    Se `get_config` não as lesse, o controle seria decorativo — que é o defeito
    que ele existe para corrigir.
    """
    aba._pureza_do_cloro = 0.10
    aba._base_do_fator_da_rede = "sidac"
    cfg = aba.get_config()
    assert cfg.chlorine_product_purity == pytest.approx(0.10)
    assert cfg.grid_co2_factor_basis == "sidac"


def test_a_aba_entrega_a_escolha_de_desinfeccao_do_projeto(aba, monkeypatch):
    """A escolha feita na Etapa 2 tem de atravessar até a ACV."""
    from netuno.core.parser import NetunoConfig

    proj = NetunoConfig()
    proj.water_quality_disinfection = "uv"
    proj.water_quality_polishing = True
    proj.area = 320.0

    class _Janela:
        config = proj

    monkeypatch.setattr(type(aba), "window", lambda self: _Janela(), raising=False)
    cfg = aba.get_config()
    assert cfg.water_quality_disinfection == "uv"
    assert cfg.water_quality_polishing is True
    assert cfg.roof_area_m2 == pytest.approx(320.0)


def test_a_pureza_fora_da_faixa_e_contida(aba):
    """Zero ou negativo dividiria por zero na conversão de massa."""
    aba._pureza_do_cloro = 0.0
    assert aba.get_config().chlorine_product_purity > 0.0
    aba._pureza_do_cloro = 5.0
    assert aba.get_config().chlorine_product_purity <= 1.0


# ─────────────── o diálogo constrói, mostra a procedência e devolve ────────────

@pytest.fixture
def dialogo(aba, qapp):
    from netuno.ui.tab_environmental import LCAParametersDialog
    return LCAParametersDialog(aba)


def test_o_dialogo_constroi_com_os_controles_novos(dialogo):
    """Um campo que só aparece na tela é o que este teste protege.

    Os testes de núcleo não constroem o diálogo, de modo que um erro de
    montagem passaria despercebido até o usuário abrir a janela.
    """
    assert dialogo.txt_chlorine_purity is not None
    assert dialogo.cmb_base_rede.count() >= 3


def test_o_dialogo_abre_em_tela_cheia(dialogo):
    from PySide6.QtCore import Qt

    assert dialogo.windowState() & Qt.WindowMaximized


def test_escolher_a_base_reescreve_o_fator_e_mostra_a_procedencia(dialogo):
    """Era o ponto: as bases não eram selecionáveis, só o número era editável."""
    valores = {}
    for i in range(dialogo.cmb_base_rede.count()):
        dialogo.cmb_base_rede.setCurrentIndex(i)
        chave = dialogo.cmb_base_rede.currentData()
        valores[chave] = float(dialogo.txt_grid_co2.text().replace(",", "."))
        assert dialogo.lbl_base_rede_fonte.text().strip(), chave

    for chave, valor in valores.items():
        assert valor == pytest.approx(fator_co2eq(chave), abs=5e-5), chave
    assert len(set(valores.values())) > 1


def test_a_justificativa_do_tubo_aparece_no_campo(dialogo):
    """Estava implementada e não era chamada em lugar nenhum."""
    for dn in (50, 75, 100, 150):
        campo = dialogo.txt_pipes_co2[dn]
        assert campo.justification is not None, dn


def test_a_justificativa_da_bomba_aparece_com_a_fonte(dialogo):
    """O método era um `pass`: existia só para não quebrar os signals.

    Até a 5.0.0 beta a potência de 2 CV era extrapolada e o diálogo avisava. Agora
    todas as potências têm massa de catálogo e intensidade de EPD, e a justificativa
    mostra as duas fontes em vez do aviso.
    """
    for cv in ("0,5", "2,0"):
        dialogo.txt_pump_cv.setText(cv)
        dialogo._update_pump_co2_justification()
        just = dialogo.txt_pump_co2.justification
        assert just is not None, cv
        assert "EXTRAPOLADO" not in just.detailed_explanation, cv
        assert "EPD" in just.source_reference and "Dancor" in just.source_reference, cv


def test_salvar_devolve_a_pureza_e_a_base_para_a_aba(dialogo, aba):
    """Sem isto o valor escolhido morreria ao fechar a janela."""
    dialogo.txt_chlorine_purity.setText("0,10")
    idx = dialogo.cmb_base_rede.findData("sidac")
    if idx >= 0:
        dialogo.cmb_base_rede.setCurrentIndex(idx)
    dialogo.save_and_accept()

    assert aba._pureza_do_cloro == pytest.approx(0.10)
    assert aba.get_config().chlorine_product_purity == pytest.approx(0.10)
    if idx >= 0:
        assert aba.get_config().grid_co2_factor_basis == "sidac"
