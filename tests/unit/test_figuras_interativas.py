"""As figuras interativas do site continuam presas às figuras e aos números do manual."""
import os
import re
import sys

import pytest

pytest.importorskip("matplotlib", reason="as figuras do manual são desenhadas com matplotlib")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")
sys.path.insert(0, MANUAL)

import gerar_figuras_interativas as gi  # noqa: E402


@pytest.fixture(scope="module")
def dados():
    return gi.dados()


def test_cada_figura_interativa_existe_no_manual(dados):
    """O site troca a figura pelo nome do arquivo; renomear uma apagaria a interativa em silêncio."""
    texto = open(os.path.join(MANUAL, "Manual-Netuno-5.md"), encoding="utf-8").read()
    js = open(os.path.join(MANUAL, "site_interativas.js"), encoding="utf-8").read()
    desenhadas = set(re.findall(r'FI\["([^"]+)"\] = \{', js))
    for arquivo in dados:
        assert os.path.exists(os.path.join(MANUAL, "figuras", arquivo)), arquivo
        assert f"figuras/{arquivo})" in texto, arquivo
        assert arquivo in desenhadas, arquivo


def test_o_balanco_de_cada_dia_fecha(dados):
    d = dados["fig01_dez_dias.png"]
    for caso, dias in d["casos"].items():
        inicio = 0
        for dia in dias:
            captado, consumo, extravasado, fim = dia[1], dia[3], dia[5], dia[6]
            assert abs(inicio + captado - consumo - extravasado - fim) <= 1, caso
            inicio = fim


def test_o_projeto_do_tutorial_da_os_numeros_do_manual(dados):
    """Os textos «Experimente» citam estes valores."""
    assert dados["fig47_permanencia.png"]["estados"]["4000"][4] == pytest.approx(27.12, abs=0.005)
    caixa = dados["fig08_fluxo_de_caixa.png"]["casos"]
    assert caixa["4000|CONCRETO"]["retorno"] == pytest.approx(16.3, abs=0.05)
    assert caixa["4000|ACO_INOX"]["retorno"] is None
    carbono = dados["fig06_carbono_no_tempo.png"]["casos"]
    assert carbono["4000|PEAD"][4] == pytest.approx(16.3, abs=0.05)
    assert carbono["4000|CONCRETO"][4] > 20


def test_a_grade_dos_dez_dias_cobre_o_caso_do_texto(dados):
    d = dados["fig01_dez_dias.png"]
    capacidade, descarte = d["padrao"]
    assert f"{capacidade}|{descarte:g}" in d["casos"]
    assert d["casos"]["2000|0"][2][1] == 136          # 1,6 mm sem descarte
    assert d["casos"]["3000|2"][5][5] == 0            # dia 6 não extravasa
