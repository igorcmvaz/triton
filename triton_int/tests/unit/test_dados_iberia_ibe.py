# -*- coding: utf-8 -*-
"""Os dados reais da base ibérica (Iberia01 por célula, ilhas ERA5, municípios e qualidade): só existem na IBE.

Confere o manifesto (tamanho e SHA-256 de cada parte, limite de 43 MiB), as contagens, a chave por código, o nível C
fixo das ilhas, a licença nos metadados, as tarifas de Espanha por camadas e que BRL e INT não levam estes ficheiros.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

import numpy as np
import pytest

from triton.core import base_climatica_iberica as ib
from triton.core import tarifarios_espanha as te

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
ARQUIVOS = ("ibe_unidades.db", "iberia01_partes.json", "chuva_iberia01_p1.db", "chuva_iberia01_p2.db",
            "chuva_iberia01_p3.db", "chuva_iberia01_p4.db", "chuva_ilhas_era5.db", "qualidade_eobs_odbl.db")
LIMITE_MIB = 43


def test_brl_e_int_nao_levam_os_dados_ibericos():
    from triton.core.edition import get_current_edition
    if get_current_edition() == "IBE":
        pytest.skip("é a IBE")
    assert not [n for n in ARQUIVOS + ("portugal_eobs.db",) if (DATA / n).exists()]
    assert not (RAIZ / "triton" / "data" / "espanha_tarifarios.json").exists()
    assert not ib.disponivel() and te.carregar() == {}



@pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")
def test_o_manifesto_confere_com_os_ficheiros_e_respeita_o_limite():
    man = json.loads((DATA / "iberia01_partes.json").read_text(encoding="utf-8"))
    assert man["limite_github_mb"] == 50 and man["limite_parte_mib"] == LIMITE_MIB and man["licenca"].startswith("ODbL")
    assert len(man["partes"]) == 4 and sum(p["celulas"] for p in man["partes"]) == 6523
    for p in man["partes"]:
        f = DATA / p["arquivo"]
        assert f.stat().st_size == p["tamanho_bytes"] < LIMITE_MIB * 2 ** 20
        assert hashlib.sha256(f.read_bytes()).hexdigest() == p["sha256"], p["arquivo"]
    for n in ARQUIVOS:
        assert (DATA / n).stat().st_size < 50 * 2 ** 20


@pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")
def test_contagens_reais_e_licenca_nos_metadados():
    c = ib.contagens()
    assert c["PT"] == 308 and c["ES"] == 8131 and c["iberia01"] == 8319 and c["era5"] == 118 and c["nenhuma"] == 2
    assert "Espanha 8131 locais" in ib.linha_de_cobertura() and "0 locais" not in ib.linha_de_cobertura()
    meta = ib.metadados()
    assert meta["licenca"] == "ODbL 1.0" and "Open Database License" in meta["aviso"]
    assert "10.5194/essd-11-1947-2019" in meta["citacao"]
    assert len(meta["sha256_iberia01"]) == 64 and len(meta["sha256_pacote"]) == 64
    assert meta["pacote_id"] == json.loads((DATA / "iberia01_partes.json").read_text(encoding="utf-8"))["pacote_id"]


@pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")
def test_chave_por_codigo_nomes_repetidos_e_lisboa_nao_e_madrid():
    repetidos = {u["nome"] for u in ib.unidades() if len(ib.candidatos(u["nome"])) > 1}
    assert len(repetidos) >= 10
    nome = sorted(repetidos)[0]
    assert ib.resolver(nome) is None
    for u in ib.candidatos(nome):
        assert ib.resolver(ib.rotulo(u)) == u["codigo"]
    lis = ib.carregar_serie("PT-1106", "01/01/1986", "31/12/2015")
    mad = ib.carregar_serie("ES-28079", "01/01/1986", "31/12/2015")
    assert lis[4] == mad[4] == 10957
    assert 600 < lis[0].sum() / 30 < 900 and 350 < mad[0].sum() / 30 < 600
    assert not np.isnan(lis[0]).any() and (lis[0] >= 0).all()


@pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")
def test_todas_as_unidades_com_cobertura_tem_celulas_e_pesos_que_somam_um():
    con = sqlite3.connect(DATA / "ibe_unidades.db")
    sem = con.execute("SELECT u.codigo FROM unidade u LEFT JOIN unidade_celula c ON c.codigo = u.codigo "
                      "WHERE u.cobertura != 'nenhuma' AND c.codigo IS NULL").fetchall()
    assert sem == []
    mau = con.execute("SELECT codigo FROM unidade_celula GROUP BY codigo HAVING abs(sum(peso) - 1.0) > 1e-9").fetchall()
    assert mau == []
    orfas = con.execute("SELECT DISTINCT celula FROM unidade_celula WHERE celula NOT IN (SELECT id FROM celula)").fetchall()
    assert orfas == []


@pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")
def test_ilhas_sao_sempre_nivel_c_com_aviso_e_ceuta_melilla_nao_tem_serie():
    ilhas = [u for u in ib.unidades() if u["regiao"] in ("Canarias", "Região Autónoma da Madeira", "Região Autónoma dos Açores")]
    assert len(ilhas) == 88 + 11 + 19
    assert {u["nivel"] for u in ilhas} == {"C"} and {u["cobertura"] for u in ilhas} == {"era5"}
    assert all("validação local" in u["motivo"] for u in ilhas)
    assert {u["codigo"] for u in ib.nao_cobertas()} == {"ES-51001", "ES-52001"}
    # Baleares entram pelo Iberia01 (não são ilhas ERA5)
    bal = [u for u in ib.unidades() if u["regiao"] == "Illes Balears"]
    assert len(bal) == 67 and {u["cobertura"] for u in bal} == {"iberia01"}


@pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")
def test_niveis_de_qualidade_seguem_a_regra_geometrica():
    for u in ib.unidades():
        if u["cobertura"] != "iberia01":
            continue
        if u["celulas_dentro"] >= 3:
            assert u["nivel"] == "A"
        elif u["celulas_dentro"] >= 1:
            assert u["nivel"] == "B"
        else:
            assert u["nivel"] in ("B", "C")


@pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")
def test_tarifas_de_espanha_camada_3_para_todos_e_nenhum_valor_inventado():
    dados = te.carregar()
    c3 = dados["camada3"]
    assert len(c3["sha256_documento"]) == 64 and c3["url"].startswith("https://ine.es/") and c3["acedido_em"]
    assert c3["eur_m3_total"]["Illes Balears"] == 2.80 and c3["eur_m3_total"]["La Rioja"] == 1.26
    cont = te.contagem_por_camada()
    assert cont[3] + cont[2] + cont[1] == 8131 and cont[0] == 0
    f = te.fatura("ES-28079")
    assert f is not None and te.camada("ES-28079") == 3
    assert "média regional" in te.aviso("ES-28079")
    assert te.fatura("PT-1106") is None                      # Portugal tem os seus tarifários; não é camada de Espanha
    # camada 1 só com documento arquivado
    for cod, m in (dados.get("municipios") or {}).items():
        if m.get("camada") == 1:
            docs = m["procedencia"]["documentos"]
            assert docs and all(len(d["sha256"]) == 64 and d["url"] and d["confirmado_em"] for d in docs), cod
