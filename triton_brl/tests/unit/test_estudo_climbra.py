# -*- coding: utf-8 -*-
"""``triton estudo``: referência direta ao CLIMBra (``clima.climbra``), ``tarifa``, ``expansao`` e os seis estudos de congresso de Santa Catarina.

* BRL: o esquema estendido valida, expande e roda; os ``estudo.json`` de ``estudos/santa-catarina/`` são válidos
  e uma amostra de um caso por estudo roda de ponta a ponta (só onde a pasta existir: ``estudos/`` é ignorada pelo Git).
* INT e IBE: as três chaves novas são recusadas com a mensagem de que só existem na Edição Brasil, e nada do que já
  existia muda (``clima.arquivo`` continua valendo).
"""
import copy
import json
from pathlib import Path

import pytest

from triton.core import estudo as E
from triton.core.edition import get_current_edition

RAIZ = Path(__file__).resolve().parents[2]
ED = get_current_edition()
BRL = ED == "BRL"
PASTA_SC = RAIZ / "estudos" / "santa-catarina"
MODELOS = 19
RECORTES = 7

REF = {"municipio": "Florianópolis", "uf": "SC", "ibge": "4205407", "modelo": "INM-CM4", "cenario": "HIST",
       "inicio": "01/01/1981", "fim": "31/12/2010"}
SUBS = {"area_captacao_m2": 200, "usuarios": 10, "demanda_per_capita_l_dia": 100, "fracao_pluvial_pct": 40,
        "volume_maximo_l": 5000, "passo_volume_l": 500}


def _doc(**mudancas):
    doc = {"esquema": {"nome": "triton-estudo", "versao": 1},
           "estudo": {"id": "teste-climbra", "titulo": "Teste", "tipologia": "escolar"},
           "projeto_base": {"modelo": "edicao"},
           "padroes": {"substituicoes": dict(SUBS)},
           "casos": [{"id": "a", "clima": {"climbra": dict(REF)}}],
           "analise": {"tipo": "technical"}}
    doc.update(mudancas)
    return doc


def _validar(doc, arquivos=False):
    return E.validar_documento(doc, RAIZ, verificar_arquivos=arquivos)


def _tem(erros, *trechos):
    return any(all(t in e for t in trechos) for e in erros)


# ══ Fora da Edição Brasil: recusado, sem mudar o resto ═════════════════════════════════════════

@pytest.mark.skipif(BRL, reason="vale para INT e IBE")
class TestForaDaBrasil:
    def test_climbra_e_recusado(self):
        _, erros, _ = _validar(_doc())
        assert _tem(erros, "casos[0] (a).clima.climbra", "Brasil") or _tem(erros, "climbra", "Brazil") or _tem(erros, "climbra")

    def test_tarifa_e_recusada(self):
        doc = _doc(padroes={"substituicoes": dict(SUBS), "tarifa": {"categoria": "comercial"}},
                   casos=[{"id": "a", "clima": {"arquivo": "x.csv"}}])
        _, erros, _ = _validar(doc)
        assert _tem(erros, "padroes.tarifa")

    def test_expansao_e_recusada(self):
        doc = _doc(casos=[], expansao={"municipios": [{"municipio": "Florianópolis"}], "modelos": ["INM-CM4"],
                                       "recortes": [{"id": "h", "cenario": "HIST", "inicio": "01/01/1981", "fim": "31/12/2010"}]})
        plano, erros, _ = _validar(doc)
        assert plano is None and _tem(erros, "expansao")

    def test_arquivo_continua_valendo(self):
        doc = _doc(casos=[{"id": "a", "clima": {"arquivo": "serie.csv"}}])
        plano, erros, _ = _validar(doc)
        assert erros == [] and plano["casos"][0]["clima_efetivo"] == {"arquivo": "serie.csv"}

    def test_campos_novos_nao_aparecem_no_plano_padrao(self):
        doc = _doc(casos=[{"id": "a", "clima": {"arquivo": "serie.csv"}}])
        plano, _, _ = _validar(doc)
        assert plano["padroes"]["tarifa"] == {} and plano["casos"][0]["tarifa_efetiva"] == {}
        assert plano["saidas"]["gravar_analise"] is True


# ══ Edição Brasil: o esquema estendido ═════════════════════════════════════════════════════════

