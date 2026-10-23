# -*- coding: utf-8 -*-
"""Os números do manual sobre o CAPEX automático e o OPEX inserido sozinho vêm do programa.

A seção 10 do manual da Brasil e da Portugal descreve o que o programa preenche num projeto novo.
Cada número impresso nas tabelas geradas (`manual/partes/_tabelas/cap10_capex_*.md`, `cap10_opex_*.md`
e, na Portugal, `cap10_custos_*.md`) é lido aqui de volta do código e dos dados, de modo independente
do gerador. Uma segunda parte **congela** as constantes que o código traz fora do registro de fontes
(0,45 kWh/m³, R$ 0,05/m³, 30% de mão de obra, 8% de acessórios): a Brasil não pode mudar de
comportamento sem que alguém decida e atualize o manual.

O arquivo é IDÊNTICO nas três edições. BRL e PRT rodam o próprio conjunto; a INT salta (o manual
inglês dela ainda não trata do assunto).
"""

from __future__ import annotations

import json
import os
import re
import sys

import pytest

from triton.core.edition import get_current_edition

EDICAO = get_current_edition()

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")
TABELAS = os.path.join(MANUAL, "partes", "_tabelas")
NBSP = chr(160)

if EDICAO == "INT":
    pytest.skip("o manual inglês da INT ainda não tem esta seção", allow_module_level=True)


def _ler(nome):
    caminho = os.path.join(TABELAS, nome)
    if not os.path.exists(caminho):
        pytest.skip(f"{nome} ainda não gerada")
    return open(caminho, encoding="utf-8").read()


def _numeros(celula):
    """Os números de uma célula, no padrão do manual (milhar com espaço inseparável ou ponto, vírgula decimal)."""
    texto = celula.replace(NBSP, "").replace(" ", "").replace("−", "-")
    achados = re.findall(r"-?\d{1,3}(?:\.\d{3})+(?:,\d+)?|-?\d+(?:,\d+)?", texto)
    return [float(a.replace(".", "").replace(",", ".")) if re.search(r"\.\d{3}(?:,|$)", a) else float(a.replace(",", "."))
            for a in achados]


def _linhas(texto):
    """As linhas de dados das tabelas do arquivo, como listas de células."""
    saida = []
    for linha in texto.split("\n"):
        if linha.startswith("|") and not re.match(r"^\|[\s:\-|]+\|$", linha):
            saida.append([c.strip() for c in linha.strip().strip("|").split("|")])
    return saida


def _celula_com(linhas, rotulo):
    achadas = [l for l in linhas if l[0].startswith(rotulo)]
    assert achadas, f"linha «{rotulo}» ausente"
    return achadas[0]


def _capitulo10():
    caminho = os.path.join(MANUAL, "partes", "10_quanto_custa.md")
    saida = []
    for linha in open(caminho, encoding="utf-8").read().split("\n"):
        m = re.match(r"^<!--\s*inclui:\s*(\S+)\s*-->\s*$", linha)
        alvo = os.path.join(MANUAL, "partes", m.group(1)) if m else None
        saida.append(open(alvo, encoding="utf-8").read() if alvo and os.path.exists(alvo) else linha)
    return "\n".join(saida)


def _brl(v, casas=2):
    """Dinheiro como o texto corrido do capítulo o imprime: R$ 16.131,96."""
    return "R$ " + f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _eur(v):
    return f"{v:,.2f}".replace(",", NBSP).replace(".", ",") + NBSP + "€"


# ═══════════════════════════════ BRASIL ═══════════════════════════════

brl = pytest.mark.skipif(EDICAO != "BRL", reason="conjunto da Edição Brasil")


@pytest.fixture(scope="module")
def ce():
    from triton.core import cost_estimates
    return cost_estimates


@pytest.fixture(scope="module")
def gerador():
    sys.path.insert(0, MANUAL)
    try:
        import gerar_tabelas
    except ModuleNotFoundError:
        pytest.skip("geradores do manual não versionados (ficam no disco do mantenedor)")
    return gerar_tabelas


