# -*- coding: utf-8 -*-
"""Testes do gerador de figuras dos estudos de Santa Catarina (sem rodar simulações)."""
import importlib.util
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "scripts" / "gerar_graficos_artigos.py"


def _modulo():
    spec = importlib.util.spec_from_file_location("gerar_graficos_artigos", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_help_funciona():
    r = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True,
                       encoding="utf-8")
    assert r.returncode == 0
    assert "--idioma" in r.stdout and "--formatos" in r.stdout


def test_formato_numerico_por_idioma():
    m = _modulo()
    assert m.num(1234.5, 1, "pt-BR") == "1.234,5"
    assert m.num(1234.5, 1, "en-GB") == "1,234.5"
    assert m.num(-2.0, 0, "en-GB") == "−2"
    assert m.num_auto(3.0, "pt-BR") == "3" and m.num_auto(0.25, "pt-BR") == "0,25"


def test_paleta_unica_e_distinta_por_tipologia():
    m = _modulo()
    slots = [t["slot"] for t in m.TIPOLOGIAS]
    assert slots == sorted(set(slots)) and len(slots) == 6
    assert len(set(m.CORES_CLARO)) == 6 and len(set(m.CORES_ESCURO)) == 6
    assert len({t["marcador"] for t in m.TIPOLOGIAS}) == 6


def test_quantis_e_escala():
    m = _modulo()
    med, lo, hi = m.quantis([1, 2, 3, 4, 5, float("nan")])
    assert (med, lo, hi) == (3.0, 1.4, 4.6)
    assert m.escolher_escala([1.2e6, -3], "moeda", "en-GB") == (1e6, "R$ million")
    assert m.escolher_escala([500], "massa", "pt-BR") == (1, "kg")


def test_formatos_invalidos_retornam_2(tmp_path):
    m = _modulo()
    assert m.principal(["--saida", str(tmp_path), "--formatos", "gif"]) == 2
