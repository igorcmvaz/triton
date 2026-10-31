# -*- coding: utf-8 -*-
"""Os projetos de exemplo da edição: abrem, simulam, poupam água e cobram o que o tarifário imprime.

INT: Nova York, Londres e Cidade do Cabo (``examples/*.triton``).
IBE: Lisboa, Porto e Funchal (``examples/portugal/*.triton``).

O arquivo é o mesmo nas três edições; cada bloco pula-se fora da sua edição (e a BRL pula os dois,
porque os exemplos dela são outros). As contas esperadas saem **à mão**, com ``Decimal``, dos números
impressos nos tarifários oficiais (os mesmos que ``examples/LEIA.md`` cita), sem chamar o motor.

Os exemplos são gerados por ferramentas de desenvolvimento (``scripts/gerar_exemplos_int.py`` e
``scripts/gerar_exemplos_prt.py``), que ficam no disco do mantenedor; aqui se confere o arquivo gravado.
"""

from __future__ import annotations

from decimal import Decimal as D
from pathlib import Path

import pytest

from triton.core.edition import EDITION_INT, EDITION_PRT, get_current_edition

RAIZ = Path(__file__).resolve().parents[2]
EDICAO = get_current_edition()

INT_EXEMPLOS = RAIZ / "examples"
PRT_EXEMPLOS = RAIZ / "examples" / "portugal"
ES_EXEMPLOS = RAIZ / "examples" / "espanha"

CIDADES_INT = ("new_york", "london", "cape_town")
CIDADES_PRT = ("lisboa", "porto", "funchal")
CIDADES_ES = ("madrid", "palma")

so_int = pytest.mark.skipif(
    EDICAO != EDITION_INT or not (INT_EXEMPLOS / "new_york.triton").is_file(),
    reason="exemplos da Edição International")
so_prt = pytest.mark.skipif(
    EDICAO != EDITION_PRT or not (PRT_EXEMPLOS / "lisboa.triton").is_file(),
    reason="exemplos da Edição Ibérica")

#: O que não pode aparecer num exemplo da INT (Brasil e Portugal) ou da IBE (Brasil).
TERMOS_DO_BRASIL = ("Florianópolis", "Florianopolis", "Brasília", "Manaus", "São Paulo", "R$", "CASAN", "CELESC",
                    "CLIMBra", "SABESP", "ANEEL", "NBR", "IPTU", "Selic")
TERMOS_DE_PORTUGAL = ("Lisboa", "Porto", "Funchal", "EPAL", "E-OBS", "ERSAR")


def _carregar(caminho: Path):
    from triton.core.parser import load_triton_project
    return load_triton_project(str(caminho))


def _conta(cfg, m3: float) -> float:
    """A conta mensal de água e esgoto do projeto, pelo motor, para ``m3`` de consumo."""
    from triton.core.economic import calculate_water_bill, esgoto_do_projeto
    return calculate_water_bill(
        m3 * 1000.0, cfg.water_tariffs, cfg.sewage_mode, cfg.sewage_rate,
        cfg.water_tax_fixed, cfg.water_tax_var, **esgoto_do_projeto(cfg))


def _simular(res, litros: float = 4000.0):
    from triton.core.simulation import run_single_simulation
    c = res["config"]
    return run_single_simulation(
        precip_data=res["precip_data"], lower_tank_vol=litros, area=c.area, runoff_coeff=c.runoff_coeff,
        discard_mm=c.discard, discard_mode=c.discard_mode,
        total_demand_per_day=c.residents_count * c.demand_value, rainwater_share=c.rainwater_share,
        start_date_str=c.start_date)


def _escalonado(faixas, volume: D) -> D:
    """Soma de ``(início, fim, preço)`` pelo trecho do volume que cai em cada faixa (fim None = aberto)."""
    total = D(0)
    for inicio, fim, preco in faixas:
        topo = volume if fim is None else min(volume, D(fim))
        if topo > D(inicio):
            total += (topo - D(inicio)) * D(preco)
    return total


# ---------------------------------------------------------------------------------------------
# INT: contas à mão
# ---------------------------------------------------------------------------------------------