# ── o que está congelado ──

@brl
def test_as_constantes_fora_do_registro_de_fontes_estao_congeladas(ce):
    """Se um destes valores mudar, o comportamento da Brasil mudou: decida, atualize o manual e este teste."""
    assert ce.LABOR_PCT == 0.30
    assert ce.ACCESSORIES_PCT == 0.08
    assert ce.PIPING_PCT == 0.18
    assert ce.MAO_DE_OBRA_MINIMA == 1400.0
    assert ce.DEFAULT_CHLORINE_COST_PER_KG == 25.0
    assert ce.R2_MINIMO_PARA_EXTRAPOLAR == 0.90
    cal = ce.estimate_calibrated_capex_opex(typology="UTI", volume_l=5000.0, uf="SP", energy_tariff_kwh=1.0)
    assert cal["opex_energy_per_m3_brl"] == pytest.approx(0.45)        # kWh/m³ x R$ 1,00/kWh
    assert cal["opex_chlorine_per_m3_brl"] == pytest.approx(0.05)      # R$/m³, fixo no código
    assert cal["volume_sup_l"] == pytest.approx(0.10 * 5000.0)
    assert ce.compute_pipe_item_cost(32, 1.0) == pytest.approx(1.25 * ce.PIPE_COST_PER_METER[32], abs=0.01)
    pisos = ce.estimate_preliminary_capex(100.0, 0.0, False)
    assert (pisos["piping"], pisos["accessories"], pisos["labor"]) == (950.0, 500.0, 1400.0)
    assert ce.PUMP_PARAMS == {"base_cost": 300.0, "base_power_kw": 0.36775, "power_exponent": 0.7, "min_cost": 280.0}


@brl
def test_a_tabela_de_precos_de_reservatorio_esta_congelada(ce):
    assert ce.LOWER_TANK_PRICE_TABLE == [
        (310.0, 246.9), (500.0, 269.9), (750.0, 459.9), (1000.0, 459.9), (2000.0, 1139.9),
        (3000.0, 2051.9), (5000.0, 2999.9), (10000.0, 5499.9), (15000.0, 6935.0)]
    assert ce.MATERIAL_COST_MULTIPLIERS == {"PEAD": 1.0, "PRFV": 1.35, "FIBRA": 1.35, "CONCRETO": 2.1, "ACO_INOX": 3.6}


@brl
def test_a_incoerencia_de_datas_do_json_de_custos_esta_registrada(ce):
    """`updated_at` (2026-08) é anterior a `coletado_em` (2026-09-09), e o manual diz isso.

    Se alguém corrigir a data, este teste cai: atualize o manual (seção «De onde vêm os números»).
    """
    db = ce.load_costs_database()
    atualizado = db["_metadata"]["updated_at"]
    coletado = db["_procedencia_precos_reservatorio"]["coletado_em"]
    incoerente = atualizado < coletado[:len(atualizado)]
    texto = _capitulo10()
    assert ("antes da coleta" in texto) == incoerente


@brl
def test_o_fator_regional_nao_altera_as_parcelas_do_projeto(ce):
    """A seção 10 diz: o fator multiplica só o total do estimador, que nenhuma tela usa."""
    a = ce.estimate_preliminary_capex(4000.0, 1000.0, True, 0.37, 2, uf="RR")
    b = ce.estimate_preliminary_capex(4000.0, 1000.0, True, 0.37, 2, uf="SP")
    for parcela in ("lower", "upper", "pump", "piping", "accessories", "labor"):
        assert a[parcela] == b[parcela], parcela
    assert a["total"] != b["total"]


@brl
def test_a_tipologia_nao_e_lida_pela_configuracao_do_projeto():
    """A seção 10 diz: nem a interface nem a CLI orçam por tipologia (o projeto não tem `building_typology`)."""
    from triton.core.parser import TritonConfig
    assert not hasattr(TritonConfig(), "building_typology")


# ── tabelas ──

