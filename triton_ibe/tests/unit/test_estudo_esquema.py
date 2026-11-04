# -*- coding: utf-8 -*-
"""``triton estudo``: o esquema do estudo.json, os apelidos, as mensagens de erro e o esqueleto de ``estudo init``.

Nada aqui simula (só os testes de apelido que conferem o efeito comparam com ``--set``); a execução dos
exemplos, a retomada, o determinismo e as tabelas estão em ``test_estudo_execucao.py``.
"""
import ast
import copy
import json
import os
import re
import shutil
import string
import subprocess
import sys
from pathlib import Path

import pytest

from triton.core import estudo as E
from triton.core.edition import get_current_edition

RAIZ = Path(__file__).resolve().parents[2]
ED = get_current_edition()
PROJETO_BASE = {"BRL": "examples/estudo_caso_1_florianopolis1.triton", "INT": "examples/london.triton",
                "IBE": "examples/portugal/funchal.triton"}[ED]


@pytest.fixture(scope="module")
def pasta_base(tmp_path_factory):
    """Uma pasta com uma cópia do projeto de exemplo da edição, para os estudos de teste citarem por caminho relativo."""
    pasta = tmp_path_factory.mktemp("estudo_esquema")
    origem = RAIZ / PROJETO_BASE
    if not origem.is_file():
        pytest.skip("projeto de exemplo ausente nesta edição")
    shutil.copyfile(origem, pasta / "base.triton")
    return pasta


def _estudo(**mudancas):
    doc = {
        "esquema": {"nome": "triton-estudo", "versao": 1},
        "estudo": {"id": "teste", "titulo": "Estudo de teste", "tipologia": "escolar"},
        "projeto_base": {"arquivo": "base.triton"},
        "casos": [{"id": "a", "nome": "Caso A", "substituicoes": {"area_captacao_m2": 200}},
                  {"id": "b", "nome": "Caso B", "grupo": "outro", "substituicoes": {"usuarios": 10}}],
        "analise": {"tipo": "technical"},
    }
    for k, v in mudancas.items():
        doc[k] = v
    return doc


def _erros(doc, base=None, arquivos=False):
    plano, erros, avisos = E.validar_documento(doc, base, verificar_arquivos=arquivos)
    return plano, erros, avisos


def _tem(erros, *trechos):
    return any(all(t in e for t in trechos) for e in erros)


# ── esquema ───────────────────────────────────────────────────────────────────────────────────

def test_estudo_minimo_valido_e_normalizado():
    plano, erros, _ = _erros(_estudo())
    assert erros == [] and plano is not None
    assert plano["estudo"]["tipologia"] == "escolar"
    assert [c["id"] for c in plano["casos"]] == ["a", "b"]
    assert plano["casos"][1]["grupo"] == "outro" and plano["casos"][0]["grupo"] == "escolar"   # grupo padrão: a tipologia
    assert plano["saidas"]["metricas"] == list(E.METRICAS_PADRAO[0])
    assert plano["saidas"]["formatos"] == ["csv", "json", "md", "tex"]


@pytest.mark.parametrize("mutacao,trecho", [
    (lambda d: d.pop("esquema"), "esquema"),
    (lambda d: d["esquema"].update(versao=2), "esquema.versao"),
    (lambda d: d["esquema"].update(nome="outro"), "esquema"),
    (lambda d: d.pop("casos"), "casos"),
    (lambda d: d.update(casos=[]), "casos"),
    (lambda d: d["estudo"].update(id="com espaço"), "estudo.id"),
    (lambda d: d["estudo"].update(tipologia="fabrica"), "estudo.tipologia"),
    (lambda d: d["analise"].update(tipo="mensal"), "analise.tipo"),
    (lambda d: d["analise"].update(volume="grande"), "analise.volume"),
    (lambda d: d["analise"].update(pesos=[1, 2]), "analise.pesos"),
    (lambda d: d["analise"].update(semente=1.5), "analise.semente"),
    (lambda d: d.update(saidas={"formatos": ["pdf"]}), "saidas.formatos"),
    (lambda d: d.update(saidas={"idioma": "fr"}), "saidas.idioma"),
    (lambda d: d.update(saidas={"casas_decimais": 12}), "saidas.casas_decimais"),
    (lambda d: d.update(saidas={"orientacao": "diagonal"}), "saidas.orientacao"),
    (lambda d: d.update(chave_estranha=1), "chave_estranha"),
    (lambda d: d["casos"][0].update(id="b"), "casos[1] (b)"),
    (lambda d: d["casos"][0].pop("id"), "casos[0].id"),
    (lambda d: d["projeto_base"].update(modelo="edicao"), "projeto_base"),
])
def test_erros_de_esquema_dizem_onde(mutacao, trecho):
    doc = _estudo()
    mutacao(doc)
    plano, erros, _ = _erros(doc)
    assert plano is None and _tem(erros, trecho), erros


