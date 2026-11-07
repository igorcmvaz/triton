"""Os pacotes da Internacional e da Ibérica não levam arquivos, modelos nem avisos do Brasil.

Auditoria final da 0.1.0: logotipo CLIMBra rastreado fora da Brasil, modelos de projeto com Florianópolis,
aviso de «652 municípios» na janela de tarifas. A Brasil não muda.
"""
import json
import os
import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
BRL = os.environ.get("TRITON_EDITION", "BRL").strip().upper() == "BRL"
BRASIL = re.compile(r"Florian[oó]polis|CLIMBra|\bR\$|\bBRL\b|Brasil|Brazil|CASAN|CELESC|SINAPI|ANEEL|\b652\b|\bSC\b",
                    re.IGNORECASE)


@pytest.mark.skipif(BRL, reason="a Brasil leva o logotipo e os modelos do Brasil")
def test_o_logotipo_do_climbra_nao_vai_fora_da_brasil():
    achados = [p for pasta in ("icons", "docs/figuras", "manual/figuras")
               for p in (RAIZ / pasta).glob("CLIMBra.*")]
    assert achados == []


@pytest.mark.skipif(BRL, reason="a Brasil leva os modelos do Brasil")
@pytest.mark.parametrize("relativo", ["templates/template_projeto_base.triton", "examples/triton-cli-template.triton",
                                      "templates/README.md"])
def test_os_modelos_de_projeto_nao_citam_o_brasil(relativo):
    # «climbra_series» é o nome do campo no formato do projeto, igual nas três edições
    texto = (RAIZ / relativo).read_text(encoding="utf-8").replace("climbra_series", "")
    achado = BRASIL.search(texto)
    assert achado is None, achado.group(0)


@pytest.mark.skipif(BRL, reason="a Brasil leva o modelo do Brasil")
def test_o_modelo_cli_parte_da_localidade_e_dos_dados_da_edicao():
    modelo = json.loads((RAIZ / "examples" / "triton-cli-template.triton").read_text(encoding="utf-8"))
    fe = modelo["inputs"]["financial_and_economic"]
    assert modelo["analysis"]["environmental"]["grid_co2_factor_kg_kwh"] == 0.0
    assert fe["elec_tariff"] == 0.0 and all(v == 0.0 for v in modelo["inputs"]["capex_and_opex"].values())
    if os.environ.get("TRITON_EDITION", "").strip().upper() == "INT":
        assert modelo["rainfall"]["file_name"] == "NewYork.csv"
        assert fe["tariff_city_name"] == "New York City"
    else:
        assert modelo["rainfall"]["climate_city_name"] == "Lisboa"
        assert fe["tariff_city_name"] == "Lisboa"


def test_o_aviso_dos_652_municipios_so_aparece_na_brasil():
    """A janela de tarifas esconde o bloco do catálogo brasileiro e o aviso de auditoria fora da Brasil."""
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication, QLabel

    from triton.core.edition import projeto_novo_da_edicao, usa_dados_do_brasil
    from triton.ui.dialogs.dialog_economic import DialogTariffs

    app = QApplication.instance() or QApplication([])
    dialogo = DialogTariffs(None, projeto_novo_da_edicao())
    dialogo.show()
    app.processEvents()
    try:
        assert dialogo.box_disclaimer.isVisibleTo(dialogo) == usa_dados_do_brasil()
        visiveis = [r.text() for r in dialogo.findChildren(QLabel) if r.isVisibleTo(dialogo)]
        if not usa_dados_do_brasil():
            assert not [t for t in visiveis if re.search(r"\b652\b|igorcmvaz|Auditoria Tarif", t)], visiveis
    finally:
        dialogo.close()
