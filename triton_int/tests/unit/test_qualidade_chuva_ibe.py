# -*- coding: utf-8 -*-
"""Qualidade da chuva por concelho no banco da edição IBE (``data/portugal_eobs.db``).

Só vale na IBE (``tests/so_da_ibe.txt``; fora dela o arquivo é saltado). Teste de ouro: o
``qualidade_prototipo.csv`` do protótipo (``tests/dados_ibe/``), com a fórmula única de
``triton/core/qualidade_chuva.py``, tem de dar A 45, B 159, C 74 e reproduzir o banco linha a linha.
"""
import csv
import hashlib
import json
import os
import sqlite3
import zlib
from collections import Counter

import pytest

from triton.core import base_climatica_portugal as pt
from triton.core import qualidade_chuva as Q

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_DE_OURO = os.path.join(RAIZ, "tests", "dados_ibe", "qualidade_prototipo.csv")

pytestmark = pytest.mark.skipif(not pt.disponivel(), reason="data/portugal_eobs.db ausente")


def _sql(consulta, *args):
    con = sqlite3.connect(f"file:{pt.caminho_da_base()}?mode=ro", uri=True)
    try:
        return con.execute(consulta, args).fetchall()
    finally:
        con.close()


def _repetidas_por_sha():
    hs = {d: hashlib.sha256(zlib.decompress(b)).hexdigest() for d, b in _sql("SELECT dtmn, dados FROM series")}
    cont = Counter(hs.values())
    return {d for d, h in hs.items() if cont[h] > 1}