def test_volume_topsis_exige_analise_completa():
    doc = _estudo(analise={"tipo": "technical", "volume": "topsis"})
    _, erros, _ = _erros(doc)
    assert _tem(erros, "topsis")
    doc = _estudo(analise={"tipo": "all", "volume": "topsis"})
    assert _erros(doc)[1] == []


def test_volume_smaa_vikor_exige_analise_completa_e_aceita_novas_metricas():
    doc = _estudo(analise={"tipo": "economic", "volume": "smaa_vikor"})
    _, erros, _ = _erros(doc)
    assert _tem(erros, "smaa_vikor")
    doc = _estudo(
        analise={"tipo": "all", "volume": "smaa_vikor"},
        saidas={"metricas": [
            "volume_l", "volume_otimo_tecnico_l", "volume_otimo_economico_l",
            "volume_otimo_ambiental_l", "volume_topsis_l", "volume_smaa_vikor_l",
            "aceitabilidade_smaa_pct", "co2_liquido_vida_kg", "payback_ambiental_anos",
        ]},
    )
    plano, erros, _ = _erros(doc)
    assert erros == [] and plano["analise"]["volume"] == "smaa_vikor"


def test_metrica_que_exige_analise_mais_completa_e_recusada():
    doc = _estudo(saidas={"metricas": ["vpl"]})
    _, erros, _ = _erros(doc)
    assert _tem(erros, "vpl"), erros
    doc = _estudo(analise={"tipo": "economic"}, saidas={"metricas": ["vpl", "economia_agua_potavel_pct"]})
    assert _erros(doc)[1] == []


def test_metrica_desconhecida_sugere_a_parecida():
    _, erros, _ = _erros(_estudo(saidas={"metricas": ["economia_agua_potavl_pct"]}))
    assert _tem(erros, "economia_agua_potavl_pct", "economia_agua_potavel_pct"), erros


def test_metricas_aceitam_o_nome_cru_do_relatorio_e_viram_canonicas():
    plano, erros, _ = _erros(_estudo(saidas={"metricas": ["potable_savings_pct", "annual_rainwater_m3", "volume_l"]}))
    assert erros == []
    assert plano["saidas"]["metricas"] == ["economia_agua_potavel_pct", "agua_pluvial_m3_ano", "volume_l"]


def test_campos_a_preencher_sao_recusados_nas_substituicoes():
    for vazio in (None, "", "XX", "«XX»"):
        doc = _estudo()
        doc["casos"][0]["substituicoes"] = {"area_captacao_m2": vazio}
        plano, erros, _ = _erros(doc)
        assert plano is None and _tem(erros, "casos[0] (a).substituicoes.area_captacao_m2"), (vazio, erros)


def test_titulo_pendente_e_so_aviso():
    doc = _estudo()
    doc["estudo"]["titulo"] = "XX"
    plano, erros, avisos = _erros(doc)
    assert erros == [] and any("estudo.titulo" in a for a in avisos)


# ── apelidos ──────────────────────────────────────────────────────────────────────────────────

