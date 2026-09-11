# -*- coding: utf-8 -*-
"""O que se configura na tela precisa sobreviver ao arquivo do projeto.

Esta é a quinta via do defeito que atravessa o programa: um valor calculado ou
informado corretamente e descartado antes de chegar ao consumidor. Aqui o
consumidor é o **futuro** — o próprio usuário, na semana seguinte, reabrindo o
estudo.

Dois defeitos desta rodada:

**A modulação por calendário não era gravada.** Sete listas existiam na
configuração e nenhuma ia para o arquivo; `demand_mode` também não era escrito a
partir da tela, de modo que o arquivo dizia sempre «constant». Uma escola
modulada por dia da semana reabria como demanda constante, com o mesmo nome e sem
aviso nenhum.

**Projeto de esquema desconhecido virava projeto padrão.** Um JSON sem as seções
do Netuno era aceito e devolvia a configuração inteiramente padrão: o usuário
abria um estudo de 180 m² e simulava 100 m².
"""

from __future__ import annotations

import json
import os
import tempfile

import numpy as np
import pytest

from netuno.core.parser import (
    FormatoDeProjetoDesconhecido, NetunoConfig, export_netuno_json,
    load_netuno_project,
)
from netuno.core.simulation import run_single_simulation

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASOS = os.path.join(RAIZ, "manual", "casos")


@pytest.fixture()
def pasta():
    with tempfile.TemporaryDirectory() as d:
        yield d


def _chuva():
    # Chuva farta e diária, de propósito: com oferta sobrando, quem limita o
    # consumo é a demanda, e a modulação aparece no resultado. Numa série pobre
    # o reservatório vazio esconderia a diferença.
    return np.full(140, 10.0, dtype=float)


# ══════════════════════════════════════════════════════════════════════════════
# A modulação por calendário
# ══════════════════════════════════════════════════════════════════════════════

def test_a_modulacao_semanal_sobrevive_ao_arquivo(pasta):
    cfg = NetunoConfig()
    cfg.demand_mode = "weekly"
    cfg.weekly_demands = [40.0] * 5 + [20.0, 5.0]
    cfg.weekly_residents = [300] * 5 + [150, 20]
    cfg.weekly_shares = [0.70] * 5 + [0.85, 1.0]

    caminho = os.path.join(pasta, "p.netuno")
    export_netuno_json(cfg, caminho, precip_data=_chuva())
    lido = load_netuno_project(caminho)["config"]

    assert lido.demand_mode == "weekly"
    assert lido.weekly_demands == cfg.weekly_demands
    assert lido.weekly_residents == cfg.weekly_residents
    assert lido.weekly_shares == cfg.weekly_shares


def test_a_modulacao_mensal_e_a_diaria_sobrevivem(pasta):
    cfg = NetunoConfig()
    cfg.demand_mode = "monthly"
    cfg.demand_monthly = [200.0] * 12
    cfg.residents_monthly = list(range(1, 13))
    cfg.monthly_shares = [0.45] * 12
    cfg.daily_demands = [100.0, 120.0, 90.0]
    cfg.daily_residents = [2, 3, 2]
    cfg.daily_shares = [0.4, 0.5, 0.4]

    caminho = os.path.join(pasta, "p.netuno")
    export_netuno_json(cfg, caminho, precip_data=_chuva())
    lido = load_netuno_project(caminho)["config"]

    assert lido.monthly_shares == cfg.monthly_shares
    assert lido.residents_monthly == cfg.residents_monthly
    assert lido.daily_demands == cfg.daily_demands
    assert lido.daily_shares == cfg.daily_shares


def test_a_modulacao_muda_o_resultado_depois_de_reabrir(pasta):
    """O teste que importa: não basta o campo voltar, o cálculo tem de usá-lo.

    Sem isto, as listas poderiam voltar do arquivo e continuar inertes — que é
    exatamente o que acontecia com as duas listas mensais, gravadas desde sempre
    e ignoradas na releitura porque o modo lido dizia «constant».
    """
    chuva = _chuva()
    cfg = NetunoConfig()
    cfg.area = 1000.0
    cfg.residents_count = 100
    cfg.demand_value = 40.0
    cfg.rainwater_share = 0.7
    cfg.demand_mode = "weekly"
    # Fim de semana fechado: dois dias em sete sem demanda relevante.
    cfg.weekly_demands = [40.0] * 5 + [2.0, 2.0]
    cfg.weekly_residents = [100] * 5 + [5, 5]
    cfg.weekly_shares = [0.7] * 7

    caminho = os.path.join(pasta, "p.netuno")
    export_netuno_json(cfg, caminho, precip_data=chuva)
    lido = load_netuno_project(caminho)["config"]

    comum = dict(precip_data=chuva, lower_tank_vol=5000.0, area=lido.area,
                 runoff_coeff=lido.runoff_coeff, discard_mm=lido.discard,
                 rainwater_share=lido.rainwater_share)
    constante = run_single_simulation(total_demand_per_day=4000.0, **comum)
    modulado = run_single_simulation(
        total_demand_per_day=4000.0, demand_mode=lido.demand_mode,
        weekly_demands=lido.weekly_demands, weekly_residents=lido.weekly_residents,
        weekly_shares=lido.weekly_shares, **comum)

    assert modulado.avg_pluvial_consumed_l_day != pytest.approx(
        constante.avg_pluvial_consumed_l_day, rel=0.01), (
        "a modulação voltou do arquivo e não mudou nada: está inerte")