@brl
def test_cadeia_do_capex(ce):
    from triton.core.parser import TritonConfig
    from triton.core.quantitativo_do_arranjo import CATALOGO_DE_PECAS
    linhas = _linhas(_ler("cap10_capex_cadeia.md"))
    cfg = TritonConfig()
    assert _numeros(_celula_com(linhas, "cisterna")[3])[0] == len(ce.LOWER_TANK_PRICE_TABLE)
    assert _numeros(_celula_com(linhas, "motobombas")[3]) == [cfg.pump_unit_cost, cfg.pump_count]
    assert _numeros(_celula_com(linhas, "acessórios")[3])[0] == len(CATALOGO_DE_PECAS)
    assert _numeros(_celula_com(linhas, "mão de obra")[3]) == [ce.LABOR_PCT * 100, ce.MAO_DE_OBRA_MINIMA]
    assert _numeros(_celula_com(linhas, "fator regional")[3]) == [
        len(ce.REGIONAL_FACTORS_BY_UF), min(ce.REGIONAL_FACTORS_BY_UF.values()), max(ce.REGIONAL_FACTORS_BY_UF.values())]


@brl
def test_precos_de_reservatorio_por_material(ce):
    with open(ce.COSTS_FILE_PATH, encoding="utf-8") as f:
        bruto = json.load(f)
    tabela = {float(v): float(p) for v, p in bruto["lower_tank_pead_prices"]}
    fatores = bruto["material_multipliers"]
    linhas = _linhas(_ler("cap10_capex_reservatorios.md"))
    cabecalho, fator, *dados = linhas
    assert _numeros(fator[1])[0] == fatores["PEAD"]
    assert [_numeros(c)[0] for c in fator[2:5]] == [fatores["FIBRA"], fatores["CONCRETO"], fatores["ACO_INOX"]]
    for l in dados:
        volume = _numeros(l[0])[0]
        if volume in tabela:
            base = tabela[volume]
        else:  # interpolação linear entre os vizinhos
            vs = sorted(tabela)
            a = max(v for v in vs if v < volume)
            b = min(v for v in vs if v > volume)
            base = tabela[a] + (tabela[b] - tabela[a]) * (volume - a) / (b - a)
        esperado = [base * fatores[m] for m in ("PEAD", "FIBRA", "CONCRETO", "ACO_INOX")]
        assert [_numeros(c)[0] for c in l[1:5]] == pytest.approx(esperado, abs=0.006)


@brl
def test_precos_de_tubo(ce):
    with open(ce.COSTS_FILE_PATH, encoding="utf-8") as f:
        precos = json.load(f)["pipes_cost_per_meter"]
    for l in _linhas(_ler("cap10_capex_tubos.md"))[1:]:
        dn = str(int(_numeros(l[0])[0]))
        assert _numeros(l[3])[0] == pytest.approx(precos[dn], abs=0.006)
        assert _numeros(l[4])[0] == pytest.approx(round(precos[dn] * 1.25, 2), abs=0.011)


@brl
def test_precos_das_pecas():
    from triton.core.quantitativo_do_arranjo import CABO, CATALOGO_DE_PECAS, CONEXAO, CURVA, TE
    esperado = {p.nome: p.preco_brl for p in CATALOGO_DE_PECAS.values()}
    esperado.update({p.nome: p.preco_brl for p in (CURVA, CONEXAO, TE, CABO)})
    linhas = [l for l in _linhas(_ler("cap10_capex_pecas.md"))[1:] if l[0] in esperado]
    assert len(linhas) == len(esperado)
    for l in linhas:
        assert _numeros(l[1])[0] == esperado[l[0]], l[0]


@brl
def test_precos_das_motobombas(ce):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from triton.ui.dialogs.pump_wizard_dialog import PUMP_CATALOG
    linhas = _linhas(_ler("cap10_capex_bombas.md"))[1:9]
    assert len(linhas) == len(PUMP_CATALOG)
    for l, m in zip(linhas, PUMP_CATALOG):
        assert _numeros(l[1])[-1] == m["kw"]
        assert _numeros(l[4])[0] == m["cost"]
        formula = max(280.0, 300.0 * (m["kw"] / 0.36775) ** 0.7)
        assert _numeros(l[5])[0] == pytest.approx(formula, abs=0.006)