def test_apelido_desconhecido_da_erro_claro_com_sugestao():
    doc = _estudo()
    doc["casos"][0]["substituicoes"] = {"area_captaçao_m2": 100}
    plano, erros, _ = _erros(doc)
    assert plano is None
    assert _tem(erros, "casos[0] (a).substituicoes.area_captaçao_m2", "area_captacao_m2")


def test_apelido_longe_de_tudo_lista_os_apelidos():
    doc = _estudo()
    doc["casos"][0]["substituicoes"] = {"xyzzy": 1}
    _, erros, _ = _erros(doc)
    assert _tem(erros, "xyzzy", "usuarios") and _tem(erros, "demanda_total_l_dia")


def test_sinonimos_e_campos_do_projeto_valem():
    for chave, valor in (("area_m2", 120), ("area", 120), ("pessoas", 5), ("runoff_coeff", 0.8), ("cost_labor", 0), ("config.area", 99)):
        doc = _estudo()
        doc["casos"][0]["substituicoes"] = {chave: valor}
        assert _erros(doc)[1] == [], chave


@pytest.mark.parametrize("chave,valor", [
    ("area_captacao_m2", 0), ("area_captacao_m2", -5), ("area_captacao_m2", "100"), ("area_captacao_m2", True),
    ("coeficiente_escoamento", 1.5), ("usuarios", 2.5), ("usuarios", -1), ("fracao_pluvial_pct", 120), ("fracao_pluvial", 40),
    ("fracao_pluvial", 1.5), ("data_inicio", "2020-01-01"), ("data_inicio", "31/02/2020"), ("regra_phi", 2),
    ("economias", 0), ("passo_volume_l", 0), ("periodo_analise_anos", 0),
])
def test_valores_fora_da_faixa_ou_do_tipo_sao_recusados(chave, valor):
    doc = _estudo()
    doc["casos"][0]["substituicoes"] = {chave: valor}
    plano, erros, _ = _erros(doc)
    assert plano is None and _tem(erros, chave), erros


def test_fracao_em_0_a_1_e_em_percentual_dao_a_mesma_fracao():
    assert E.validar_valor_de_apelido("fracao_pluvial", 0.4) == 0.4
    assert E.validar_valor_de_apelido("fracao_pluvial_pct", 40) == 40.0
    with pytest.raises(ValueError, match="fracao_pluvial_pct"):
        E.validar_valor_de_apelido("fracao_pluvial", 40)


def test_dois_nomes_para_o_mesmo_parametro_sao_conflito():
    for par in ({"area_captacao_m2": 100, "area_m2": 100}, {"fracao_pluvial": 0.4, "fracao_pluvial_pct": 40},
                {"demanda_total_l_dia": 500, "demanda_per_capita_l_dia": 100}, {"volume_reservatorio_l": 1000, "volume_maximo_l": 5000}):
        doc = _estudo()
        doc["casos"][0]["substituicoes"] = par
        plano, erros, _ = _erros(doc)
        assert plano is None and _tem(erros, "casos[0] (a).substituicoes."), (par, erros)


def test_caso_vence_o_padrao_mesmo_com_outro_apelido():
    doc = _estudo(padroes={"substituicoes": {"fracao_pluvial_pct": 30, "usuarios": 4}})
    doc["casos"][0]["substituicoes"] = {"fracao_pluvial": 0.5}
    plano, erros, _ = _erros(doc)
    assert erros == []
    ef = plano["casos"][0]["substituicoes_efetivas"]
    assert ef == {"usuarios": 4, "fracao_pluvial": 0.5}
    assert plano["casos"][1]["substituicoes_efetivas"] == {"fracao_pluvial_pct": 30.0, "usuarios": 10}


def test_caminho_pontilhado_com_secao_desconhecida_e_recusado():
    doc = _estudo()
    doc["casos"][0]["substituicoes"] = {"nao_existe.x.y": 1}
    _, erros, _ = _erros(doc)
    assert _tem(erros, "nao_existe.x.y", "inputs")


def test_chaves_com_sublinhado_sao_comentarios():
    doc = _estudo()
    doc["_comentario"] = "qualquer coisa"
    doc["casos"][0]["_nota"] = "x"
    doc["casos"][0]["substituicoes"]["_porque"] = "medido"
    assert _erros(doc)[1] == []


