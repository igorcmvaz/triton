"""Os PDFs de exemplo da IBE (Lisboa e Porto, com a E-OBS) trazem o aviso vermelho de uso não comercial.

Decisão do titular (25/10/2026). Os de série própria (Funchal) e os da INT não o levam. Regerar com
``scripts/gerar_relatorios_exemplo.py``, que também confere o rodapé.
"""
import os
import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
EXEMPLOS = RAIZ / "reports" / "exemplos"
IBE = os.environ.get("TRITON_EDITION", "BRL").strip().upper() == "IBE"
fitz = pytest.importorskip("fitz")


def _texto(pdf: Path) -> str:
    with fitz.open(pdf) as d:
        return re.sub(r"\s+", " ", " ".join(p.get_text() for p in d))


@pytest.mark.skipif(not IBE, reason="só a IBE usa a E-OBS")
@pytest.mark.parametrize("cidade", ["lisboa", "porto"])
def test_os_pdfs_da_e_obs_trazem_o_aviso_vermelho_a_licenca_e_a_qualidade(cidade):
    pdfs = sorted((EXEMPLOS / cidade).glob("*_pt.pdf"))
    assert len(pdfs) == 3
    for pdf in pdfs:
        t = _texto(pdf)
        assert "NÃO PODE SER USADA COMERCIALMENTE" in t, pdf.name
        assert "o titular do programa não responde por uso comercial" in t, pdf.name
        assert "Cornes" in t and "Qualidade da chuva" in t and "Cobertura" in t, pdf.name


@pytest.mark.skipif(not IBE, reason="só a IBE tem o Funchal")
def test_o_pdf_de_serie_propria_nao_leva_o_aviso_da_e_obs_mas_leva_o_credito_cc_by():
    for pdf in (EXEMPLOS / "funchal").glob("*_pt.pdf"):
        t = _texto(pdf)
        assert "NÃO PODE SER USADA COMERCIALMENTE" not in t and "Open-Meteo" in t, pdf.name


def test_os_pdfs_de_exemplo_da_internacional_nao_levam_o_aviso():
    for pdf in EXEMPLOS.glob("*/*_en.pdf"):
        assert "COMMERCIALLY" not in _texto(pdf), pdf.name
