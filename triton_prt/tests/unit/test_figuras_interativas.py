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
from triton.core.edition import get_current_edition  # noqa: E402

EDICAO = get_current_edition()


def texto_do_manual():
    """O manual montado da edição: o inglês na INT (é o que ela publica), o principal nas demais."""
    if EDICAO == "INT":
        caminho = os.path.join(MANUAL, "en", "Triton-User-Manual.md")
        if os.path.exists(caminho):
            return open(caminho, encoding="utf-8").read()
    return open(os.path.join(MANUAL, "Manual-Triton.md"), encoding="utf-8").read()


@pytest.fixture(scope="module")
def dados():
    return gi.dados()


def test_cada_figura_interativa_existe_no_manual(dados):
    """O site troca a figura pelo nome do arquivo; renomear uma apagaria a interativa em silêncio."""
    texto = texto_do_manual()
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
    caixa = dados["fig08_fluxo_de_caixa.png"]["casos"]
    carbono = dados["fig06_carbono_no_tempo.png"]["casos"]
    if EDICAO == "INT":
        # Nova York, com a tarifa publicada e os custos ilustrativos do tutorial: não há retorno
        # financeiro, e o retorno de carbono do polietileno é de 12,4 anos (concreto: 32,5).
        assert dados["fig47_permanencia.png"]["estados"]["4000"][4] == pytest.approx(26.83, abs=0.005)
        assert caixa["4000|CONCRETO"]["retorno"] is None
        assert caixa["4000|ACO_INOX"]["retorno"] is None
        assert carbono["4000|PEAD"][4] == pytest.approx(12.4, abs=0.05)
        assert carbono["4000|CONCRETO"][4] > 30
        return
    assert dados["fig47_permanencia.png"]["estados"]["4000"][4] == pytest.approx(27.12, abs=0.005)
    assert caixa["4000|CONCRETO"]["retorno"] == pytest.approx(16.3, abs=0.05)
    assert caixa["4000|ACO_INOX"]["retorno"] is None
    assert carbono["4000|PEAD"][4] == pytest.approx(16.3, abs=0.05)
    assert carbono["4000|CONCRETO"][4] > 20


def test_a_grade_dos_dez_dias_cobre_o_caso_do_texto(dados):
    d = dados["fig01_dez_dias.png"]
    capacidade, descarte = d["padrao"]
    assert f"{capacidade}|{descarte:g}" in d["casos"]
    if EDICAO == "INT":
        # Nova York, 21 a 30/09/2018: o dia 3 (1,9 mm) capta 162 L sem descarte e nada com 2 mm; o dia 5
        # (59,8 mm) extravasa 2.913 L num tanque de 2.000 L (os números da seção do balanço diário).
        assert d["casos"]["2000|0"][2][1] == 162
        assert d["casos"]["2000|2"][2][1] == 0
        assert d["casos"]["2000|2"][4][5] == 2913
        return
    assert d["casos"]["2000|0"][2][1] == 136          # 1,6 mm sem descarte
    assert d["casos"]["3000|2"][5][5] == 0            # dia 6 não extravasa
