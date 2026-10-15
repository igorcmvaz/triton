# -*- coding: utf-8 -*-
"""Os padrões por edição: o ``TritonConfig()`` cru é histórico; a fábrica da edição é neutra.

Regra (auditoria/ESPECIFICACAO_DE_NEUTRALIDADE.md): o código é o mesmo nas três edições e o
motor não conhece edição. Quem conhece é a camada que cria o projeto: ``configuracao_da_edicao``
(leitores de projeto e linha de comando) e ``projeto_novo_da_edicao`` (interface). Estes testes
fixam o desenho para que ninguém volte a neutralizar por heurística dentro do dataclass
(compararia o valor com «o número da CASAN» e zeraria o que o usuário digitou igual).

Rodam em todas as edições: escolhem a edição pela variável de ambiente, com ``monkeypatch``.
"""

import json
import os
from dataclasses import asdict, fields

import numpy as np
import pytest

from triton.core import edition as E
from triton.core.parser import TritonConfig, load_triton_project

#: Campos que mudam a cada instância e não são «padrão».
_VOLATEIS = {"project_id", "created_at", "data_base_estudo"}


def _comparavel(cfg):
    return {k: v for k, v in asdict(cfg).items() if k not in _VOLATEIS}


def _texto_de_valores(cfg) -> str:
    """Todos os valores textuais da configuração, juntos, para procurar o Brasil."""
    return " | ".join(str(v) for k, v in asdict(cfg).items() if isinstance(v, str))


@pytest.mark.parametrize("edicao", ["BRL", "INT", "PRT"])
def test_o_tritonconfig_cru_traz_os_padroes_historicos_em_qualquer_edicao(monkeypatch, edicao):
    """O motor e os testes dele usam o ``TritonConfig()`` cru: ele não depende da edição."""
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    referencia = _comparavel(TritonConfig())
    monkeypatch.setenv("TRITON_EDITION", edicao)
    cfg = TritonConfig()
    assert _comparavel(cfg) == referencia
    assert cfg.elec_tariff == pytest.approx(0.6957) and cfg.pump_unit_cost == pytest.approx(300.0)
    assert len(cfg.water_tariffs) == 5 and cfg.tariff_city_name == "Florianópolis"
    assert cfg.precos_de_catalogo is True