@pytest.mark.skipif(not BRL, reason="CLIMBra e tarifas municipais só na Edição Brasil")
class TestEsquemaEstendido:
    def test_climbra_valido(self):
        plano, erros, _ = _validar(_doc(), arquivos=True)
        assert erros == []
        assert plano["casos"][0]["clima_efetivo"]["climbra"]["modelo"] == "INM-CM4"

    def test_arquivo_e_climbra_juntos_sao_erro(self):
        doc = _doc(casos=[{"id": "a", "clima": {"arquivo": "x.csv", "climbra": dict(REF)}}])
        _, erros, _ = _validar(doc)
        assert _tem(erros, "arquivo", "climbra")

    @pytest.mark.parametrize("campo,valor,trecho", [("modelo", "NAO-EXISTE", "modelo"), ("cenario", "SSP999", "cenario"),
                                                    ("ibge", "42", "ibge"), ("inicio", "1981", "inicio"), ("municipio", "XX", "municipio")])
    def test_valores_invalidos(self, campo, valor, trecho):
        ref = dict(REF)
        ref[campo] = valor
        _, erros, _ = _validar(_doc(casos=[{"id": "a", "clima": {"climbra": ref}}]))
        assert _tem(erros, trecho)

    def test_chave_desconhecida_tem_sugestao(self):
        ref = dict(REF)
        ref["modello"] = "INM-CM4"
        _, erros, _ = _validar(_doc(casos=[{"id": "a", "clima": {"climbra": ref}}]))
        assert _tem(erros, "modello")

    def test_municipio_ausente_da_climbra(self):
        ref = dict(REF, municipio="Município Inexistente")
        _, erros, _ = _validar(_doc(casos=[{"id": "a", "clima": {"climbra": ref}}]), arquivos=True)
        assert _tem(erros, "não está na base CLIMBra")

    def test_homonimo_de_outra_uf_e_recusado(self):
        """Ipirá existe na CLIMBra (BA); com uf = SC o catálogo de tarifas não o conhece."""
        ref = dict(REF, municipio="Ipirá", uf="SC", ibge="4207601")
        _, erros, _ = _validar(_doc(casos=[{"id": "a", "clima": {"climbra": ref}}]), arquivos=True)
        assert _tem(erros, "UF SC")

    def test_padrao_de_modelo_e_cenario_completa_o_caso(self):
        doc = _doc(padroes={"substituicoes": dict(SUBS), "clima": {"climbra": {"modelo": "KACE", "cenario": "HIST"}}},
                   casos=[{"id": "a", "clima": {"climbra": {"municipio": "Joinville", "uf": "SC"}}}])
        plano, erros, _ = _validar(doc)
        assert erros == []
        assert plano["casos"][0]["clima_efetivo"]["climbra"] == {"modelo": "KACE", "cenario": "HIST", "municipio": "Joinville", "uf": "SC"}

    def test_arquivo_do_caso_descarta_climbra_do_padrao(self):
        doc = _doc(padroes={"substituicoes": dict(SUBS), "clima": {"climbra": dict(REF)}},
                   casos=[{"id": "a", "clima": {"arquivo": "serie.csv"}}])
        plano, _, _ = _validar(doc)
        assert plano["casos"][0]["clima_efetivo"] == {"arquivo": "serie.csv"}

    def test_modelo_da_edicao_aceita_climbra_no_lugar_do_arquivo(self):
        _, erros, _ = _validar(_doc())
        assert not _tem(erros, "clima.arquivo")

    def test_tarifa_categoria_invalida(self):
        doc = _doc(padroes={"substituicoes": dict(SUBS), "tarifa": {"categoria": "espacial"}})
        _, erros, _ = _validar(doc)
        assert _tem(erros, "padroes.tarifa.categoria")

    def test_tarifa_nao_aceita_preco(self):
        doc = _doc(padroes={"substituicoes": dict(SUBS), "tarifa": {"categoria": "comercial", "preco_m3": 9.9}})
        _, erros, _ = _validar(doc)
        assert _tem(erros, "preco_m3")

    def test_gravar_analise_precisa_ser_booleano(self):
        doc = _doc(saidas={"gravar_analise": "nao"})
        _, erros, _ = _validar(doc)
        assert _tem(erros, "gravar_analise")


