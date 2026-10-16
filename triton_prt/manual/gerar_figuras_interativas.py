# -*- coding: utf-8 -*-
"""Os dados das figuras interativas do site de documentação (Edição Portugal).

Cada figura interativa é a mesma figura do manual, com os parâmetros em que o
leitor quer mexer. Nada é calculado no navegador: o simulador corre aqui, numa
grelha de valores, e a página só escolhe a célula. Por isso o site mostra os
mesmos números do programa e do PDF, e uma correção no motor chega às duas
coisas na mesma montagem.

As chaves do dicionário são os nomes dos ficheiros das figuras estáticas, e é
por eles que o site encontra onde pôr cada uma.

Uso: chamado por gerar_site.py.
"""

from __future__ import annotations

import os
os.environ["TRITON_EDITION"] = "PRT"

import sys
from datetime import datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
for p in (str(RAIZ), str(AQUI)):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402

from gerar_figuras import REGIMES_HIPOTETICOS  # noqa: E402
from gerar_tabelas import (  # noqa: E402
    CHUVA_23, CIDADES_GUIA14, CUSTOS_TUTORIAL, NOMES_CIDADES, TARIFA_CASAN, TUTORIAL,
    _CFG_LISBOA, _config_ambiental, _config_economica, _config_projeto, _config_tutorial,
    _pressurizadores_ilustrativos, _serie,
)
from triton.core.simulation import run_single_simulation  # noqa: E402

INICIO = datetime(1991, 1, 1)     # o mesmo calendário das figuras do manual (1991-2020)
DIAS_MES = 30.4375
MATERIAIS = [("CONCRETO", "Betão armado"), ("PEAD", "Polietileno (PEAD)"),
             ("FIBRA", "Fibra de vidro (PRFV)"), ("ACO_INOX", "Aço inoxidável")]


def _r(x, casas=0):
    return round(float(x), casas) if casas else int(round(float(x)))


# ── o balanço de dez dias ─────────────────────────────────────────────────────

def dez_dias():
    """Os dez dias do exemplo, com a capacidade e a lâmina de descarte a variar."""
    capacidades = [1000, 1500, 2000, 2500, 3000]
    descartes = [0.0, 1.0, 2.0, 3.0]
    casos = {}
    for c in capacidades:
        for d in descartes:
            r = run_single_simulation(
                precip_data=np.array(CHUVA_23, dtype=float), lower_tank_vol=float(c),
                area=100.0, runoff_coeff=0.85, discard_mm=d, discard_mode=1,
                total_demand_per_day=200.0, rainwater_share=0.40,
                store_daily_details=True)
            casos[f"{c}|{d:g}"] = [
                [_r(x.eff_precip_mm, 1), _r(x.harvested_liters), _r(x.pluvial_demand_liters),
                 _r(x.pluvial_consumed_liters), _r(x.potable_consumed_liters),
                 _r(x.spilled_liters), _r(x.lower_tank_end_liters), x.satisfaction_type]
                for x in r.daily_results]
    return {"chuva": CHUVA_23, "capacidades": capacidades, "descartes": descartes,
            "padrao": [2000, 2.0], "area": 100.0, "coef": 0.85, "demanda": 200.0,
            "fracao": 0.40, "casos": casos}


# ── o nível da cisterna, dia a dia ────────────────────────────────────────────