def test_arquivo_inexistente_e_apontado_quando_se_verificam_arquivos(pasta_base):
    doc = _estudo(projeto_base={"arquivo": "nao_existe.triton"})
    _, erros, _ = _erros(doc, pasta_base, arquivos=True)
    assert _tem(erros, "nao_existe.triton"), erros
    _, erros, _ = _erros(_estudo(), pasta_base, arquivos=True)
    assert erros == []


def test_modelo_da_edicao_exige_os_dados_do_caso():
    doc = _estudo(projeto_base={"modelo": "edicao"})
    _, erros, _ = _erros(doc)
    assert _tem(erros, "casos[0] (a)", "clima.arquivo"), erros


# ── efeito dos apelidos, conferido contra «--set» e contra o caminho pontilhado ───────────────

def _economia_pela_cli(projeto: Path, overrides):
    from triton import cli
    bundle = cli._load_bundle(str(projeto))
    cfg = bundle["config"]
    cli._apply_overrides(cfg, overrides)
    precip = cli._get_precipitation(bundle)
    rel = cli.run_analysis(cfg, precip, "technical", None, cli.PESOS_PADRAO, {}, "x", 0, 42)
    return rel["technical"]["summary"]["optimal_volume_l"], {r["lower_tank_volume_l"]: r["potable_savings_pct"]
                                                              for r in rel["technical"]["alternatives"]}


def _rodar_caso(pasta, substituicoes, extra=None):
    doc = _estudo(casos=[{"id": "c", "substituicoes": substituicoes, **(extra or {})}],
                  analise={"tipo": "technical"}, saidas={"metricas": ["volume_l", "economia_agua_potavel_pct"]})
    arq = pasta / "t.json"
    arq.write_text(json.dumps(doc), encoding="utf-8")
    plano, _ = E.carregar_plano(arq)
    return E.executar_caso(plano, plano["casos"][0])


def test_apelidos_aplicam_o_mesmo_que_set_da_cli(pasta_base):
    r = _rodar_caso(pasta_base, {"area_captacao_m2": 210.0, "fracao_pluvial_pct": 35})
    assert r["status"] == "ok", r.get("erro")
    volume, tabela = _economia_pela_cli(pasta_base / "base.triton", ["area=210", "rainwater_share=0.35"])
    assert r["volume_selecionado_l"] == volume
    assert r["metricas"]["economia_agua_potavel_pct"] == pytest.approx(tabela[volume], rel=1e-9)
    assert r["metricas"]["area_captacao_m2"] == 210.0 and r["metricas"]["fracao_pluvial_pct"] == pytest.approx(35.0)


def test_demanda_total_divide_pelos_usuarios(pasta_base):
    r = _rodar_caso(pasta_base, {"usuarios": 5, "demanda_total_l_dia": 1000})
    assert r["status"] == "ok", r.get("erro")
    assert r["metricas"]["demanda_total_l_dia"] == pytest.approx(1000.0)
    assert r["metricas"]["usuarios"] == 5
    r2 = _rodar_caso(pasta_base, {"usuarios": 5, "demanda_per_capita_l_dia": 200})
    assert r2["metricas"]["demanda_total_l_dia"] == pytest.approx(r["metricas"]["demanda_total_l_dia"])
    assert r2["metricas"]["economia_agua_potavel_pct"] == pytest.approx(r["metricas"]["economia_agua_potavel_pct"])


def test_volume_fixo_desliga_a_varredura(pasta_base):
    r = _rodar_caso(pasta_base, {"volume_reservatorio_l": 3000})
    assert r["status"] == "ok", r.get("erro")
    assert r["volume_selecionado_l"] == 3000.0 and r["metricas"]["volume_l"] == 3000.0