# ══════════════════════════════════════════════════════════════════════════════
# Arquivo que não é projeto do Netuno
# ══════════════════════════════════════════════════════════════════════════════

def test_json_sem_as_secoes_do_projeto_e_recusado(pasta):
    caminho = os.path.join(pasta, "outro.netuno")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"format_version": "5.0", "area": 180.0, "residents": 4}, f)

    with pytest.raises(FormatoDeProjetoDesconhecido) as erro:
        load_netuno_project(caminho)
    # A mensagem precisa nomear o arquivo: o usuário costuma ter vários abertos.
    assert "outro.netuno" in str(erro.value)


def test_projeto_do_esquema_corrente_continua_abrindo(pasta):
    cfg = NetunoConfig()
    cfg.area = 180.0
    caminho = os.path.join(pasta, "bom.netuno")
    export_netuno_json(cfg, caminho, precip_data=_chuva())
    assert load_netuno_project(caminho)["config"].area == 180.0


# ══════════════════════════════════════════════════════════════════════════════
# Os arquivos de exemplo que acompanham o manual
# ══════════════════════════════════════════════════════════════════════════════

def _resultados_publicados():
    caminho = os.path.join(CASOS, "resultados.json")
    if not os.path.exists(caminho):
        pytest.skip("casos do manual ainda não gerados")
    return json.load(open(caminho, encoding="utf-8"))


def test_todo_caso_do_manual_abre_e_traz_a_chuva_dentro():
    for arquivo in sorted(_resultados_publicados()):
        proj = load_netuno_project(os.path.join(CASOS, arquivo))
        assert proj["precip_data"] is not None, arquivo
        assert len(proj["precip_data"]) > 0, arquivo


def test_todo_caso_do_manual_reproduz_o_numero_publicado():
    """O arquivo gravado, relido e simulado tem de dar o número impresso.

    É o que garante que o leitor abre o caso e vê a tabela do capítulo. Um campo
    que se perca na gravação aparece aqui como número diferente.
    """
    import sys
    sys.path.insert(0, os.path.join(RAIZ, "manual"))
    from gerar_casos import simular_do_arquivo

    for arquivo, publicado in sorted(_resultados_publicados().items()):
        obtido = simular_do_arquivo(os.path.join(CASOS, arquivo))
        assert obtido["potencial_pct"] == pytest.approx(
            publicado["potencial_pct"], abs=0.05), arquivo
        assert obtido["modo"] == publicado["modo"], arquivo


def test_o_caso_da_escola_guarda_mesmo_a_modulacao():
    """O caso que só existe porque o defeito da modulação foi corrigido."""
    caminho = os.path.join(CASOS, "08_escola_semanal.netuno")
    if not os.path.exists(caminho):
        pytest.skip("casos do manual ainda não gerados")
    cfg = load_netuno_project(caminho)["config"]
    assert cfg.demand_mode == "weekly"
    assert len(cfg.weekly_demands) == 7
    assert cfg.weekly_demands[-1] < cfg.weekly_demands[0], "domingo fechado"


def test_os_estudos_de_exemplo_estao_no_esquema_corrente():
    """Os três de `examples/` eram lidos como projeto padrão, em silêncio."""
    pasta = os.path.join(RAIZ, "examples")
    if not os.path.isdir(pasta):
        pytest.skip("pasta de exemplos ausente")
    achados = 0
    for arquivo in sorted(os.listdir(pasta)):
        # O modelo vazio da automação não é estudo de caso: não tem chuva, e
        # serve de ponto de partida para quem monta projeto por fora da janela.
        if not arquivo.startswith("estudo_caso_"):
            continue
        achados += 1
        proj = load_netuno_project(os.path.join(pasta, arquivo))
        assert proj["precip_data"] is not None, arquivo
        assert proj["config"].area > 100.0, arquivo
    assert achados == 3
