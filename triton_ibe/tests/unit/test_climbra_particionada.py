"""
Base CLIMBra dividida por modelo (`data/climbra_<modelo>.db`): descoberta, leitura e equivalência.

Duas frentes:
- o leitor (`triton/core/climate_database.py`), que roda nas três edições, com bancos sintéticos;
- a base real da Edição Brasil (`data/climbra_<modelo>.db`, 19 partes): integridade contra o manifesto
  `data/climbra_partes.json` (é o que a verificação de integração contínua roda) e, se o
  `data/climbra.db` único estiver no disco, igualdade das séries lidas.
"""

import hashlib
import json
import os
import sqlite3
import zlib
from pathlib import Path

import numpy as np
import pytest

from triton.core import climate_database as cd

RAIZ = Path(__file__).resolve().parents[2]

CIDADES = ["São Paulo", "Florianópolis", "Belém"]
MODELOS = ["INM-CM4", "ACCESS-CM2"]
DIAS = {"HIST": 12419, "SSP245": 31411, "SSP585": 31411}

ESQUEMA = (
    "CREATE TABLE climbra_meta (key TEXT PRIMARY KEY, value TEXT)",
    "CREATE TABLE climbra_cities (city TEXT PRIMARY KEY, city_norm TEXT NOT NULL)",
    "CREATE INDEX idx_climbra_cities_norm ON climbra_cities(city_norm)",
    "CREATE TABLE climbra_series (city TEXT NOT NULL, model TEXT NOT NULL, scenario TEXT NOT NULL, "
    "count INTEGER NOT NULL, data BLOB NOT NULL, PRIMARY KEY (city, model, scenario))",
)


def _serie(cidade, modelo, cenario, deslocamento=0.0):
    semente = sum(ord(c) for c in cidade + modelo + cenario) + int(deslocamento * 1000)
    rng = np.random.default_rng(semente)
    return np.round(rng.gamma(0.4, 8.0, DIAS[cenario]), 1).astype(np.float16)


def _criar_banco(caminho, modelos, cenarios=tuple(DIAS), cidades=CIDADES, deslocamento=0.0, meta=None):
    """Banco sintético no esquema do CLIMBra; devolve {(cidade, modelo, cenario): array float16}."""
    conn = sqlite3.connect(str(caminho))
    for comando in ESQUEMA:
        conn.execute(comando)
    conn.executemany("INSERT INTO climbra_cities VALUES (?, ?)", [(c, cd._normalize_name(c)) for c in cidades])
    series = {}
    for m in modelos:
        for c in cidades:
            for s in cenarios:
                arr = _serie(c, m, s, deslocamento)
                series[(c, m, s)] = arr
                conn.execute("INSERT INTO climbra_series VALUES (?, ?, ?, ?, ?)",
                             (c, m, s, len(arr), zlib.compress(arr.tobytes(), 6)))
    conn.executemany("INSERT INTO climbra_meta VALUES (?, ?)", list((meta or {"dtype": "float16"}).items()))
    conn.commit()
    conn.close()
    return series


@pytest.fixture
def pasta_de_bancos(tmp_path, monkeypatch):
    """Aponta o leitor para uma pasta vazia e esquece o cache, antes e depois."""
    pasta = tmp_path / "data"
    pasta.mkdir()
    for variavel in ("TRITON_CLIMBRA_DB", "TRITON_CLIMATE_DB", "TRITON_CLIMBRA_DIR"):
        monkeypatch.delenv(variavel, raising=False)
    monkeypatch.setenv("TRITON_CLIMBRA_DB", str(pasta))
    cd.limpar_cache_da_base()
    yield pasta
    cd.limpar_cache_da_base()


def _ler(cidade, modelo, cenario):
    return cd.load_national_climate_series(cidade, modelo, cenario)[0]


def test_le_um_banco_por_modelo(pasta_de_bancos):
    esperado = {}
    for m in MODELOS:
        esperado.update(_criar_banco(pasta_de_bancos / f"climbra_{m}.db", [m]))
    assert sorted(Path(p).name for p in cd.get_climate_db_paths()) == sorted(f"climbra_{m}.db" for m in MODELOS)
    assert cd.get_available_climate_models() == ["INM-CM4", "ACCESS-CM2"]
    assert sorted(cd.get_available_climate_cities()) == sorted(CIDADES)
    assert cd.find_matching_climate_city_name("sao paulo") == "São Paulo"
    for (c, m, s), arr in esperado.items():
        lida, inicio, fim, total, selecionados, _ = cd.load_national_climate_series(c, m, s)
        assert np.array_equal(lida, arr.astype(np.float64))
        assert total == selecionados == DIAS[s]
    assert cd.load_national_climate_series("Belém", "INM-CM4", "SSP245")[1:3] == ("01/01/2015", "31/12/2100")

