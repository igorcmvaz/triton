"""Na varredura, cada volume é uma cisterna diferente e tem preço próprio.

A linha de comando cobrava o preço declarado no projeto para todos os volumes
da varredura, de 1.000 L a 20.000 L. O custo não crescia com a capacidade, o
VPL só subia, e o ótimo econômico caía no fim da curva — enquanto a aba
econômica da interface, que precifica cada volume, apontava outro volume para
o mesmo projeto. Os testes abaixo prendem a CLI ao mesmo preço da interface.
"""
import os

import pytest

from netuno.cli import _get_precipitation, _load_bundle, _preco_da_cisterna, run_analysis
from netuno.core.cost_estimates import estimate_preliminary_capex

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASO = os.path.join(RAIZ, "manual", "casos", "02_tutorial_varredura.netuno")


def load_project_file(caminho):
    bundle = _load_bundle(caminho)
    return bundle["config"], _get_precipitation(bundle)


@pytest.fixture(scope="module")
def relatorio():
    cfg, precip = load_project_file(CASO)
    return run_analysis(cfg, precip, "economic"), cfg


def test_o_preco_da_cisterna_e_o_mesmo_da_interface(relatorio):
    _, cfg = relatorio
    for volume in (1000.0, 4000.0, 12000.0):
        interface = estimate_preliminary_capex(
            volume, cfg.upper_tank_vol, bool(cfg.upper_tank_used), cfg.pump_power_kw,
            cfg.pump_count, lower_material=cfg.lower_tank_material,
            upper_material=cfg.upper_tank_material)["lower"]
        assert _preco_da_cisterna(cfg, volume) == pytest.approx(interface)


def test_o_capex_cresce_com_o_volume_na_varredura(relatorio):
    rel, _ = relatorio
    linhas = [l for l in rel["economic"]["alternatives"] if l["lower_tank_volume_l"] > 0]
    capex = [l["capex_brl"] for l in sorted(linhas, key=lambda l: l["lower_tank_volume_l"])]
    assert all(b > a for a, b in zip(capex, capex[1:])), capex


def test_o_vpl_tem_maximo_interior(relatorio):
    rel, _ = relatorio
    linhas = sorted((l for l in rel["economic"]["alternatives"] if l["lower_tank_volume_l"] > 0),
                    key=lambda l: l["lower_tank_volume_l"])
    vpl = [l["npv_brl"] for l in linhas]
    melhor = vpl.index(max(vpl))
    assert 0 < melhor < len(vpl) - 1, "o VPL máximo caiu na borda da varredura"
    assert vpl[-1] < max(vpl)


def test_volume_unico_mantem_o_preco_declarado():
    cfg, precip = load_project_file(CASO)
    rel = run_analysis(cfg, precip, "economic", volume=4000.0)
    declarado = cfg.cost_lower_tank
    # o CAPEX do volume único parte do preço que o projeto declarou
    assert rel["economic"]["alternatives"][0]["capex_brl"] >= declarado
