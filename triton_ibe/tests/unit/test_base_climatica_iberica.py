# -*- coding: utf-8 -*-
"""Leitor da base ibérica (Iberia01 por célula, chave por código, ilhas nível C) com um pacote sintético.

O pacote sintético tem a mesma estrutura dos ficheiros reais; o teste vale em qualquer edição e não depende dos dados
da IBE. Os testes com os dados reais ficam em ``test_base_iberica_dados_reais.py`` (só na IBE).
"""
import json
import sqlite3
import zlib

import numpy as np
import pytest

from triton.core import base_climatica_iberica as ib

DIAS = 366  # 1971 não é bissexto; a série sintética tem 366 dias só para o teste
INICIO = "1971-01-01"


def _blob(q):
    q = np.asarray(q, dtype=np.uint16)
    return zlib.compress(q.view(np.uint8).reshape(-1, 2).T.tobytes(), 9)


@pytest.fixture()
def pacote(tmp_path, monkeypatch):
    s1 = np.arange(DIAS) % 50          # 0,0 a 4,9 mm
    s2 = np.full(DIAS, 20)             # 2,0 mm
    s3 = np.full(DIAS, 65535)          # falha
    s3[:10] = 10
    era = np.full(DIAS, 5)
    for nome, cels in (("p1", [(1, 40.0, -4.0, s1), (2, 40.1, -4.0, s2)]), ("p2", [(3, 41.0, 2.0, s3)])):
        con = sqlite3.connect(tmp_path / f"chuva_iberia01_{nome}.db")
        con.execute("CREATE TABLE celula (id INTEGER PRIMARY KEY, lat REAL, lon REAL, inicio TEXT, dias INTEGER, passo_mm REAL, dados BLOB)")
        for cid, la, lo, s in cels:
            con.execute("INSERT INTO celula VALUES (?,?,?,?,?,?,?)", (cid, la, lo, INICIO, DIAS, 0.1, _blob(s)))
        con.commit(); con.close()
    con = sqlite3.connect(tmp_path / "chuva_ilhas_era5.db")
    con.execute("CREATE TABLE celula (id INTEGER PRIMARY KEY, lat REAL, lon REAL, inicio TEXT, dias INTEGER, passo_mm REAL, dados BLOB)")
    con.execute("INSERT INTO celula VALUES (?,?,?,?,?,?,?)", (1_000_000_001, 28.25, -16.5, INICIO, DIAS, 0.1, _blob(era)))
    con.commit(); con.close()
    con = sqlite3.connect(tmp_path / "ibe_unidades.db")
    con.executescript("""
    CREATE TABLE unidade (codigo TEXT PRIMARY KEY, pais TEXT, regiao TEXT, provincia TEXT, nome TEXT, populacao INTEGER,
        fonte TEXT, cobertura TEXT, metodo TEXT, celulas_dentro INTEGER, dist_celula_km REAL, nivel TEXT, motivo TEXT);
    CREATE TABLE unidade_celula (codigo TEXT, celula INTEGER, peso REAL, PRIMARY KEY (codigo, celula));
    CREATE TABLE celula (id INTEGER PRIMARY KEY, lat REAL, lon REAL, fonte TEXT, parte TEXT);
    CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT);""")
    con.executemany("INSERT INTO celula VALUES (?,?,?,?,?)", [
        (1, 40.0, -4.0, "iberia01", "p1"), (2, 40.1, -4.0, "iberia01", "p1"), (3, 41.0, 2.0, "iberia01", "p2"),
        (1_000_000_001, 28.25, -16.5, "era5", "ilhas_era5")])
    U = [("ES-28079", "ES", "Comunidad de Madrid", "Madrid", "Madrid", 3000000, "t", "iberia01", "média", 2, 0.0, "B", "m"),
         ("ES-10001", "ES", "Extremadura", "Cáceres", "Madrid", 10, "t", "iberia01", "média", 1, 0.0, "B", "m"),
         ("ES-08019", "ES", "Cataluña", "Barcelona", "Barcelona", 1600000, "t", "iberia01", "um", 1, 0.0, "B", "m"),
         ("ES-38001", "ES", "Canarias", "Santa Cruz de Tenerife", "Adeje", 1, "t", "era5", "nó", 0, None, "C", "ERA5 sem validação local"),
         ("ES-51001", "ES", "Ceuta", "Ceuta", "Ceuta", 1, "t", "nenhuma", "", 0, None, "", "fora do domínio"),
         ("PT-1106", "PT", "Lisboa", "", "Lisboa", None, "t", "iberia01", "um", 2, 0.0, "B", "m")]
    con.executemany("INSERT INTO unidade VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", U)
    con.executemany("INSERT INTO unidade_celula VALUES (?,?,?)", [
        ("ES-28079", 1, 0.5), ("ES-28079", 2, 0.5), ("ES-10001", 2, 1.0), ("ES-08019", 3, 1.0),
        ("ES-38001", 1_000_000_001, 1.0), ("PT-1106", 1, 1.0)])
    con.executemany("INSERT INTO metadados VALUES (?,?)", [("pacote_id", "teste-1"), ("sha256_pacote", "ab" * 32),
                                                           ("fonte", "Iberia01 v1.0"), ("licenca", "ODbL 1.0")])
    con.commit(); con.close()
    (tmp_path / "iberia01_partes.json").write_text(json.dumps(
        {"partes": [{"arquivo": "chuva_iberia01_p1.db"}, {"arquivo": "chuva_iberia01_p2.db"}]}), encoding="utf-8")
    monkeypatch.setenv("TRITON_IBERIA_DADOS", str(tmp_path))
    ib.limpar_cache()
    yield tmp_path
    ib.limpar_cache()