def _nova_york_a_mao(m3: D) -> D:
    """US$ 5,35 por CCF (1 CCF = 2,8316847 m³); esgoto 159% da água; mínimo US$ 0,49/dia (30,4375 dias/mês)."""
    agua = max(m3 * D("5.35") / D("2.8316847"), D("0.49") * D("30.4375"))
    return agua * (1 + D("1.59"))


def _londres_a_mao(m3: D) -> D:
    """Água £ 2,7346/m³ + £ 66,87/ano; águas residuais £ 1,4721/m³ + £ 128,13/ano; meses de 1/12 do ano."""
    return (D("66.87") / 12 + m3 * D("2.7346")) + m3 * D("1.4721") + D("128.13") / 12


def _cidade_do_cabo_a_mao(m3: D) -> D:
    """Água por faixas (R/kl) + R 103,65 fixos; esgoto: 70% do consumo, por faixas, até 35 kl + R 56,66 fixos."""
    agua = D("103.65") + _escalonado([(0, 6, "25.05"), (6, "10.5", "34.42"), ("10.5", 35, "54.60"), (35, None, "109.98")], m3)
    esgoto = D("56.66") + _escalonado([(0, "4.2", "18.28"), ("4.2", "7.35", "25.11"), ("7.35", "24.5", "42.18"),
                                       ("24.5", 35, "73.91")], m3 * D("0.7"))
    return agua + esgoto


A_MAO_INT = {"new_york": _nova_york_a_mao, "london": _londres_a_mao, "cape_town": _cidade_do_cabo_a_mao}


@so_int
@pytest.mark.parametrize("cidade", CIDADES_INT)
@pytest.mark.parametrize("m3", [2, 5, 10, 18, 25, 40, 60])
def test_a_conta_de_agua_e_esgoto_confere_com_o_tarifario_impresso(cidade, m3):
    cfg = _carregar(INT_EXEMPLOS / f"{cidade}.triton")["config"]
    esperado = A_MAO_INT[cidade](D(m3))
    assert _conta(cfg, m3) == pytest.approx(float(esperado), abs=2e-3), (cidade, m3)


@so_int
def test_contas_de_18_m3_calculadas_a_mao_e_escritas_por_extenso():
    """Âncoras independentes das funções acima: o consumo da casa do tutorial (4 × 150 L × 30 dias = 18 m³)."""
    ny, ld, ct = (_carregar(INT_EXEMPLOS / f"{c}.triton")["config"] for c in CIDADES_INT)
    # Nova York: 18 / 2,8316847 × 5,35 = 34,0080 de água (96,3 / 2,8316847); × 2,59 = 88,0808
    assert _conta(ny, 18) == pytest.approx(88.0808, abs=2e-3)
    # Londres: 5,5725 + 49,2228 de água; 26,4978 + 10,6775 de águas residuais = 91,9706
    assert _conta(ld, 18) == pytest.approx(91.9706, abs=1e-3)
    # Cidade do Cabo: água 103,65 + 6×25,05 + 4,5×34,42 + 7,5×54,60 = 818,34; esgoto (12,6 kl)
    # 56,66 + 4,2×18,28 + 3,15×25,11 + 5,25×42,18 = 433,9775; total 1252,3175
    assert _conta(ct, 18) == pytest.approx(1252.3175, abs=1e-3)


@so_int
def test_o_esgoto_da_cidade_do_cabo_para_no_teto_de_35_kl():
    """Acima de 35 kl de esgoto (50 kl de água) o tarifário impresso não cobra mais esgoto."""
    ct = _carregar(INT_EXEMPLOS / "cape_town.triton")["config"]
    agua = lambda m3: _escalonado([(0, 6, "25.05"), (6, "10.5", "34.42"), ("10.5", 35, "54.60"), (35, None, "109.98")], D(m3))
    assert _conta(ct, 70) - float(agua(70)) == pytest.approx(_conta(ct, 50) - float(agua(50)), abs=1e-6)


@so_int
@pytest.mark.parametrize("cidade", CIDADES_INT)
def test_o_exemplo_da_int_abre_simula_e_economiza_agua(cidade):
    from triton.core.economic import run_economic_analysis
    res = _carregar(INT_EXEMPLOS / f"{cidade}.triton")
    c = res["config"]
    assert len(res["precip_data"]) == 10958
    assert (c.area, c.residents_count, c.demand_value, c.rainwater_share) == (150.0, 4, 150.0, 0.28)
    sim = _simular(res)
    assert sim.potential_potable_savings_pct > 5.0
    eco = run_economic_analysis(c, sim)
    assert eco.annual_water_savings_brl > 0.0


