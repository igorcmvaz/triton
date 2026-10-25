"""A CLI por edição: números e língua dos estudos, fonte da chuva e nome do projeto na saída.

Revisão final 2: ``series-length`` e os demais estudos saíam em português com milhar brasileiro na
Internacional; o JSON/HTML do ``analyze`` não trazia a fonte da chuva nem a licença; ``source_project``
gravava o caminho absoluto da máquina. A Brasil não muda.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
ED = {"triton_brl": "BRL", "triton_int": "INT", "triton_ibe": "IBE"}.get(RAIZ.name.lower(), "BRL")
PROJETO = {"BRL": "examples/estudo_caso_1_florianopolis1.triton", "INT": "examples/new_york.triton",
           "IBE": "examples/portugal/lisboa.triton"}[ED]


def _cli(*args):
    env = {k: v for k, v in os.environ.items() if k != "TRITON_EDITION"}
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "-m", "triton.cli", *args], cwd=str(RAIZ), env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600)
    assert r.returncode == 0, r.stderr
    return r.stdout


def test_series_length_na_lingua_e_no_numero_da_edicao():
    saida = _cli("series-length", PROJETO)
    if ED == "INT":
        assert "Ideal volume with the whole series" in saida and "A série" not in saida
        assert "Volume ideal" not in saida
        linha = next(l for l in saida.splitlines() if l.startswith("Ideal volume"))
        assert linha.split(": ")[1].split()[0].replace(",", "").isdigit() and "." not in linha.split(": ")[1].split()[0]
    elif ED == "IBE":
        linha = next(l for l in saida.splitlines() if l.startswith("Volume ideal"))
        assert "," not in linha.split(": ")[1].split()[0]          # milhar pt: «5.000»
    else:
        assert "Volume ideal com a série inteira" in saida


@pytest.mark.skipif(ED != "INT", reason="só a Internacional é em inglês")
def test_os_outros_estudos_da_internacional_saem_em_ingles():
    incerteza = _cli("uncertainty", PROJETO, "--samples", "10")
    assert "Monte Carlo uncertainty" in incerteza and "Volume analysed" in incerteza
    demanda = _cli("stochastic-demand", PROJETO, "--samples", "10")
    assert "Mean demand" in demanda and "Draw:" in demanda and "Demanda" not in demanda
    prob = _cli("probabilistic-study", PROJETO, "--samples", "10", "--quiet")
    assert "Probabilistic modulation" in prob and "Sampled variables" in prob
    assert "Número de pessoas" not in prob and "R$" not in _cli("probabilistic-study", "--list-variables")


def test_analyze_json_traz_so_o_nome_do_projeto_e_a_fonte_da_chuva(tmp_path):
    destino = tmp_path / "saida.json"
    _cli("analyze", str(RAIZ / PROJETO), "--analysis", "technical", "--format", "json", "--output", str(destino))
    prov = json.loads(destino.read_text(encoding="utf-8"))["provenance"]
    assert prov["source_project"] == Path(PROJETO).name
    if ED == "BRL":
        assert "rainfall_source" not in prov
    elif ED == "INT":
        assert any("Open-Meteo" in l and "CC BY 4.0" in l for l in prov["rainfall_source"]["credit_and_licence"])
    else:
        texto = " ".join(prov["rainfall_source"]["credit_and_licence"])
        assert "E-OBS" in texto and "não comerciais" in texto and "Cobertura" in texto


@pytest.mark.skipif(ED == "BRL", reason="a Brasil não muda")
def test_analyze_html_traz_a_fonte_da_chuva(tmp_path):
    destino = tmp_path / "saida.html"
    _cli("analyze", str(RAIZ / PROJETO), "--analysis", "technical", "--format", "html", "--output", str(destino))
    html = destino.read_text(encoding="utf-8")
    assert ("Open-Meteo" if ED == "INT" else "E-OBS") in html


def test_o_rodape_do_laudo_traz_o_credito_cc_by_das_series_era5():
    from triton.core.edition import usa_dados_do_brasil
    from triton.core.licenca_eobs import rodape_do_laudo
    aud = {"climate_model": "ERA5 (Open-Meteo)", "climate_city_name": "Funchal", "chuva_serie_propria": True}
    texto = rodape_do_laudo(aud, ingles=False)
    if usa_dados_do_brasil():
        assert texto == ""
    else:
        assert "Open-Meteo" in texto and "CC BY 4.0" in texto
    assert "Open-Meteo" not in rodape_do_laudo({"climate_model": "E-OBS v33.0e"}, ingles=True)