@brl
def test_precos_da_etap():
    from triton.core.water_quality import size_etap, size_first_flush_system
    texto = _ler("cap10_capex_etap.md")
    for area in (150.0, 300.0, 600.0):
        assert _eur_brl(size_etap(roof_area_m2=area).pre_filter_capex) in texto
    assert _eur_brl(size_etap().disinfection_capex) in texto
    ff = size_first_flush_system(discard_mm=2.0, roof_area_m2=150.0)
    assert _eur_brl(ff.first_flush_total_capex) in texto
    assert _eur_brl(ff.first_flush_annual_opex) in texto


def _eur_brl(v):
    return "R$ " + f"{v:,.2f}".replace(",", NBSP).replace(".", ",")


@brl
def test_tipologias_e_fatores_regionais(ce):
    texto = _ler("cap10_capex_tipologias.md")
    for cod, c in ce.TYPOLOGY_COST_CONFIGS.items():
        l = _celula_com(_linhas(texto), cod + ":")
        assert _numeros(l[2])[0] == c["electrical_panel_cost"]
        assert _numeros(l[6])[0] == c["pipes_base_cost"]
        assert _numeros(l[8])[0] == c["min_labor_cost"]
        r = ce.estimate_calibrated_capex_opex(typology=cod, volume_l=5000.0, uf="SP")
        orc = [x for x in _linhas(texto) if x[0] == cod][0]
        assert _numeros(orc[7])[0] == pytest.approx(round(r["capex_total_brl"]), abs=1.0)
    fatores = {}
    linhas = _linhas(_ler("cap10_capex_regional.md"))[1:]
    for l in linhas:
        for i in range(0, 6, 2):
            if l[i]:
                fatores[l[i]] = _numeros(l[i + 1])[0]
    assert fatores == pytest.approx({k: round(v, 2) for k, v in ce.REGIONAL_FACTORS_BY_UF.items()})


@brl
def test_procedencia_registrada(ce):
    db = ce.load_costs_database()
    texto = _ler("cap10_capex_procedencia.md")
    proc = db["_procedencia_precos_reservatorio"]
    d, m, a = proc["coletado_em"].split("-")[::-1][0], proc["coletado_em"].split("-")[1], proc["coletado_em"].split("-")[0]
    assert f"{d}/{m}/{a}" in texto
    assert proc["fabricante"] in texto and "Copafer" in texto
    mes, ano = db["_metadata"]["updated_at"].split("-")[1], db["_metadata"]["updated_at"].split("-")[0]
    assert f"{mes}/{ano}" in texto


@brl
def test_constantes_sem_fonte_impressas(ce):
    linhas = _linhas(_ler("cap10_capex_constantes.md"))
    assert _numeros(_celula_com(linhas, "consumo específico")[1])[0] == 0.45
    assert _numeros(_celula_com(linhas, "custo de cloração")[1])[0] == 0.05
    assert _numeros(_celula_com(linhas, "mão de obra")[1])[0] == 30
    assert _numeros(_celula_com(linhas, "acessórios sem arranjo")[1])[0] == 8


@brl
def test_opex_de_partida():
    from triton.core.chlorination import Cloracao
    from triton.core.edition import projeto_novo_da_edicao
    cfg = projeto_novo_da_edicao()
    texto = _ler("cap10_opex_itens.md")
    for nome, meses, fixo, _ in cfg.op_costs:
        l = _celula_com(_linhas(texto), nome)
        assert _numeros(l[1])[0] == fixo and _numeros(l[2])[0] == meses
    cl = Cloracao(dose_mg_por_litro=cfg.chlorine_dose_mg_l, pureza=cfg.chlorine_product_purity)
    l = _celula_com(_linhas(texto), "cloração")
    assert _numeros(l[1])[:3] == [cfg.chlorine_dose_mg_l, cfg.chlorine_product_purity * 100, cfg.chlorine_cost_per_kg]
    assert _numeros(l[1])[3] == pytest.approx(cl.produto_kg_por_m3, abs=5e-6)
    assert _numeros(_celula_com(_linhas(texto), "energia")[1])[0] == pytest.approx(cfg.elec_tariff, abs=5e-5)