@so_int
@pytest.mark.parametrize("cidade,moeda", [("new_york", "USD"), ("london", "GBP"), ("cape_town", "ZAR")])
def test_cada_exemplo_da_int_traz_a_sua_moeda_e_nenhum_custo_inventado(cidade, moeda):
    from triton.core.dados_do_relatorio import moeda_do_projeto
    res = _carregar(INT_EXEMPLOS / f"{cidade}.triton")
    c = res["config"]
    assert moeda_do_projeto(res["ui_state"])["code"] == moeda
    for campo in ("cost_lower_tank", "cost_upper_tank", "cost_labor", "cost_piping", "cost_accessories",
                  "pump_unit_cost", "elec_tariff", "chlorine_cost_per_kg"):
        assert getattr(c, campo) == 0.0, campo
    assert all(op[2] == 0.0 and op[3] == 0.0 for op in c.op_costs)
    notas = res["analysis"]
    assert "enter your own" in notas["costs"]
    assert notas["tariff_validity"] == c.tariff_vigencia
    assert notas["tariff_source"] and notas["tariff_assumptions"]


@so_int
@pytest.mark.parametrize("cidade", CIDADES_INT)
def test_o_exemplo_da_int_nao_traz_brasil_nem_portugal(cidade):
    texto = (INT_EXEMPLOS / f"{cidade}.triton").read_text(encoding="utf-8")
    achados = [t for t in TERMOS_DO_BRASIL + TERMOS_DE_PORTUGAL if t in texto]
    assert not achados, achados


# ---------------------------------------------------------------------------------------------
# IBE: contas à mão (números impressos nos tarifários de 2026; IVA conforme a nota de cada um)
# ---------------------------------------------------------------------------------------------

def _lisboa_a_mao(m3: D) -> D:
    """EPAL (água, IVA 6%) + saneamento da Câmara (escalões sobre 90% do volume, TRH 0,032 por m³ recolhido)
    + adicional C.M. Lisboa 0,1483, resíduos 2,2333 + 0,1710 por m³ e TGR 0,0523 por m³ (sem IVA)."""
    agua = (D("5.82") + _escalonado([(0, 5, "0.4634"), (5, 15, "0.8666"), (15, 25, "2.0398"), (25, None, "2.5961")], m3)) * D("1.06")
    recolhido = m3 * D("0.9")
    saneamento = (D("2.999")
                  + _escalonado([(0, 5, "0.2198"), (5, 15, "0.5787"), (15, 25, "1.3621"), (25, None, "1.7165")], recolhido)
                  + recolhido * D("0.032"))
    return agua + saneamento + m3 * D("0.1483") + D("2.2333") + m3 * D("0.171") + m3 * D("0.0523")


def _porto_a_mao(m3: D) -> D:
    """Águas e Energia do Porto 2026: água (disponibilidade 0,1242 €/dia × 30 e escalões), saneamento (0,0665 × 30) e
    TRH 0,0392 €/m³, tudo com IVA de 6%."""
    agua = D("0.1242") * 30 + _escalonado([(0, 5, "0.4945"), (5, 15, "0.9649"), (15, 25, "1.7657"), (25, None, "3.0016")], m3)
    san = D("0.0665") * 30 + _escalonado([(0, 5, "0.3875"), (5, 15, "0.7606"), (15, 25, "1.4608"), (25, None, "2.4423")], m3)
    return (agua + san + m3 * D("0.0392")) * D("1.06")


def _funchal_a_mao(m3: D) -> D:
    """Câmara do Funchal 2026 (valores sem IVA, IVA de 4% a confirmar): água 4,12 fixa + 5 escalões; saneamento
    1,97 fixa + (0; 0,33+0,22; 0,41+0,60) por escalão; resíduos 2,19 fixa."""
    agua = D("4.12") + _escalonado([(0, 5, "0.39"), (5, 15, "0.69"), (15, 25, "1.28"), (25, 50, "2.87"), (50, None, "5.02")], m3)
    san = D("1.97") + _escalonado([(0, 5, "0"), (5, 15, "0.55"), (15, None, "1.01")], m3)
    return (agua + san + D("2.19")) * D("1.04")