def serie_diaria():
    """O nível ao fim de cada dia, em seis capacidades, nos trinta anos."""
    serie = _serie()
    volumes = [1000, 2000, 5000, 8000, 12000, 20000]
    anos = [(INICIO + timedelta(days=i)).year for i in range(len(serie))]
    primeiro = {}
    for i, a in enumerate(anos):
        primeiro.setdefault(a, i)
    lista_anos = sorted(primeiro)
    niveis, resumo = {}, {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  store_daily_details=True, **_config_tutorial())
        niv = [_r(d.lower_tank_end_liters) for d in r.daily_results]
        niveis[str(v)] = niv
        por_ano = []
        for a in lista_anos:
            dias = [d for i, d in enumerate(r.daily_results) if anos[i] == a]
            demanda = sum(d.pluvial_demand_liters for d in dias)
            usado = sum(d.pluvial_consumed_liters for d in dias)
            por_ano.append([
                _r(sum(d.precip_mm for d in dias)),
                _r(100.0 * usado / demanda, 1) if demanda else 0.0,
                _r(sum(d.spilled_liters for d in dias) / 1000.0, 1),
                sum(1 for d in dias if d.lower_tank_end_liters <= 0.05 * v),
                sum(1 for d in dias if d.satisfaction_type == 2),
                len(dias)])
        resumo[str(v)] = por_ano
    return {"inicio": INICIO.strftime("%Y-%m-%d"), "anos": lista_anos,
            "primeiro_dia": [primeiro[a] for a in lista_anos],
            "chuva": [_r(x, 1) for x in serie], "volumes": volumes,
            "padrao": 5000, "niveis": niveis, "resumo": resumo,
            "demanda_pluvial": _r(TUTORIAL["moradores"] * TUTORIAL["per_capita"]
                                  * TUTORIAL["rainwater_share"])}


# ── a permanência da autonomia ────────────────────────────────────────────────

def permanencia():
    """Curva de permanência da autonomia e renovações, de 500 L a 20.000 L."""
    serie = _serie()
    volumes = list(range(500, 20001, 500))
    pontos = list(range(0, 101, 2))
    curvas, estados = {}, {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  store_daily_details=True, **_config_tutorial())
        demanda = r.daily_results[0].pluvial_demand_liters
        aut = np.array([d.lower_tank_end_liters / demanda for d in r.daily_results])
        curvas[str(v)] = [_r(np.percentile(aut, 100 - p), 2) for p in pontos]
        niveis = np.array([d.lower_tank_end_liters for d in r.daily_results]) / v
        estados[str(v)] = [
            _r(r.avg_pluvial_consumed_l_day * 365.25 / v, 1),       # renovações/ano
            _r(np.mean(niveis <= 0.05) * 100.0, 1),                 # % vazia
            _r(np.mean(niveis >= 0.95) * 100.0, 1),                 # % cheia
            _r(np.median(aut), 1),                                  # autonomia mediana
            _r(r.potential_potable_savings_pct, 2)]
    return {"volumes": volumes, "pontos": pontos, "curvas": curvas,
            "estados": estados, "referencias": [2000, 5000, 10000, 20000],
            "padrao": 5000,
            "demanda_pluvial": _r(TUTORIAL["moradores"] * TUTORIAL["per_capita"]
                                  * TUTORIAL["rainwater_share"])}


# ── a fatura nos três regimes de mínimo ───────────────────────────────────────

TARIFAS_DOS_REGIMES = {
    "franq": REGIMES_HIPOTETICOS[0][1],
    "disp": REGIMES_HIPOTETICOS[1][1],
    "sem": REGIMES_HIPOTETICOS[2][1],
}


def regimes():
    from triton.core.economic import calculate_water_bill
    consumos = [round(0.25 * i, 2) for i in range(0, 161)]
    curvas = []
    for chave, nome, exemplo in [
            ("disp", "Tarifa de disponibilidade", "hipotética: 40 u.m. mais 5 u.m./m³"),
            ("franq", "Franquia no valor mínimo", "hipotética: 50 u.m. pelos primeiros 10 m³, depois 5 u.m./m³"),
            ("sem", "Sem valor mínimo", "hipotética: 5 u.m./m³")]:
        tarifa = TARIFAS_DOS_REGIMES[chave]
        curvas.append({"chave": chave, "nome": nome, "exemplo": exemplo,
                       "fatura": [_r(calculate_water_bill(c * 1000.0, tarifa, 1, 0.0, 0.0, 0.0), 2)
                                  for c in consumos]})
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=TUTORIAL["volume"],
                              **_config_projeto())
    antes = (r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day) * DIAS_MES / 1000.0
    depois = r.avg_potable_consumed_l_day * DIAS_MES / 1000.0
    return {"consumos": consumos, "curvas": curvas,
            "padrao": [round(antes * 4) / 4, round(depois * 4) / 4]}