def test_caminho_pontilhado_do_triton_equivale_ao_apelido(pasta_base):
    por_apelido = _rodar_caso(pasta_base, {"area_captacao_m2": 175.0})
    por_caminho = _rodar_caso(pasta_base, {"inputs.building_and_demand.catchment_area_m2": 175.0})
    assert por_apelido["status"] == por_caminho["status"] == "ok", (por_apelido.get("erro"), por_caminho.get("erro"))
    assert por_caminho["metricas"] == por_apelido["metricas"]


def test_caminho_pontilhado_inexistente_da_erro_do_caso(pasta_base):
    r = _rodar_caso(pasta_base, {"inputs.building_and_demand.area_do_telhado": 175.0})
    assert r["status"] == "erro" and "area_do_telhado" in r["erro"] and "catchment_area_m2" in r["erro"]
    r = _rodar_caso(pasta_base, {"inputs.building_and_demand.catchment_area_m2": "grande"})
    assert r["status"] == "erro" and "catchment_area_m2" in r["erro"]


def test_erro_do_caso_nao_vaza_caminho_absoluto(pasta_base):
    doc = _estudo(casos=[{"id": "c", "projeto": "nao_existe.triton"}], projeto_base={"arquivo": "base.triton"})
    arq = pasta_base / "t2.json"
    arq.write_text(json.dumps(doc), encoding="utf-8")
    plano, erros, _ = E.validar_documento(doc, pasta_base, verificar_arquivos=False)
    plano["base_dir"], plano["sha256"], plano["caminho"] = pasta_base, "0", arq
    r = E.executar_caso(plano, plano["casos"][0])
    assert r["status"] == "erro"
    assert str(pasta_base) not in r["erro"] and not re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", r["erro"])


def test_substituicao_de_demanda_com_modulacao_gera_alerta(pasta_base):
    from triton import cli
    doc = _estudo(casos=[{"id": "c", "substituicoes": {"usuarios": 3}}])
    plano, _, _ = E.validar_documento(doc, pasta_base, verificar_arquivos=False)
    plano["base_dir"] = pasta_base
    montado = E.montar_caso(plano, plano["casos"][0])
    assert isinstance(montado["alertas"], list)       # sem modulação no exemplo: sem alerta
    assert not montado["alertas"]


# ── esqueleto, tipologias e esquema JSON ──────────────────────────────────────────────────────

@pytest.mark.parametrize("tipologia", list(E.TIPOLOGIAS))
def test_esqueleto_de_cada_tipologia_nao_traz_valor_inventado(tipologia):
    esq = E.esqueleto(Path("meu-estudo"), tipologia)
    assert esq["estudo"]["tipologia"] == tipologia and esq["estudo"]["id"] == "meu-estudo"
    for caso in esq["casos"]:
        assert caso["grupo"] == tipologia
        assert all(v is None for k, v in caso["substituicoes"].items()), "o esqueleto não pode trazer números"
        assert caso["clima"]["arquivo"] == "XX" and caso["nome"] == "XX"
    assert esq["projeto_base"]["arquivo"] == "XX" and esq["estudo"]["titulo"] == "XX"
    # a validação recusa o esqueleto, dizendo o que preencher
    _, erros, _ = E.validar_documento(json.loads(json.dumps(esq)))
    assert erros and _tem(erros, "area_captacao_m2") and _tem(erros, "projeto_base.arquivo")


def test_rotulos_das_tipologias_existem_nas_quatro_linguas():
    for t, d in E.TIPOLOGIAS.items():
        assert set(d["rotulo"]) == {"pt", "en", "es", "zh"}, t
    for lingua in ("pt-BR", "pt-PT", "en", "es", "zh"):
        assert all(E.rotulo_da_tipologia(t, lingua) for t in list(E.TIPOLOGIAS) + [E.TIPOLOGIA_OUTRA])


def test_tipologia_aceita_sinonimos():
    assert E.tipologia_canonica("Escola") == "escolar"
    assert E.tipologia_canonica("hospital") == "hospitalar"
    assert E.tipologia_canonica("airport") == "aeroportuario"
    assert E.tipologia_canonica("residencial_unifamiliar") == "residencial-unifamiliar"
    assert E.tipologia_canonica("fabrica") is None