A_MAO_PRT = {"lisboa": _lisboa_a_mao, "porto": _porto_a_mao, "funchal": _funchal_a_mao}


@so_prt
@pytest.mark.parametrize("cidade", CIDADES_PRT)
@pytest.mark.parametrize("m3", [3, 10, 18, 30, 60])
def test_a_conta_de_agua_e_saneamento_confere_com_o_tarifario_impresso(cidade, m3):
    cfg = _carregar(PRT_EXEMPLOS / f"{cidade}.triton")["config"]
    assert _conta(cfg, m3) == pytest.approx(float(A_MAO_PRT[cidade](D(m3))), abs=2e-3), (cidade, m3)


@so_prt
def test_contas_de_10_e_30_m3_conferidas_com_as_contas_impressas_no_json_do_tarifario():
    """As contas de conferência do ``portugal_tarifarios.json`` foram feitas à mão, só com números impressos."""
    esperado = {"lisboa": (25.8683, 94.3767), "porto": (20.2995, 93.3293), "funchal": (17.0872, 67.5272)}
    for cidade, (c10, c30) in esperado.items():
        cfg = _carregar(PRT_EXEMPLOS / f"{cidade}.triton")["config"]
        assert _conta(cfg, 10) == pytest.approx(c10, abs=1e-3), cidade
        assert _conta(cfg, 30) == pytest.approx(c30, abs=1e-3), cidade


@so_prt
@pytest.mark.parametrize("cidade", CIDADES_PRT)
def test_o_exemplo_da_prt_abre_simula_e_economiza_agua(cidade):
    from triton.core.economic import run_economic_analysis
    res = _carregar(PRT_EXEMPLOS / f"{cidade}.triton")
    c = res["config"]
    assert res["precip_data"] is not None and len(res["precip_data"]) == 10957   # 1986-2015
    assert (c.area, c.residents_count, c.demand_value, c.rainwater_share) == (150.0, 4, 150.0, 0.28)
    sim = _simular(res)
    assert sim.potential_potable_savings_pct > 5.0
    eco = run_economic_analysis(c, sim)
    assert eco.annual_water_savings_brl > 0.0


@so_prt
def test_a_chuva_de_cada_cidade_e_a_da_sua_fonte():
    """Lisboa e Porto: Iberia01 (ODbL) por código, 1986-2015. Funchal: ERA5 de ilha (nível C) da base das ilhas."""
    lisboa, porto, funchal = (_carregar(PRT_EXEMPLOS / f"{c}.triton") for c in CIDADES_PRT)
    anual = lambda r: float(r["precip_data"].sum()) / 30.0
    for r in (lisboa, porto, funchal):
        c = r["config"]
        assert c.climate_model == "Iberia01 v1.0" and c.climate_scenario == "IBERIA01"
        assert (c.climate_start_date, c.climate_end_date) == ("01/01/1986", "31/12/2015")
        assert r["chuva_da_climbra"] is True and not r.get("aviso_chuva")
    assert [r["config"].climate_city_name for r in (lisboa, porto, funchal)] == [
        "Lisboa [PT-1106]", "Porto [PT-1312]", "Funchal [PT-3103]"]
    assert 740 < anual(lisboa) < 755 and 1190 < anual(porto) < 1205 and 525 < anual(funchal) < 540


@so_prt
def test_o_funchal_do_exemplo_e_a_serie_era5_das_ilhas_e_confere_com_o_funchal_csv():
    """A série ERA5 de ilha do exemplo é a mesma célula do ``Funchal.csv`` (Open-Meteo): totais anuais iguais em 1991-2015."""
    import numpy as np
    from triton.core import base_climatica_iberica as ib
    from triton.core.parser import load_precipitation
    assert ib.fonte_da_unidade("PT-3103") == "era5" and ib.unidade("PT-3103")["nivel"] == "C"
    ilha = ib.carregar_serie("PT-3103", "01/01/1991", "31/12/2015")[0]
    csv = load_precipitation(str(RAIZ / "data" / "rainfall" / "Funchal.csv"))[:len(ilha)]
    assert abs(float(ilha.sum()) - float(csv.sum())) / float(csv.sum()) < 0.005