# ── o fluxo de caixa ──────────────────────────────────────────────────────────

def fluxo_de_caixa():
    """Colunas anuais e saldo descontado, por volume e material da cisterna."""
    from triton.core.economic import run_economic_analysis
    serie = _serie()
    volumes = [2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000]
    casos = {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **_config_projeto())
        for chave, _ in MATERIAIS:
            e = run_economic_analysis(_config_economica(v, chave), r)
            n = int(np.ceil(len(e.monthly_cash_flows) / 12.0))
            econ, custo, acum = [0.0] * (n + 1), [0.0] * (n + 1), [0.0] * (n + 1)
            custo[0], acum[0] = e.capex_total, -e.capex_total
            for f in e.monthly_cash_flows:
                a = (f.month - 1) // 12 + 1
                econ[a] += f.water_savings + f.iptu_savings
                custo[a] += f.pump_cost + f.om_cost + f.chlorine_cost
                acum[a] = f.cumulative_discounted
            casos[f"{v}|{chave}"] = {
                "economia": [_r(x) for x in econ], "custo": [_r(x) for x in custo],
                "acumulado": [_r(x) for x in acum], "capex": _r(e.capex_total),
                "vpl": _r(e.vpl), "retorno": (_r(e.payback_years, 1) if e.payback_years else None),
                "tir": _r(e.tir_annual_pct, 1) if e.tir_annual_pct == e.tir_annual_pct else None,
                "potencial": _r(r.potential_potable_savings_pct, 2)}
    return {"volumes": volumes, "materiais": MATERIAIS, "padrao": [5000, "CONCRETO"],
            "casos": casos, "tma": CUSTOS_TUTORIAL["tma"], "anos": 20}


# ── o carbono ao longo da vida útil ───────────────────────────────────────────

def carbono():
    from triton.core.environmental import calculate_lca
    serie = _serie()
    volumes = [1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000]
    casos = {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **_config_projeto())
        for chave, _ in MATERIAIS:
            cfg = _config_ambiental(r)
            cfg.lower_material_key = chave
            lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, cfg)
            ret = lca.environmental_payback_years
            casos[f"{v}|{chave}"] = [_r(lca.total_embodied_co2_kg, 1), _r(lca.net_annual_avoided_co2_kg, 3),
                                     _r(lca.lower_tank_mass_kg), _r(lca.annual_avoided_co2_kg, 1),
                                     _r(ret, 2) if ret and ret == ret and ret != float("inf") else None]
    return {"volumes": volumes, "materiais": MATERIAIS, "padrao": 5000,
            "casos": casos, "anos": 20}


# ── os três concelhos ─────────────────────────────────────────────────────────

def cidades():
    """Regime mensal e curva de potencial de Lisboa, Porto e Funchal."""
    volumes = list(range(0, 20001, 1000))
    saida = []
    for chave in CIDADES_GUIA14:
        serie = _serie(chave)
        anos = len(serie) / 365.25
        meses = np.zeros(12)
        for i, x in enumerate(serie):
            meses[(INICIO + timedelta(days=i)).month - 1] += float(x)
        pot = [_r(run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                        **_config_tutorial()).potential_potable_savings_pct, 2)
               for v in volumes]
        saida.append({"chave": chave, "nome": NOMES_CIDADES.get(chave, chave),
                      "anual": _r(serie.sum() / anos),
                      "mensal": [_r(m / anos) for m in meses],
                      "dias_chuva": _r(np.mean(serie > 0.1) * 100.0, 1),
                      "potencial": pot})
    return {"volumes": volumes, "cidades": saida,
            "fracao": TUTORIAL["rainwater_share"], "padrao": 5000}


# ── a decisão multicritério ───────────────────────────────────────────────────

VOLUMES_MCDM = (1000, 2000, 3000, 4000, 5000, 8000, 12000)
MATERIAL_MCDM = "PEAD"

ROTULOS_DOS_CRITERIOS = (
    "Maior potencial", "Menor extravasamento", "Maior VAL", "Menor período de recuperação",
    "Maior TIR", "Menor emissão de CO₂e", "Menor consumo da rede",
)


