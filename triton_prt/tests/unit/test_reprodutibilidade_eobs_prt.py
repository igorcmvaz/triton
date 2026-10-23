# -*- coding: utf-8 -*-
"""Reprodutibilidade da chuva E-OBS no projeto: pacote_id, versão e SHA-256 gravados; série incorporada.

Só vale na PRT (``tests/so_da_prt.txt``). Ao salvar com chuva da base E-OBS, o arquivo grava o pacote de
que a série vem e, por padrão, a própria série. Ao reabrir com um pacote diferente, o projeto avisa (no
programa e no laudo) e regista a mudança. Projeto antigo, sem pacote_id, abre sem erro e diz que o pacote
não está registado. O mesmo arquivo dá os mesmos resultados com ``TRITON_EDITION=PRT`` e ``=IBE``.
"""
import json

import numpy as np
import pytest

from triton.core import base_climatica_portugal as pt
from triton.core import parser as P
from triton.core.parser import TritonConfig, export_triton_json, load_triton_project, serie_da_climbra

pytestmark = pytest.mark.skipif(not pt.disponivel(), reason="data/portugal_eobs.db ausente")


def _cfg(concelho="Faro", distrito="Faro", ini="01/01/2001", fim="31/12/2010"):
    cfg = TritonConfig()
    cfg.climate_source_mode = "national_db"
    cfg.climate_city_uf, cfg.climate_city_name = distrito, concelho
    cfg.climate_model, cfg.climate_scenario = pt.MODELO_EOBS, pt.CENARIO_EOBS
    cfg.climate_start_date, cfg.climate_end_date, cfg.start_date = ini, fim, ini
    return cfg


def _gravar(tmp_path, cfg=None, nome="p.triton", **kw):
    cfg = cfg or _cfg()
    serie = serie_da_climbra(cfg)
    destino = tmp_path / nome
    export_triton_json(cfg, str(destino), precip_data=serie, **kw)
    return destino, serie, json.loads(destino.read_text(encoding="utf-8"))


def _outro_pacote(monkeypatch, sufixo="0"):
    atual = dict(pt.pacote())
    outro = {**atual, "pacote_id": "PT-EOBS-v34.0-deadbeef", "sha256_pacote": "deadbeef" + sufixo * 56,
             "versao_eobs": "v34.0"}
    monkeypatch.setattr(P, "_pacote_atual_da_eobs", lambda: outro)
    return atual, outro


def test_ao_salvar_grava_o_pacote_e_incorpora_a_serie_por_padrao(tmp_path):
    _, serie, dados = _gravar(tmp_path)
    chuva = dados["rainfall"]
    meta = pt.metadados()
    pacote = chuva["pacote_chuva"]
    assert pacote["pacote_id"] == meta["pacote_id"] and pacote["versao_eobs"] == "v33.0e"
    assert pacote["sha256_pacote"] == meta["sha256_pacote"] and len(pacote["sha256_pacote"]) == 64
    assert pacote["qualidade_versao"] == meta["qualidade_versao"]
    assert pacote["serie_incorporada"] is True and pacote["historico"] == []
    assert len(chuva["precipitation_mm"]) == len(serie) == chuva["total_days"]
    assert chuva["climbra_series"]["origem"] == "E-OBS (Portugal)"


def test_incorporar_serie_pode_ser_desligado(tmp_path):
    cfg = _cfg()
    destino, serie, dados = _gravar(tmp_path, cfg, incorporar_serie=False)
    chuva = dados["rainfall"]
    assert chuva["precipitation_mm"] == [] and chuva["pacote_chuva"]["serie_incorporada"] is False
    proj = load_triton_project(str(destino))
    assert proj["chuva_da_climbra"] and np.array_equal(proj["precip_data"], serie) and not proj.get("aviso_chuva")
    cfg2 = _cfg()
    cfg2.incorporar_serie_eobs = False
    _, _, dados2 = _gravar(tmp_path, cfg2, "q.triton")
    assert dados2["rainfall"]["precipitation_mm"] == []


