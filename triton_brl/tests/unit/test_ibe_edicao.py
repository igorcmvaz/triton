# -*- coding: utf-8 -*-
"""«IBE» é sinónimo de edição (como «POR»); o valor interno, o rótulo e a pasta continuam «PRT»."""
import os
import subprocess
import sys

import pytest

from triton.core import edition as E

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.parametrize("codigo", ["IBE", "ibe", " Ibe ", "POR", "PRT"])
def test_ibe_e_por_abrem_como_prt(monkeypatch, codigo):
    monkeypatch.setenv("TRITON_EDITION", codigo)
    assert E.get_current_edition() == "PRT"
    assert E.is_prt_edition() and E.usa_dados_de_portugal() and not E.usa_dados_do_brasil()
    assert E.rotulo_da_edicao(curto=True) == "PRT"


def test_set_current_edition_ibe_grava_o_valor_interno_prt(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    E.set_current_edition("IBE")
    assert os.environ["TRITON_EDITION"] == "PRT"
    assert E.get_current_edition() == "PRT"


def test_ibe_nao_cria_um_quarto_valor_de_edicao():
    assert E.EDICOES == ("BRL", "INT", "PRT")
    assert "IBE" not in E.EDICOES


def test_em_processo_novo_tritonedition_ibe_abre_como_prt():
    env = dict(os.environ, TRITON_EDITION="IBE")
    saida = subprocess.run(
        [sys.executable, "-c", "from triton.core import edition as e; print(e.get_current_edition())"],
        cwd=RAIZ, env=env, capture_output=True, text=True, timeout=120)
    assert saida.stdout.strip() == "PRT", saida.stderr


def test_edicao_invalida_continua_a_cair_na_brl(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "XYZ")
    assert E.get_current_edition() == "BRL"
    with pytest.raises(ValueError):
        E.set_current_edition("XYZ")