def _candidatos_mcdm():
    """Os mesmos candidatos da figura do programa, com os sete critérios."""
    from triton.core.economic import run_economic_analysis
    from triton.core.environmental import calculate_lca
    from triton.core.topsis import TopsisCandidate
    serie = _serie()
    cands = []
    for v in VOLUMES_MCDM:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **_config_projeto())
        e = run_economic_analysis(_config_economica(v, MATERIAL_MCDM), r)
        amb = _config_ambiental(r)
        amb.lower_material_key = MATERIAL_MCDM
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        cands.append(TopsisCandidate(
            lower_tank_vol=float(v), water_saved_m3_yr=r.annual_pluvial_consumed_m3,
            vpl_brl=e.vpl, co2_saved_kg_lifetime=lca.lifetime_net_co2_saved_kg,
            capex_brl=e.capex_total,
            potential_savings_pct=r.potential_potable_savings_pct,
            overflow_m3_yr=r.annual_spill_m3,
            discounted_payback_years=e.payback_years,
            irr_pct=e.tir_annual_pct,
            potable_consumed_m3_yr=r.annual_potable_consumed_m3))
    return cands


def multicriterio():
    """A matriz de decisão do TOPSIS; a pontuação sai do peso escolhido na página."""
    from triton.core.topsis import (
        CRITERION_GROUPS, CRITERION_IS_BENEFIT, CRITERION_KEYS,
        _decision_matrix, calculate_topsis_scores)
    cands = _candidatos_mcdm()
    matriz = _decision_matrix(cands)
    padrao = calculate_topsis_scores(cands, None)
    return {
        "volumes": [int(c.lower_tank_vol) for c in cands],
        "criterios": [{"chave": k, "rotulo": r, "eixo": g, "beneficio": bool(b),
                       "unidade": u, "casas": d}
                      for k, r, g, b, u, d in zip(
                          CRITERION_KEYS, ROTULOS_DOS_CRITERIOS, CRITERION_GROUPS,
                          CRITERION_IS_BENEFIT,
                          ["%", "m³/ano", "€", "anos", "% a.a.", "kg CO₂e", "m³/ano"],
                          [2, 1, 0, 1, 1, 0, 1])],
        "matriz": [[_r(x, 4) for x in linha] for linha in matriz],
        "eixos": [("technical", "Técnico"), ("economic", "Económico"),
                  ("environmental", "Ambiental")],
        "capex": [_r(c.capex_brl) for c in cands],
        "sem_retorno": [c.discounted_payback_years is None for c in cands],
        "escores_padrao": [_r(x, 6) for x in padrao.scores],
        "material": MATERIAL_MCDM,
    }


def smaa():
    """Aceitabilidade estocástica: com que frequência cada volume vence."""
    from triton.core.mcdm_methods import run_smaa_analysis
    cands = _candidatos_mcdm()
    casos = {}
    for motor, v in (("vikor", 0.0), ("vikor", 0.5), ("vikor", 1.0), ("topsis", 0.5)):
        res = run_smaa_analysis(cands, num_samples=5000, random_seed=42,
                                engine=motor, v_param=v)
        casos[f"{motor}|{v:g}"] = {
            "aceitabilidade": [[_r(x, 2) for x in linha] for linha in res.rank_acceptabilities],
            "primeiro": [_r(x, 2) for x in res.first_rank_probs],
            "central": [[_r(x, 4) for x in linha] for linha in res.central_weights],
            "confianca": [_r(x, 2) for x in res.confidence_factors],
        }
    return {"volumes": [int(c.lower_tank_vol) for c in cands], "casos": casos,
            "padrao": ["vikor", 0.5], "sorteios": 5000, "semente": 42}


# ── os índices pluviométricos, ano a ano ──────────────────────────────────────

