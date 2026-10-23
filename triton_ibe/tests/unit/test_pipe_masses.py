"""Verificação das massas lineares de tubo.

Elas já foram cenário interno. O erro não era pequeno nem
sistemático: o DN 110 ficava 47% abaixo do peso real e o DN 20, 36% acima, de
modo que nem a ordem de grandeza se salvava para os diâmetros grandes — que são
justamente os da linha de captação.

Agora vêm de peso de produto (Amanco Wavin) para DN 20 a 60, e de geometria
normativa para os demais. Estes testes protegem a coerência interna dessa
tabela, que é o que um erro de digitação quebraria primeiro.
"""

from __future__ import annotations

import math

import pytest

from triton.core.environmental import (
    PIPE_EMISSION_FACTORS_PER_METER,
    PIPE_LINEAR_MASS_KG_PER_M,
    PIPE_LINEAR_MASS_SOURCE,
    PVC_PIPE_CO2E_PER_KG,
)

# Densidade efetiva calibrada nos seis pesos reais de produto, incluindo a bolsa.
DENSIDADE_EFETIVA_G_CM3 = 1.511

# Diâmetro externo e espessura de parede, das normas dimensionais.
GEOMETRIA_NBR_5648 = {75: (75.0, 4.2), 85: (85.0, 4.7), 110: (110.0, 6.1)}
GEOMETRIA_NBR_5688_REFORCADA = {100: (101.6, 2.5), 150: (150.0, 3.6)}


def massa_por_geometria(diametro_externo: float, espessura: float) -> float:
    """Massa linear de um tubo, em kg/m, pela seção anular."""
    area_mm2 = math.pi * espessura * (diametro_externo - espessura)
    volume_cm3_por_metro = area_mm2  # mm² × 1000 mm ÷ 1000 mm³/cm³
    return volume_cm3_por_metro * DENSIDADE_EFETIVA_G_CM3 / 1000.0


def test_toda_massa_declara_origem():
    assert set(PIPE_LINEAR_MASS_KG_PER_M) == set(PIPE_LINEAR_MASS_SOURCE)
    for dn, fonte in PIPE_LINEAR_MASS_SOURCE.items():
        assert fonte.strip(), f"DN {dn} sem origem declarada"


def test_massas_dos_diametros_de_pressao_batem_com_a_geometria():
    """Confere as entradas calculadas contra a própria fórmula.

    Se alguém editar um número à mão sem refazer a conta, este teste acusa.
    """
    for dn, (de, e) in GEOMETRIA_NBR_5648.items():
        assert PIPE_LINEAR_MASS_KG_PER_M[dn] == pytest.approx(massa_por_geometria(de, e), rel=1e-3)


def test_massas_dos_diametros_de_drenagem_batem_com_a_geometria():
    for dn, (de, e) in GEOMETRIA_NBR_5688_REFORCADA.items():
        assert PIPE_LINEAR_MASS_KG_PER_M[dn] == pytest.approx(massa_por_geometria(de, e), rel=1e-3)


def test_massa_cresce_com_o_diametro_dentro_de_cada_norma():
    """Monotonia dentro de cada família; entre famílias não vale.

    O DN 100 de drenagem é mais leve que o DN 85 de pressão, porque a parede é
    de 2,5 mm contra 4,7 mm. Isso não é erro: são normas e serviços distintos, e
    um teste que exigisse monotonia global estaria exigindo a coisa errada.
    """
    pressao = [20, 25, 32, 40, 50, 60, 75, 85, 110]
    drenagem = [100, 150]
    for familia in (pressao, drenagem):
        massas = [PIPE_LINEAR_MASS_KG_PER_M[dn] for dn in familia]
        assert massas == sorted(massas), familia


def test_emissao_por_metro_e_massa_vezes_fator():
    for dn, massa in PIPE_LINEAR_MASS_KG_PER_M.items():
        esperado = massa * PVC_PIPE_CO2E_PER_KG
        assert PIPE_EMISSION_FACTORS_PER_METER[dn] == pytest.approx(esperado, abs=1e-4)


def test_fator_do_tubo_e_o_da_epd():
    """A EPD declara 2,36 kg CO₂e por kg de tubo instalado, módulos A1–A3."""
    assert PVC_PIPE_CO2E_PER_KG == 2.36


def test_massas_em_faixa_fisicamente_plausivel():
    """Um tubo de PVC predial fica entre 0,1 e 4 kg/m nesta faixa de diâmetros."""
    for dn, massa in PIPE_LINEAR_MASS_KG_PER_M.items():
        assert 0.05 < massa < 5.0, f"DN {dn}: {massa} kg/m"


def test_densidade_implicita_e_coerente_em_todas_as_entradas():
    """Nenhuma linha pode implicar densidade absurda de PVC.

    Serve para os DN 20–60, que vêm de peso medido: se o peso e a espessura
    discordarem, a densidade implícita sai fora da faixa do PVC comercial.
    """
    espessuras = {20: 1.5, 25: 1.7, 32: 2.1, 40: 2.4, 50: 3.0, 60: 3.3}
    for dn, e in espessuras.items():
        area_mm2 = math.pi * e * (dn - e)
        densidade = PIPE_LINEAR_MASS_KG_PER_M[dn] * 1000.0 / area_mm2
        assert 1.35 < densidade < 1.65, f"DN {dn}: densidade implícita {densidade:.3f} g/cm³"
