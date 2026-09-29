"""Valores calculados e não inseridos no documento.

O gerador formatava três números e usava dois. Não eram números errados: eram
números corretos que ficavam na variável e não chegavam ao papel.

Dois testes fecham o percurso de cada um, e um terceiro cobre o que a ligação
da ETAP acrescentou: sem nomear os estágios de desinfecção, dois laudos com
valores de tratamento muito diferentes ficariam indistinguíveis, e o leitor não
saberia que a diferença está na escolha, e não em erro de cálculo.
"""

from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from netuno.core.environmental import (  # noqa: E402
    EnvironmentalConfig,
    calculate_lca,
)
from netuno.core.report_generator import (  # noqa: E402
    generate_environmental_html_report,
    generate_executive_html_report,
)

PROJETO = {
    "ref_code": "NET-OMIT-001",
    "rain_file": "ClimaFpolis.csv",
    "area": 250.0,
    "runoff": 0.85,
    "discard": 2.0,
    "residents": 5,
    "demand": 150.0,
    "share": 0.40,
    "lower_vol": 5000.0,
    "potential_pct": 35.5,
    "pluv_day": 120.0,
    "potable_day": 180.0,
    "spill_day": 40.0,
    "sat_full": 62.0,
    "sat_null": 13.7,
    "capex": 9500.0,
    "annual_gross": 3200.0,
    "vpl": 28500.0,
    "tir": 26.5,
    "payback_s": "4,1",
    "payback_d": "5,5",
    "annual_pluvial_m3": 120.0,
}


def test_o_laudo_executivo_traz_a_confiabilidade(qapp):
    """Dizer que 62% dos dias tiveram atendimento integral não diz o resto.

    O percentual de dias em que a demanda pluvial não foi atendida é o indicador
    de confiabilidade que o leitor procura, e era calculado e descartado.
    """
    html = generate_executive_html_report(PROJETO)
    assert "13,7" in html
    assert "Atendimento Nulo" in html


def _acv(metodo: str):
    cfg = EnvironmentalConfig(
        annual_water_saved_m3=120.0,
        water_quality_disinfection=metodo,
    )
    return calculate_lca(5000.0, 120.0, cfg)


def test_o_laudo_ambiental_traz_a_dose_de_cloro(qapp):
    """A tabela mostrava a massa anual sem a dose que a origina.

    Sem a dose não há como conferir a conta, que é a razão de a tabela existir.
    """
    lca = _acv("cloro")
    html = generate_environmental_html_report(PROJETO, lca_result=lca)
    assert "mg Cl2/L" in html
    assert "produto/ano" in html


def test_o_laudo_ambiental_nomeia_os_estagios_de_desinfeccao(qapp):
    uv = generate_environmental_html_report(PROJETO, lca_result=_acv("uv"))
    assert "ultravioleta" in uv.lower()

    cloro = generate_environmental_html_report(PROJETO, lca_result=_acv("cloro"))
    assert "ultravioleta" not in cloro.lower()


def test_a_emissao_por_litro_continua_no_cartao(qapp):
    """Estava listada como omitida e não estava: aparece sob o payback ambiental.

    O teste a fixa para que a correção das outras duas não a derrube.
    """
    html = generate_environmental_html_report(PROJETO, lca_result=_acv("cloro"))
    assert "g CO2e/L" in html