def test_a_serie_e_lida_em_outra_thread_e_o_cache_nao_se_corrompe(pasta_de_bancos):
    """Regressão: a conexão aberta na thread da interface falhava na thread de simulação (a série
    «não existia»), e quem alterava o array devolvido corrompia o cache compartilhado."""
    import threading
    _criar_banco(pasta_de_bancos / "climbra_INM-CM4.db", ["INM-CM4"])
    primeira = _ler("Belém", "INM-CM4", "HIST")
    esperado = primeira.copy()
    resultado = {}

    def _na_thread():
        try:
            resultado["serie"] = _ler("Belém", "INM-CM4", "SSP245")
        except Exception as erro:  # pragma: no cover - o que se quer evitar
            resultado["erro"] = repr(erro)

    t = threading.Thread(target=_na_thread)
    t.start()
    t.join()
    assert "erro" not in resultado, resultado.get("erro")
    assert len(resultado["serie"]) == DIAS["SSP245"]
    primeira[:] = 0.0                                   # o chamador altera a sua cópia...
    assert np.array_equal(_ler("Belém", "INM-CM4", "HIST"), esperado)   # ...e o cache segue intacto


def test_caminho_do_banco_aponta_para_uma_parte(pasta_de_bancos):
    _criar_banco(pasta_de_bancos / "climbra_ACCESS-CM2.db", ["ACCESS-CM2"])
    _criar_banco(pasta_de_bancos / "climbra_INM-CM4.db", ["INM-CM4"])
    caminho = cd.get_climate_db_path()
    assert Path(caminho).name == "climbra_INM-CM4.db"      # o modelo padrão
    assert os.path.isfile(caminho)


def test_continua_lendo_o_banco_unico_antigo(pasta_de_bancos):
    esperado = _criar_banco(pasta_de_bancos / "climbra.db", MODELOS)
    assert [Path(p).name for p in cd.get_climate_db_paths()] == ["climbra.db"]
    assert Path(cd.get_climate_db_path()).name == "climbra.db"
    assert cd.get_available_climate_models() == ["INM-CM4", "ACCESS-CM2"]
    for (c, m, s), arr in esperado.items():
        assert np.array_equal(_ler(c, m, s), arr.astype(np.float64))


def test_a_parte_tem_precedencia_e_o_banco_unico_cobre_o_que_falta(pasta_de_bancos):
    unico = _criar_banco(pasta_de_bancos / "climbra.db", MODELOS, deslocamento=1.0)     # valores distintos
    parte = _criar_banco(pasta_de_bancos / "climbra_INM-CM4.db", ["INM-CM4"])
    cd.limpar_cache_da_base()
    # modelo com parte: vale a parte
    assert np.array_equal(_ler("Belém", "INM-CM4", "HIST"), parte[("Belém", "INM-CM4", "HIST")].astype(np.float64))
    # modelo sem parte: cai no banco único
    assert np.array_equal(_ler("Belém", "ACCESS-CM2", "HIST"), unico[("Belém", "ACCESS-CM2", "HIST")].astype(np.float64))


def test_modelo_dividido_por_cenario(pasta_de_bancos):
    esperado = {}
    for cen in DIAS:
        esperado.update(_criar_banco(pasta_de_bancos / f"climbra_INM-CM4__{cen}.db", ["INM-CM4"], cenarios=(cen,)))
    assert cd.get_available_climate_models() == ["INM-CM4"]
    for (c, m, s), arr in esperado.items():
        assert np.array_equal(_ler(c, m, s), arr.astype(np.float64))


def test_modelo_ausente_nos_bancos_gera_erro_claro(pasta_de_bancos, tmp_path):
    _criar_banco(pasta_de_bancos / "climbra_INM-CM4.db", ["INM-CM4"])
    with pytest.raises(FileNotFoundError):
        cd.load_national_climate_series("São Paulo", "KACE", "HIST")


def test_variavel_de_ambiente_com_um_arquivo_de_parte(tmp_path, monkeypatch):
    arquivo = tmp_path / "climbra_KACE.db"
    esperado = _criar_banco(arquivo, ["KACE"])
    monkeypatch.delenv("TRITON_CLIMATE_DB", raising=False)
    monkeypatch.setenv("TRITON_CLIMBRA_DB", str(arquivo))
    cd.limpar_cache_da_base()
    try:
        assert cd.get_climate_db_path() == str(arquivo.resolve())
        assert np.array_equal(_ler("Belém", "KACE", "SSP585"), esperado[("Belém", "KACE", "SSP585")].astype(np.float64))
    finally:
        cd.limpar_cache_da_base()


