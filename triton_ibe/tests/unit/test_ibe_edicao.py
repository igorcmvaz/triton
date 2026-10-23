# -*- coding: utf-8 -*-
"""A edição chama-se «IBE» (Triton IBE, Península Ibérica); «PRT» e «POR», os nomes antigos, são sinónimos dela."""
import os
import subprocess
import sys

import pytest

from triton.core import edition as E

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.parametrize("codigo", ["IBE", "ibe", " Ibe ", "POR", "por", "PRT", "prt", " Prt "])
def test_ibe_prt_e_por_abrem_como_ibe(monkeypatch, codigo):
    monkeypatch.setenv("TRITON_EDITION", codigo)
    assert E.get_current_edition() == "IBE"
    assert E.is_ibe_edition() and E.is_prt_edition() and E.usa_dados_de_portugal()
    assert not E.usa_dados_do_brasil() and not E.is_int_edition() and not E.is_brl_edition()
    assert E.rotulo_da_edicao(curto=True) == "IBE"
    assert E.rotulo_da_edicao() == "Edição Ibérica (IBE)"


@pytest.mark.parametrize("codigo", ["IBE", "PRT", "POR"])
def test_set_current_edition_grava_sempre_o_valor_interno_ibe(monkeypatch, codigo):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    E.set_current_edition(codigo)
    assert os.environ["TRITON_EDITION"] == "IBE"
    assert E.get_current_edition() == "IBE"


def test_o_valor_interno_e_ibe_e_prt_e_so_um_alias():
    assert E.EDITION_IBE == "IBE" and E.EDITION_PRT == "IBE"
    assert E.EDICOES == ("BRL", "INT", "IBE")
    assert "PRT" not in E.EDICOES and "POR" not in E.EDICOES
    assert E.is_prt_edition is E.is_ibe_edition


@pytest.mark.parametrize("codigo", ["IBE", "PRT", "POR"])
def test_em_processo_novo_tritonedition_abre_como_ibe(codigo):
    env = dict(os.environ, TRITON_EDITION=codigo)
    saida = subprocess.run(
        [sys.executable, "-c", "from triton.core import edition as e; print(e.get_current_edition())"],
        cwd=RAIZ, env=env, capture_output=True, text=True, timeout=120)
    assert saida.stdout.strip() == "IBE", saida.stderr


@pytest.mark.parametrize("codigo", ["ibe", "IBE", "prt", "PRT", "por", "POR"])
def test_a_linha_de_comando_aceita_os_tres_nomes(monkeypatch, codigo):
    """``--edition`` do main.py: as seis grafias estão entre as escolhas e viram «IBE»."""
    texto = open(os.path.join(RAIZ, "main.py"), encoding="utf-8").read()
    assert f'"{codigo}"' in texto
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    E.set_current_edition(codigo)
    assert os.environ["TRITON_EDITION"] == "IBE"


def test_o_nome_ibe_e_o_visivel_e_nao_sobra_portugal_pt_no_rotulo(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "PRT")
    assert "PRT" not in E.rotulo_da_edicao() and "Portugal" not in E.rotulo_da_edicao()


def test_edicao_invalida_continua_a_cair_na_brl(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "XYZ")
    assert E.get_current_edition() == "BRL"
    with pytest.raises(ValueError):
        E.set_current_edition("XYZ")