@pytest.mark.skipif(not BRL, reason="expansão só na Edição Brasil")
class TestExpansao:
    EXP = {"uf": "SC", "modelos": ["INM-CM4", "KACE"],
           "municipios": [{"municipio": "Florianópolis", "ibge": "4205407"}, {"municipio": "Joinville", "ibge": "4209102"}],
           "recortes": [{"id": "hist", "cenario": "HIST", "inicio": "01/01/1981", "fim": "31/12/2010"},
                        {"id": "prox", "rotulo": "Próximo", "cenario": "SSP245", "inicio": "01/01/2021", "fim": "31/12/2050"}]}

    def _plano(self, **exp):
        e = {**self.EXP, **exp}
        plano, erros, _ = _validar(_doc(casos=[], expansao=e), arquivos=True)
        assert erros == [], erros
        return plano

    def test_um_caso_por_municipio_modelo_recorte_em_ordem_estavel(self):
        plano = self._plano()
        ids = [c["id"] for c in plano["casos"]]
        assert len(ids) == 2 * 2 * 2 == len(set(ids))
        assert ids[0] == "florianopolis__INM-CM4__hist" and ids[-1] == "joinville__KACE__prox"
        assert ids == [c["id"] for c in self._plano()["casos"]]

    def test_dimensoes_e_clima_de_cada_caso(self):
        c = self._plano()["casos"][1]
        assert c["dimensoes"] == {"municipio": "Florianópolis", "ibge": "4205407", "modelo": "INM-CM4", "recorte": "prox",
                                  "cenario": "SSP245", "inicio": "01/01/2021", "fim": "31/12/2050"}
        assert c["clima_efetivo"]["climbra"]["uf"] == "SC" and c["grupo"] == "prox"

    def test_modelos_todos_sao_os_19(self):
        plano = self._plano(modelos="todos")
        assert len(plano["casos"]) == 2 * MODELOS * 2

    def test_pode_misturar_com_casos_explicitos(self):
        doc = _doc(expansao=dict(self.EXP, modelos=["INM-CM4"]))
        plano, erros, _ = _validar(doc, arquivos=True)
        assert erros == [] and len(plano["casos"]) == 1 + 4

    def test_id_repetido_entre_explicito_e_expandido(self):
        doc = _doc(casos=[{"id": "florianopolis__INM-CM4__hist", "clima": {"climbra": dict(REF)}}],
                   expansao=dict(self.EXP, modelos=["INM-CM4"]))
        _, erros, _ = _validar(doc)
        assert _tem(erros, "id repetido")

    @pytest.mark.parametrize("mudanca,trecho", [({"modelos": ["XX"]}, "modelos"), ({"recortes": []}, "recortes"),
                                                ({"municipios": []}, "municipios"),
                                                ({"recortes": [{"id": "x", "cenario": "HIST"}]}, "inicio")])
    def test_erros_da_expansao(self, mudanca, trecho):
        _, erros, _ = _validar(_doc(casos=[], expansao={**self.EXP, **mudanca}))
        assert _tem(erros, trecho)

    def test_expansao_sem_casos_e_estudo_valido_mas_vazio_e_erro(self):
        _, erros, _ = _validar(_doc(casos=[], expansao={"municipios": [{"municipio": "Joinville"}], "modelos": ["INM-CM4"], "recortes": []}))
        assert erros

    def test_csv_tidy_tem_as_colunas_das_dimensoes(self):
        plano = self._plano(modelos=["INM-CM4"])
        plano["saidas"]["metricas"] = ["volume_l"]
        cab = E.csv_tidy(plano, [None] * len(plano["casos"]), "pt-BR").splitlines()[0].split(",")
        assert cab[:4] == ["estudo_id", "caso_id", "caso", "grupo"]
        assert cab[4:11] == ["municipio", "ibge", "modelo", "recorte", "cenario", "inicio", "fim"]

    def test_json_schema_conhece_as_chaves_novas(self):
        esq = E.esquema_json()
        assert "expansao" in esq["properties"] and "tarifa" in esq["properties"]["padroes"]["properties"]
        assert "climbra" in esq["properties"]["padroes"]["properties"]["clima"]["properties"]


