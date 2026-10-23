# -*- coding: utf-8 -*-
"""Procedência e confiança dos tarifários portugueses, por concelho e serviço (Edição Ibérica).

Só vale na IBE (``tests/so_da_ibe.txt``; fora dela o arquivo é saltado). O esquema é o do consenso do
debate IBE: três estados (verde, amarelo, cinza) por concelho e por serviço (água, saneamento, resíduos).
Garante, sobre ``tarifas_portugal/`` (``entidades.json``, ``CONFIANCA_POR_CONCELHO.csv``,
``fontes/FONTES.tsv``) e o campo ``procedencia`` de ``portugal_tarifarios.json``, que:

* nenhum concelho fica sem estado (278 do continente, mais Funchal e Ponta Delgada);
* NÃO EXISTE VERDE SEM ``verificado_por`` («fatura» ou «humano»; um modelo de IA nunca conta), nem sem
  documento com URL e SHA-256, reconfirmação em menos de 12 meses, transcrição conferida e nenhuma
  pendência com efeito acima de 1 %; o verde do concelho exige os três serviços verdes;
* FONTES.tsv (registo mínimo de 11 campos) é coerente com entidades.json e com a procedência dos
  tarifários transcritos, e o SHA-256 dos ficheiros presentes bate;
* o CSV é o que ``procedencia_pt.py`` calcula (quando a ferramenta de desenvolvimento existe).

Os testes lêem arquivos de dados: não dependem de Qt nem da rede.
"""

import csv
import hashlib
import importlib.util
import json
import os
import sqlite3

import pytest

from triton.core.edition import usa_dados_de_portugal

pytestmark = pytest.mark.skipif(not usa_dados_de_portugal(), reason="só vale na Edição Ibérica")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARIFAS = os.path.join(RAIZ, "tarifas_portugal")
ENTIDADES = os.path.join(TARIFAS, "entidades.json")
CSV = os.path.join(TARIFAS, "CONFIANCA_POR_CONCELHO.csv")
FONTES = os.path.join(TARIFAS, "fontes", "FONTES.tsv")
TARIFARIOS = os.path.join(RAIZ, "triton", "data", "portugal_tarifarios.json")
BASE_EOBS = os.path.join(RAIZ, "data", "portugal_eobs.db")

ESTADOS = ("verde", "amarelo", "cinza")
INDEPENDENTES = ("fatura", "humano")
SERVICOS = ("agua", "saneamento", "residuos")
MESES = 12
LIMITE_PCT = 1.0