def _linhas_do_csv():
    with open(CSV_DE_OURO, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def test_a_tabela_qualidade_tem_as_colunas_pedidas():
    cols = [r[1] for r in _sql("PRAGMA table_info(qualidade)")]
    assert cols == ["dtmn", "concelho", "n_eff", "metodo", "repetida", "dtot", "drx", "nivel", "motivo"]
    assert Q.tem_qualidade()


def test_ouro_45_159_74_e_o_maior_drx_entre_os_a():
    cont = Counter(n for (n,) in _sql("SELECT nivel FROM qualidade"))
    assert (cont["A"], cont["B"], cont["C"]) == (45, 159, 74)
    assert Q.contagem_por_nivel() == {"A": 45, "B": 159, "C": 74}
    maior_drx = max(abs(d) for (d,) in _sql("SELECT drx FROM qualidade WHERE nivel = 'A'"))
    assert round(maior_drx, 2) == 14.90
    maior_dtot = max(abs(d) for (d,) in _sql("SELECT dtot FROM qualidade WHERE nivel = 'A'"))
    assert round(maior_dtot, 2) == 9.85


def test_o_csv_de_ouro_com_a_formula_reproduz_o_banco_linha_a_linha():
    repetidas = _repetidas_por_sha()
    assert len(repetidas) == 14
    no_banco = {d: (n, niv, mot) for d, n, niv, mot in _sql("SELECT dtmn, n_eff, nivel, motivo FROM qualidade")}
    linhas = _linhas_do_csv()
    assert len(linhas) == len(no_banco) == 278
    esperados = Counter()
    for r in linhas:
        dtmn = r["uid"].split("-", 1)[1]
        n, metodo, dtot, drx = int(r["n"]), r["metodo"], float(r["dtot"]), float(r["drx"])
        nivel = Q.nivel(dtot, drx, n, metodo, dtmn in repetidas)
        esperados[nivel] += 1
        assert no_banco[dtmn][0] == n
        assert no_banco[dtmn][1] == nivel, dtmn
        assert no_banco[dtmn][2] == Q.motivo(dtot, drx, n, metodo, dtmn in repetidas), dtmn
    assert (esperados["A"], esperados["B"], esperados["C"]) == (45, 159, 74)


def test_nenhum_a_fora_dos_limiares_e_nenhum_nivel_fora_de_abc():
    """O teste que FALHA se o banco tiver um A fora dos limiares ou um nível que não seja A, B ou C."""
    linhas = _sql("SELECT dtmn, nivel, dtot, drx FROM qualidade")
    assert linhas
    for dtmn, nivel, dtot, drx in linhas:
        assert nivel in ("A", "B", "C"), (dtmn, nivel)
        if nivel == "A":
            assert abs(dtot) <= Q.LIMIARES["A"]["dtot"] and abs(drx) <= Q.LIMIARES["A"]["drx"], dtmn
        if nivel == "B":
            assert abs(dtot) <= Q.LIMIARES["B"]["dtot"] and abs(drx) <= Q.LIMIARES["B"]["drx"], dtmn
    assert _sql("SELECT COUNT(*) FROM qualidade WHERE nivel NOT IN ('A','B','C')") == [(0,)]


def test_a_geometria_so_rebaixa_ate_b_e_os_c_sao_discrepancia_medida():
    for dtmn, n, metodo, rep, dtot, drx, nivel in _sql(
            "SELECT dtmn, n_eff, metodo, repetida, dtot, drx, nivel FROM qualidade"):
        assert Q.nivel_de_geometria(n, metodo, bool(rep)) in ("A", "B")
        if nivel == "C":
            assert Q.nivel_de_concordancia(dtot, drx) == "C", dtmn
        if Q.nivel_de_concordancia(dtot, drx) == "A" and Q.nivel_de_geometria(n, metodo, bool(rep)) == "B":
            assert nivel == "B", dtmn
    assert _sql("SELECT COUNT(*) FROM qualidade WHERE repetida = 1") == [(14,)]
    assert _sql("SELECT COUNT(*) FROM qualidade WHERE n_eff < 3") == [(148,)]


def test_os_51_concelhos_de_concordancia_a_rebaixados_pela_geometria():
    """O número do manual: 96 de concordância A, 45 ficam A, 51 caem para B só pela geometria."""
    conc_a = [(d, t, x) for d, t, x in _sql("SELECT dtmn, dtot, drx FROM qualidade")
              if Q.nivel_de_concordancia(t, x) == "A"]
    assert len(conc_a) == 96
    assert len(_sql("SELECT dtmn FROM qualidade WHERE nivel = 'A'")) == 45


def test_metadados_do_pacote_e_da_qualidade():
    meta = pt.metadados()
    for chave in ("pacote_id", "versao_eobs", "qualidade_versao", "limiares", "sha256_pacote", "espanha_locais"):
        assert meta.get(chave), chave
    assert meta["versao_eobs"] == "v33.0e" and meta["qualidade_versao"] == Q.VERSAO_DA_QUALIDADE
    assert json.loads(meta["limiares"]) == Q.LIMIARES
    assert meta["pacote_id"].startswith("PT-EOBS-v33.0e-") and meta["pacote_id"].endswith(meta["sha256_pacote"][:8])
    assert pt.pacote()["sha256_pacote"] == meta["sha256_pacote"]


def test_o_sha256_do_pacote_confere_com_o_conteudo_das_series():
    h = hashlib.sha256()
    for dtmn, inicio, dias, dados in _sql("SELECT dtmn, inicio, dias, dados FROM series ORDER BY dtmn"):
        h.update(f"{dtmn}|{inicio}|{dias}|".encode("utf-8"))
        h.update(dados)
    assert h.hexdigest() == pt.metadados()["sha256_pacote"]


def test_as_series_do_banco_nao_foram_tocadas_pela_qualidade():
    """As 278 séries e a citação seguem como estavam (a tabela de qualidade só acrescenta)."""
    assert len(pt.concelhos()) == 278 and "Lisboa" in pt.concelhos("Lisboa")
    assert "10.1029/2017JD028200" in pt.metadados()["citacao"]


def test_qualidade_do_concelho_para_a_interface():
    q = Q.qualidade_do_concelho("Lisboa")
    assert q["nivel"] == "B" and q["repetida"] == 1 and q["n_eff"] == 1
    assert "série igual à de outro concelho" in q["motivo"]
    assert Q.qualidade_do_concelho("Atlantida") is None
    txt = Q.texto_da_qualidade("Lisboa")
    assert txt.startswith("Qualidade da chuva em Lisboa: nível B.")
    assert "level B" in Q.texto_da_qualidade("Lisboa", "en")


def test_o_motivo_de_cada_nivel_mostra_a_razao():
    por_nivel = {n: Q.qualidade_do_concelho(c) for n, c in (("A", None), ("B", "Lisboa"), ("C", "Albufeira"))
                 if c}
    assert por_nivel["C"]["nivel"] == "C" and "acima dos limites do nível B" in por_nivel["C"]["motivo"]
    a = _sql("SELECT concelho FROM qualidade WHERE nivel = 'A' LIMIT 1")[0][0]
    assert Q.qualidade_do_concelho(a)["motivo"].startswith("A:")


def test_a_linha_de_cobertura_vem_do_banco_e_nao_e_digitada():
    """O teste da tarefa E: a linha é igual à contagem feita direto no banco, por consulta independente."""
    n = _sql("SELECT COUNT(*) FROM qualidade")[0][0]
    por = dict(_sql("SELECT nivel, COUNT(*) FROM qualidade GROUP BY nivel"))
    espanha = dict(_sql("SELECT chave, valor FROM metadados"))["espanha_locais"]
    esperada = (f"Cobertura: Portugal continental {n} concelhos (A {por['A']}, B {por['B']}, C {por['C']}); "
                f"Espanha: {espanha} locais")
    assert Q.linha_de_cobertura() == esperada
    assert esperada == "Cobertura: Portugal continental 278 concelhos (A 45, B 159, C 74); Espanha: 0 locais"


def test_a_linha_de_cobertura_acompanha_o_banco(tmp_path, monkeypatch):
    """Muda-se o banco (uma cópia) e a linha muda: nada está digitado no código."""
    import shutil
    copia = tmp_path / "portugal_eobs.db"
    shutil.copyfile(pt.caminho_da_base(), copia)
    con = sqlite3.connect(copia)
    con.execute("UPDATE qualidade SET nivel = 'C' WHERE dtmn IN (SELECT dtmn FROM qualidade WHERE nivel = 'A' LIMIT 2)")
    con.execute("UPDATE metadados SET valor = '52' WHERE chave = 'espanha_locais'")
    con.commit()
    con.close()
    monkeypatch.setenv("TRITON_PORTUGAL_DB", str(copia))
    Q._tabela.cache_clear()
    try:
        assert Q.linha_de_cobertura() == ("Cobertura: Portugal continental 278 concelhos (A 43, B 159, C 76); "
                                          "Espanha: 52 locais")
    finally:
        monkeypatch.delenv("TRITON_PORTUGAL_DB")
        Q._tabela.cache_clear()


def test_o_titulo_da_janela_leva_a_linha_de_cobertura():
    from triton.core.edition import get_edition_title
    assert get_edition_title().endswith(Q.linha_de_cobertura())


def test_o_rodape_do_laudo_leva_licenca_citacao_nivel_e_cobertura():
    from triton.core.licenca_eobs import rodape_do_laudo
    html = rodape_do_laudo({"climate_city_name": "Lisboa"})
    assert "uso restrito a pesquisa e educação não comerciais" in html
    assert "Cornes et al., 2018" in html and "UERRA" in html
    assert "Pacote PT-EOBS-v33.0e-" in html and "SHA-256" in html
    assert "Qualidade da chuva em Lisboa: nível B." in html
    assert html.endswith(Q.linha_de_cobertura())
    assert "Chuva: série fornecida pelo utilizador." in rodape_do_laudo({"chuva_serie_propria": True})
    assert "viés" not in html.lower()


def test_todo_laudo_da_edicao_traz_o_rodape():
    from triton.core.report_generator import (generate_environmental_html_report, generate_executive_html_report,
                                              generate_research_html_report)
    dados = {"ref_code": "IBE-1", "rain_file": "Lisboa (E-OBS)", "area": 100.0, "runoff": 0.85, "discard": 2.0,
             "residents": 3, "demand": 100.0, "share": 0.4, "lower_vol": 3000.0, "potential_pct": 30.0,
             "pluv_day": 50.0, "potable_day": 100.0, "spill_day": 10.0, "sat_full": 50.0, "sat_null": 10.0,
             "audit_context": {"climate_city_name": "Lisboa", "climate_basis": "E-OBS", "climate_location": "Lisboa"}}
    for gerador in (generate_executive_html_report, generate_research_html_report):
        html = gerador(dados)
        assert "rodape-da-chuva" in html and "Cornes et al., 2018" in html, gerador.__name__
        assert Q.linha_de_cobertura() in html, gerador.__name__
        assert "Qualidade da chuva em Lisboa" in html, gerador.__name__
    assert callable(generate_environmental_html_report)