def test_a_reabertura_com_o_mesmo_pacote_reproduz_a_serie_sem_aviso(tmp_path):
    destino, serie, _ = _gravar(tmp_path)
    proj = load_triton_project(str(destino))
    assert np.array_equal(proj["precip_data"], serie)
    assert proj["chuva_da_climbra"] and not proj.get("aviso_chuva")
    proc = proj["chuva_procedencia"]
    assert proc["registrado"] and not proc["mudou"] and proc["serie_incorporada"]
    assert proc["pacote_id"] == pt.metadados()["pacote_id"]
    assert proj["config"].chuva_procedencia["pacote_id"] == proc["pacote_id"]


def test_pacote_diferente_com_serie_incorporada_avisa_e_mantem_a_serie_do_estudo(tmp_path, monkeypatch):
    destino, serie, _ = _gravar(tmp_path)
    antigo, novo = _outro_pacote(monkeypatch)
    proj = load_triton_project(str(destino))
    assert np.array_equal(proj["precip_data"], serie)                       # reproduz o estudo
    aviso = proj["aviso_chuva"]
    assert antigo["pacote_id"] in aviso and novo["pacote_id"] in aviso and "série incorporada" in aviso
    proc = proj["chuva_procedencia"]
    assert proc["mudou"] and proc["pacote_id"] == antigo["pacote_id"]       # a série continua a ser do pacote antigo
    assert proc["historico"][-1]["tipo"] == "serie_incorporada_de_outro_pacote"


def test_pacote_diferente_sem_serie_incorporada_avisa_e_regista_a_mudanca(tmp_path, monkeypatch):
    destino, serie, _ = _gravar(tmp_path, incorporar_serie=False)
    antigo, novo = _outro_pacote(monkeypatch)
    proj = load_triton_project(str(destino))
    assert proj["precip_data"] is not None and len(proj["precip_data"]) == len(serie)  # segue com a série da base
    assert "mudou" in proj["aviso_chuva"] and antigo["pacote_id"] in proj["aviso_chuva"]
    proc = proj["chuva_procedencia"]
    assert proc["mudou"] and proc["pacote_id"] == novo["pacote_id"]
    assert proc["historico"][-1] == {"em": proc["historico"][-1]["em"], "tipo": "serie_recomposta_de_outro_pacote",
                                     "gravado": antigo["pacote_id"], "instalado": novo["pacote_id"]}


def test_o_historico_da_mudanca_sobrevive_a_um_novo_salvamento(tmp_path):
    """Projeto gravado com um pacote antigo (série diferente da instalada): reaberto e salvo de novo, mantém o pacote dele."""
    destino, serie, dados = _gravar(tmp_path)
    dados["rainfall"]["precipitation_mm"][5] += 7.0                 # a série do pacote antigo difere da instalada
    dados["rainfall"]["pacote_chuva"].update({"pacote_id": "PT-EOBS-v32.0-0ldp4ck", "sha256_pacote": "a" * 64,
                                              "versao_eobs": "v32.0"})
    destino.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    proj = load_triton_project(str(destino))
    assert proj["chuva_procedencia"]["mudou"] and proj["aviso_chuva"]
    assert not np.array_equal(proj["precip_data"], serie)           # a série do estudo, não a instalada
    destino2 = tmp_path / "segundo.triton"
    export_triton_json(proj["config"], str(destino2), precip_data=proj["precip_data"])
    chuva2 = json.loads(destino2.read_text(encoding="utf-8"))["rainfall"]
    pacote = chuva2["pacote_chuva"]
    assert pacote["pacote_id"] == "PT-EOBS-v32.0-0ldp4ck" and pacote["sha256_pacote"] == "a" * 64   # a procedência não se perde
    assert pacote["historico"][-1]["tipo"] == "serie_incorporada_de_outro_pacote"
    assert pacote["historico"][-1]["instalado"] == pt.metadados()["pacote_id"]
    assert pacote["serie_incorporada"] is True and chuva2["climbra_series"] is None
    reaberto = load_triton_project(str(destino2))
    assert np.array_equal(reaberto["precip_data"], proj["precip_data"]) and reaberto["chuva_procedencia"]["mudou"]
    assert len(reaberto["chuva_procedencia"]["historico"]) == 2     # a anterior e a desta abertura


def test_o_aviso_da_mudanca_chega_ao_rodape_do_laudo(tmp_path, monkeypatch):
    from triton.core.licenca_eobs import rodape_do_laudo
    destino, _, _ = _gravar(tmp_path)
    _outro_pacote(monkeypatch)
    proj = load_triton_project(str(destino))
    html = rodape_do_laudo({"climate_city_name": "Faro", "chuva_procedencia": proj["chuva_procedencia"]})
    assert "Aviso: O pacote de chuva da E-OBS mudou" in html and "PT-EOBS-v34.0-deadbeef" in html