def _ler_json(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def entidades():
    if not os.path.isfile(ENTIDADES):
        pytest.skip("tarifas_portugal/entidades.json ausente nesta instalação")
    return _ler_json(ENTIDADES)


@pytest.fixture(scope="module")
def linhas():
    if not os.path.isfile(CSV):
        pytest.skip("tarifas_portugal/CONFIANCA_POR_CONCELHO.csv ausente nesta instalação")
    with open(CSV, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


@pytest.fixture(scope="module")
def fontes():
    """FONTES.tsv: caminho → registo mínimo (11 colunas, sem cabeçalho)."""
    if not os.path.isfile(FONTES):
        pytest.skip("fontes/FONTES.tsv ausente nesta instalação")
    cols = ["caminho", "origem", "sha256", "data_coleta", "entidade", "concelhos", "tipo", "vigencia",
            "confirmado_em", "verificado_por", "redistribuivel"]
    out = {}
    with open(FONTES, encoding="utf-8") as f:
        for linha in f:
            c = linha.rstrip("\r\n").split("\t")
            if not c[0]:
                continue
            assert len(c) == len(cols), f"{c[0]}: {len(c)} colunas em FONTES.tsv (esperadas {len(cols)})"
            out[c[0]] = dict(zip(cols, c))
    return out


@pytest.fixture(scope="module")
def transcritos():
    dados = _ler_json(TARIFARIOS)
    return {k: v for k, v in dados.items() if not k.startswith("_")}


def _concelhos_esperados():
    con = sqlite3.connect(BASE_EOBS)
    try:
        nomes = {r[0] for r in con.execute("select concelho from series")}
    finally:
        con.close()
    return nomes | {"Funchal", "Ponta Delgada"}


def _meses(iso, hoje):
    return (hoje.year - int(iso[0:4])) * 12 + hoje.month - int(iso[5:7])


# --- 1. nenhum concelho sem estado -------------------------------------------------------------

def test_todos_os_concelhos_tem_estado_por_servico(linhas):
    esperados = _concelhos_esperados()
    assert len(esperados) == 280
    nomes = [l["concelho"] for l in linhas]
    assert len(nomes) == len(set(nomes)), "concelho repetido no CSV"
    assert set(nomes) == esperados, (sorted(esperados - set(nomes)), sorted(set(nomes) - esperados))
    for l in linhas:
        por = [l["estado_agua"], l["estado_saneamento"], l["estado_residuos"]]
        assert l["estado"] in ESTADOS and all(e in ESTADOS for e in por), l["concelho"]
        esperado = "verde" if all(e == "verde" for e in por) else ("cinza" if all(e == "cinza" for e in por) else "amarelo")
        assert l["estado"] == esperado, f"{l['concelho']}: estado do concelho incoerente com o dos serviços"
        assert l["entidade"].strip() and l["o_que_falta"].strip(), l["concelho"]


def test_o_cadastro_de_entidades_cobre_todos_os_concelhos(entidades):
    assert set(entidades["concelhos"]) == _concelhos_esperados()
    servidos = set()
    for e in entidades["entidades"].values():
        for s in e["servicos"].values():
            servidos.update(s["concelhos"])
    assert set(entidades["concelhos"]) <= servidos, "concelho sem entidade em nenhum serviço"


# --- 2. nenhum verde sem verificado_por (e sem o resto dos requisitos) -------------------------

def test_a_regra_do_verde_exige_tudo_e_verificado_por():
    from datetime import date
    from triton.core.tarifarios_portugal import avaliar_servico
    hoje = date(2026, 10, 23)
    doc = {"url": "https://x/doc.pdf", "sha256": "ab" * 32, "confirmado_em": "2026-10-07", "verificado_por": "fatura"}
    ok = dict(documentos=[doc], transcrito=True, conferido=True, pendencias=[], hoje=hoje)
    assert avaliar_servico(**ok)[0] == "verde"
    assert avaliar_servico(**{**ok, "documentos": [{**doc, "verificado_por": "humano"}]})[0] == "verde"
    for sem in ({"verificado_por": ""}, {"verificado_por": "modelo"}, {"verificado_por": "ia"},
                {"verificado_por": "claude"}, {"url": ""}, {"sha256": ""}, {"confirmado_em": ""},
                {"confirmado_em": "2025-10-01"}):
        assert avaliar_servico(**{**ok, "documentos": [{**doc, **sem}]})[0] == "amarelo", sem
    assert avaliar_servico(**{**ok, "transcrito": False})[0] == "amarelo"
    assert avaliar_servico(**{**ok, "conferido": False})[0] == "amarelo"
    assert avaliar_servico(**{**ok, "pendencias": [{"efeito_pct": 1.5, "texto": "x"}]})[0] == "amarelo"
    assert avaliar_servico(**{**ok, "pendencias": [{"efeito_pct": None, "texto": "x"}]})[0] == "amarelo"
    assert avaliar_servico(**{**ok, "pendencias": [{"efeito_pct": 0.9, "texto": "x"}]})[0] == "verde"
    assert avaliar_servico(**{**ok, "documentos": []})[0] == "cinza"
    # basta um documento sem verificação para o serviço não ser verde
    assert avaliar_servico(**{**ok, "documentos": [doc, {**doc, "verificado_por": ""}]})[0] == "amarelo"


def test_nenhum_verde_sem_verificado_por_documento_conferencia_e_sem_pendencia_grande(linhas, entidades, fontes, transcritos):
    from datetime import date
    for l in linhas:
        verdes = [s for s in SERVICOS if l["estado_" + s] == "verde"]
        if l["estado"] == "verde":
            assert len(verdes) == 3, l["concelho"]
        if not verdes:
            continue
        quando = date.fromisoformat(l["gerado_em"])
        nome = l["concelho"]
        assert nome in transcritos, f"{nome}: verde sem transcrição"
        proc = transcritos[nome]["procedencia"]
        assert proc.get("conferido") is True and transcritos[nome].get("conferencia"), f"{nome}: verde sem conferência"
        for s in verdes:
            docs = [d for d in entidades["documentos"].values()
                    if d["tipo"] == "oficial" and s in d["servicos"]
                    and (nome in d.get("concelhos", []) or d.get("entidade_toda"))]
            assert docs, f"{nome}/{s}: verde sem documento"
            assert proc["servicos"][s] == "transcrito", f"{nome}/{s}: verde sem transcrição do serviço"
            for d in docs:
                for caminho in d["ficheiros"]:
                    r = fontes[caminho]
                    assert r["verificado_por"] in INDEPENDENTES, f"{nome}/{s}: verde sem verificado_por em {caminho}"
                    assert r["sha256"] and r["origem"].startswith("http"), f"{nome}/{s}: {caminho} sem URL ou SHA-256"
                    assert r["confirmado_em"] and _meses(r["confirmado_em"], quando) < MESES, \
                        f"{nome}/{s}: {caminho} sem reconfirmação recente"
            for p in proc.get("pendencias", []):
                if s in p["servicos"]:
                    assert p["efeito_pct"] is not None and p["efeito_pct"] <= LIMITE_PCT, \
                        f"{nome}/{s}: pendência acima de 1 %"


def test_sem_verificacao_independente_registada_nao_ha_verde(linhas, fontes):
    """Enquanto FONTES.tsv não registar `fatura` ou `humano` em nenhum documento, o CSV não pode ter verde."""
    if any(r["verificado_por"] in INDEPENDENTES for r in fontes.values()):
        pytest.skip("há verificações independentes registadas: vale o teste anterior")
    verdes = [l["concelho"] for l in linhas
              if "verde" in (l["estado"], l["estado_agua"], l["estado_saneamento"], l["estado_residuos"])]
    assert not verdes, verdes


def test_lisboa_nasce_amarela_pelas_pendencias_e_pela_falta_de_verificacao(linhas):
    from triton.core import tarifarios_portugal as tp
    lisboa = next(l for l in linhas if l["concelho"] == "Lisboa")
    assert lisboa["estado"] == "amarelo"
    por = tp.estados("Lisboa")
    assert {s: e for s, (e, _) in por.items()} == {"agua": "amarelo", "saneamento": "amarelo", "residuos": "amarelo"}
    assert any("2,59" in m for m in por["saneamento"][1]), por["saneamento"]


def test_estado_cinza_e_sem_documento_e_amarelo_tem_documento(linhas):
    for l in linhas:
        if l["estado"] == "cinza":
            assert not l["url_documento"], l["concelho"]
        if l["estado"] == "amarelo":
            # documentos entregues pelo autor podem não ter URL de origem (Alto Minho, Bragança): fica a ficha da ERSAR
            assert l["url_documento"] or l["url_ficha_ersar"], f"{l['concelho']}: amarelo sem URL de documento nem de ficha"


# --- 3. consistência com FONTES.tsv -------------------------------------------------------------

def test_documentos_de_entidades_json_batem_com_fontes_tsv(entidades, fontes):
    todos = []
    for did, d in entidades["documentos"].items():
        assert d["tipo"] in ("oficial", "secundario", "indice", "fora_do_tema"), did
        assert d["ficheiros"], did
        for caminho in d["ficheiros"]:
            assert caminho in fontes, f"{did}: {caminho} não está em FONTES.tsv"
            assert fontes[caminho]["tipo"] == d["tipo"], f"{caminho}: tipo diferente de entidades.json"
            if d["tipo"] == "oficial":
                assert fontes[caminho]["entidade"] == d["entidade"], caminho
            todos.append(caminho)
        if d["tipo"] == "oficial":
            assert d["entidade"] in entidades["entidades"], f"{did}: entidade {d['entidade']} desconhecida"
            assert d["servicos"] and set(d["servicos"]) <= set(SERVICOS), did
            assert d["vigencia_inicio"] and d["vigencia_precisao"] in ("dia", "mes", "ano", "publicacao"), did
            assert d.get("concelhos") or d.get("entidade_toda"), f"{did}: sem concelho nem entidade inteira"
            for c in d.get("concelhos", []):
                assert c in entidades["concelhos"], f"{did}: concelho {c} desconhecido"
    assert len(todos) == len(set(todos)), "o mesmo ficheiro em dois documentos"
    assert set(todos) == set(fontes), (sorted(set(fontes) - set(todos)), sorted(set(todos) - set(fontes)))


def test_o_registo_minimo_de_cada_ficheiro_esta_completo(fontes):
    from datetime import date
    for caminho, r in fontes.items():
        assert len(r["sha256"]) == 64 and set(r["sha256"]) <= set("0123456789abcdef"), caminho
        assert r["data_coleta"] and r["tipo"], caminho
        date.fromisoformat(r["data_coleta"])
        date.fromisoformat(r["confirmado_em"])
        assert r["confirmado_em"] >= r["data_coleta"], f"{caminho}: confirmado_em anterior à coleta"
        assert r["verificado_por"] in ("",) + INDEPENDENTES, f"{caminho}: verificado_por «{r['verificado_por']}» não vale"
        assert r["redistribuivel"] in ("0", "1"), caminho
        if caminho.lower().endswith((".pdf", ".jpg", ".html")):
            assert r["redistribuivel"] == "0", f"{caminho}: documento de terceiros não vai no instalador"
        if r["tipo"] == "oficial":
            assert r["concelhos"] and r["vigencia"], caminho


def test_sha256_dos_ficheiros_presentes_bate_com_fontes_tsv(fontes):
    presentes = 0
    for caminho, r in fontes.items():
        ficheiro = os.path.join(TARIFAS, "fontes", *caminho.split("/"))
        if not os.path.isfile(ficheiro):
            continue
        h = hashlib.sha256()
        with open(ficheiro, "rb") as f:
            for bloco in iter(lambda: f.read(1 << 20), b""):
                h.update(bloco)
        assert h.hexdigest() == r["sha256"], f"{caminho}: o SHA-256 do ficheiro difere do registado"
        presentes += 1
    if not presentes:
        pytest.skip("nenhum documento arquivado nesta instalação (fontes/ fica fora do Git)")


def test_o_indice_da_ersar_esta_registado(entidades, fontes):
    ind = entidades["_verificacao"]["indice_ersar"]
    assert ind["url"].startswith("https://www.ersar.pt/")
    assert fontes["_indice_ersar/tarifa-concelho.json"]["sha256"] == ind["sha256"]
    assert ind["registos"] > 2000


def test_servicos_de_cada_entidade_so_citam_concelhos_e_documentos_que_existem(entidades):
    for nome, e in entidades["entidades"].items():
        for s, v in e["servicos"].items():
            assert s in SERVICOS, (nome, s)
            for c in v["concelhos"]:
                assert c in entidades["concelhos"], (nome, c)
            for did in v["documentos"]:
                assert did in entidades["documentos"], (nome, did)


def test_a_procedencia_dos_transcritos_bate_com_fontes_tsv(transcritos, fontes, entidades):
    oficiais = {c for d in entidades["documentos"].values() if d["tipo"] == "oficial" for c in d["ficheiros"]}
    assert set(transcritos) >= {"Lisboa", "Porto", "Funchal"}
    for nome, d in transcritos.items():
        proc = d["procedencia"]
        assert set(proc["servicos"]) == set(SERVICOS), nome
        assert set(proc["servicos"].values()) <= {"transcrito", "nao_transcrito"}, nome
        for doc in proc["documentos"]:
            r = fontes[doc["ficheiro"]]
            assert doc["ficheiro"] in oficiais, (nome, doc["ficheiro"])
            na_procedencia = (doc["url"], doc["sha256"], doc["confirmado_em"], doc["verificado_por"])
            em_fontes = (r["origem"].split()[0], r["sha256"], r["confirmado_em"], r["verificado_por"])
            assert na_procedencia == em_fontes, f"{nome}: a procedência de {doc['ficheiro']} difere de FONTES.tsv"
        cobertos = {s for doc in proc["documentos"] for s in doc["servicos"]}
        transcr = {s for s, v in proc["servicos"].items() if v == "transcrito"}
        assert transcr <= cobertos, f"{nome}: serviço transcrito sem documento"
        assert proc["vigencia_inicio"] and proc["recolhido_em"], nome


def test_pendencias_tem_servicos_e_efeito_estimado(transcritos):
    for nome, d in transcritos.items():
        for p in d["procedencia"].get("pendencias", []):
            assert p["servicos"] and set(p["servicos"]) <= set(SERVICOS), (nome, p)
            assert p["efeito_pct"] is None or p["efeito_pct"] >= 0, (nome, p)
            assert p["texto"].strip(), (nome, p)
            assert "gravidade" not in p, "a regra é o efeito (1 %), não uma gravidade escrita à mão"


# --- 4. o programa mostra a procedência ---------------------------------------------------------

def test_o_programa_le_a_procedencia_dos_transcritos():
    from triton.core import tarifarios_portugal as tp
    for concelho in ("Lisboa", "Porto", "Funchal"):
        texto = tp.procedencia(concelho)
        assert "amarelo" in texto.split(":")[0], texto
        assert "vigência 01/01/2026" in texto and "conferido com as contas impressas" in texto, texto
        assert "sem verificação independente" in texto, texto
    assert "pendência(s) com efeito acima de 1 %" in tp.procedencia("Funchal")
    assert "resíduos urbanos (EMAP" in tp.procedencia("Porto")
    assert tp.procedencia("Coimbra") == "" and tp.procedencia("Atlantida") == ""
    assert tp.estados("Coimbra") == {}


# --- 5. o CSV é o que a ferramenta calcula ------------------------------------------------------

def test_o_csv_e_o_que_procedencia_pt_calcula(linhas):
    caminho = os.path.join(TARIFAS, "procedencia_pt.py")
    if not os.path.isfile(caminho):
        pytest.skip("procedencia_pt.py é ferramenta de desenvolvimento e fica fora do Git")
    espec = importlib.util.spec_from_file_location("procedencia_pt", caminho)
    modulo = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(modulo)
    from datetime import date
    quando = date.fromisoformat(linhas[0]["gerado_em"])
    calculado = {l["concelho"]: l for l in modulo.avaliar(quando)}
    assert set(calculado) == {l["concelho"] for l in linhas}
    for l in linhas:
        c = calculado[l["concelho"]]
        assert (c["estado"], c["estados"]["agua"], c["estados"]["saneamento"], c["estados"]["residuos"]) == \
               (l["estado"], l["estado_agua"], l["estado_saneamento"], l["estado_residuos"]), l["concelho"]
        assert c["entidade"] == l["entidade"], l["concelho"]