@brl
def test_tarifa_de_energia_da_base():
    import statistics
    caminho = os.path.join(RAIZ, "triton", "data", "brazil_cities_tariffs.json")
    cidades = json.load(open(caminho, encoding="utf-8"))["cities"].values()
    valores = [c["energia_r_kwh"] for c in cidades if c.get("energia_r_kwh", 0) > 0]
    linhas = _linhas(_ler("cap10_opex_energia.md"))
    assert _numeros(_celula_com(linhas, "municípios com tarifa")[1])[0] == len(valores)
    assert _numeros(_celula_com(linhas, "menor tarifa")[1])[0] == pytest.approx(min(valores), abs=5e-5)
    assert _numeros(_celula_com(linhas, "mediana")[1])[0] == pytest.approx(statistics.median(valores), abs=5e-5)
    assert _numeros(_celula_com(linhas, "maior tarifa")[1])[0] == pytest.approx(max(valores), abs=5e-5)
    assert _numeros(_celula_com(linhas, "municípios cuja")[1])[0] == sum(
        1 for c in cidades if c.get("status_energia") == "EXPIRED_ANEEL_REF")


@brl
def test_bandeiras_vem_do_motor(gerador):
    """Os acréscimos impressos são os que o motor aplica: diferença de custeio dividida pela energia."""
    from triton.core.economic import run_economic_analysis
    from triton.core.pump_energy import compute_annual_pump_energy
    from triton.core.simulation import run_single_simulation
    g = gerador
    r = run_single_simulation(precip_data=g._serie(), lower_tank_vol=g.VOLUME, **g._config_projeto())
    linhas = _linhas(_ler("cap10_opex_energia.md"))
    base = {}
    for chave, rotulo in (("verde", "verde"), ("amarela", "amarela"), ("vermelha_1", "vermelha, patamar 1"),
                          ("vermelha_2", "vermelha, patamar 2")):
        cfg = g._config_economica(g.VOLUME, "CONCRETO")
        cfg.tariff_flag = chave
        base[chave] = (run_economic_analysis(cfg, r).annual_opex_brl, compute_annual_pump_energy(cfg, r).annual_kwh)
    for chave, rotulo in (("amarela", "amarela"), ("vermelha_1", "vermelha, patamar 1"), ("vermelha_2", "vermelha, patamar 2")):
        esperado = (base[chave][0] - base["verde"][0]) / base[chave][1]
        assert _numeros(_celula_com(linhas, rotulo)[1])[0] == pytest.approx(esperado, abs=5e-6)


@brl
def test_premissas_de_partida():
    from triton.core.edition import projeto_novo_da_edicao
    novo = projeto_novo_da_edicao()
    linhas = _linhas(_ler("cap10_opex_premissas.md"))
    assert _numeros(_celula_com(linhas, "taxa mínima de atratividade")[1])[0] == novo.tma
    assert _numeros(_celula_com(linhas, "inflação dos custos")[1])[0] == novo.inflation
    assert _numeros(_celula_com(linhas, "reajuste da tarifa de água")[1])[0] == novo.water_tariff_escalation
    assert _numeros(_celula_com(linhas, "período de análise")[1])[0] == novo.analysis_period_years


