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
do Triton era aceito e devolvia a configuração inteiramente padrão: o usuário
abria um estudo de 180 m² e simulava 100 m².
"""

from __future__ import annotations

import json
import os

import pytest

from triton.core.parser import (
    FormatoDeProjetoDesconhecido, TritonConfig, export_triton_json,
    load_triton_project,
)

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASOS = os.path.join(RAIZ, "manual", "casos")


# ══════════════════════════════════════════════════════════════════════════════
# A modulação por calendário
# ══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
# Arquivo que não é projeto do Triton
# ══════════════════════════════════════════════════════════════════════════════


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
        proj = load_triton_project(os.path.join(CASOS, arquivo))
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


def test_legado_com_demanda_mensal_preserva_modo_e_vetor(tmp_path):
    """Valida que arquivo legado .csv/.net com demanda mensal não degrada silenciosamente para constante."""
    arquivo_teste = tmp_path / "escola_com_ferias.csv"
    # Monta um CSV no formato clássico do Netuno 4 com demanda mensal (12 valores)
    linhas = [
        "Arquivo dados;Florianopolis1.csv",
        "Área de captação;250,0",
        "Demanda de água total;1;1;200;0;0;180;180;180;180;180;180;180;180;0;0;",
        "Número de moradores;0;1;10;",
        "Percentual de água potável;40,0",
        "Coeficiente de escoamento;0,85",
        "Descarte precipitação;1,0",
    ]
    arquivo_teste.write_text("\n".join(linhas), encoding="utf-8")

    proj = load_triton_project(str(arquivo_teste))
    cfg = proj["config"]
    b_data = proj["building_data"]

    assert cfg.demand_mode == "monthly"
    assert len(cfg.demand_monthly) == 12
    # Mês 1 e 2 são férias (0 L/dia)
    assert cfg.demand_monthly[0] == 0.0
    assert cfg.demand_monthly[1] == 0.0
    assert cfg.demand_monthly[2] == 180.0
    assert b_data["demand_mode"] == "monthly"
    assert b_data["monthly_demands"] == cfg.demand_monthly
