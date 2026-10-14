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

from triton.core.environmental import (  # noqa: E402
    EnvironmentalConfig,
    calculate_lca,
    pump_embodied_co2_is_extrapolated,
)
from triton.core.environmental_justifications import (  # noqa: E402
    get_operational_justification,
    get_pipe_justification,
    get_pump_justification,
)
from triton.core.grid_emission_factors import (  # noqa: E402
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
    from triton.core.environmental import PUMP_EMBEDDED_CO2, PUMP_MASS_KG, PUMP_KG_CO2E_POR_KG
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


# ─────────────────────────────── pureza do produto ─────────────────────────────


# ──────────────────────── o diálogo entrega o que o usuário escolheu ───────────

@pytest.fixture
def aba(qapp):
    from triton.ui.tab_environmental import TabEnvironmental
    return TabEnvironmental()


# ─────────────── o diálogo constrói, mostra a procedência e devolve ────────────

@pytest.fixture
def dialogo(aba, qapp):
    from triton.ui.tab_environmental import LCAParametersDialog
    return LCAParametersDialog(aba)


def test_a_justificativa_do_tubo_aparece_no_campo(dialogo):
    """Estava implementada e não era chamada em lugar nenhum."""
    for dn in (50, 75, 100, 150):
        campo = dialogo.txt_pipes_co2[dn]
        assert campo.justification is not None, dn


def test_a_justificativa_da_bomba_aparece_com_a_fonte(dialogo):
    """O método era um `pass`: existia só para não quebrar os signals.

    Até a 1.0.0 beta a potência de 2 CV era extrapolada e o diálogo avisava. Agora
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