@brl
def test_numeros_do_texto_corrido_e_do_exemplo(gerador):
    """R$ 740,00, R$ 48,82, R$ 16.131,96, R$ 14.061,19 e 16,3 contra 9,2 anos: impressos no capítulo 10."""
    from triton.core.economic import run_economic_analysis
    from triton.core.quantitativo_do_arranjo import sincronizar_com_o_arranjo
    from triton.core.simulation import run_single_simulation
    g = gerador
    r = run_single_simulation(precip_data=g._serie(), lower_tank_vol=g.VOLUME, **g._config_projeto())
    digitado = g._config_economica(g.VOLUME, "CONCRETO")
    sem_rotinas = g._config_economica(g.VOLUME, "CONCRETO")
    sem_rotinas.op_costs = []
    auto = g._config_economica(g.VOLUME, "CONCRETO")
    auto.capex_do_arranjo = auto.mao_de_obra_automatica = True
    auto.cost_piping = auto.cost_accessories = auto.cost_labor = 0.0
    auto.econ_lower_tank_vol = g.VOLUME
    sincronizar_com_o_arranjo(auto)
    e_dig, e_sem, e_auto = (run_economic_analysis(c, r) for c in (digitado, sem_rotinas, auto))
    texto = _capitulo10()
    rotinas = sum(fixo * 12.0 / meses for _, meses, fixo, _ in digitado.op_costs)
    assert _brl(rotinas) in texto
    assert _brl(e_dig.annual_opex_brl) in texto
    assert _brl(e_dig.capex_total) in texto
    assert _brl(e_auto.capex_total) in texto
    assert e_sem.annual_opex_brl == pytest.approx(e_dig.annual_opex_brl)   # o resumo não inclui as rotinas
    peso = _ler("cap10_opex_peso.md")
    assert _numeros(_celula_com(_linhas(peso), "payback")[1])[0] == pytest.approx(e_dig.payback_years, abs=0.05)
    assert _numeros(_celula_com(_linhas(peso), "payback")[2])[0] == pytest.approx(e_sem.payback_years, abs=0.05)
    assert _numeros(_celula_com(_linhas(peso), "valor presente")[2])[0] == pytest.approx(e_sem.vpl, abs=0.006)
    exemplo = _linhas(_ler("cap10_capex_exemplo.md"))
    assert _numeros(_celula_com(exemplo, "**investimento total**")[2])[0] == pytest.approx(e_auto.capex_total, abs=0.006)


# ═══════════════════════════════ PORTUGAL ═══════════════════════════════

prt = pytest.mark.skipif(EDICAO != "PRT", reason="conjunto da Edição Portugal")


@pytest.fixture(scope="module")
def gerador_prt():
    sys.path.insert(0, MANUAL)
    try:
        import gerar_tabelas
    except ModuleNotFoundError:
        pytest.skip("geradores do manual não versionados (ficam no disco do mantenedor)")
    return gerar_tabelas


@prt
def test_prt_os_custos_do_projeto_novo_estao_a_zero():
    """O texto da seção 10 afirma: preço de obra, de equipamento, de cloro e de eletricidade partem de zero."""
    from triton.core.edition import projeto_novo_da_edicao
    cfg = projeto_novo_da_edicao()
    for campo in ("cost_lower_tank", "cost_upper_tank", "cost_piping", "cost_accessories", "cost_labor",
                  "pump_unit_cost", "elec_tariff", "chlorine_cost_per_kg"):
        assert getattr(cfg, campo) == 0.0, campo
    assert all(fixo == 0.0 and var == 0.0 for _, _, fixo, var in cfg.op_costs)
    assert not cfg.capex_do_arranjo and not cfg.mao_de_obra_automatica and not cfg.precos_de_catalogo
    assert cfg.tariff_city_name == "Lisboa"


@prt
def test_prt_a_tabela_do_estado_do_projeto_novo():
    from triton.core.edition import projeto_novo_da_edicao
    cfg = projeto_novo_da_edicao()
    linhas = _linhas(_ler("cap10_custos_estado.md"))
    assert _numeros(_celula_com(linhas, "preço de cada eletrobomba")[1])[0] == 0.0
    assert "projeto parte de %d eletrobombas" % cfg.pump_count in _celula_com(linhas, "preço de cada eletrobomba")[2]
    assert _numeros(_celula_com(linhas, "tarifa de eletricidade")[1])[0] == cfg.elec_tariff
    assert _celula_com(linhas, "tarifário de água")[1].startswith(f"{cfg.tariff_city_name}, desde {cfg.tariff_vigencia}")
    assert _numeros(_celula_com(linhas, "taxa de atualização")[1])[0] == cfg.tma
    assert _numeros(_celula_com(linhas, "inflação dos custos")[1])[0] == cfg.inflation
    assert _numeros(_celula_com(linhas, "rotinas de manutenção")[1])[0] == len(cfg.op_costs)
    with open(os.path.join(RAIZ, "triton", "data", "costs_database.json"), encoding="utf-8") as f:
        base = json.load(f)
    assert _numeros(_celula_com(linhas, "base de custos interna")[1])[0] == len(base["regional_factors_by_uf"])
    assert base["_metadata"]["currency"] == "BRL"   # o texto diz «em reais, de origem brasileira»


