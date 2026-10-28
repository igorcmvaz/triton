# -*- coding: utf-8 -*-
"""``triton estudo``: rodar o estudo-exemplo da edição de ponta a ponta, as saídas para o artigo, o determinismo,
a retomada, o paralelo, o resumo, o texto com marcadores e o lote.

O exemplo de cada edição está em ``examples/estudos/<tipologia>-exemplo/`` (3 casos). Nada aqui inventa dado: os
estudos montados nos testes reusam o projeto de exemplo da edição, copiado para a pasta temporária.
"""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from triton import __version__
from triton.core import estudo as E
from triton.core.edition import get_current_edition

RAIZ = Path(__file__).resolve().parents[2]
ED = get_current_edition()
EXEMPLO = RAIZ / "examples" / "estudos" / {"BRL": "tres-tipologias-exemplo", "INT": "residencial-unifamiliar-exemplo",
                                          "IBE": "residencial-unifamiliar-exemplo"}[ED] / "estudo.json"
IDS_DO_EXEMPLO = {"BRL": ["florianopolis-residencia", "brasilia-escritorio", "manaus-escola"],
                  "INT": ["new_york", "london", "cape_town"], "IBE": ["lisboa", "porto", "funchal"]}[ED]
PROJETO_BASE = {"BRL": "examples/estudo_caso_1_florianopolis1.triton", "INT": "examples/london.triton",
                "IBE": "examples/portugal/funchal.triton"}[ED]
DATA_FIXA = "1700000000"       # SOURCE_DATE_EPOCH: 2023-11-14
LINGUA = {"BRL": "pt-BR", "INT": "en", "IBE": "pt-PT"}[ED]

pytestmark = pytest.mark.skipif(not EXEMPLO.is_file(), reason="estudo-exemplo ausente nesta edição")