INDICES = [
    ("PRCPTOT", "Precipitação total anual", "mm", 0,
     "Soma da chuva dos dias húmidos, isto é, dos dias com 1 mm ou mais."),
    ("R95p", "Chuva dos dias muito húmidos", "mm", 0,
     "Soma da chuva dos dias que passam do percentil 95 dos dias húmidos da série."),
    ("RX1day", "Maior chuva num dia", "mm", 1,
     "A maior lâmina diária do ano."),
    ("RX5day", "Maior chuva em cinco dias", "mm", 1,
     "A maior soma de cinco dias consecutivos dentro do ano."),
    ("SDII", "Intensidade média dos dias húmidos", "mm/dia", 1,
     "Chuva do ano dividida pelo número de dias húmidos."),
    ("R20mm", "Dias com 20 mm ou mais", "dias", 0,
     "Quantos dias do ano tiveram lâmina de 20 mm ou mais."),
    ("CDD", "Maior período seco", "dias", 0,
     "A maior sequência de dias seguidos com menos de 1 mm."),
    ("CWD", "Maior período húmido", "dias", 0,
     "A maior sequência de dias seguidos com 1 mm ou mais."),
    ("Seasonality_Index", "Índice de sazonalidade", "—", 2,
     "Concentração da chuva ao longo dos meses, de Walsh e Lawler (1981): "
     "abaixo de 0,20 o regime é muito uniforme; 1,20 ou mais, extremo."),
]


def indices_pluviometricos():
    """Os nove índices, ano a ano, nos três concelhos do guia."""
    import pandas as pd
    from triton.core.calculator import IndicesCalculator
    saida = []
    for chave in CIDADES_GUIA14:
        serie = _serie(chave)
        datas = [INICIO + timedelta(days=i) for i in range(len(serie))]
        df = pd.DataFrame({"date": datas, "precipitation": [float(x) for x in serie]})
        calc = IndicesCalculator(df, exclude_incomplete=False)
        tabela = calc.compute_climate_indices()
        saida.append({
            "chave": chave, "nome": NOMES_CIDADES.get(chave, chave),
            "anos": [int(a) for a in tabela["year"]],
            "valores": {k: [_r(x, c) for x in tabela[k]] for k, _, _, c, _ in INDICES},
        })
    return {"cidades": saida,
            "indices": [{"chave": k, "nome": n, "unidade": u, "casas": c, "texto": t}
                        for k, n, u, c, t in INDICES],
            "padrao": ["Lisboa", "PRCPTOT"]}


# ── o investimento aberto por rubrica ─────────────────────────────────────────

def investimento():
    """O CAPEX por rubrica, na mesma definição do programa, por volume e material."""
    from gerar_figuras_decisao import rubricas_do_investimento
    volumes = [1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000]
    casos, conferido = {}, True
    for v in volumes:
        for chave, _ in MATERIAIS:
            valores, capex = rubricas_do_investimento(v, chave)
            casos[f"{v}|{chave}"] = [_r(x) for x in valores]
            conferido = conferido and abs(sum(valores) - capex) < 0.51
    return {"volumes": volumes, "materiais": MATERIAIS, "padrao": [5000, "PEAD"],
            "rubricas": ["Reservatório inferior (cisterna)",
                         "Reservatório superior (1 000 L, PEAD)", "Mão de obra",
                         "Tubagem", "Acessórios",
                         "Eletrobombas (serviço e reserva)",
                         "Linha de tratamento, além da verba dos acessórios"],
            "casos": casos, "fecha_com_o_capex": conferido,
            "area": TUTORIAL["area"], "descarte": TUTORIAL["discard_mm"]}


# ── a fatura aberta em parcelas ───────────────────────────────────────────────