@prt
def test_prt_parametros_ilustrativos_do_tutorial(gerador_prt):
    g = gerador_prt
    linhas = _linhas(_ler("cap10_custos_ilustrativos.md"))
    assert _numeros(_celula_com(linhas, "mão de obra")[1])[0] == g.CUSTOS_TUTORIAL["cost_labor"]
    assert _numeros(_celula_com(linhas, "eletrobomba, por unidade")[1])[0] == g.CUSTOS_TUTORIAL["pump_unit_cost"]
    assert _numeros(_celula_com(linhas, "tarifa de eletricidade")[1])[0] == g.CUSTOS_TUTORIAL["elec_tariff"]
    for nome, meses, fixo, _ in g.MANUTENCAO_TUTORIAL:
        l = _celula_com(linhas, "rotina: " + nome[0].lower() + nome[1:])
        assert _numeros(l[1]) == [fixo, meses]


@prt
def test_prt_o_peso_das_rotinas_e_o_texto_corrido(gerador_prt):
    from triton.core.economic import run_economic_analysis
    from triton.core.simulation import run_single_simulation
    g = gerador_prt
    r = run_single_simulation(precip_data=g._serie(), lower_tank_vol=g.VOLUME, **g._config_projeto())
    com, sem = g._config_economica(g.VOLUME, "CONCRETO"), g._config_economica(g.VOLUME, "CONCRETO")
    sem.op_costs = []
    ec, es = run_economic_analysis(com, r), run_economic_analysis(sem, r)
    linhas = _linhas(_ler("cap10_custos_peso.md"))
    assert _numeros(_celula_com(linhas, "valor atual")[1])[0] == pytest.approx(ec.vpl, abs=0.006)
    assert _numeros(_celula_com(linhas, "valor atual")[2])[0] == pytest.approx(es.vpl, abs=0.006)
    por_ano = sum(fixo * 12.0 / meses for _, meses, fixo, _ in com.op_costs)
    assert f"{por_ano:,.2f}".replace(",", " ").replace(".", ",") in _capitulo10().replace(NBSP, " ")
    assert es.annual_opex_brl == pytest.approx(ec.annual_opex_brl)


@prt
def test_prt_series_publicas_do_registo():
    pasta = os.path.join(RAIZ, "..", "..", "validacao_precipitacao_prt", "dados_automaticos")
    if not os.path.isdir(pasta):
        pytest.skip("pasta das séries públicas ausente nesta máquina")
    linhas = _linhas(_ler("cap10_custos_series_publicas.md"))
    d = json.load(open(os.path.join(pasta, "eurostat_eletricidade_domestica.json"), encoding="utf-8"))
    ult = sorted(d["resumo"]["PT"])[-1]
    l = _celula_com(linhas, "eletricidade doméstica, com impostos")
    assert _numeros(l[1])[0] == d["resumo"]["PT"][ult]
    assert _numeros(l[2])[0] == d["resumo"]["ES"][ult]
    assert d["sha256"][:12] in l[4]


@prt
def test_prt_o_texto_nao_promete_o_que_nao_existe():
    """O texto declara «não implementado» o que é só plano, e não traz preço europeu inventado."""
    texto = _capitulo10()
    assert "Nada disto existe no programa" in texto
    assert "Não está implementado" in texto
    assert "R$" not in texto