@pytest.fixture(autouse=True)
def _data_fixa(monkeypatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", DATA_FIXA)


@pytest.fixture(scope="module")
def saida_do_exemplo(tmp_path_factory):
    """O estudo-exemplo rodado uma vez; os testes só leem."""
    os.environ["SOURCE_DATE_EPOCH"] = DATA_FIXA
    pasta = tmp_path_factory.mktemp("exemplo") / "saida"
    ex = E.rodar_estudo(EXEMPLO, pasta)
    assert ex.erros == [], ex.erros
    return pasta, ex


def _arquivos(pasta: Path):
    return sorted(p for p in pasta.rglob("*") if p.is_file())


def _lido(pasta: Path):
    return {p.relative_to(pasta).as_posix(): p.read_bytes() for p in _arquivos(pasta)}


# ── o exemplo de ponta a ponta ────────────────────────────────────────────────────────────────

def test_exemplo_roda_e_gera_todas_as_saidas(saida_do_exemplo):
    pasta, ex = saida_do_exemplo
    assert ex.codigo == 0 and ex.calculados == IDS_DO_EXEMPLO and ex.pulados == []
    for nome in ("resultados.csv", "resultados.json", "tabela.md", "tabela.tex", "resumo.md", "estudo.json"):
        assert (pasta / nome).is_file(), nome
    for caso in IDS_DO_EXEMPLO:
        assert (pasta / "casos" / caso / "resultado.json").is_file()
        assert (pasta / "casos" / caso / "analise.json").is_file()


def test_csv_tidy_uma_linha_por_caso_e_metrica_com_ponto_decimal(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    texto = (pasta / "resultados.csv").read_text(encoding="utf-8")
    assert "\r" not in texto and not texto.startswith("﻿")
    linhas = list(csv.DictReader(texto.splitlines()))
    plano, _ = E.carregar_plano(EXEMPLO)
    metricas = plano["saidas"]["metricas"]
    assert len(linhas) == len(IDS_DO_EXEMPLO) * len(metricas)
    assert [l["caso_id"] for l in linhas[::len(metricas)]] == IDS_DO_EXEMPLO
    assert [l["metrica"] for l in linhas[:len(metricas)]] == metricas
    for l in linhas:
        assert l["status"] == "ok" and l["unidade"] and l["rotulo"]
        assert re.fullmatch(r"-?\d+(\.\d+)?(e-?\d+)?", l["valor"]), l      # máquina-legível: ponto, sem milhar
        float(l["valor"])


def test_json_tem_proveniencia_completa(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    dados = json.loads((pasta / "resultados.json").read_text(encoding="utf-8"))
    assert dados["esquema"] == {"nome": "triton-estudo-resultados", "versao": 1}
    pv = dados["proveniencia"]
    assert pv["triton"]["versao"] == __version__ and pv["triton"]["edicao"] == ED
    assert pv["estudo"]["sha256"] == hashlib.sha256(EXEMPLO.read_bytes()).hexdigest()
    assert pv["data_de_execucao"] == "2023-11-14"
    projetos = [a for a in pv["arquivos"] if a["papel"] == "projeto"]
    assert len(projetos) == len(IDS_DO_EXEMPLO)
    for a in projetos:
        origem = (EXEMPLO.parent / a["caminho"]).resolve()
        assert origem.is_file() and a["sha256"] == hashlib.sha256(origem.read_bytes()).hexdigest()
    assert [c["id"] for c in dados["casos"]] == IDS_DO_EXEMPLO
    for c in dados["casos"]:
        assert c["status"] == "ok" and c["fonte_da_chuva"]["serie"]["sha256"] and c["fonte_da_chuva"]["serie"]["dias"] > 3000
        assert set(c["metricas"]) == set(c["unidades"]) == {m["id"] for m in dados["metricas"]}


def test_licenca_e_credito_da_chuva_herdados_do_analyze(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    dados = json.loads((pasta / "resultados.json").read_text(encoding="utf-8"))
    fontes = " ".join(dados["fontes_da_chuva_e_licencas"])
    resumo = (pasta / "resumo.md").read_text(encoding="utf-8")
    if ED == "INT":
        assert "Open-Meteo" in fontes and "CC BY 4.0" in fontes
    elif ED == "IBE":
        assert "E-OBS" in fontes and "comerciais" in fontes
        assert "E-OBS" in resumo and "E-OBS" in (pasta / "tabela.md").read_text(encoding="utf-8")
        assert "E-OBS" in (pasta / "tabela.tex").read_text(encoding="utf-8")
    else:
        assert dados["fontes_da_chuva_e_licencas"] == []       # a BRL não muda: sem bloco de fonte


def test_metricas_batem_com_o_analyze_da_cli(saida_do_exemplo):
    """O estudo não recalcula nada à parte: os números são os do ``cli.run_analysis`` do mesmo projeto."""
    from triton import cli
    pasta, _ = saida_do_exemplo
    plano, _ = E.carregar_plano(EXEMPLO)
    caso = plano["casos"][0]
    arq = (EXEMPLO.parent / caso["projeto"]).resolve()
    bundle = cli._load_bundle(str(arq))
    rel = cli.run_analysis(bundle["config"], cli._get_precipitation(bundle), plano["analise"]["tipo"], None,
                           tuple((bundle["analysis"] or {}).get("topsis_weights", cli.PESOS_PADRAO)),
                           (bundle["analysis"] or {}).get("environmental", {}), arq.name, 0, 42)
    volume = rel["technical"]["summary"]["optimal_volume_l"]
    linha = next(r for r in rel["technical"]["alternatives"] if r["lower_tank_volume_l"] == volume)
    res = json.loads((pasta / "casos" / caso["id"] / "resultado.json").read_text(encoding="utf-8"))
    assert res["volume_selecionado_l"] == volume
    assert res["metricas"]["economia_agua_potavel_pct"] == pytest.approx(linha["potable_savings_pct"], rel=1e-9)
    assert res["metricas"]["agua_pluvial_m3_ano"] == pytest.approx(linha["annual_rainwater_m3"], rel=1e-9)


def test_saidas_sem_caminho_absoluto(saida_do_exemplo, tmp_path):
    pasta, _ = saida_do_exemplo
    proibidos = [str(pasta), str(pasta.parent), pasta.as_posix(), str(RAIZ), RAIZ.as_posix(), str(Path.home()), Path.home().as_posix()]
    unidade = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]")
    for arq in _arquivos(pasta):
        texto = arq.read_text(encoding="utf-8")
        for p in proibidos:
            assert p not in texto, f"{arq.name} cita {p}"
        assert not unidade.search(texto), f"{arq.name} traz caminho de disco: {unidade.search(texto)}"
        assert not re.search(r"(?<![\w:.])/(home|Users|tmp|var|mnt)/", texto), arq.name


def test_tabelas_md_e_tex_para_o_artigo(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    md = (pasta / "tabela.md").read_text(encoding="utf-8")
    tex = (pasta / "tabela.tex").read_text(encoding="utf-8")
    plano, _ = E.carregar_plano(EXEMPLO)
    assert md.count("\n|") >= len(IDS_DO_EXEMPLO) + 2 and "---:" in md
    for caso in plano["casos"]:
        assert caso["nome"] in md and caso["nome"] in tex
    for trecho in ("\\toprule", "\\midrule", "\\bottomrule", "\\begin{tabular}", "\\end{table}", "\\caption{", "\\label{tab:"):
        assert trecho in tex, trecho
    assert "\\usepackage{booktabs}" in tex
    corpo = tex.split("\\midrule")[1].split("\\bottomrule")[0]
    assert corpo.count("\\\\") == len(IDS_DO_EXEMPLO)
    assert re.search(r"(?<!\\)%", tex.replace("\n% ", "\n")) is None or "\\%" in tex     # % só escapado fora dos comentários
    cabecalho = tex.split("\\toprule")[1].split("\\midrule")[0]
    assert "\\%" in cabecalho and "m$^3$" in cabecalho and "_" not in cabecalho


def test_numeros_das_tabelas_no_formato_da_edicao(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    plano, _ = E.carregar_plano(EXEMPLO)
    assert E.resolver_idioma("auto") == LINGUA
    md = (pasta / "tabela.md").read_text(encoding="utf-8")
    resultado = json.loads((pasta / "casos" / IDS_DO_EXEMPLO[0] / "resultado.json").read_text(encoding="utf-8"))
    economia = resultado["metricas"]["economia_agua_potavel_pct"]
    volume = resultado["metricas"]["volume_l"]
    if ED == "INT":
        assert f"{economia:.1f}" in md and f"{volume:,.0f}" in md            # 26.8 ; 4,000
    else:
        assert f"{economia:.1f}".replace(".", ",") in md                        # 17,5
        assert f"{volume:,.0f}".replace(",", ".") in md                         # 5.000
    assert E.formatar_numero(1234.5, 1, "en") == "1,234.5"
    assert E.formatar_numero(1234.5, 1, "pt-BR") == "1.234,5"
    assert E.formatar_numero(1234.5, 1, "pt-PT") == "1.234,5"
    assert E.formatar_numero(1234.5, 1, "es") == "1.234,5"
    assert E.formatar_numero(1234.5, 1, "zh") == "1,234.5"
    assert E.formatar_numero(-0.04, 1, "en") == "0.0" and E.formatar_numero(None, 1, "en") is None


def test_resumo_md_e_curto_e_diz_o_essencial(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    resumo = (pasta / "resumo.md").read_text(encoding="utf-8")
    assert len(resumo.splitlines()) < 60
    assert f"Triton {__version__}" in resumo and ED in resumo
    plano, _ = E.carregar_plano(EXEMPLO)
    assert plano["sha256"][:12] in resumo


# ── determinismo ──────────────────────────────────────────────────────────────────────────────

def test_duas_execucoes_dao_saidas_identicas(saida_do_exemplo, tmp_path):
    pasta, _ = saida_do_exemplo
    outra = tmp_path / "outra"
    E.rodar_estudo(EXEMPLO, outra)
    a, b = _lido(pasta), _lido(outra)
    assert sorted(a) == sorted(b)
    diferentes = [k for k in a if a[k] != b[k]]
    assert not diferentes, diferentes


def test_ordem_dos_casos_segue_o_estudo_nao_o_alfabeto(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    dados = json.loads((pasta / "resultados.json").read_text(encoding="utf-8"))
    assert [c["id"] for c in dados["casos"]] == IDS_DO_EXEMPLO


def test_paralelo_da_o_mesmo_resultado_que_o_serial(saida_do_exemplo, tmp_path):
    pasta, _ = saida_do_exemplo
    par = tmp_path / "paralelo"
    ex = E.rodar_estudo(EXEMPLO, par, paralelo=2)
    assert ex.codigo == 0 and ex.calculados == IDS_DO_EXEMPLO
    a, b = _lido(pasta), _lido(par)
    assert [k for k in a if a[k] != b[k]] == []


# ── retomada ──────────────────────────────────────────────────────────────────────────────────

def test_pasta_com_resultados_exige_retomar_ou_sobrescrever(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    with pytest.raises(ValueError, match="retomar"):
        E.rodar_estudo(EXEMPLO, pasta)


def test_retomar_pula_os_casos_prontos(tmp_path):
    saida = tmp_path / "s"
    E.rodar_estudo(EXEMPLO, saida)
    antes = _lido(saida)
    ex = E.rodar_estudo(EXEMPLO, saida, retomar=True)
    assert ex.calculados == [] and ex.pulados == IDS_DO_EXEMPLO and ex.codigo == 0
    assert _lido(saida) == antes


def test_retomar_refaz_so_o_que_faltou_ou_mudou(tmp_path):
    saida = tmp_path / "s"
    E.rodar_estudo(EXEMPLO, saida)
    apagado = IDS_DO_EXEMPLO[1]
    shutil.rmtree(saida / "casos" / apagado)
    ex = E.rodar_estudo(EXEMPLO, saida, retomar=True)
    assert ex.calculados == [apagado] and ex.pulados == [i for i in IDS_DO_EXEMPLO if i != apagado]
    # caso cujo resultado ficou com a impressão digital de outro estudo: é refeito
    arq = saida / "casos" / IDS_DO_EXEMPLO[0] / "resultado.json"
    dados = json.loads(arq.read_text(encoding="utf-8"))
    dados["chave"] = "0" * 64
    arq.write_text(json.dumps(dados), encoding="utf-8")
    ex = E.rodar_estudo(EXEMPLO, saida, retomar=True)
    assert ex.calculados == [IDS_DO_EXEMPLO[0]]


def test_sobrescrever_refaz_tudo(tmp_path):
    saida = tmp_path / "s"
    E.rodar_estudo(EXEMPLO, saida)
    ex = E.rodar_estudo(EXEMPLO, saida, sobrescrever=True)
    assert ex.calculados == IDS_DO_EXEMPLO and ex.pulados == []


# ── estudos montados nos testes (projeto de exemplo copiado) ──────────────────────────────────

def _pasta_com_base(tmp_path):
    origem = RAIZ / PROJETO_BASE
    if not origem.is_file():
        pytest.skip("projeto de exemplo ausente")
    shutil.copyfile(origem, tmp_path / "base.triton")
    return tmp_path


def _gravar(pasta, nome, doc):
    arq = pasta / nome
    arq.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return arq


def _estudo(eid="teste", tipologia="escolar", casos=None, **extra):
    doc = {"esquema": {"nome": "triton-estudo", "versao": 1},
           "estudo": {"id": eid, "titulo": f"Estudo {eid}", "tipologia": tipologia},
           "projeto_base": {"arquivo": "base.triton"},
           "casos": casos or [{"id": "c1", "nome": "Caso 1", "substituicoes": {"area_captacao_m2": 120}},
                              {"id": "c2", "nome": "Caso 2", "substituicoes": {"area_captacao_m2": 240}}],
           "analise": {"tipo": "technical"},
           "saidas": {"metricas": ["volume_l", "economia_agua_potavel_pct", "agua_pluvial_m3_ano"], "idioma": "en"}}
    doc.update(extra)
    return doc


def test_mais_area_aproveita_mais_chuva(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    arq = _gravar(pasta, "estudo.json", _estudo())
    ex = E.rodar_estudo(arq, pasta / "s")
    assert ex.codigo == 0
    v = {r["id"]: r["metricas"]["agua_pluvial_m3_ano"] for r in ex.resultados}
    assert v["c2"] > v["c1"] > 0


def test_modelo_da_edicao_com_serie_de_chuva_da_edicao(tmp_path):
    """Sem projeto base: o modelo da edição, em que nada é presumido, e a série de exemplo da edição por nome."""
    from triton.core.edition import serie_de_exemplo_da_edicao
    doc = _estudo(projeto_base={"modelo": "edicao"}, casos=[
        {"id": "m1", "clima": {"arquivo": serie_de_exemplo_da_edicao(), "nome": "Local de teste"},
         "substituicoes": {"area_captacao_m2": 150, "usuarios": 4, "demanda_per_capita_l_dia": 120, "fracao_pluvial_pct": 40,
                           "volume_maximo_l": 10000, "passo_volume_l": 1000}}])
    arq = _gravar(tmp_path, "estudo.json", doc)
    plano, _ = E.carregar_plano(arq)
    assert E.verificar_casos(plano) == []
    ex = E.rodar_estudo(arq, tmp_path / "s")
    assert ex.codigo == 0, ex.resultados[0].get("erro")
    m = ex.resultados[0]["metricas"]
    assert m["area_captacao_m2"] == 150 and m["usuarios"] == 4 and m["demanda_total_l_dia"] == 480 and m["fracao_pluvial_pct"] == pytest.approx(40)
    assert 0 < m["economia_agua_potavel_pct"] <= 40 and m["dias_da_serie"] > 3000
    assert ex.resultados[0]["fonte_da_chuva"]["serie"]["sha256"]


def test_caso_com_erro_nao_derruba_o_estudo_e_da_codigo_1(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    (pasta / "quebrado.triton").write_text(json.dumps({"schema": {"name": "outro"}}), encoding="utf-8")
    doc = _estudo(casos=[{"id": "bom", "substituicoes": {"area_captacao_m2": 150}},
                         {"id": "ruim", "projeto": "quebrado.triton"}])
    arq = _gravar(pasta, "estudo.json", doc)
    ex = E.rodar_estudo(arq, pasta / "s")
    assert ex.codigo == 1 and ex.erros == ["ruim"] and ex.calculados == ["bom"]
    linhas = list(csv.DictReader((pasta / "s" / "resultados.csv").read_text(encoding="utf-8").splitlines()))
    assert {l["status"] for l in linhas if l["caso_id"] == "ruim"} == {"erro"}
    assert all(l["valor"] == "" for l in linhas if l["caso_id"] == "ruim")
    dados = json.loads((pasta / "s" / "resultados.json").read_text(encoding="utf-8"))
    ruim = next(c for c in dados["casos"] if c["id"] == "ruim")
    assert ruim["status"] == "erro" and ruim["erro"] and str(pasta) not in ruim["erro"]
    assert "--" in (pasta / "s" / "tabela.tex").read_text(encoding="utf-8")        # célula vazia
    # a CLI devolve 1
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "run", str(arq), "--saida", str(pasta / "s2"), "--quiet"],
                       cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
    assert r.returncode == 1, (r.stdout, r.stderr)


def test_cli_run_devolve_zero_e_imprime_o_resumo(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    arq = _gravar(pasta, "estudo.json", _estudo())
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "run", str(arq), "--saida", str(pasta / "s")],
                       cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
    assert r.returncode == 0, r.stderr
    assert "tabela.tex" in r.stdout and "[1/2]" in r.stderr
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "run", str(arq), "--saida", str(pasta / "s")],
                       cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
    assert r.returncode == 2 and "retomar" in r.stderr


def test_paralelo_invalido(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    arq = _gravar(pasta, "estudo.json", _estudo())
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "run", str(arq), "--saida", str(pasta / "s"), "--paralelo", "0"],
                       cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
    assert r.returncode == 2


def test_validate_fundo_acha_o_caminho_pontilhado_errado(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    doc = _estudo(casos=[{"id": "x", "substituicoes": {"inputs.nao_existe.campo": 1}}])
    arq = _gravar(pasta, "estudo.json", doc)
    plano, _ = E.carregar_plano(arq)
    erros = E.verificar_casos(plano)
    assert len(erros) == 1 and "nao_existe" in erros[0] and "casos[0] (x)" in erros[0]
    assert str(pasta) not in erros[0]


def test_formatos_pedidos_sao_os_gravados(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    doc = _estudo()
    doc["saidas"]["formatos"] = ["csv", "md"]
    arq = _gravar(pasta, "estudo.json", doc)
    E.rodar_estudo(arq, pasta / "s")
    nomes = {p.name for p in (pasta / "s").iterdir() if p.is_file()}
    assert nomes == {"resultados.csv", "tabela.md", "resumo.md", "estudo.json"}


def test_xlsx_opcional_tem_numeros_de_verdade(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    pasta = _pasta_com_base(tmp_path)
    doc = _estudo()
    doc["saidas"]["formatos"] = ["xlsx"]
    arq = _gravar(pasta, "estudo.json", doc)
    E.rodar_estudo(arq, pasta / "s")
    wb = openpyxl.load_workbook(pasta / "s" / "tabela.xlsx")
    assert wb.sheetnames == ["tabela", "tidy", "proveniencia"]
    ws = wb["tabela"]
    assert ws.max_row == 3 and isinstance(ws.cell(row=2, column=3).value, float)
    assert any("sha256" in str(c.value) or len(str(c.value)) == 64 for row in wb["proveniencia"].iter_rows() for c in row)


def test_orientacao_metricas_nas_linhas_e_idiomas(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    doc = _estudo()
    doc["saidas"].update(orientacao="metricas_nas_linhas", idioma="es")
    arq = _gravar(pasta, "estudo.json", doc)
    E.rodar_estudo(arq, pasta / "s")
    md = (pasta / "s" / "tabela.md").read_text(encoding="utf-8")
    assert "Métrica" in md and "Caso 1" in md and "Ahorro de agua potable" in md
    plano, res = E.carregar_saida(pasta / "s")
    for idioma, termo in (("zh", "饮用水节约率"), ("en", "Potable water saving"), ("pt-BR", "Economia de água potável")):
        assert termo in E.tabela_md(plano, res, idioma)


def test_casas_decimais_por_metrica(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    doc = _estudo()
    doc["saidas"]["casas_decimais"] = {"padrao": 0, "economia_agua_potavel_pct": 3}
    arq = _gravar(pasta, "estudo.json", doc)
    E.rodar_estudo(arq, pasta / "s")
    plano, res = E.carregar_saida(pasta / "s")
    tab = E.montar_tabela(plano, res, "en")
    assert re.fullmatch(r"\d+\.\d{3}", tab["linhas"][0][2]) and re.fullmatch(r"[\d,]+", tab["linhas"][0][3])


# ── resumo ────────────────────────────────────────────────────────────────────────────────────

def test_resumo_refaz_as_tabelas_sem_recalcular(saida_do_exemplo, tmp_path):
    pasta, _ = saida_do_exemplo
    copia = tmp_path / "copia"
    shutil.copytree(pasta, copia)
    for nome in ("resultados.csv", "resultados.json", "tabela.md", "tabela.tex", "resumo.md"):
        (copia / nome).unlink()
    E.refazer_resumo(copia)
    assert _lido(copia) == _lido(pasta)


def test_resumo_com_outro_estudo_muda_metricas_e_casas(saida_do_exemplo, tmp_path):
    pasta, _ = saida_do_exemplo
    copia = tmp_path / "copia"
    shutil.copytree(pasta, copia)
    doc = json.loads((copia / "estudo.json").read_text(encoding="utf-8"))
    doc["saidas"]["metricas"] = ["economia_agua_potavel_pct", "volume_l"]
    doc["saidas"]["casas_decimais"] = {"padrao": 2}
    alt = tmp_path / "alt.json"
    alt.write_text(json.dumps(doc), encoding="utf-8")
    E.refazer_resumo(copia, alt, idioma="en")
    linhas = list(csv.DictReader((copia / "resultados.csv").read_text(encoding="utf-8").splitlines()))
    assert [l["metrica"] for l in linhas[:2]] == ["economia_agua_potavel_pct", "volume_l"]
    assert "Potable water saving (%)" in (copia / "tabela.md").read_text(encoding="utf-8")


def test_resumo_de_pasta_sem_resultados(tmp_path):
    (tmp_path / "x").mkdir()
    with pytest.raises(FileNotFoundError):
        E.refazer_resumo(tmp_path / "x")


# ── texto com marcadores ──────────────────────────────────────────────────────────────────────

def test_texto_troca_marcadores_por_numeros_reais_e_deixa_xx(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    plano, res = E.carregar_saida(pasta)
    r0 = res[0]
    modelo = ("N={{n_casos}}; primeiro={{economia_agua_potavel_pct:%s}}; min={{economia_agua_potavel_pct:@min}}; "
              "max={{ economia_agua_potavel_pct : @max | 2 }}; ausente={{economia_agua_potavel_pct:nao_existe}}; "
              "xx existente: XX; sem_resultado={{vpl:%s}}") % (IDS_DO_EXEMPLO[0], IDS_DO_EXEMPLO[0])
    texto, faltas = E.substituir_marcadores(modelo, plano, res, LINGUA)
    ok = [r["metricas"]["economia_agua_potavel_pct"] for r in res]
    esperado_min = E.formatar_numero(min(ok), 1, LINGUA)
    esperado_max = E.formatar_numero(max(ok), 2, LINGUA)
    assert f"N={len(IDS_DO_EXEMPLO)};" in texto
    assert f"primeiro={E.formatar_numero(r0['metricas']['economia_agua_potavel_pct'], 1, LINGUA)};" in texto
    assert f"min={esperado_min};" in texto and f"max={esperado_max};" in texto
    assert "ausente=«XX»" in texto and "xx existente: XX" in texto
    assert "{{" not in texto.split("sem_resultado=")[0]
    # «vpl» não está entre as métricas gravadas do exemplo (ou está, na BRL): se não há valor, vira XX e entra na lista
    assert any("nao_existe" in f for f in faltas)


def test_modelo_de_texto_do_exemplo_fecha_sem_xx(saida_do_exemplo):
    """O modelo distribuído com o exemplo usa só casos e métricas do exemplo: todos os marcadores viram número."""
    pasta, _ = saida_do_exemplo
    modelo = EXEMPLO.parent / "modelo_texto.md"
    assert modelo.is_file()
    plano, res = E.carregar_saida(pasta)
    texto, faltas = E.substituir_marcadores(modelo.read_text(encoding="utf-8"), plano, res, LINGUA)
    assert faltas == [] and "{{" not in texto and "XX" not in texto
    assert str(len(IDS_DO_EXEMPLO)) in texto


def test_texto_metrica_desconhecida_e_erro(saida_do_exemplo):
    pasta, _ = saida_do_exemplo
    plano, res = E.carregar_saida(pasta)
    with pytest.raises(ValueError, match="economia_agua_potavl"):
        E.substituir_marcadores("{{economia_agua_potavl:x}}", plano, res, "en")
    with pytest.raises(ValueError):
        E.substituir_marcadores("{{so_um_lado}}", plano, res, "en")


def test_texto_por_grupo_e_cli(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    doc = _estudo(casos=[{"id": "u", "grupo": "g1", "substituicoes": {"area_captacao_m2": 100}},
                         {"id": "v", "grupo": "g2", "substituicoes": {"area_captacao_m2": 300}}])
    arq = _gravar(pasta, "estudo.json", doc)
    E.rodar_estudo(arq, pasta / "s")
    plano, res = E.carregar_saida(pasta / "s")
    t, faltas = E.substituir_marcadores("{{agua_pluvial_m3_ano:@media(g2)}} {{agua_pluvial_m3_ano:@max(g3)}}", plano, res, "en")
    v = res[1]["metricas"]["agua_pluvial_m3_ano"]
    assert t.startswith(E.formatar_numero(v, 1, "en")) and t.endswith("«XX»") and len(faltas) == 1
    modelo = pasta / "modelo.md"
    modelo.write_text("Total: {{agua_pluvial_m3_ano:u}} e {{agua_pluvial_m3_ano:zzz}}.\n", encoding="utf-8")
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    comando = [sys.executable, "-m", "triton.cli", "estudo", "texto", str(pasta / "s"), "--modelo", str(modelo)]
    r = subprocess.run(comando, cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
    assert r.returncode == 0, r.stderr
    saida = (pasta / "s" / "texto.md").read_text(encoding="utf-8")
    assert "«XX»" in saida and "{{" not in saida
    r = subprocess.run(comando + ["--estrito"], cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=600)
    assert r.returncode == 1


# ── init ──────────────────────────────────────────────────────────────────────────────────────

def test_init_cria_esqueleto_que_a_validacao_recusa(tmp_path):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    pasta = tmp_path / "meu-estudo"
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "init", str(pasta), "--tipologia", "hospital"],
                       cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0, r.stderr
    doc = json.loads((pasta / "estudo.json").read_text(encoding="utf-8"))
    assert doc["estudo"]["tipologia"] == "hospitalar" and (pasta / "casos").is_dir() and (pasta / "modelo_texto.md").is_file()
    assert "{{n_casos}}" in (pasta / "modelo_texto.md").read_text(encoding="utf-8")
    again = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "init", str(pasta)], cwd=str(RAIZ), env=env,
                           capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert again.returncode == 2 and "--forcar" in again.stderr
    again = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "init", str(pasta), "--forcar", "--tipologia", "escolar"],
                           cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert again.returncode == 0
    val = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "validate", str(pasta / "estudo.json")], cwd=str(RAIZ),
                         env=env, capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert val.returncode == 2 and "area_captacao_m2" in val.stderr
    # o modelo de texto gerado é aceito pelo substituidor (todos os marcadores são válidos)
    plano, _, _ = E.validar_documento(_estudo())
    E.substituir_marcadores((pasta / "modelo_texto.md").read_text(encoding="utf-8"), plano, [None, None], "en")


def test_init_tipologia_invalida(tmp_path):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "init", str(tmp_path / "x"), "--tipologia", "fabrica"],
                       cwd=str(RAIZ), env=env, capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 2 and "escolar" in r.stderr


# ── lote ──────────────────────────────────────────────────────────────────────────────────────

def test_lote_roda_varios_estudos_e_compara_tipologias(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    lote = pasta / "lote"
    lote.mkdir()
    shutil.copyfile(pasta / "base.triton", lote / "base.triton")
    _gravar(lote, "estudo_a.json", _estudo("escolas", "escolar", [
        {"id": "e1", "nome": "E1", "substituicoes": {"area_captacao_m2": 120}},
        {"id": "e2", "nome": "E2", "substituicoes": {"area_captacao_m2": 180}}]))
    _gravar(lote, "estudo_b.json", _estudo("hospitais", "hospitalar", [
        {"id": "h1", "nome": "H1", "substituicoes": {"area_captacao_m2": 300}}]))
    _gravar(lote, "outro.json", {"nao": "e um estudo"})     # não casa com estudo*.json
    saida = pasta / "saida"
    execucoes, comp = E.rodar_lote(lote, saida)
    assert [len(e.calculados) for e in execucoes] == [2, 1] and comp == ["comparativo.csv", "comparativo.md", "comparativo.tex", "comparativo.json"]
    assert (saida / "escolas" / "resultados.csv").is_file() and (saida / "hospitais" / "tabela.tex").is_file()
    linhas = list(csv.DictReader((saida / "comparativo.csv").read_text(encoding="utf-8").splitlines()))
    assert {l["estudo_id"] for l in linhas} == {"escolas", "hospitais"} and {l["tipologia"] for l in linhas} == {"escolar", "hospitalar"}
    esc = next(l for l in linhas if l["estudo_id"] == "escolas" and l["metrica"] == "agua_pluvial_m3_ano")
    assert esc["n"] == "2" and float(esc["minimo"]) <= float(esc["media"]) <= float(esc["maximo"])
    j = json.loads((saida / "comparativo.json").read_text(encoding="utf-8"))
    assert [e["estudo_id"] for e in j["estudos"]] == ["escolas", "hospitais"]
    assert "\\toprule" in (saida / "comparativo.tex").read_text(encoding="utf-8")
    texto = "\n".join(p.read_text(encoding="utf-8") for p in saida.glob("comparativo.*"))
    assert str(pasta) not in texto and not re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", texto)
    # de novo, retomando: nada é recalculado
    execucoes, _ = E.rodar_lote(lote, saida, retomar=True)
    assert [len(e.calculados) for e in execucoes] == [0, 0] and [len(e.pulados) for e in execucoes] == [2, 1]


def test_lote_recusa_ids_repetidos_e_pasta_sem_estudos(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    lote = pasta / "lote"
    lote.mkdir()
    shutil.copyfile(pasta / "base.triton", lote / "base.triton")
    with pytest.raises(ValueError):
        E.rodar_lote(lote, pasta / "s")
    _gravar(lote, "estudo1.json", _estudo("igual"))
    _gravar(lote, "estudo2.json", _estudo("igual"))
    with pytest.raises(ValueError, match="igual"):
        E.rodar_lote(lote, pasta / "s")


def test_lote_recursivo(tmp_path):
    pasta = _pasta_com_base(tmp_path)
    sub = pasta / "lote" / "sub"
    sub.mkdir(parents=True)
    shutil.copyfile(pasta / "base.triton", sub / "base.triton")
    _gravar(sub, "estudo.json", _estudo("so_no_sub"))
    with pytest.raises(ValueError):
        E.descobrir_estudos(pasta / "lote")
    assert [p.name for p in E.descobrir_estudos(pasta / "lote", recursivo=True)] == ["estudo.json"]


# ── catálogo e esquema na CLI ─────────────────────────────────────────────────────────────────

def test_cli_apelidos_e_esquema():
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "apelidos"], cwd=str(RAIZ), env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0 and "area_captacao_m2" in r.stdout and "economia_agua_potavel_pct" in r.stdout
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "esquema"], cwd=str(RAIZ), env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0 and json.loads(r.stdout)["title"].startswith("triton-estudo")