def fatura():
    """A fatura de Lisboa aberta em quota fixa, escalões de água, saneamento e resíduos."""
    consumos = [round(0.25 * i, 2) for i in range(0, 121)]
    iva_agua = 1.0 + float(_CFG_LISBOA.water_tax_var) / 100.0
    disponibilidade = sum(t[2] for t in TARIFA_CASAN if t[3] == -1) * iva_agua
    faixas = [(i, f, p * iva_agua) for i, f, p, c in TARIFA_CASAN if c == 1]
    san_fixo = float(_CFG_LISBOA.water_tax_fixed)
    san_faixas = [(float(i), 999999.0 if f is None else float(f), float(p))
                  for i, f, p in _CFG_LISBOA.sewage_tariffs]
    coef_san = float(_CFG_LISBOA.sewage_volume_factor)
    linhas = []
    for c in consumos:
        parcelas = [disponibilidade]
        for inicio, fim, preco in faixas:
            parcelas.append(max(0.0, min(c, fim) - inicio) * preco)
        c_san = c * coef_san
        san_var = sum(max(0.0, min(c_san, fim) - inicio) * preco for inicio, fim, preco in san_faixas)
        parcelas.append(san_fixo + san_var)
        linhas.append([_r(x, 2) for x in parcelas])
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=TUTORIAL["volume"],
                              **_config_projeto())
    antes = (r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day) * DIAS_MES / 1000.0
    depois = r.avg_potable_consumed_l_day * DIAS_MES / 1000.0
    return {"consumos": consumos, "parcelas": linhas,
            "rubricas": ["Quota de serviço da água (fixa, com IVA)"] +
                        [f"Escalão de água de {i:.0f} a {f:.0f} m³ (com IVA)" if f < 999 else
                         f"Escalão de água acima de {i:.0f} m³ (com IVA)" for i, f, _ in faixas] +
                        ["Saneamento e resíduos (fixo + variável)"],
            "precos": [_r(p, 2) for _, _, p in faixas], "fixo": _r(disponibilidade, 2),
            "padrao": [round(antes * 4) / 4, round(depois * 4) / 4]}


# ── a sensibilidade: que premissa move o resultado ────────────────────────────

def sensibilidade():
    """O tornado do VAL, com a amplitude de variação nas mãos do leitor."""
    from triton.core.economic import run_robust_economic_analysis, run_sensitivity_analysis
    from gerar_figuras_decisao import ROTULOS_DO_TORNADO, base_do_tornado
    base = base_do_tornado()
    vpl = run_robust_economic_analysis(**base).vpl
    amplitudes = [10, 20, 30, 50]
    casos = {}
    for a in amplitudes:
        curvas = run_sensitivity_analysis(base, variations_pct=[-float(a), float(a)])
        por_premissa = {}
        for rotulo, curva in curvas.items():
            ponto = {round(pct): valor for pct, valor in curva}
            por_premissa[ROTULOS_DO_TORNADO.get(rotulo, rotulo)] = [_r(ponto[-a]), _r(ponto[a])]
        casos[str(a)] = por_premissa
    return {"vpl_base": _r(vpl), "amplitudes": amplitudes, "padrao": 30, "casos": casos,
            "premissas": sorted(casos["30"]),
            "volume": int(TUTORIAL["volume"]), "material": "Betão armado",
            "anos": base["analysis_period_years"]}


# ── quanto a cobertura capta ──────────────────────────────────────────────────

def captacao():
    """Chuva aproveitável por metro quadrado, mês a mês, nos três concelhos."""
    from triton.core.hydrology_defaults import COEFICIENTES_POR_MATERIAL
    descartes = [0.0, 1.0, 2.0, 3.0]
    cidades = []
    for chave in CIDADES_GUIA14:
        serie = _serie(chave)
        anos = len(serie) / 365.25
        meses = {}
        for d in descartes:
            soma = np.zeros(12)
            for i, x in enumerate(serie):
                efetiva = max(0.0, float(x) - d) if float(x) > 0 else 0.0
                soma[(INICIO + timedelta(days=i)).month - 1] += efetiva
            meses[f"{d:g}"] = [_r(v / anos, 1) for v in soma]
        cidades.append({"chave": chave, "nome": NOMES_CIDADES.get(chave, chave),
                        "mensal": meses,
                        "anual": {k: _r(sum(v), 1) for k, v in meses.items()}})
    return {"cidades": cidades, "descartes": descartes,
            "materiais": [[n, c] for n, c in COEFICIENTES_POR_MATERIAL],
            "fonte_coeficientes": "Lista de coeficientes de escoamento por material de cobertura do programa; "
                                  "declare o valor adotado no projeto.",
            "padrao": ["Lisboa", 2.0, 150, "Telha Cerâmica"],
            "areas": list(range(20, 601, 10)),
            "demanda_pluvial_tutorial": _r(TUTORIAL["moradores"] * TUTORIAL["per_capita"]
                                           * TUTORIAL["rainwater_share"])}