@pytest.mark.skipif(not BRL, reason="CLIMBra só na Edição Brasil")
class TestExecucaoComClimbra:
    def test_um_caso_roda_com_clima_e_tarifa_do_programa(self, tmp_path):
        doc = _doc(padroes={"substituicoes": dict(SUBS), "tarifa": {"categoria": "comercial", "se_ausente": "residencial"}},
                   analise={"tipo": "economic"})
        arq = tmp_path / "estudo.json"
        arq.write_text(json.dumps(doc), encoding="utf-8")
        plano, _ = E.carregar_plano(arq)
        r = E.executar_caso(plano, plano["casos"][0])
        assert r["status"] == "ok", r.get("erro")
        papeis = {a["papel"] for a in r["arquivos"]}
        assert {"base-climbra", "tarifas"} <= papeis and all(len(a["sha256"]) == 64 for a in r["arquivos"])
        assert r["fonte_da_chuva"]["serie"]["dias"] == 10957
        assert r["metricas"]["capex"] and r["metricas"]["economia_anual_agua"]
        r2 = E.executar_caso(plano, plano["casos"][0])
        assert r["metricas"] == r2["metricas"] and r["fonte_da_chuva"] == r2["fonte_da_chuva"]   # reprodutível

    def test_sem_tarifa_declarada_nenhuma_tarifa_e_aplicada(self, tmp_path):
        arq = tmp_path / "estudo.json"
        arq.write_text(json.dumps(_doc()), encoding="utf-8")
        plano, _ = E.carregar_plano(arq)
        r = E.executar_caso(plano, plano["casos"][0])
        assert r["status"] == "ok" and not any(a["papel"] == "tarifas" for a in r["arquivos"])

    def test_serie_de_360_dias_gera_alerta_de_recorte(self, tmp_path):
        ref = dict(REF, modelo="KACE", cenario="SSP585", inicio="01/01/2071", fim="31/12/2100")
        arq = tmp_path / "estudo.json"
        arq.write_text(json.dumps(_doc(casos=[{"id": "a", "clima": {"climbra": ref}}])), encoding="utf-8")
        plano, _ = E.carregar_plano(arq)
        r = E.executar_caso(plano, plano["casos"][0])
        assert r["status"] == "ok" and any("recorte pedido" in a for a in r["alertas"])

    def test_chave_do_caso_muda_com_o_modelo(self, tmp_path):
        arqs = []
        for modelo in ("INM-CM4", "KACE"):
            arq = tmp_path / f"{modelo}.json"
            arq.write_text(json.dumps(_doc(casos=[{"id": "a", "clima": {"climbra": dict(REF, modelo=modelo)}}])), encoding="utf-8")
            arqs.append(E.carregar_plano(arq)[0])
        ch = [E.chave_do_caso(p, p["casos"][0], E.arquivos_do_caso(p, p["casos"][0])) for p in arqs]
        assert ch[0] != ch[1]


# ══ Os seis estudos de congresso de Santa Catarina ═════════════════════════════════════════════

AEROPORTOS_SC = ("sbcd", "sbch", "sbfl", "sbja", "sbjv", "sblj", "sbnf", "sncp", "snd4", "snd6", "ssbl", "ssck", "ssim", "ssja", "ssku", "ssln", "ssoe", "ssss", "sstb", "ssvi", "ssxx")
SUBTIPOS_SC = {
    "escolar": ("fnde-creche-tipo1", "fnde-creche-tipo2", "fnde-escola-5salas", "fnde-escola-9salas-2pav", "universitaria"),
    "comercial": ("escritorios-4pav", "escritorios-8pav", "salas-lojas-12pav"),
    "residencial-unifamiliar": ("casa-popular", "casa-media", "casa-alto-padrao"),
    "residencial-multifamiliar": ("multi-16-aptos", "multi-32-aptos", "multi-64-aptos"),
    "hospitalar": ("hospital-40-leitos", "hospital-120-leitos", "hospital-300-leitos"),
    "aeroportos": AEROPORTOS_SC,
}
TARIFA_SC = {"escolar": "publica", "comercial": "comercial", "residencial-unifamiliar": "residencial", "residencial-multifamiliar": "residencial",
             "hospitalar": "publica", "aeroportos": "comercial"}


@pytest.mark.skipif(not BRL or not all((PASTA_SC / e).is_dir() for e in SUBTIPOS_SC),
                    reason="estudos de Santa Catarina: só na BRL e fora do Git (estudos/ é ignorada)")