def test_disponivel_so_com_os_ficheiros(pacote, tmp_path, monkeypatch):
    assert ib.disponivel()
    vazio = tmp_path / "vazio"
    vazio.mkdir()
    monkeypatch.setenv("TRITON_IBERIA_DADOS", str(vazio))
    monkeypatch.chdir(vazio)
    ib.limpar_cache()
    if ib.pasta_dos_dados() is None:
        assert not ib.disponivel()


def test_serie_por_celula_e_media_ponderada(pacote):
    serie, ini, fim, dias, n, ident = ib.carregar_serie("ES-28079")
    assert dias == DIAS and n == DIAS and ini == "01/01/1971"
    esperado = 0.5 * (np.arange(DIAS) % 50) * 0.1 + 0.5 * 2.0
    assert np.allclose(serie, esperado)
    assert ident == "Iberia01 v1.0/ES-28079"


def test_recorte_por_datas(pacote):
    serie, ini, fim, dias, n, _ = ib.carregar_serie("PT-1106", "02/01/1971", "11/01/1971")
    assert (ini, fim, n) == ("02/01/1971", "11/01/1971", 10)
    assert np.allclose(serie, (np.arange(1, 11) % 50) * 0.1)


def test_chave_por_codigo_e_nome_repetido(pacote):
    assert ib.resolver("ES-28079") == "ES-28079"
    assert ib.resolver("Madrid [ES-10001]") == "ES-10001"
    assert ib.resolver("Barcelona") == "ES-08019"          # nome único
    assert ib.resolver("Madrid") is None                    # repetido
    assert ib.resolver("barcelóna") == "ES-08019"           # sem acentos nem maiúsculas
    with pytest.raises(ValueError, match="ambíguo"):
        ib.carregar_serie("Madrid")
    with pytest.raises(FileNotFoundError):
        ib.carregar_serie("Atlantida")


def test_rotulo_gravado_resolve_de_volta(pacote):
    u = ib.unidade("ES-10001")
    assert ib.rotulo(u) == "Madrid [ES-10001]"
    assert ib.resolver(ib.rotulo(u)) == "ES-10001"


def test_dia_sem_dado_vira_nan_e_nao_zero(pacote, monkeypatch):
    with sqlite3.connect(pacote / "ibe_unidades.db") as con:
        con.execute("INSERT INTO unidade VALUES ('ES-99999','ES','X','Y','Falha',1,'t','iberia01','um',1,0,'B','m')")
        con.execute("INSERT INTO unidade_celula VALUES ('ES-99999', 3, 1.0)")
    ib.limpar_cache()
    serie = ib.carregar_serie("ES-99999")[0]
    assert np.isnan(serie[10:]).all() and np.allclose(serie[:10], 1.0)


def test_ilhas_nivel_c_e_fonte_era5(pacote):
    assert ib.fonte_da_unidade("ES-38001") == "era5"
    assert ib.qualidade("ES-38001")["nivel"] == "C"
    serie, *_, ident = ib.carregar_serie("ES-38001")
    assert np.allclose(serie, 0.5) and ident.startswith("ERA5/")
    assert "ERA5" in ib.texto_da_fonte("ES-38001") and "validação local" in ib.texto_da_fonte("ES-38001")


def test_nao_coberta_diz_o_motivo(pacote):
    assert [u["codigo"] for u in ib.nao_cobertas()] == ["ES-51001"]
    with pytest.raises(FileNotFoundError, match="fora do domínio"):
        ib.carregar_serie("ES-51001")


def test_parte_nao_instalada_da_erro_claro(pacote):
    (pacote / "chuva_iberia01_p2.db").unlink()
    ib.limpar_cache()
    with pytest.raises(FileNotFoundError, match="não está instalada"):
        ib.carregar_serie("ES-08019")
    assert ib.carregar_serie("ES-28079")[3] == DIAS          # as outras partes seguem a funcionar


def test_regioes_busca_e_contagens_reais(pacote):
    chaves = [k for k, _ in ib.regioes()]
    assert "PT|Lisboa" in chaves and "ES|Canarias" in chaves
    assert ("PT|Lisboa", "Portugal · Lisboa") in ib.regioes("PT")
    assert [u["codigo"] for u in ib.buscar("madr")] == ["ES-28079", "ES-10001"]
    assert [u["codigo"] for u in ib.buscar("ES-08019")] == ["ES-08019"]
    c = ib.contagens()
    assert c["ES"] == 5 and c["PT"] == 1 and c["era5"] == 1 and c["nenhuma"] == 1
    assert "Espanha 5 locais" in ib.linha_de_cobertura("pt")
    assert "0 locais" not in ib.linha_de_cobertura("pt")
    assert ib.contagem_por_nivel() == {"A": 0, "B": 4, "C": 1}


def test_pacote_identifica_o_conteudo(pacote):
    p = ib.pacote()
    assert p["pacote_id"] == "teste-1" and p["licenca"] == "ODbL 1.0"