# ── qual sobrepressor gasta menos ─────────────────────────────────────────────

CATALOGO_DO_SITE = _pressurizadores_ilustrativos()
CONTROLES_PT = {"pressostato": "pressostato", "fluxostato": "fluxostato",
                "eletronico": "controlador eletrónico"}


def comparar_do_site(volume_m3_ano, pressao_m, partidas_ano, vazao_do_ponto_l_min=None):
    from triton.core.pressurizer_catalog import VAZAO_DO_PONTO_PADRAO_L_MIN, energia
    vazao = VAZAO_DO_PONTO_PADRAO_L_MIN if vazao_do_ponto_l_min is None else vazao_do_ponto_l_min
    lista = [energia(p, volume_m3_ano, pressao_m, partidas_ano, vazao) for p in CATALOGO_DO_SITE]
    return sorted(lista, key=lambda e: (not e.atende, e.kwh_ano))


def pressurizadores():
    """Os seis modelos genéricos comparados em pressão, volume e arranques."""
    from triton.core.pressurizer_catalog import VAZAO_DO_PONTO_PADRAO_L_MIN
    pressoes = [round(5 + 2.5 * i, 1) for i in range(15)]      # 5 a 40 m.c.a.
    volumes = [50, 100, 150, 200, 300, 400]                    # m³/ano elevados
    partidas = [500, 1200, 2500, 5000]
    casos = {}
    for p in pressoes:
        for v in volumes:
            for n in partidas:
                casos[f"{p:g}|{v}|{n}"] = [
                    {"chave": e.chave, "atende": bool(e.atende),
                     "vazao": _r(e.vazao_l_min, 1), "vazao_bomba": _r(e.vazao_da_bomba_l_min, 1),
                     "horas": _r(e.horas_ano), "kwh": _r(e.kwh_ano, 1),
                     "kwh_m3": _r(e.kwh_por_m3, 3)}
                    for e in comparar_do_site(float(v), float(p), float(n))]
    return {"pressoes": pressoes, "volumes": volumes, "partidas": partidas,
            "padrao": [15, 150, 1200], "casos": casos,
            "vazao_do_ponto": VAZAO_DO_PONTO_PADRAO_L_MIN,
            "modelos": [{"chave": p.chave, "rotulo": p.rotulo, "cv": _r(p.potencia_cv, 3),
                         "controle": CONTROLES_PT.get(p.controle, p.controle), "kw": _r(p.potencia_kw, 3),
                         "kw_eletrico": _r(p.potencia_eletrica_kw, 3),
                         "pressao_maxima": _r(p.pressao_maxima_m, 1),
                         "retardo": _r(p.retardo_s, 1),
                         "fonte": "modelo genérico com curva ilustrativa, sem marca",
                         "curva": [[_r(q, 2), _r(h, 2)] for q, h in p.curva]}
                        for p in CATALOGO_DO_SITE],
            "tarifa": CUSTOS_TUTORIAL["elec_tariff"]}


# ── as classes de qualidade ───────────────────────────────────────────────────

CLASSES_DE_QUALIDADE_PT = {
    "classe_1": ("Classe 1: conjunto mínimo de referência",
                 "Conjunto de parâmetros de base para todos os usos não potáveis que o programa cobre: "
                 "descarga de sanitas e urinóis, lavagem de pavimentos e veículos, reserva de incêndio, "
                 "uso ornamental, rega paisagística e sistemas de arrefecimento."),
    "classe_2": ("Classe 2 (adaptada, não normativa): rega de jardins e lavagem de pavimentos e veículos",
                 "Contacto ocasional com a pele e geração moderada de aerossóis."),
    "classe_3": ("Classe 3 (adaptada, não normativa): torres de arrefecimento e caldeiras industriais",
                 "Usos industriais e de climatização com controlo exigente de biofilme e incrustação."),
    "classe_4": ("Classe 4 (adaptada, não normativa): lavandaria e usos não potáveis exigentes",
                 "Usos que requerem água límpida e sem odor para não manchar tecidos."),
}