def test_sem_bancos_nao_ha_caminho(tmp_path, monkeypatch):
    monkeypatch.setenv("TRITON_CLIMBRA_DB", str(tmp_path))      # pasta sem bancos
    monkeypatch.delenv("TRITON_CLIMATE_DB", raising=False)
    monkeypatch.setattr(cd, "_pastas_de_busca", lambda: [str(tmp_path)])
    cd.limpar_cache_da_base()
    try:
        assert cd.get_climate_db_path() is None
        assert cd.get_climate_db_paths() == []
        assert cd.get_available_climate_models() == []
    finally:
        cd.limpar_cache_da_base()


# ── Base real, se estiver no disco ───────────────────────────────────────────

DATA = RAIZ / "data"
PARTES_REAIS = sorted(DATA.glob("climbra_*.db"))
BANCO_UNICO = DATA / "climbra.db"


@pytest.fixture
def base_real(monkeypatch):
    if not PARTES_REAIS:
        pytest.skip("partes data/climbra_<modelo>.db ausentes nesta máquina")
    for variavel in ("TRITON_CLIMBRA_DB", "TRITON_CLIMATE_DB", "TRITON_CLIMBRA_DIR"):
        monkeypatch.delenv(variavel, raising=False)
    monkeypatch.setenv("TRITON_CLIMBRA_DIR", str(DATA))
    cd.limpar_cache_da_base()
    yield
    cd.limpar_cache_da_base()


def test_partes_reais_cabem_no_github(base_real):
    assert len(PARTES_REAIS) == len(cd.CLIMATE_MODELS)
    assert {p.stem[len("climbra_"):] for p in PARTES_REAIS} == set(cd.CLIMATE_MODELS)
    for parte in PARTES_REAIS:
        assert parte.stat().st_size < 50 * 1024 * 1024, f"{parte.name} passa do aviso de 50 MB do GitHub"
    assert cd.get_available_climate_models() == cd.CLIMATE_MODELS
    assert len(cd.get_available_climate_cities()) == 652


@pytest.mark.skipif(not BANCO_UNICO.is_file(), reason="climbra.db único ausente nesta máquina")
def test_partes_reais_dao_a_mesma_serie_que_o_banco_unico(base_real):
    cidades = ["São Paulo", "Florianópolis", "Manaus", "Brasília", "Salvador", "Cruzeiro do Sul"]
    modelos = ["INM-CM4", "ACCESS-CM2", "KACE", "UKESM1-0-LL", "NorESM2-MM"]   # com e sem calendário de 360 dias
    unico = sqlite3.connect(f"file:{BANCO_UNICO.as_posix()}?mode=ro", uri=True)
    try:
        for c in cidades:
            real = cd.find_matching_climate_city_name(c)
            for m in modelos:
                for s in cd.CLIMATE_SCENARIOS:
                    contagem, blob = unico.execute(
                        "SELECT count, data FROM climbra_series WHERE city = ? AND model = ? AND scenario = ?",
                        (real, m, s)).fetchone()
                    bruto = zlib.decompress(blob)
                    dtype = np.float16 if len(bruto) == contagem * 2 else np.float32
                    esperado = np.frombuffer(bruto, dtype=dtype).astype(np.float64)
                    lida, _i, _f, total, _sel, _p = cd.load_national_climate_series(c, m, s)
                    assert total == contagem
                    assert np.array_equal(lida, esperado), (c, m, s)
    finally:
        unico.close()


def test_as_partes_reais_batem_com_o_manifesto():
    """Íntegras: SHA-256 do arquivo, contagem de séries e limite de 100 MB do GitHub, sem script de apoio."""
    manifesto_arquivo = DATA / "climbra_partes.json"
    if not manifesto_arquivo.is_file() or not PARTES_REAIS:
        pytest.skip("partes data/climbra_<modelo>.db ou manifesto ausentes nesta máquina")
    manifesto = json.loads(manifesto_arquivo.read_text(encoding="utf-8"))
    registros = {p["arquivo"]: p for p in manifesto["partes"]}
    assert sorted(p.name for p in PARTES_REAIS) == sorted(registros), "partes e manifesto não coincidem"
    assert {p["modelo"] for p in registros.values()} == set(cd.CLIMATE_MODELS)
    total = 0
    for parte in PARTES_REAIS:
        registro = registros[parte.name]
        assert parte.stat().st_size < 100 * 1024 * 1024, f"{parte.name} passa do limite de 100 MB do GitHub"
        resumo = hashlib.sha256()
        with open(parte, "rb") as f:
            for bloco in iter(lambda: f.read(1 << 20), b""):
                resumo.update(bloco)
        assert resumo.hexdigest() == registro["sha256"], f"{parte.name}: SHA-256 difere do manifesto"
        conn = sqlite3.connect(f"file:{parte.as_posix()}?mode=ro", uri=True)
        try:
            series = conn.execute("SELECT COUNT(*) FROM climbra_series").fetchone()[0]
        finally:
            conn.close()
        assert series == registro["series"], f"{parte.name}: {series} séries, o manifesto diz {registro['series']}"
        total += series
    assert str(total) == manifesto["origem"]["total_series"]