@so_prt
def test_os_exemplos_da_ibe_nao_trazem_a_e_obs_nem_a_restricao_nao_comercial():
    for cidade in CIDADES_PRT + CIDADES_ES:
        pasta = ES_EXEMPLOS if cidade in CIDADES_ES else PRT_EXEMPLOS
        texto = (pasta / f"{cidade}.triton").read_text(encoding="utf-8")
        assert "E-OBS" not in texto and "EOBS" not in texto, cidade


@so_prt
@pytest.mark.parametrize("cidade", CIDADES_ES)
def test_o_exemplo_de_espanha_abre_simula_e_declara_os_limites_da_tarifa(cidade):
    from triton.core.economic import run_economic_analysis
    res = _carregar(ES_EXEMPLOS / f"{cidade}.triton")
    c = res["config"]
    assert c.climate_scenario == "IBERIA01" and c.climate_city_name.endswith("]")
    assert len(res["precip_data"]) == 10957 and not res.get("aviso_chuva")
    sim = _simular(res)
    assert sim.potential_potable_savings_pct > 5.0
    assert run_economic_analysis(c, sim).annual_water_savings_brl > 0.0
    notas = res["analysis"]
    assert "introduza os seus" in notas["custos"]
    texto = " ".join(notas["hipoteses_tarifarias"]) + " " + " ".join(notas["fontes_tarifarias"])
    if cidade == "madrid":
        assert notas["camada_tarifaria"] == 1 and "NÃO CONFERIDA" in texto
    else:
        assert notas["camada_tarifaria"] == 3 and "indicativa" in texto


@so_prt
def test_so_o_funchal_tem_eletricidade_e_com_a_fonte_secundaria_registada():
    lisboa, porto, funchal = (_carregar(PRT_EXEMPLOS / f"{c}.triton") for c in CIDADES_PRT)
    assert lisboa["config"].elec_tariff == porto["config"].elec_tariff == 0.0
    c = funchal["config"]
    assert c.elec_tariff == 0.1673 and c.elec_tax_var == 0.0 and c.elec_tax_fixed == 0.0
    nota = funchal["analysis"]["eletricidade"]
    assert "FONTE SECUNDÁRIA" in nota and "20/02/2025" in nota and "0,3386" in nota and "sem IVA" in nota
    from triton.core.economic import run_economic_analysis
    assert run_economic_analysis(c, _simular(funchal)).annual_pump_cost_brl > 0.0


@so_prt
@pytest.mark.parametrize("cidade", CIDADES_PRT)
def test_cada_exemplo_da_prt_traz_euros_vigencia_fontes_e_nenhum_custo_inventado(cidade):
    from triton.core.dados_do_relatorio import moeda_do_projeto
    res = _carregar(PRT_EXEMPLOS / f"{cidade}.triton")
    c = res["config"]
    assert moeda_do_projeto(res["ui_state"])["code"] == "EUR"
    assert c.tariff_vigencia == "01/01/2026"
    for campo in ("cost_lower_tank", "cost_upper_tank", "cost_labor", "cost_piping", "cost_accessories",
                  "pump_unit_cost", "chlorine_cost_per_kg"):
        assert getattr(c, campo) == 0.0, campo
    assert all(op[2] == 0.0 and op[3] == 0.0 for op in c.op_costs)
    notas = res["analysis"]
    assert "introduza os seus" in notas["custos"]
    assert notas["fontes_tarifarias"] and notas["hipoteses_tarifarias"]


@so_prt
def test_as_duvidas_do_porto_e_do_funchal_ficam_a_vista_nas_notas_do_exemplo():
    porto, funchal = (_carregar(PRT_EXEMPLOS / f"{c}.triton")["analysis"] for c in ("porto", "funchal"))
    assert "a confirmar" in " ".join(porto["hipoteses_tarifarias"])
    texto = " ".join(funchal["hipoteses_tarifarias"])
    assert "NÃO foram verificados" in texto and "1.º escalão" in texto


@so_prt
@pytest.mark.parametrize("cidade", CIDADES_PRT)
def test_o_exemplo_da_prt_nao_traz_o_brasil(cidade):
    texto = (PRT_EXEMPLOS / f"{cidade}.triton").read_text(encoding="utf-8")
    achados = [t for t in TERMOS_DO_BRASIL if t in texto]
    assert not achados, achados