def classes_de_qualidade():
    """Os parâmetros de cada classe, como o programa os define."""
    from triton.core.water_quality import WATER_QUALITY_CLASSES
    classes = []
    for chave, c in WATER_QUALITY_CLASSES.items():
        nome, descricao = CLASSES_DE_QUALIDADE_PT.get(chave, (c.nome, c.descricao))
        classes.append({
            "chave": chave, "nome": nome, "descricao": descricao,
            "normativa": chave == "classe_1",
            "turbidez": _r(c.turbidez_max_ntu, 1), "cor": _r(c.cor_aparente_max_uh, 1),
            "ph": [_r(c.ph_min, 1), _r(c.ph_max, 1)],
            "cloro": [_r(c.cloro_residual_min_mg_l, 2), _r(c.cloro_residual_max_mg_l, 2)],
            "coliformes": _r(c.coliformes_termo_max_ufc_100ml, 1),
            "desinfeccao": bool(c.exige_desinfeccao),
            "filtracao": bool(c.exige_filtracao_fina)})
    return {"classes": classes, "padrao": "classe_1",
            "parametros": [
                {"chave": "turbidez", "nome": "Turvação", "unidade": "NTU", "casas": 1,
                 "texto": "Mede a água turva. Serve de indicador da eficiência da desinfeção: partícula em suspensão abriga microrganismos e consome cloro."},
                {"chave": "cor", "nome": "Cor aparente", "unidade": "uH", "casas": 1,
                 "texto": "Parâmetro de aceitação do utilizador; nas classes do programa é acréscimo de projeto."},
                {"chave": "coliformes", "nome": "Coliformes termotolerantes", "unidade": "UFC/100 mL", "casas": 0,
                 "texto": "Indicador de contaminação fecal. Muitas referências falam em Escherichia coli, subconjunto destes organismos, de modo que o limite aqui é mais restritivo."}]}


# ── o valor atual líquido contra o volume ─────────────────────────────────────

def vpl_por_volume():
    """A curva de VAL da varredura, por material, com o máximo marcado."""
    from triton.core.economic import run_economic_analysis
    serie = _serie()
    volumes = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000]
    casos = {}
    for chave, _ in MATERIAIS:
        linha = []
        for v in volumes:
            if v == 0:
                linha.append([0.0, None, 0.0])
                continue
            r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **_config_projeto())
            e = run_economic_analysis(_config_economica(v, chave), r)
            linha.append([_r(e.vpl), _r(e.payback_years, 1) if e.payback_years else None,
                          _r(r.potential_potable_savings_pct, 2)])
        casos[chave] = linha
    return {"volumes": volumes, "materiais": MATERIAIS, "casos": casos,
            "padrao": "CONCRETO", "anos": 20}


def dados():
    etapas = [("fig01_dez_dias.png", dez_dias),
              ("fig48_programa_serie_diaria.png", serie_diaria),
              ("fig47_permanencia.png", permanencia),
              ("fig05_regimes.png", regimes),
              ("fig08_fluxo_de_caixa.png", fluxo_de_caixa),
              ("fig06_carbono_no_tempo.png", carbono),
              ("fig03_cidades.png", cidades),
              ("fig51_programa_topsis.png", multicriterio),
              ("fig23_smaa.png", smaa),
              ("fig16_indices.png", indices_pluviometricos),
              ("fig21_investimento.png", investimento),
              ("fig07_fatura.png", fatura),
              ("fig24_tornado.png", sensibilidade),
              ("fig35_escoamento.png", captacao),
              ("fig00k_energia.png", pressurizadores),
              ("fig36_classes.png", classes_de_qualidade),
              ("fig49_programa_vpl.png", vpl_por_volume)]
    saida = {}
    for nome, f in etapas:
        print(f"  figura interativa: {nome}")
        saida[nome] = f()
    return saida


if __name__ == "__main__":
    import json
    import time
    t = time.time()
    d = dados()
    print(len(json.dumps(d)) // 1024, "KB em", round(time.time() - t), "s")
