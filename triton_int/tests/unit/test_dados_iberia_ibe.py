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
    assert not (RAIZ / "triton" / "data" / "espanha_tarifarios_fontes.tsv").exists()
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
    assert f is not None and te.camada("ES-08019") == 3      # Barcelona: sem tarifa própria transcrita
    assert "média regional" in te.aviso("ES-08019")
    assert te.fatura("PT-1106") is None                      # Portugal tem os seus tarifários; não é camada de Espanha
    # camada 1 só com documento arquivado
    for cod, m in (dados.get("municipios") or {}).items():
        if m.get("camada") == 1:
            docs = m["procedencia"]["documentos"]
            assert docs and all(len(d["sha256"]) == 64 and d["url"] and d["confirmado_em"] for d in docs), cod


# ---- camada 1 de Espanha: 7 municípios transcritos (30/10/2026), ainda não conferidos --------------------------------
CAMADA1 = {"ES-28079": "Madrid", "ES-41091": "Sevilla", "ES-30030": "Murcia", "ES-15030": "A Coruña",
           "ES-35016": "Las Palmas de Gran Canaria", "ES-33024": "Gijón", "ES-47186": "Valladolid"}
SHA_FONTES = "63ee9e017b5668341dc5173e457a03f02b9bd13f9d71c83e88f18130376562c8"
ARQ_TARIFAS = RAIZ / "triton" / "data" / "espanha_tarifarios.json"
ARQ_FONTES = RAIZ / "triton" / "data" / "espanha_tarifarios_fontes.tsv"
ibe = pytest.mark.skipif(not ib.disponivel(), reason="dados ibéricos só na IBE")


@ibe
def test_camada_1_le_os_sete_municipios_sem_alterar_valores():
    mun = te.carregar()["municipios"]
    assert set(mun) == set(CAMADA1)
    for cod, nome in CAMADA1.items():
        m = mun[cod]
        assert m["nome"] == nome and m["camada"] == 1 and m["origem_do_valor"] == "transcrito"
        assert m["procedencia"]["conferido"] is False
        assert m["codigo_ine"] == cod[3:] and m["vigencia"] and m["iva_observacao"]
        assert te.camada(cod) == 1 and te.fatura(cod) is not None
    # valores transcritos que não podem mudar sem nova leitura da fonte
    assert mun["ES-28079"]["agua"]["fixa_mes"] == 6.1425 and mun["ES-28079"]["agua"]["escaloes"][0] == [0.0, 10, 0.4562]
    assert mun["ES-47186"]["agua"]["escaloes"][-1][2] > 0 and mun["ES-33024"]["saneamiento"]["escaloes"] == [[0.0, None, 0.1982]]
    assert mun["ES-15030"]["saneamiento"]["escaloes"] == [[0.0, 6, 0.38], [6, None, 0.42]]


@ibe
def test_cada_documento_da_camada_1_tem_url_data_e_sha256():
    for cod, m in te.carregar()["municipios"].items():
        docs = m["procedencia"]["documentos"]
        assert docs, cod
        for d in docs:
            assert d["url"].startswith("https://") and d["confirmado_em"] == "2026-10-30" and len(d["sha256"]) == 64, cod
        f = te.fonte_da_camada1(cod)
        assert f["url"] == docs[0]["url"] and f["sha256"] == docs[0]["sha256"] and f["vigencia"]


@ibe
def test_iva_nulo_nao_quebra_o_leitor_e_o_aviso_diz_o_que_falta():
    from triton.core.fatura_portuguesa import conta_mensal
    assert te.iva_ausente("ES-28079") == [] and te.iva_ausente("ES-41091") == []
    assert te.iva_ausente("ES-47186") == ["agua", "saneamiento"]
    assert te.iva_ausente("ES-15030") == ["saneamiento", "parcelas"]
    assert te.iva_ausente("ES-35016") == ["saneamiento"]
    f = te.fatura("ES-47186")
    assert f.iva_agua_pct == 0.0 and f.iva_saneamento_pct == 0.0           # nulo = sem IVA no cálculo
    assert 10.0 < conta_mensal(f, 10) < 12.0                                # 10,82 EUR (CONFERENCIA.md), sem IVA
    assert "IVA do saneamento não consta da fonte" in te.aviso("ES-35016")
    assert "IVA da água não consta da fonte" in te.aviso("ES-47186")
    assert "IVA of sanitation" not in te.nota_da_camada1("ES-35016", "en") and "VAT of sanitation is not stated" in te.nota_da_camada1("ES-35016", "en")
    assert te.aviso("ES-28079").startswith("Tarifa transcrita, ainda não conferida")      # IVA completo, mas não conferido