def test_na_brl_a_fabrica_devolve_exatamente_o_tritonconfig(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    assert _comparavel(E.configuracao_da_edicao()) == _comparavel(TritonConfig())
    novo = E.projeto_novo_da_edicao()
    assert novo.capex_do_arranjo is True and novo.mao_de_obra_automatica is True
    esperado = TritonConfig()
    esperado.capex_do_arranjo = esperado.mao_de_obra_automatica = True
    assert _comparavel(novo) == _comparavel(esperado)


@pytest.mark.parametrize("edicao", ["INT", "PRT"])
def test_fora_da_brl_a_fabrica_nao_traz_preco_tarifa_nem_cidade_do_brasil(monkeypatch, edicao):
    monkeypatch.setenv("TRITON_EDITION", edicao)
    cfg = E.configuracao_da_edicao()
    assert cfg.water_tariffs == [] and cfg.elec_tariff == 0.0
    assert cfg.pump_unit_cost == 0.0 and cfg.chlorine_cost_per_kg == 0.0
    assert all(c[2] == 0.0 and c[3] == 0.0 for c in cfg.op_costs) and cfg.op_costs  # roteiro mantido
    assert cfg.precos_de_catalogo is False and cfg.iptu_green_enabled is False
    assert cfg.capex_do_arranjo is False and cfg.mao_de_obra_automatica is False
    texto = _texto_de_valores(cfg)
    for brasil in ("Florianópolis", "CASAN", "INM-CM4", "HIST"):
        assert brasil not in texto, (brasil, texto)
    assert cfg.climate_city_uf != "SC" and cfg.tariff_city_uf != "SC" and cfg.elec_city_uf != "SC"


def test_na_internacional_nao_ha_localidade_climatica_predefinida(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "INT")
    cfg = E.projeto_novo_da_edicao()
    assert cfg.climate_source_mode == "custom_file"
    assert (cfg.climate_city_uf, cfg.climate_city_name, cfg.climate_model, cfg.climate_scenario) == ("", "", "", "")
    assert cfg.tariff_city_name == "CUSTOM" and cfg.water_tariffs == []


def test_em_portugal_o_projeto_novo_parte_de_lisboa_na_e_obs(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "PRT")
    from triton.core import base_climatica_portugal as pt
    cfg = E.projeto_novo_da_edicao()
    assert cfg.climate_source_mode == "national_db"
    assert (cfg.climate_city_uf, cfg.climate_city_name) == (pt.DISTRITO_PADRAO, pt.CONCELHO_PADRAO)
    assert (cfg.climate_model, cfg.climate_scenario) == (pt.MODELO_EOBS, pt.CENARIO_EOBS)
    assert (cfg.climate_start_date, cfg.climate_end_date) == (pt.INICIO_PADRAO, pt.FIM_PADRAO)
    assert "Florianópolis" not in _texto_de_valores(cfg)


def _projeto_minimo(tmp_path, fe=None, co=None):
    """Um .triton sem quase nada: só o que o leitor exige e a chuva."""
    inputs = {}
    if fe is not None:
        inputs["financial_and_economic"] = fe
    if co is not None:
        inputs["capex_and_opex"] = co
    dados = {"schema": "triton-project", "metadata": {"name": "mínimo"},
             "rainfall": {"file_name": "x.csv", "precipitation_mm": [0.0, 5.0, 1.0]},
             "inputs": inputs}
    caminho = tmp_path / "minimo.triton"
    caminho.write_text(json.dumps(dados), encoding="utf-8")
    return str(caminho)


@pytest.mark.parametrize("edicao", ["INT", "PRT"])
def test_o_leitor_de_projeto_preenche_o_que_falta_com_o_neutro_da_edicao(tmp_path, monkeypatch, edicao):
    monkeypatch.setenv("TRITON_EDITION", edicao)
    cfg = load_triton_project(_projeto_minimo(tmp_path))["config"]
    assert cfg.climate_city_name != "Florianópolis" and cfg.tariff_city_name != "Florianópolis"
    assert cfg.elec_tariff == 0.0 and cfg.pump_unit_cost == 0.0
    assert cfg.cost_lower_tank == 0.0 and cfg.cost_piping == 0.0 and cfg.precos_de_catalogo is False


def test_na_brl_o_leitor_continua_a_preencher_com_o_historico(tmp_path, monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    cfg = load_triton_project(_projeto_minimo(tmp_path))["config"]
    assert (cfg.climate_city_uf, cfg.climate_city_name) == ("SC", "Florianópolis")
    assert cfg.climate_model == "ACCESS-CM2" and cfg.climate_end_date == "31/12/2014"
    assert cfg.elec_tariff == 1.0 and cfg.pump_unit_cost == 320.0
    assert (cfg.cost_lower_tank, cfg.cost_upper_tank, cfg.cost_labor) == (2500.0, 380.0, 1500.0)
    assert cfg.precos_de_catalogo is True


@pytest.mark.parametrize("edicao", ["BRL", "INT", "PRT"])
def test_o_que_o_usuario_grava_vale_em_qualquer_edicao_mesmo_igual_ao_padrao_historico(tmp_path, monkeypatch, edicao):
    """A neutralização por heurística zerava a tarifa de 0,6957 digitada pelo usuário: não pode."""
    monkeypatch.setenv("TRITON_EDITION", edicao)
    fe = {"elec_tariff": 0.6957, "water_tariffs": [[0.0, 0.0, 46.34, -1], [0.0, 10.0, 3.08, 1],
                                                    [10.0, 25.0, 14.31, 1], [25.0, 50.0, 19.14, 1],
                                                    [50.0, 999999.0, 24.08, 1]]}
    cfg = load_triton_project(_projeto_minimo(tmp_path, fe=fe, co={"cost_lower_tank": 2500.0}))["config"]
    assert cfg.elec_tariff == pytest.approx(0.6957)
    assert len(cfg.water_tariffs) == 5 and cfg.water_tariffs[0][2] == pytest.approx(46.34)
    assert cfg.cost_lower_tank == 2500.0


def test_projeto_gravado_e_relido_nao_muda_em_nenhuma_edicao(tmp_path, monkeypatch):
    """Gravar e reler devolve a mesma configuração, qualquer que seja a edição que lê."""
    from triton.core.parser import export_triton_json
    cfg = TritonConfig()
    destino = tmp_path / "ida_e_volta.triton"
    export_triton_json(cfg, str(destino), precip_data=np.zeros(30))
    for edicao in ("BRL", "INT", "PRT"):
        monkeypatch.setenv("TRITON_EDITION", edicao)
        lido = load_triton_project(str(destino))["config"]
        for campo in ("elec_tariff", "pump_unit_cost", "chlorine_cost_per_kg", "water_tariffs",
                      "tariff_city_name", "climate_city_name", "precos_de_catalogo", "op_costs"):
            assert json.loads(json.dumps(getattr(lido, campo))) == json.loads(json.dumps(getattr(cfg, campo))), (edicao, campo)


def test_a_configuracao_tem_todos_os_campos_do_dataclass_sem_hook_de_edicao():
    """Guarda: o dataclass não pergunta pela edição (nada de ``__post_init__`` que neutraliza)."""
    assert not hasattr(TritonConfig, "__post_init__")
    assert {f.name for f in fields(TritonConfig)} >= {"water_tariffs", "elec_tariff", "op_costs"}


def test_as_listas_por_edicao_apontam_para_testes_que_existem():
    """Uma entrada velha em so_da_brl.txt / so_da_prt.txt deixaria um teste fora da execução sem ninguém ver."""
    import re
    pasta = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raiz = os.path.dirname(pasta)
    for lista in ("so_da_brl.txt", "so_da_prt.txt"):
        caminho = os.path.join(pasta, lista)
        if not os.path.isfile(caminho):
            continue
        for linha in open(caminho, encoding="utf-8"):
            entrada = linha.strip()
            if not entrada or entrada.startswith("#"):
                continue
            arquivo, _, resto = entrada.partition("::")
            assert os.path.isfile(os.path.join(raiz, arquivo)), f"{lista}: {arquivo} não existe"
            if resto:
                teste = resto.split("::")[-1]
                texto = open(os.path.join(raiz, arquivo), encoding="utf-8").read()
                assert re.search(rf"def {re.escape(teste)}\b", texto), f"{lista}: {entrada} não existe"
