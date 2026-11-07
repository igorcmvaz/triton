"""O banco de custos distribuído (``triton/data/costs_database.json``) por edição.

Brasil: preços em reais e fatores regionais por UF, como sempre. Internacional e Ibérica: só a estrutura,
sem preço, sem moeda e sem fatores regionais; o programa abre e as telas de custo funcionam vazias.
Este teste lê o arquivo distribuído e roda o programa num processo à parte, sem o banco de referência
que ``tests/conftest.py`` injeta para testar o motor de custos.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ARQUIVO = RAIZ / "triton" / "data" / "costs_database.json"
EDICAO = os.environ.get("TRITON_EDITION", "BRL").strip().upper()
BRL = EDICAO == "BRL"


def _dinheiro(banco):
    """Todo valor monetário do banco: preços das tabelas, custos unitários e de tipologia, manutenção."""
    for chave in ("lower_tank_pead_prices", "upper_tank_pead_prices"):
        yield from (float(linha[1]) for linha in banco.get(chave, []))
    yield from (float(v) for v in banco.get("pipes_cost_per_meter", {}).values())
    yield float(banco.get("chlorine_cost_per_kg", 0.0))
    par = banco.get("pump_cost_parameters", {})
    yield from (float(par.get(k, 0.0)) for k in ("base_cost", "min_cost"))
    for cfg in banco.get("typology_subsystems_configs", {}).values():
        yield from (float(v) for k, v in cfg.items()
                    if isinstance(v, (int, float)) and ("cost" in k or k == "maint_base_annual"))
    for item in banco.get("default_maintenance_items", []):
        yield float(item.get("fixed_cost", 0.0))
        yield float(item.get("variable_cost_per_m3", 0.0))


def test_o_arquivo_distribuido_e_da_edicao():
    banco = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    if BRL:
        assert banco["_metadata"]["currency"] == "BRL"
        assert len(banco["regional_factors_by_uf"]) == 27
        return
    assert banco["_metadata"]["currency"] == ""
    assert banco["regional_factors_by_uf"] == {}
    assert "_procedencia_precos_reservatorio" not in banco
    assert not any(valor for valor in _dinheiro(banco)), "preço diferente de zero no banco distribuído"
    texto = ARQUIVO.read_text(encoding="utf-8")
    for termo in ("R$", "BRL", "SINAPI", "Fortlev", "Copafer", "Florian", "Sobrado"):
        assert termo not in texto, termo


def test_o_programa_abre_e_os_custos_saem_vazios_com_o_arquivo_distribuido():
    if BRL:
        return
    codigo = (
        "from triton.core import cost_estimates as ce\n"
        "c = ce.estimate_preliminary_capex(5000.0, 500.0, True, 0.37, 1)\n"
        "assert c['total'] == 0.0 and c['lower'] == 0.0 and c['pump'] == 0.0, c\n"
        "assert ce.estimate_tank_price(20000.0) == 0.0\n"
        "assert ce.REGIONAL_FACTORS_BY_UF == {}\n"
        "assert ce.compute_pipe_item_cost(50, 10.0) == 0.0\n"
        "itens = ce.default_maintenance_items(True)\n"
        "assert itens and all(i[2] == 0.0 and i[3] == 0.0 for i in itens), itens\n"
        "assert ce.estimate_calibrated_capex_opex('MFL', 10000.0, 'XX')['capex_total_brl'] == 0.0\n"
        "from triton.core.edition import configuracao_da_edicao, projeto_novo_da_edicao\n"
        "configuracao_da_edicao(); projeto_novo_da_edicao()\n"
        "print('ok')\n"
    )
    env = {k: v for k, v in os.environ.items()}
    r = subprocess.run([sys.executable, "-c", codigo], cwd=str(RAIZ), env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=120)
    assert r.returncode == 0 and r.stdout.strip() == "ok", r.stderr


def test_sem_o_arquivo_as_edicoes_sem_preco_caem_num_banco_neutro():
    if BRL:
        return
    from triton.core import cost_estimates as ce

    banco = ce._banco_neutro()
    assert banco["regional_factors_by_uf"] == {}
    assert not any(_dinheiro(banco))
    assert banco["default_maintenance_items"]
