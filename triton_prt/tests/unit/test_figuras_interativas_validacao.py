"""Cada painel interativo do site é conferido contra o próprio programa.

O site não calcula nada: mostra células de grades que `gerar_figuras_interativas.py`
produziu rodando o motor. Estes testes refazem a conta pelo caminho normal do
programa e comparam com o que o site vai mostrar. A única exceção é o TOPSIS,
que a página recalcula em JavaScript porque os pesos são do leitor; esse é
conferido rodando o próprio JavaScript do site contra o módulo do programa.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np
import pytest

pytest.importorskip("matplotlib", reason="as figuras do manual são desenhadas com matplotlib")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")
for caminho in (RAIZ, MANUAL):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

import gerar_figuras_interativas as gi  # noqa: E402
from gerar_tabelas import (  # noqa: E402
    TARIFA_CASAN, TUTORIAL, _config_economica, _config_projeto, _config_tutorial, _serie,
)
from triton.core.simulation import run_single_simulation  # noqa: E402

APROX = dict(rel=1e-6, abs=0.51)   # os dados do site vão arredondados


@pytest.fixture(scope="module")
def serie():
    return _serie()


def test_dez_dias_refaz_a_simulacao():
    d = gi.dez_dias()
    for capacidade, descarte in ((1000, 0.0), (2000, 2.0), (3000, 3.0)):
        r = run_single_simulation(
            precip_data=np.array(gi.CHUVA_23, dtype=float), lower_tank_vol=float(capacidade),
            area=d["area"], runoff_coeff=d["coef"], discard_mm=descarte, discard_mode=1,
            total_demand_per_day=d["demanda"], rainwater_share=d["fracao"],
            store_daily_details=True)
        guardado = d["casos"][f"{capacidade}|{descarte:g}"]
        for dia, x in zip(guardado, r.daily_results):
            assert dia[0] == pytest.approx(x.eff_precip_mm, abs=0.051)
            assert dia[1] == pytest.approx(x.harvested_liters, **APROX)
            assert dia[5] == pytest.approx(x.spilled_liters, **APROX)
            assert dia[6] == pytest.approx(x.lower_tank_end_liters, **APROX)
            assert dia[7] == x.satisfaction_type


def test_o_nivel_diario_e_o_do_programa(serie):
    d = gi.serie_diaria()
    for volume in (2000, 8000):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume),
                                  store_daily_details=True, **_config_tutorial())
        niveis = d["niveis"][str(volume)]
        assert len(niveis) == len(r.daily_results)
        for guardado, x in zip(niveis, r.daily_results):
            assert guardado == pytest.approx(x.lower_tank_end_liters, **APROX)


def test_a_permanencia_e_o_potencial_do_programa(serie):
    d = gi.permanencia()
    for volume in (1000, 4000, 20000):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume),
                                  store_daily_details=True, **_config_tutorial())
        demanda = r.daily_results[0].pluvial_demand_liters
        autonomia = np.array([x.lower_tank_end_liters / demanda for x in r.daily_results])
        curva = d["curvas"][str(volume)]
        for i, p in enumerate(d["pontos"]):
            assert curva[i] == pytest.approx(np.percentile(autonomia, 100 - p), abs=0.011)
        estado = d["estados"][str(volume)]
        assert estado[0] == pytest.approx(r.avg_pluvial_consumed_l_day * 365.25 / volume, abs=0.051)
        assert estado[4] == pytest.approx(r.potential_potable_savings_pct, abs=0.005)


def test_a_curva_das_cidades_e_a_do_programa():
    from triton.core.parser import load_precipitation
    d = gi.cidades()
    cidade = d["cidades"][0]
    caminho = os.path.join(RAIZ, "data", "rainfall", f"{cidade['chave']}.csv")
    serie_cidade = load_precipitation(caminho)[: 30 * 365]
    for k in (2, 4, 20):
        r = run_single_simulation(precip_data=serie_cidade,
                                  lower_tank_vol=float(d["volumes"][k]), **_config_tutorial())
        assert cidade["potencial"][k] == pytest.approx(r.potential_potable_savings_pct, abs=0.005)


def test_as_tres_tarifas_batem_com_a_funcao_da_fatura():
    from triton.core.economic import calculate_water_bill
    d = gi.regimes()
    tarifas = {
        "disp": [(0.0, 0.0, 46.34, -1), (0.0, 10.0, 3.08, 1), (10.0, 25.0, 14.31, 1),
                 (25.0, 50.0, 19.14, 1), (50.0, 999999.0, 24.08, 1)],
        "franq": [(0.0, 0.0, 52.89, -1), (0.0, 10.0, 0.0, 1), (10.0, 15.0, 9.815, 1),
                  (15.0, 20.0, 10.917, 1), (20.0, 999999.0, 12.8, 1)],
        "sem": [(0.0, 10.0, 5.29, 1), (10.0, 15.0, 9.815, 1), (15.0, 20.0, 10.917, 1),
                (20.0, 999999.0, 12.8, 1)],
    }
    for curva in d["curvas"]:
        for i in (0, 20, 40, 73, 120):
            esperado = calculate_water_bill(d["consumos"][i] * 1000.0, tarifas[curva["chave"]],
                                            1, 0.0, 0.0, 0.0)
            assert curva["fatura"][i] == pytest.approx(esperado, abs=0.011)


def test_a_fatura_aberta_soma_o_que_a_funcao_do_programa_cobra():
    from triton.core.economic import calculate_water_bill
    d = gi.fatura()
    for i in (0, 12, 40, 73, 100):
        consumo = d["consumos"][i]
        agua = sum(d["parcelas"][i][:-1])
        assert agua == pytest.approx(
            calculate_water_bill(consumo * 1000.0, TARIFA_CASAN, 1, 0.0, 0.0, 0.0), abs=0.011)
        # Com esgoto a 100%, a parcela de esgoto iguala a de água.
        assert sum(d["parcelas"][i]) == pytest.approx(
            calculate_water_bill(consumo * 1000.0, TARIFA_CASAN, 1, 100.0, 0.0, 0.0), abs=0.011)


def test_o_fluxo_de_caixa_e_o_da_analise_economica(serie):
    from triton.core.economic import run_economic_analysis
    d = gi.fluxo_de_caixa()
    for volume, material in ((2000, "CONCRETO"), (4000, "PEAD"), (12000, "ACO_INOX")):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume), **_config_projeto())
        e = run_economic_analysis(_config_economica(volume, material), r)
        caso = d["casos"][f"{volume}|{material}"]
        assert caso["capex"] == pytest.approx(e.capex_total, **APROX)
        assert caso["vpl"] == pytest.approx(e.vpl, **APROX)
        assert caso["potencial"] == pytest.approx(r.potential_potable_savings_pct, abs=0.005)
        if e.payback_years is None:
            assert caso["retorno"] is None
        else:
            assert caso["retorno"] == pytest.approx(e.payback_years, abs=0.051)
        assert caso["acumulado"][-1] == pytest.approx(e.vpl, **APROX)


def test_o_carbono_e_o_da_avaliacao_de_ciclo_de_vida(serie):
    from triton.core.environmental import calculate_lca
    from gerar_tabelas import _config_ambiental
    d = gi.carbono()
    for volume, material in ((2000, "PEAD"), (4000, "CONCRETO"), (20000, "FIBRA")):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume), **_config_projeto())
        cfg = _config_ambiental(r)
        cfg.lower_material_key = material
        lca = calculate_lca(float(volume), r.annual_pluvial_consumed_m3, cfg)
        caso = d["casos"][f"{volume}|{material}"]
        assert caso[0] == pytest.approx(lca.total_embodied_co2_kg, abs=0.051)
        assert caso[1] == pytest.approx(lca.net_annual_avoided_co2_kg, abs=0.0006)
        assert caso[2] == pytest.approx(lca.lower_tank_mass_kg, **APROX)


def test_o_investimento_fecha_com_o_capex_da_analise(serie):
    from triton.core.economic import run_economic_analysis
    d = gi.investimento()
    assert d["fecha_com_o_capex"]
    for volume, material in ((1000, "PEAD"), (4000, "CONCRETO"), (20000, "FIBRA")):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume), **_config_projeto())
        e = run_economic_analysis(_config_economica(volume, material), r)
        assert sum(d["casos"][f"{volume}|{material}"]) == pytest.approx(e.capex_total, abs=1.01)


def test_os_indices_sao_os_do_calculador_do_programa():
    import pandas as pd
    from datetime import timedelta
    from triton.core.calculator import IndicesCalculator
    from triton.core.parser import load_precipitation
    d = gi.indices_pluviometricos()
    cidade = d["cidades"][0]
    serie_cidade = load_precipitation(
        os.path.join(RAIZ, "data", "rainfall", f"{cidade['chave']}.csv"))[: 30 * 365]
    datas = [gi.INICIO + timedelta(days=i) for i in range(len(serie_cidade))]
    tabela = IndicesCalculator(
        pd.DataFrame({"date": datas, "precipitation": [float(x) for x in serie_cidade]}),
        exclude_incomplete=False).compute_climate_indices()
    for chave, _, _, casas, _ in gi.INDICES:
        guardado = cidade["valores"][chave]
        esperado = list(tabela[chave])
        assert len(guardado) == len(esperado)
        for a, b in zip(guardado, esperado):
            assert a == pytest.approx(b, abs=0.5 * 10 ** -casas + 1e-9)


def test_a_matriz_de_decisao_e_a_do_topsis_do_programa():
    from triton.core.topsis import _decision_matrix, calculate_topsis_scores
    d = gi.multicriterio()
    cands = gi._candidatos_mcdm()
    matriz = _decision_matrix(cands)
    for linha_site, linha in zip(d["matriz"], matriz):
        for a, b in zip(linha_site, linha):
            assert a == pytest.approx(b, rel=1e-4, abs=1e-4)
    escores = calculate_topsis_scores(cands, None).scores
    for a, b in zip(d["escores_padrao"], escores):
        assert a == pytest.approx(b, abs=1e-6)


def test_a_aceitabilidade_smaa_e_a_do_programa():
    from triton.core.mcdm_methods import run_smaa_analysis
    d = gi.smaa()
    cands = gi._candidatos_mcdm()
    for chave in ("vikor|0", "topsis|0.5"):
        motor, v = chave.split("|")
        res = run_smaa_analysis(cands, num_samples=d["sorteios"], random_seed=d["semente"],
                                engine=motor, v_param=float(v))
        for a, b in zip(d["casos"][chave]["primeiro"], res.first_rank_probs):
            assert a == pytest.approx(b, abs=0.011)


@pytest.mark.skipif(shutil.which("node") is None, reason="o Node não está instalado")
def test_o_topsis_do_site_reproduz_o_do_programa(tmp_path):
    """O único cálculo feito no navegador: conferido com pesos sorteados."""
    from triton.core.topsis import CRITERION_IS_BENEFIT, calculate_topsis_scores
    d = gi.multicriterio()
    cands = gi._candidatos_mcdm()
    fonte = open(os.path.join(MANUAL, "site_interativas.js"), encoding="utf-8").read()
    ini = fonte.index("function topsisEscores(")
    fim = fonte.index("\nFI[", ini)
    funcao = fonte[ini:fim]

    rng = np.random.default_rng(7)
    pesos = [[1 / 7] * 7] + [list(x) for x in rng.dirichlet(np.ones(7), size=40)]
    entrada = {"matriz": d["matriz"], "beneficio": [bool(x) for x in CRITERION_IS_BENEFIT],
               "volumes": d["volumes"], "pesos": pesos}
    script = tmp_path / "topsis.js"
    script.write_text(
        funcao + "\nconst e = " + json.dumps(entrada) + ";\n"
        "console.log(JSON.stringify(e.pesos.map(w => topsisEscores(e.matriz, w, e.beneficio, e.volumes))));",
        encoding="utf-8")
    saida = subprocess.run(["node", str(script)], capture_output=True, text=True, timeout=120)
    assert saida.returncode == 0, saida.stderr
    resultados = json.loads(saida.stdout)

    for w, resultado in zip(pesos, resultados):
        esperado = calculate_topsis_scores(cands, w)
        for a, b in zip(resultado["escores"], esperado.scores):
            assert a == pytest.approx(b, abs=2e-4)
        assert resultado["postos"] == [int(x) for x in esperado.rankings]
        proximidade = esperado.criterion_proximity_to_best
        for linha_js, linha in zip(resultado["proximidade"], proximidade):
            for a, b in zip(linha_js, linha):
                assert a == pytest.approx(b, abs=1e-4)


def test_a_captacao_e_a_lamina_da_serie_com_o_descarte_do_programa():
    from datetime import timedelta
    from triton.core.hydrology_defaults import COEFICIENTES_POR_MATERIAL
    from triton.core.parser import load_precipitation
    d = gi.captacao()
    assert [list(x) for x in COEFICIENTES_POR_MATERIAL] == d["materiais"]
    cidade = d["cidades"][0]
    serie_cidade = load_precipitation(
        os.path.join(RAIZ, "data", "rainfall", f"{cidade['chave']}.csv"))[: 30 * 365]
    anos = len(serie_cidade) / 365.25
    for descarte in ("0", "2"):
        meses = np.zeros(12)
        for i, x in enumerate(serie_cidade):
            efetiva = max(0.0, float(x) - float(descarte)) if float(x) > 0 else 0.0
            meses[(gi.INICIO + timedelta(days=i)).month - 1] += efetiva
        for guardado, esperado in zip(cidade["mensal"][descarte], meses / anos):
            assert guardado == pytest.approx(esperado, abs=0.051)


def test_os_pressurizadores_sao_os_do_catalogo_do_programa():
    from triton.core.pressurizer_catalog import CATALOGO, comparar
    d = gi.pressurizadores()
    assert [m["chave"] for m in d["modelos"]] == [p.chave for p in CATALOGO]
    for pressao, volume, partidas in ((5, 50, 500), (15, 150, 1200), (40, 400, 5000)):
        esperado = comparar(float(volume), float(pressao), float(partidas))
        guardado = d["casos"][f"{pressao:g}|{volume}|{partidas}"]
        assert [x["chave"] for x in guardado] == [e.chave for e in esperado]
        for x, e in zip(guardado, esperado):
            assert x["atende"] == bool(e.atende)
            assert x["kwh"] == pytest.approx(e.kwh_ano, abs=0.051)
            assert x["kwh_m3"] == pytest.approx(e.kwh_por_m3, abs=0.0006)


def test_as_classes_de_qualidade_sao_as_do_programa():
    from triton.core.water_quality import WATER_QUALITY_CLASSES
    d = gi.classes_de_qualidade()
    assert [c["chave"] for c in d["classes"]] == list(WATER_QUALITY_CLASSES)
    for c in d["classes"]:
        original = WATER_QUALITY_CLASSES[c["chave"]]
        assert c["turbidez"] == pytest.approx(original.turbidez_max_ntu)
        assert c["cor"] == pytest.approx(original.cor_aparente_max_uh)
        assert c["coliformes"] == pytest.approx(original.coliformes_termo_max_ufc_100ml)
        assert c["desinfeccao"] == original.exige_desinfeccao
        assert c["filtracao"] == original.exige_filtracao_fina
    # Só a classe 1 pode ser apresentada como requisito normativo.
    assert [c["chave"] for c in d["classes"] if c["normativa"]] == ["classe_1"]


def test_a_curva_de_vpl_e_a_da_analise_economica(serie):
    from triton.core.economic import run_economic_analysis
    d = gi.vpl_por_volume()
    for material in ("CONCRETO", "PEAD"):
        for k in (1, 4, len(d["volumes"]) - 1):
            volume = d["volumes"][k]
            r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume),
                                      **_config_projeto())
            e = run_economic_analysis(_config_economica(volume, material), r)
            assert d["casos"][material][k][0] == pytest.approx(e.vpl, **APROX)
            assert d["casos"][material][k][2] == pytest.approx(
                r.potential_potable_savings_pct, abs=0.005)


def test_os_tres_criterios_do_manual_continuam_apontando_volumes_diferentes(serie):
    """A prosa da seção do volume ideal afirma isso; se mudar, o texto mente."""
    from triton.core.economic import run_economic_analysis
    from gerar_tabelas import VOLUMES_VARREDURA
    vols, pots, vpls = [], [], []
    for v in VOLUMES_VARREDURA:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **_config_projeto())
        vols.append(v / 1000.0)
        pots.append(r.potential_potable_savings_pct)
        vpls.append(0.0 if v == 0 else
                    run_economic_analysis(_config_economica(float(v), "CONCRETO"), r).vpl)
    vols, pots, vpls = np.array(vols), np.array(pots), np.array(vpls)
    marginal = np.zeros_like(pots)
    marginal[1:] = np.diff(pots) / np.diff(vols)
    ideais = np.where((vols > 0) & (marginal <= 1.0))[0]
    i_ideal = int(ideais[0]) if len(ideais) else len(vols) - 1
    escolhas = {i_ideal, int(np.argmax(vpls)), int(np.argmax(pots))}
    assert len(escolhas) == 3, f"os três critérios coincidiram em {escolhas}"
    assert vols[int(np.argmax(pots))] == max(vols[i] for i in escolhas)
    texto = open(os.path.join(MANUAL, "partes", "24_volume_ideal.md"), encoding="utf-8").read()
    assert "eles apontam três volumes diferentes" in texto
    # A legenda não repete números que dependem da grade e das premissas.
    assert "ambos em 5 m³" not in texto


def test_nenhum_painel_ficou_sem_figura_no_manual():
    texto = open(os.path.join(MANUAL, "Manual-Triton.md"), encoding="utf-8").read()
    js = open(os.path.join(MANUAL, "site_interativas.js"), encoding="utf-8").read()
    desenhadas = set(re.findall(r'FI\["([^"]+)"\] = \{', js))
    # A curva de retorno usa a grade da página inicial e não tem entrada própria.
    for arquivo in set(gi.dados()) | {"fig02_curva_de_retorno.png"}:
        assert arquivo in desenhadas, arquivo
        assert f"figuras/{arquivo})" in texto, arquivo
