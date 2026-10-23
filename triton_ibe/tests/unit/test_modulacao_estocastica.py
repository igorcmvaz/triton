# -*- coding: utf-8 -*-
"""Modulação probabilística: o estudo refeito com per capita, pessoas e fração não potável sorteados."""
from pathlib import Path

import pytest

from triton.cli import _get_precipitation, _load_bundle
from triton.core import modulacao_estocastica as M

RAIZ = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------- custos, tarifas e horizonte


# ---------------------------------------------------------------- modelos climáticos


_caso_09_en = RAIZ / "manual" / "casos" / "09_modulation_tutorial.triton"
_caso_09_pt = RAIZ / "manual" / "casos" / "09_modulacao_tutorial.triton"
_c09 = _caso_09_en if _caso_09_en.exists() else _caso_09_pt

_caso_10_en = RAIZ / "manual" / "casos" / "10_modulation_catchment.triton"
_caso_10_pt = RAIZ / "manual" / "casos" / "10_modulacao_captacao.triton"
_c10 = _caso_10_en if _caso_10_en.exists() else _caso_10_pt

CASOS_MODULACAO = [
    (str(_c09.name), 0) if _c09.exists() else ("10_modulacao_tutorial.triton", 0),
    (str(_c10.name), 0) if _c10.exists() else ("11_modulacao_climbra.triton", 19),
]


@pytest.mark.parametrize("arquivo, modelos", CASOS_MODULACAO)
def test_casos_de_modulacao_abrem_montados_e_centrados_no_projeto(arquivo, modelos):
    """Os exemplos da ferramenta: modulação gravada, N de mil e triagem centrada no projeto relido."""
    b = _load_bundle(str(RAIZ / "manual" / "casos" / arquivo))
    cfg = b["config"]
    estado = b["ui_state"]["modulacao_estocastica"]
    assert estado["amostras"] == 1000 and estado["semente"] == 42
    par = M.ParametrosIncertos.de_dict(estado["parametros"])
    par.validar()
    assert len(par.modelos_climaticos) == modelos
    assert cfg.lower_tank_mode == 1  # varredura: as figuras por volume têm o que mostrar
    for chave in M.CATALOGO:
        assert par.variaveis[chave].valor_central() == pytest.approx(M.valor_do_projeto(cfg, chave), abs=1e-9), chave