def test_metricas_tem_rotulo_nas_quatro_linguas_e_unidade():
    for mid, m in E.METRICAS.items():
        assert set(m["rotulos"]) == {"pt", "en", "es", "zh"}, mid
        assert m["unidade"], mid
    assert len({s for s in E._SINONIMO_DE_METRICA}) >= len(E.METRICAS)


def test_esquema_json_valida_o_exemplo_e_o_esqueleto():
    jsonschema = pytest.importorskip("jsonschema")
    esquema = E.esquema_json()
    jsonschema.Draft202012Validator.check_schema(esquema)
    jsonschema.validate(E.esqueleto(Path("x"), "escolar"), esquema)
    jsonschema.validate(_estudo(), esquema)
    com_erro = _estudo()
    com_erro["analise"]["tipo"] = "mensal"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(com_erro, esquema)


# ── textos e traduções ────────────────────────────────────────────────────────────────────────

def _mensagens_do_estudo():
    achadas = set()
    for arq in ("triton/core/reporting/estudo.py", "triton/cli_estudo.py", "triton/core/reporting/estudo_consolidar.py", "triton/cli_progresso.py"):
        arvore = ast.parse((RAIZ / arq).read_text(encoding="utf-8"))
        for n in ast.walk(arvore):
            if not isinstance(n, ast.Call):
                continue
            if getattr(n.func, "id", None) in ("_m", "_t") and n.args and isinstance(n.args[0], ast.Constant):
                achadas.add(n.args[0].value)
            if isinstance(n.func, ast.Attribute) and n.func.attr in ("add_argument", "add_parser"):
                for k in n.keywords:
                    if k.arg in ("help", "description") and isinstance(k.value, ast.Constant):
                        achadas.add(k.value.value)
    return achadas


def _campos(texto):
    return sorted(f[1] for f in string.Formatter().parse(texto) if f[1] is not None)


def test_toda_mensagem_do_estudo_tem_traducao_em_ingles_com_os_mesmos_campos():
    from triton.cli_textos import _EN
    msgs = _mensagens_do_estudo()
    assert len(msgs) > 100
    faltam = sorted(m for m in msgs if m not in _EN)
    assert not faltam, f"sem tradução em inglês: {faltam[:5]}"
    for m in msgs:
        assert _campos(m) == _campos(_EN[m]), m


def test_mensagens_em_portugues_de_portugal_mantem_os_campos():
    from triton.ui.portugues_de_portugal import para_portugal
    for m in _mensagens_do_estudo():
        assert _campos(para_portugal(m)) == _campos(m), m


def test_ajuda_do_estudo_na_lingua_da_edicao():
    env = {k: v for k, v in os.environ.items()}
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "--help"], cwd=str(RAIZ), env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0, r.stderr
    for acao in ("init", "validate", "run", "resumo", "lote", "texto"):
        assert acao in r.stdout
    if ED == "INT":
        assert "Batch studies" in r.stdout and "gathers" in r.stdout
    elif ED == "IBE":
        assert "Executa" in r.stdout
        assert "arquivo" not in r.stdout.lower()
    else:
        assert "Estudos em lote" in r.stdout


def test_codigo_de_saida_2_para_estudo_invalido(tmp_path):
    arq = tmp_path / "estudo.json"
    arq.write_text(json.dumps(_estudo(projeto_base={"arquivo": "nao_existe.triton"})), encoding="utf-8")
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "validate", str(arq)], cwd=str(RAIZ), env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 2 and "nao_existe.triton" in r.stderr
    r = subprocess.run([sys.executable, "-m", "triton.cli", "estudo", "validate", str(tmp_path / "ausente.json")], cwd=str(RAIZ),
                       env=env, capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 2


def test_limpar_caminhos_tira_o_caminho_da_maquina(tmp_path):
    texto = f"falhou em {tmp_path / 'a' / 'b.triton'} e C:\\Users\\alguem\\x\\y.csv"
    limpo = E.limpar_caminhos(texto, tmp_path)
    assert str(tmp_path) not in limpo and "Users" not in limpo and "y.csv" in limpo
