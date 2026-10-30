# -*- coding: utf-8 -*-
"""``triton estudo consolidar``: junta os ``resultados.csv`` de vários estudos; duckdb e biblioteca padrão dão os mesmos bytes."""
import csv
import os
import random
import subprocess
import sys
from pathlib import Path

import pytest

from triton.core import _opcional
from triton.core import estudo as E
from triton.core import estudo_consolidar as C

RAIZ = Path(__file__).resolve().parents[2]
CABECALHO = ["estudo_id", "caso_id", "caso", "grupo", "metrica", "rotulo", "valor", "unidade", "status"]


def _escrever(pasta, estudo_id, linhas, dims=None):
    """Grava um resultados.csv como o ``estudo run`` (com colunas de dimensão opcionais entre ``grupo`` e ``metrica``)."""
    dims = dims or {}
    pasta.mkdir(parents=True, exist_ok=True)
    cab = CABECALHO[:4] + list(dims) + CABECALHO[4:]
    with open(pasta / "resultados.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cab)
        for caso_id, nome, grupo, metrica, valor, unidade, status in linhas:
            w.writerow([estudo_id, caso_id, nome, grupo, *dims.values(), metrica, f"rot {metrica}", valor, unidade, status])


@pytest.fixture()
def pasta_de_execucoes(tmp_path):
    base = tmp_path / "execucoes"
    _escrever(base / "lote1" / "est-a", "est-a", [
        ("c1", "Prédio, «A»", "escolar", "economia_agua_potavel_pct", "40.0", "%", "ok"),
        ("c2", "Prédio B", "escolar", "economia_agua_potavel_pct", "60.0", "%", "ok"),
        ("c1", "Prédio, «A»", "escolar", "volume_l", "5000.0", "L", "ok"),
        ("c3", "Falhou", "escolar", "volume_l", "", "L", "erro"),
    ], dims={"cidade": "X"})
    _escrever(base / "lote1" / "est-b", "est-b", [
        ("c1", "Prédio, «A»", "escolar", "economia_agua_potavel_pct", "50.0", "%", "ok"),
        ("c9", "Casa", "comercial", "economia_agua_potavel_pct", "10.5", "%", "ok"),
        ("c9", "Casa", "comercial", "economia_anual_agua", "1234.5", "R$", "ok"),
        ("c9", "Casa", "comercial", "economia_anual_agua", "99.0", "€", "ok"),
    ])
    _escrever(base / "outro" / "est-c", "est-c", [
        ("c1", "Prédio, «A»", "escolar", "economia_agua_potavel_pct", "45.5", "%", "ok"),
    ])
    return base


def _bytes(pasta):
    return {n: (pasta / n).read_bytes() for n in ("consolidado.csv", "consolidado.md")}


def test_agrupa_por_tipologia_caso_metrica_com_as_quatro_estatisticas(pasta_de_execucoes, tmp_path):
    arquivos, n_arq, n_linhas, motor = C.consolidar([pasta_de_execucoes], tmp_path / "s", "en", "csv")
    assert arquivos == ["consolidado.csv", "consolidado.md"] and n_arq == 3 and motor == "csv"
    linhas = list(csv.DictReader(open(tmp_path / "s" / "consolidado.csv", encoding="utf-8", newline="")))
    assert list(linhas[0]) == C.CABECALHO_CSV and len(linhas) == n_linhas
    por = {(L["tipologia"], L["caso_id"], L["metrica"], L["unidade"]): L for L in linhas}
    eco = por[("escolar", "c1", "economia_agua_potavel_pct", "%")]
    assert (eco["n"], eco["estudos"], eco["registros"]) == ("3", "3", "3")
    assert (eco["minimo"], eco["media"], eco["mediana"], eco["maximo"]) == ("40.0", "45.16666667", "45.5", "50.0")
    assert eco["caso"] == "Prédio, «A»"                                   # vírgula e aspas sobrevivem ao CSV
    falhou = por[("escolar", "c3", "volume_l", "L")]
    assert (falhou["n"], falhou["registros"], falhou["media"]) == ("0", "1", "")   # caso com erro: sem estatística
    # moedas diferentes nunca se misturam: o grupo é separado pela unidade
    assert por[("comercial", "c9", "economia_anual_agua", "R$")]["n"] == "1"
    assert por[("comercial", "c9", "economia_anual_agua", "€")]["n"] == "1"


def test_ordem_estavel_e_independente_da_ordem_das_pastas(pasta_de_execucoes, tmp_path):
    C.consolidar([pasta_de_execucoes / "lote1", pasta_de_execucoes / "outro"], tmp_path / "a", "en", "csv")
    C.consolidar([pasta_de_execucoes / "outro", pasta_de_execucoes / "lote1", pasta_de_execucoes / "outro"], tmp_path / "b", "en", "csv")
    assert _bytes(tmp_path / "a") == _bytes(tmp_path / "b")
    chaves = [(L["tipologia"], L["caso_id"], L["metrica"], L["unidade"])
              for L in csv.DictReader(open(tmp_path / "a" / "consolidado.csv", encoding="utf-8", newline=""))]
    assert chaves == sorted(chaves)


def test_numeros_com_a_formatacao_do_estudo_run_e_markdown_no_idioma(pasta_de_execucoes, tmp_path):
    C.consolidar([pasta_de_execucoes], tmp_path / "pt", "pt-BR", "csv")
    C.consolidar([pasta_de_execucoes], tmp_path / "en", "en", "csv")
    texto = (tmp_path / "pt" / "consolidado.csv").read_text(encoding="utf-8")
    assert "45.16666667" in texto and "\r" not in texto                     # ponto decimal, 10 algarismos, fim de linha LF
    md_pt = (tmp_path / "pt" / "consolidado.md").read_text(encoding="utf-8")
    md_en = (tmp_path / "en" / "consolidado.md").read_text(encoding="utf-8")
    assert "Consolidado dos resultados" in md_pt and "45,2" in md_pt and "Mediana" in md_pt
    assert "Consolidated results" in md_en and "45.2" in md_en and "Median" in md_en
    for md in (md_pt, md_en):
        assert str(tmp_path) not in md and "\\" not in md.split("|")[0]       # sem caminho da máquina


def test_pastas_sem_resultados_ou_com_cabecalho_errado_dao_erro_claro(tmp_path):
    vazia = tmp_path / "vazia"
    vazia.mkdir()
    with pytest.raises(ValueError, match="resultados.csv"):
        C.consolidar([vazia], tmp_path / "s", "en", "csv")
    with pytest.raises(FileNotFoundError):
        C.consolidar([tmp_path / "nao_existe"], tmp_path / "s", "en", "csv")
    ruim = tmp_path / "ruim"
    ruim.mkdir()
    (ruim / "resultados.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="estudo_id"):
        C.consolidar([ruim], tmp_path / "s", "en", "csv")
    with pytest.raises(ValueError, match="motor|engine"):
        C.agrupar([], "xyz")


def test_motor_duckdb_sem_o_pacote_diz_o_extra(pasta_de_execucoes, tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "duckdb", None)
    with pytest.raises(ValueError, match=r"\[analise\]"):
        C.consolidar([pasta_de_execucoes], tmp_path / "s", "en", "duckdb")
    # auto sem o pacote cai na biblioteca padrão, sem erro
    monkeypatch.setattr(_opcional, "disponivel", lambda nome: False)
    assert C.consolidar([pasta_de_execucoes], tmp_path / "s", "en", "auto")[3] == "csv"


def _gerar_muitos(base, semente=7):
    rng = random.Random(semente)
    for e in range(4):
        linhas = []
        for c in range(25):
            for m, un in (("economia_agua_potavel_pct", "%"), ("volume_l", "L"), ("co2_liquido_vida_kg", "kg CO2e")):
                bruto = rng.uniform(-1e5, 1e5) if rng.random() < .9 else rng.choice([0.1 + 0.2, 1e-9, 123456789.123456789, 1 / 3])
                status = "ok" if rng.random() < .9 else "erro"
                linhas.append((f"c{c % 12:02d}", f"Caso é {c % 12}", rng.choice(["escolar", "hospitalar"]) if c % 5 == 0 else "escolar",
                               m, repr(bruto) if status == "ok" else "", un, status))
        _escrever(base / f"e{e}", f"est-{e}", linhas)
    return base


def test_duckdb_e_biblioteca_padrao_dao_os_mesmos_bytes(tmp_path):
    pytest.importorskip("duckdb")
    base = _gerar_muitos(tmp_path / "muitos")
    r_csv = C.consolidar([base], tmp_path / "csv", "en", "csv")
    r_db = C.consolidar([base], tmp_path / "db", "en", "duckdb")
    assert (r_csv[3], r_db[3]) == ("csv", "duckdb") and r_csv[1:3] == r_db[1:3]
    assert _bytes(tmp_path / "csv") == _bytes(tmp_path / "db")
    assert C.consolidar([base], tmp_path / "auto", "en", "auto")[3] == "duckdb"
    assert _bytes(tmp_path / "auto") == _bytes(tmp_path / "db")


def test_so_biblioteca_padrao_e_deterministico_em_duas_execucoes(tmp_path):
    base = _gerar_muitos(tmp_path / "muitos")
    C.consolidar([base], tmp_path / "x", "pt-BR", "csv")
    C.consolidar([base], tmp_path / "y", "pt-BR", "csv")
    assert _bytes(tmp_path / "x") == _bytes(tmp_path / "y")
    assert len((tmp_path / "x" / "consolidado.csv").read_text(encoding="utf-8").splitlines()) > 20


def test_consolidar_um_estudo_real_confere_com_o_resultados_csv(tmp_path):
    """Pasta de saída de verdade (``csv_tidy``): a média de um caso único é o próprio valor do ``resultados.csv``."""
    plano = {"estudo": {"id": "e1"}, "casos": [{"id": "c1", "nome": "Caso 1", "grupo": "escolar"}],
             "saidas": {"metricas": ["volume_l"]}}
    res = [{"status": "ok", "metricas": {"volume_l": 7000.0}}]
    texto = E.csv_tidy(plano, res, "en")
    pasta = tmp_path / "saida" / "e1"
    pasta.mkdir(parents=True)
    (pasta / "resultados.csv").write_text(texto, encoding="utf-8", newline="")
    C.consolidar([tmp_path / "saida"], tmp_path / "s", "en", "csv")
    linha = list(csv.DictReader(open(tmp_path / "s" / "consolidado.csv", encoding="utf-8", newline="")))[0]
    esperado = list(csv.DictReader(texto.splitlines(), delimiter=","))[0]["valor"]
    assert linha["media"] == linha["minimo"] == linha["maximo"] == esperado and linha["n"] == "1"


def test_cli_consolidar_de_ponta_a_ponta(pasta_de_execucoes, tmp_path):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "consolidar", str(pasta_de_execucoes), "--saida",
                        str(tmp_path / "s"), "--motor", "csv"], cwd=str(RAIZ), env=env, capture_output=True, text=True,
                       encoding="utf-8", timeout=300)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "s" / "consolidado.csv").is_file() and "consolidado.md" in r.stdout
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "consolidar", str(tmp_path / "nada"), "--saida",
                        str(tmp_path / "s2")], cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 2 and not (tmp_path / "s2").exists()


def test_o_modulo_nao_importa_o_duckdb_no_topo():
    import ast
    arvore = ast.parse((RAIZ / "triton" / "core" / "estudo_consolidar.py").read_text(encoding="utf-8"))
    topo = {a.name.split(".")[0] for n in arvore.body if isinstance(n, ast.Import) for a in n.names}
    topo |= {n.module.split(".")[0] for n in arvore.body if isinstance(n, ast.ImportFrom) and n.module}
    assert "duckdb" not in topo
