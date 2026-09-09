"""O elo entre o assistente de motobomba e o cálculo de energia.

O assistente já fazia a hidráulica inteira: altura geométrica informada, perda de
carga estimada, altura manométrica resultante e seleção cruzada com o catálogo de
motobombas comerciais. O que faltava era o último passo — o retorno levava
potência, vazão, custo e diâmetros, e **descartava a altura manométrica e o
rendimento**, que são os dois parâmetros que o assistente existe para
determinar.

Quem rodasse o assistente e depois olhasse a emissão de bombeamento via um
cálculo que ignorava o desnível informado. Uma casa térrea e um sobrado davam a
mesma emissão.
"""

from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from netuno.core.pump_hydraulics import energia_especifica_kwh_por_m3  # noqa: E402
from netuno.ui.dialogs.pump_wizard_dialog import (  # noqa: E402
    PUMP_CATALOG,
    PumpSelectionWizardDialog,
)


@pytest.fixture
def assistente(qapp):
    return PumpSelectionWizardDialog(upper_tank_vol=500.0)


def test_o_catalogo_tem_bombas_reais_e_coerentes():
    assert len(PUMP_CATALOG) >= 5
    for bomba in PUMP_CATALOG:
        for campo in ("brand", "cv", "kw", "flow_lh", "max_h", "cost"):
            assert bomba.get(campo), f"{bomba.get('label')} sem {campo}"
        # kW e CV têm de concordar: 1 CV ≈ 0,7355 kW.
        assert bomba["kw"] == pytest.approx(bomba["cv"] * 0.7355, rel=0.12), bomba["label"]

    # Catálogo ordenado por porte, que é o que a seleção percorre.
    potencias = [b["kw"] for b in PUMP_CATALOG]
    assert potencias == sorted(potencias)


def test_a_altura_manometrica_sai_do_assistente(assistente):
    """Era calculada e descartada."""
    assistente.spin_h_geom.setValue(10.0)
    assistente.recalculate()
    dados = assistente.selected_pump_data

    assert dados["manometric_head_m"] > 0
    assert dados["geometric_head_m"] == pytest.approx(10.0)
    assert dados["head_loss_m"] >= 0
    # Manométrica é geométrica mais perdas.
    assert dados["manometric_head_m"] == pytest.approx(
        dados["geometric_head_m"] + dados["head_loss_m"], rel=1e-6
    )


def test_desnivel_maior_leva_a_bomba_maior(assistente):
    """É o propósito do assistente, e precisa continuar valendo."""
    potencias = []
    for altura in (4.0, 15.0, 40.0):
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        potencias.append(assistente.selected_pump_data["kw"])
    assert potencias == sorted(potencias)
    assert potencias[-1] > potencias[0]


def test_a_bomba_escolhida_vence_a_altura_pedida(assistente):
    """Selecionar bomba que não alcança o desnível seria erro de projeto."""
    for altura in (4.0, 10.0, 20.0, 35.0):
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        dados = assistente.selected_pump_data
        modelo = next(b for b in PUMP_CATALOG if b["kw"] == dados["kw"])
        assert modelo["max_h"] >= dados["manometric_head_m"], (
            f"{modelo['label']} não alcança {dados['manometric_head_m']:.1f} mca"
        )


def test_a_energia_por_m3_acompanha_o_desnivel(assistente):
    """O que se ganhou ao fechar o elo.

    Antes a energia saía da vazão nominal do catálogo, que não muda com a
    altura: casa térrea e sobrado davam o mesmo consumo por metro cúbico.
    """
    consumos = []
    for altura in (4.0, 15.0, 40.0):
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        dados = assistente.selected_pump_data
        consumos.append(
            energia_especifica_kwh_por_m3(
                dados["manometric_head_m"], dados["efficiency"] / 100.0
            )
        )
    assert consumos == sorted(consumos)
    assert consumos[-1] > 3 * consumos[0]


def test_o_rendimento_do_assistente_chega_ao_retorno(assistente):
    """Era o segundo parâmetro calculado e descartado."""
    assistente.spin_efficiency.setValue(62.0)
    assistente.recalculate()
    assert assistente.selected_pump_data["efficiency"] == pytest.approx(62.0)


def test_a_configuracao_nasce_sem_altura_informada():
    """Zero significa «não informada», e é o que faz a precedência funcionar.

    Com altura informada manda ρ·g·H/η; sem ela, a vazão informada; sem as duas,
    o valor de recurso. Se o padrão fosse um número, não haveria como distinguir
    «o usuário quis 12 m» de «ninguém informou nada».
    """
    from netuno.core.parser import NetunoConfig

    assert NetunoConfig().pump_manometric_head_m == 0.0