def test_projeto_antigo_sem_pacote_id_abre_e_diz_que_o_pacote_nao_esta_registado(tmp_path):
    """Compatibilidade: um arquivo gravado antes do registo do pacote (só a referência, sem 'pacote_chuva')."""
    destino, serie, dados = _gravar(tmp_path, incorporar_serie=False)
    del dados["rainfall"]["pacote_chuva"]
    destino.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    proj = load_triton_project(str(destino))
    assert np.array_equal(proj["precip_data"], serie) and proj["chuva_da_climbra"]
    proc = proj["chuva_procedencia"]
    assert proc["registrado"] is False and "não registado" in proc["nota"] and not proc["mudou"]
    assert not proj.get("aviso_chuva")                                      # nota, não alerta a cada abertura
    from triton.core.licenca_eobs import rodape_do_laudo
    assert "não registado" in rodape_do_laudo({"climate_city_name": "Faro", "chuva_procedencia": proc})


def test_projeto_antigo_com_a_serie_incorporada_e_sem_pacote_abre(tmp_path):
    destino, serie, dados = _gravar(tmp_path)
    del dados["rainfall"]["pacote_chuva"]
    destino.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    proj = load_triton_project(str(destino))
    assert np.array_equal(proj["precip_data"], serie) and proj["chuva_procedencia"]["registrado"] is False


def test_projeto_de_antes_da_e_obs_sem_referencia_continua_a_abrir(tmp_path):
    """O formato mais antigo: série incorporada e nenhuma referência; não há procedência a registar."""
    cfg = _cfg()
    cfg.climate_source_mode = "custom_file"
    destino = tmp_path / "antigo.triton"
    export_triton_json(cfg, str(destino), precip_data=np.arange(40, dtype=float))
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert "pacote_chuva" not in dados["rainfall"]
    proj = load_triton_project(str(destino))
    assert len(proj["precip_data"]) == 40 and "chuva_procedencia" not in proj


@pytest.mark.parametrize("nome", ["PRT", "IBE"])
def test_o_mesmo_projeto_da_os_mesmos_resultados_com_prt_e_ibe(tmp_path, monkeypatch, nome):
    destino, serie, _ = _gravar(tmp_path)
    monkeypatch.setenv("TRITON_EDITION", nome)
    proj = load_triton_project(str(destino))
    assert np.array_equal(proj["precip_data"], serie)
    assert proj["config"].climate_city_name == "Faro" and proj["config"].climate_scenario == pt.CENARIO_EOBS
    assert proj["chuva_procedencia"]["pacote_id"] == pt.metadados()["pacote_id"]
    assert not proj.get("aviso_chuva")
    from triton.cli import _load_bundle
    assert np.array_equal(_load_bundle(str(destino))["precip_data"], serie)


def test_prt_e_ibe_leem_o_mesmo_arquivo_com_o_mesmo_resultado_numerico(tmp_path, monkeypatch):
    from triton.core.simulation import run_single_simulation
    destino, _, _ = _gravar(tmp_path)
    leituras, simulacoes = {}, {}
    for nome in ("PRT", "IBE"):
        monkeypatch.setenv("TRITON_EDITION", nome)
        proj = load_triton_project(str(destino))
        cfg = proj["config"]
        leituras[nome] = (proj["precip_data"].copy(), cfg.climate_city_name, cfg.area, cfg.water_tariffs,
                          proj["chuva_procedencia"]["pacote_id"])
        r = run_single_simulation(precip_data=proj["precip_data"], lower_tank_vol=5000.0, area=cfg.area,
                                  total_demand_per_day=300.0, rainwater_share=0.4)
        simulacoes[nome] = (r.potential_potable_savings_pct, r.avg_pluvial_consumed_l_day, r.avg_spilled_l_day)
    a, b = leituras["PRT"], leituras["IBE"]
    assert np.array_equal(a[0], b[0]) and a[1:] == b[1:]
    assert simulacoes["PRT"] == simulacoes["IBE"] and simulacoes["PRT"][0] > 0