@ibe
def test_camada_correta_por_municipio_ine():
    cont = te.contagem_por_camada()
    assert cont[1] == 7 and cont[2] == 0 and cont[3] == 8131 - 7 and cont[0] == 0
    for cod in ("ES-08019", "ES-46250", "ES-50297", "ES-28080"):
        assert te.camada(cod) == 3, cod
        assert "média regional" in te.aviso(cod)
        assert te.nota_da_camada1(cod) == ""
    for cod in CAMADA1:
        assert te.camada(cod) == 1 and "média regional" not in te.aviso(cod)


@ibe
def test_aviso_de_nao_conferido_com_a_fonte_na_procedencia_e_no_laudo():
    from triton.core.licenca_eobs import rodape_do_laudo
    from triton.core.base_climatica_iberica import CENARIO_IBERIA01
    for cod in CAMADA1:
        a = te.aviso(cod)
        assert "Tarifa transcrita, ainda não conferida (segunda leitura pendente)" in a
        assert te.fatura(cod).vigencia and te.fonte_da_camada1(cod)["url"] in a
        assert "ainda não conferida" in te.procedencia(cod) and te.conferida(cod) is False
    aud = {"climate_scenario": CENARIO_IBERIA01, "climate_city_name": "ES-28079", "tariff_city_code": "ES-28079"}
    assert "ainda não conferida (segunda leitura pendente)" in rodape_do_laudo(aud)
    assert "not yet checked (second reading pending)" in rodape_do_laudo(aud, ingles=True)
    aud["tariff_city_code"] = "ES-08019"                                   # camada 3: o aviso de média regional
    assert "média regional" in rodape_do_laudo(aud)
    aud["tariff_city_code"] = "PT-1106"
    assert "Tarifa transcrita" not in rodape_do_laudo(aud)


@ibe
def test_aplicar_grava_a_tarifa_da_camada_1_no_projeto():
    from triton.core.parser import TritonConfig
    cfg = TritonConfig()
    assert te.aplicar("ES-47186", cfg) and cfg.tariff_city_name == "ES-47186" and cfg.tariff_vigencia
    assert te.aplicar("ES-35016", TritonConfig())


@ibe
def test_tamanho_e_sha256_do_arquivo_de_fontes():
    assert ARQ_TARIFAS.stat().st_size < 0.2 * 2 ** 20 and ARQ_FONTES.stat().st_size < 0.05 * 2 ** 20
    texto = ARQ_FONTES.read_bytes().replace(b"\r\n", b"\n")              # o Git pode converter o fim de linha
    assert hashlib.sha256(texto).hexdigest() == SHA_FONTES
    assert te.carregar()["arquivo_de_fontes"]["sha256_com_fim_de_linha_lf"] == SHA_FONTES
    linhas = texto.decode("utf-8").splitlines()
    cab = linhas[0].split("\t")
    assert cab[:5] == ["municipio", "codigo_ine", "url", "data_acesso", "sha256"]
    por = {}
    for l in linhas[1:]:
        c = l.split("\t")
        por.setdefault(c[1], set()).add((c[2], c[4]))
    for cod, m in te.carregar()["municipios"].items():
        for d in m["procedencia"]["documentos"]:
            assert (d["url"], d["sha256"]) in por[cod[3:]], (cod, d["url"])


@ibe
def test_interface_mostra_camada_1_nao_conferida_com_fonte_e_iva_em_falta_traduzidos():
    pytest.importorskip("PySide6")
    from triton.ui import translation as T
    from triton.ui.tab_project import TabProject
    txt = TabProject._procedencia_espanha("ES-47186", 1)
    assert "ainda não conferida (segunda leitura pendente)" in txt and "valladolid.es" in txt
    assert "IVA da água não consta da fonte" in txt and "IVA do saneamento não consta da fonte" in txt
    for chave in ("🟡 Tarifa transcrita, ainda não conferida (segunda leitura pendente)",
                  "IVA do saneamento não consta da fonte", "IVA das parcelas adicionais não consta da fonte"):
        for lang in ("en", "es", "zh"):
            assert T.tr(chave, lang) != chave, (lang, chave)
