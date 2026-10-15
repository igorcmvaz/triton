"""
Base CLIMBra dividida por modelo (`data/climbra_<modelo>.db`): descoberta, leitura e equivalência.

Duas frentes:
- o leitor (`triton/core/climate_database.py`), que roda nas três edições, com bancos sintéticos;
- os scripts de manutenção da Edição Brasil (`scripts/dividir_base_climbra.py` e
  `scripts/compilar_base_climbra.py`), que só existem nela e são saltados nas outras.

Se a base real estiver presente (`data/climbra.db` e as partes), compara amostras: a série lida
das partes tem de ser idêntica à do banco único.
"""

import importlib
import json
import os
import sqlite3
import sys
import zlib
from pathlib import Path

import numpy as np
import pytest

from triton.core import climate_database as cd

RAIZ = Path(__file__).resolve().parents[2]
SCRIPTS = RAIZ / "scripts"

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


# ── Scripts da Edição Brasil ─────────────────────────────────────────────────

def _modulo_do_script(nome):
    if not (SCRIPTS / f"{nome}.py").is_file():
        pytest.skip(f"scripts/{nome}.py existe só na Edição Brasil")
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    return importlib.import_module(nome)


def test_dividir_gera_partes_identicas_ao_banco_unico(tmp_path, pasta_de_bancos):
    div = _modulo_do_script("dividir_base_climbra")
    origem = tmp_path / "climbra.db"
    esperado = _criar_banco(origem, MODELOS, meta={"dtype": "float16", "compiled_at": "2026-01-01T00:00:00",
                                                    "title": "x", "license": "CC0"})
    destino = tmp_path / "partes"
    registros = div.dividir(str(origem), str(destino), verbose=False)
    assert sorted(r["arquivo"] for r in registros) == sorted(f"climbra_{m}.db" for m in MODELOS)
    assert div.verificar(str(destino), str(origem), verbose=False) == []

    # metadados da parte
    conn = sqlite3.connect(str(destino / "climbra_INM-CM4.db"))
    meta = dict(conn.execute("SELECT key, value FROM climbra_meta"))
    nomes = {n for (n,) in conn.execute("SELECT name FROM sqlite_master")}
    conn.close()
    assert meta["model"] == "INM-CM4" and meta["schema_version"] == "2" and meta["layout"] == "per-model"
    assert meta["scenarios"] == "HIST,SSP245,SSP585" and meta["total_series"] == str(len(CIDADES) * 3)
    assert json.loads(meta["periods"])["SSP245"]["end"] == "2100-12-31"
    assert len(meta["content_sha256"]) == 64
    assert {"climbra_meta", "climbra_cities", "climbra_series", "idx_climbra_cities_norm"} <= nomes

    # equivalência pelo leitor: copia só as partes para a pasta que ele consulta
    for arq in destino.glob("climbra_*.db"):
        (pasta_de_bancos / arq.name).write_bytes(arq.read_bytes())
    cd.limpar_cache_da_base()
    assert [Path(p).name for p in cd.get_climate_db_paths()] == sorted(f"climbra_{m}.db" for m in MODELOS)
    for (c, m, s), arr in esperado.items():
        assert np.array_equal(_ler(c, m, s), arr.astype(np.float64))


def test_verificar_acusa_arquivo_adulterado_e_serie_diferente(tmp_path):
    div = _modulo_do_script("dividir_base_climbra")
    origem = tmp_path / "climbra.db"
    _criar_banco(origem, ["INM-CM4"], meta={"dtype": "float16"})
    destino = tmp_path / "partes"
    div.dividir(str(origem), str(destino), verbose=False)
    parte = destino / "climbra_INM-CM4.db"
    conn = sqlite3.connect(str(parte))
    conn.execute("UPDATE climbra_series SET data = ? WHERE city = 'Belém' AND scenario = 'HIST'",
                 (zlib.compress(np.zeros(DIAS["HIST"], dtype=np.float16).tobytes()),))
    conn.commit()
    conn.close()
    problemas = div.verificar(str(destino), str(origem), verbose=False)
    texto = "\n".join(problemas)
    assert "SHA-256 do arquivo" in texto
    assert "hash do conteúdo" in texto
    assert "difere da origem" in texto


def test_modelo_acima_do_limite_e_dividido_por_cenario(tmp_path, pasta_de_bancos):
    div = _modulo_do_script("dividir_base_climbra")
    origem = tmp_path / "climbra.db"
    esperado = _criar_banco(origem, ["INM-CM4"], meta={"dtype": "float16"})
    destino = tmp_path / "partes"
    registros = div.dividir(str(origem), str(destino), limite_mb=0.01, verbose=False)
    assert sorted(r["arquivo"] for r in registros) == [f"climbra_INM-CM4__{c}.db" for c in sorted(DIAS)]
    assert not (destino / "climbra_INM-CM4.db").exists()
    assert div.verificar(str(destino), str(origem), verbose=False) == []
    for arq in destino.glob("climbra_*.db"):
        (pasta_de_bancos / arq.name).write_bytes(arq.read_bytes())
    cd.limpar_cache_da_base()
    for (c, m, s), arr in esperado.items():
        assert np.array_equal(_ler(c, m, s), arr.astype(np.float64))


def test_compilar_gera_as_partes_direto_dos_csv(tmp_path, pasta_de_bancos):
    comp = _modulo_do_script("compilar_base_climbra")
    csv_dir = tmp_path / "csv"
    csv_dir.mkdir()
    esperado = {}
    sufixo = {"HIST": "_Histórico", "SSP245": "_SSP245", "SSP585": "_SSP585"}
    for m in MODELOS:
        for c in CIDADES:
            for s in DIAS:
                arr = _serie(c, m, s)
                esperado[(c, m, s)] = arr
                (csv_dir / f"(Triton){c}_{m}{sufixo[s]}.csv").write_text(
                    "\n".join(f"{float(v):.1f}".replace(".", ",") for v in arr) + "\n", encoding="utf-8")
    saida = tmp_path / "saida"
    registros = comp.compile_partes(str(csv_dir), str(saida), num_workers=1)
    assert sorted(r["arquivo"] for r in registros) == sorted(f"climbra_{m}.db" for m in MODELOS)
    assert comp.verify_partes(str(saida)) is True
    for arq in saida.glob("climbra_*.db"):
        (pasta_de_bancos / arq.name).write_bytes(arq.read_bytes())
    cd.limpar_cache_da_base()
    for (c, m, s), arr in esperado.items():
        assert np.array_equal(_ler(c, m, s), arr.astype(np.float64))


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
