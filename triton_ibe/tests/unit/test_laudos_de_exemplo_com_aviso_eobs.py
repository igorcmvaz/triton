"""Os PDFs de exemplo da IBE trazem a fonte e a licença certas: Iberia01 (ODbL), sem o aviso da E-OBS.

Desde 31/10/2026 Lisboa e Porto usam o Iberia01 (uso comercial permitido, com atribuição); o aviso vermelho de
uso não comercial é da E-OBS e só aparece em projetos que a escolhem. O Funchal usa a ERA5 de ilha (CC BY).
Regerar com ``scripts/gerar_relatorios_exemplo.py``, que também confere o rodapé.
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


@pytest.mark.skipif(not IBE, reason="só a IBE usa o Iberia01")
@pytest.mark.parametrize("cidade", ["lisboa", "porto"])
def test_os_pdfs_do_iberia01_trazem_a_licenca_a_atribuicao_e_a_qualidade_sem_o_aviso_da_e_obs(cidade):
    pdfs = sorted((EXEMPLOS / cidade).glob("*_pt.pdf"))
    assert len(pdfs) == 3
    for pdf in pdfs:
        t = _texto(pdf)
        assert "NÃO PODE SER USADA COMERCIALMENTE" not in t and "E-OBS" not in t, pdf.name
        assert "Iberia01" in t and "ODbL" in t and "Herrera" in t, pdf.name
        assert "Qualidade da chuva" in t, pdf.name


@pytest.mark.skipif(not IBE, reason="só a IBE tem o Funchal")
def test_o_pdf_de_serie_propria_nao_leva_o_aviso_da_e_obs_mas_leva_o_credito_cc_by():
    for pdf in (EXEMPLOS / "funchal").glob("*_pt.pdf"):
        t = _texto(pdf)
        assert "NÃO PODE SER USADA COMERCIALMENTE" not in t and "Open-Meteo" in t, pdf.name


def test_os_pdfs_de_exemplo_da_internacional_nao_levam_o_aviso():
    for pdf in EXEMPLOS.glob("*/*_en.pdf"):
        assert "COMMERCIALLY" not in _texto(pdf), pdf.name