class TestEstudosSantaCatarina:
    """Estudos gerados fora do repositório (``estudos/`` está no .gitignore): seis estudos (escolar, comercial, residencial unifamiliar e
    multifamiliar, hospitalar e aeroportos), cada um com subtipos; 32 municípios com série CLIMBra (aeroportos: 21 aeródromos), os 19 modelos
    climáticos e um só recorte (histórico 1981–2010). Onde a tarifa é a Pública, São Bento do Sul roda em ``<subtipo>-sbs.json`` com a Comercial."""

    @pytest.fixture(scope="class")
    def planos(self):
        out = {}
        for est, subs in SUBTIPOS_SC.items():
            for sub in subs:
                for suf in ("", "-sbs"):
                    arq = PASTA_SC / est / "json" / f"{sub}{suf}.json"
                    if arq.is_file():
                        out[(est, sub, suf)], _ = E.carregar_plano(arq)
        return out

    def test_cada_estudo_tem_os_seus_arquivos(self):
        from triton.cli import load_triton_project
        for est, subs in SUBTIPOS_SC.items():
            assert (PASTA_SC / est / f"{est}.md").is_file(), est
            for sub in subs:
                assert (PASTA_SC / est / "json" / f"{sub}.json").is_file(), (est, sub)
                if TARIFA_SC[est] == "publica":
                    assert (PASTA_SC / est / "json" / f"{sub}-sbs.json").is_file(), (est, sub)
                cfg = load_triton_project(str(PASTA_SC / est / "triton" / f"{sub}.triton"))["config"]
                assert cfg.cost_lower_tank > 0 and cfg.cost_piping > 0 and cfg.cost_accessories > 0, (est, sub)
                assert cfg.pump_unit_cost > 0 and cfg.pump_count == 2 and len(cfg.op_costs) > 0, (est, sub)

    def test_validam_com_municipios_conferidos(self, planos):
        assert len(planos) == sum(len(s) * (2 if TARIFA_SC[e] == "publica" and e != "aeroportos" else 1) for e, s in SUBTIPOS_SC.items())

    def test_contagem_de_casos(self, planos):
        fontes = json.loads((PASTA_SC / "_fontes" / "municipios_sc_climbra.json").read_text(encoding="utf-8"))
        n = fontes["total_na_climbra"]
        assert n == sum(1 for m in fontes["municipios"] if m["na_climbra"]) == 32
        for (est, sub, suf), plano in planos.items():
            if est == "aeroportos":
                esperado = 1 * MODELOS
            else:
                esperado = (1 if suf else (n - 1 if TARIFA_SC[est] == "publica" else n)) * MODELOS
            assert len(plano["casos"]) == esperado, (est, sub, suf)

    def test_tarifa_de_cada_estudo(self, planos):
        for (est, sub, suf), plano in planos.items():
            esperada = "comercial" if suf else TARIFA_SC[est]
            assert plano["padroes"]["tarifa"]["categoria"] == esperada, (est, sub, suf)
            if suf:
                assert {c["dimensoes"]["municipio"] for c in plano["casos"]} == {"São Bento do Sul"}

    def test_municipios_sao_de_sc_e_tem_ibge_42(self, planos):
        for plano in planos.values():
            for c in plano["casos"]:
                assert c["dimensoes"]["ibge"].startswith("42")
                assert c["clima_efetivo"]["climbra"]["uf"] == "SC"

    def test_os_19_modelos_e_um_recorte_historico(self, planos):
        from triton.core.climate_database import CLIMATE_MODELS
        for plano in planos.values():
            dims = [c["dimensoes"] for c in plano["casos"]]
            assert {d["modelo"] for d in dims} == set(CLIMATE_MODELS)
            assert {(d["recorte"], d["cenario"], d["inicio"], d["fim"]) for d in dims} == {("hist-1981-2010", "HIST", "01/01/1981", "31/12/2010")}

    def test_origem_declarada_e_semente(self):
        for est, subs in SUBTIPOS_SC.items():
            for sub in subs:
                doc = json.loads((PASTA_SC / est / "json" / f"{sub}.json").read_text(encoding="utf-8"))
                assert "definições do autor" in doc["padroes"]["substituicoes"]["_origem"]
                assert doc["analise"]["semente"] == 42 and doc["analise"]["pesos"] == [0.333, 0.333, 0.334]
                assert doc["saidas"]["gravar_analise"] is True

    def test_um_caso_de_cada_estudo_roda(self, planos):
        vistos = set()
        for (est, sub, suf), plano in planos.items():
            if est in vistos or suf:
                continue
            vistos.add(est)
            r = E.executar_caso(plano, plano["casos"][0])
            assert r["status"] == "ok", (est, sub, r.get("erro"))
            assert r["metricas"]["volume_l"] and r["metricas"]["economia_agua_potavel_pct"] is not None
