"""
Geração e Execução dos 3 Estudos de Caso de Referência do Triton:
1. Residencial Unifamiliar (Florianópolis/SC) - Florianopolis1.csv
2. Edifício Comercial / Escritórios (Brasília/DF) - Brasilia2.csv
3. Escola Pública Integral (Manaus/AM) - Manaus3.csv
"""

import os
import sys
import json
import math
import hashlib
import numpy as np

# Garante que o triton está no path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from triton.core.parser import TritonConfig, load_precipitation, format_ptbr
from triton.core.simulation import run_single_simulation, run_sweep_simulation
from triton.core.cost_estimates import (
    estimate_preliminary_capex, estimate_pipe_network_cost,
    estimate_annual_chlorination_cost, estimate_tank_price_linear,
    annualize_operational_costs,
    LOWER_TANK_PRICE_TABLE, UPPER_TANK_PRICE_TABLE,
    MATERIAL_COST_MULTIPLIERS, PIPE_COST_PER_METER,
)
from triton.core.economic import (
    calculate_effective_tariff, run_robust_economic_analysis,
    calculate_water_bill
)
from triton.core.environmental import (
    EnvironmentalConfig, PipeInput, PumpInput, MATERIAL_PRESETS,
    PUMP_EMBEDDED_CO2, PIPE_EMISSION_FACTORS_PER_METER,
    normalize_material_key, calculate_lca, run_environmental_sweep
)
from triton.core.topsis import calculate_topsis_scores, TopsisCandidate
from triton import __version__


def run_case_study(
    case_id: str,
    title: str,
    typology: str,
    rain_filename: str,
    area_m2: float,
    runoff_c: float,
    discard_mm: float,
    discard_mode: int,
    discard_days: int,
    residents: int,
    demand_l_hab_day: float,
    share_pct: float,
    upper_vol_l: float,
    upper_used: bool,
    pump_thresh_pct: float,
    sweep_max_l: float,
    sweep_step_l: float,
    delta_ideal: float,
    lower_mat: str,
    upper_mat: str,
    pipes: list,
    pump_power_kw: float,
    pump_flow_rate: float,
    pump_efficiency: float,
    pump_count: int,
    pump_startup_h: float,
    elec_tariff: float,
    chlorine_enabled: bool,
    chlorine_dose: float,
    chlorine_cost_kg: float,
    chlorine_co2_kg: float,
    water_tariffs: list,
    sewage_rate: float,
    sewage_mode: int,
    tma_annual: float,
    inflation_annual: float,
    analysis_years: int = 20,
    out_dir: str = "examples"
):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rain_path = os.path.join(base_dir, "data", "rainfall", rain_filename)
    if not os.path.exists(rain_path):
        raise FileNotFoundError(f"Arquivo pluviométrico não encontrado: {rain_path}")

    precip_data = load_precipitation(rain_path)
    with open(rain_path, "rb") as rain_stream:
        rain_sha256 = hashlib.sha256(rain_stream.read()).hexdigest()
    total_days = len(precip_data)
    years_sim = total_days / 365.25

    # 1. Configuração do Triton
    cfg = TritonConfig()
    cfg.precip_file = rain_filename
    cfg.area = area_m2
    cfg.runoff_coeff = runoff_c
    cfg.discard = discard_mm
    cfg.discard_mode = discard_mode
    cfg.discard_days_interval = discard_days
    cfg.residents_count = residents
    cfg.demand_value = demand_l_hab_day
    cfg.rainwater_share = share_pct / 100.0
    cfg.upper_tank_vol = upper_vol_l
    cfg.upper_tank_used = 1 if upper_used else 0
    cfg.pumping_threshold = upper_vol_l * (pump_thresh_pct / 100.0) if upper_used else 0.0
    cfg.lower_tank_max = sweep_max_l
    cfg.lower_tank_step = sweep_step_l
    cfg.delta_ideal = delta_ideal
    cfg.lower_tank_material = lower_mat
    cfg.upper_tank_material = upper_mat
    cfg.pipes_list = pipes
    cfg.pump_power_kw = pump_power_kw
    cfg.pump_flow_rate = pump_flow_rate
    cfg.pump_efficiency = pump_efficiency
    cfg.pump_count = pump_count
    cfg.pump_startup_time_h = pump_startup_h
    cfg.elec_tariff = elec_tariff
    cfg.chlorine_treatment_enabled = chlorine_enabled
    cfg.chlorine_dose_mg_l = chlorine_dose
    cfg.chlorine_cost_per_kg = chlorine_cost_kg
    cfg.chlorine_co2_kg_per_kg = chlorine_co2_kg
    cfg.water_tariffs = water_tariffs
    cfg.sewage_rate = sewage_rate
    cfg.sewage_mode = sewage_mode
    cfg.tma = tma_annual / 12.0
    cfg.inflation = inflation_annual / 12.0
    cfg.analysis_period_years = analysis_years

    # 2. Simulação Técnica (Etapa 3 / 4)
    tot_daily_demand = residents * demand_l_hab_day
    sw_tech = run_sweep_simulation(
        precip_data=precip_data,
        lower_tank_max=sweep_max_l,
        lower_tank_step=sweep_step_l,
        area=area_m2,
        runoff_coeff=runoff_c,
        discard_mm=discard_mm,
        discard_mode=discard_mode,
        discard_days_interval=discard_days,
        total_demand_per_day=tot_daily_demand,
        rainwater_share=cfg.rainwater_share,
        upper_tank_vol=upper_vol_l if upper_used else 0.0,
        upper_tank_used=upper_used,
        pumping_threshold=cfg.pumping_threshold,
        delta_ideal_threshold=delta_ideal
    )
    opt_tech_vol = sw_tech.optimal_lower_tank_vol if sw_tech.optimal_lower_tank_vol is not None else sw_tech.results_by_volume[0].lower_tank_vol

    # 3. Análise Econômico-Financeira na Varredura (Etapa 5)
    econ_sweep_records = []
    best_vpl_vol = 0.0
    max_vpl = -1e9

    for r_item in sw_tech.results_by_volume:
        v_vol = r_item.lower_tank_vol
        annual_m3 = r_item.annual_pluvial_consumed_m3
        
        # CAPEX do ponto da varredura
        est = estimate_preliminary_capex(
            lower_volume_l=v_vol,
            upper_volume_l=upper_vol_l,
            upper_used=upper_used,
            pump_power_kw=pump_power_kw,
            pump_count=pump_count,
            lower_material=lower_mat,
            upper_material=upper_mat,
            pipes=pipes
        )
        total_capex = est["total"]

        # Tarifas efetivas
        tw_v, ts_v = calculate_effective_tariff(
            cfg, annual_m3,
            annual_total_demand_m3=tot_daily_demand * 365.25 / 1000.0,
        )

        # Horas de bomba anuais
        p_hrs = 0.0
        if upper_used and pump_flow_rate > 0:
            t_rec = (r_item.total_pumped_liters / max(1.0, years_sim)) / pump_flow_rate
            ann_cyc = r_item.total_pump_cycles / max(1.0, years_sim)
            t_part = ann_cyc * pump_startup_h
            p_hrs = (t_rec + t_part) / max(0.01, pump_efficiency / 100.0)

        # Cloração
        ann_cl2_kg, ann_cl2_cost = estimate_annual_chlorination_cost(
            annual_m3, chlorine_dose if chlorine_enabled else 0.0, chlorine_cost_kg
        )

        econ_res = run_robust_economic_analysis(
            initial_investment=total_capex,
            annual_water_saved_m3=annual_m3,
            water_tariff_per_m3=tw_v,
            sewage_tariff_per_m3=ts_v,
            sewage_mode=sewage_mode,
            water_tariff_escalation_rate=0.05,
            sewage_tariff_escalation_rate=0.05,
            elec_tariff_escalation_rate=0.05,
            inflation_rate=inflation_annual / 100.0,
            discount_rate=tma_annual / 100.0,
            annual_om_cost_base=annualize_operational_costs(cfg.op_costs, annual_m3),
            pump_power_kw=pump_power_kw,
            pump_hours_year=p_hrs,
            elec_tariff_kwh=elec_tariff,
            analysis_period_years=analysis_years,
            annual_chlorine_cost=ann_cl2_cost
        )

        if econ_res.vpl > max_vpl:
            max_vpl = econ_res.vpl
            best_vpl_vol = v_vol

        econ_sweep_records.append({
            "vol_l": v_vol,
            "annual_m3": annual_m3,
            "capex": total_capex,
            "capex_breakdown": est,
            "vpl": econ_res.vpl,
            "tir": econ_res.tir_pct,
            "payback_d": econ_res.payback_discounted_years,
            "payback_s": econ_res.payback_simple_years,
            "pump_hrs": p_hrs,
            "pump_kwh": pump_power_kw * p_hrs,
            "annual_om": annualize_operational_costs(cfg.op_costs, annual_m3),
            "water_tariff": tw_v,
            "sewage_tariff": ts_v,
            "cl2_kg": ann_cl2_kg,
            "cl2_cost": ann_cl2_cost,
            "econ_obj": econ_res
        })

    # 4. Avaliação do Ciclo de Vida (ACV) e Varredura Ambiental (Etapa 6)
    pipe_inputs = []
    for p in pipes:
        dn, length = p[0], p[1]
        pipe_inputs.append(PipeInput(diameter_mm=dn, length_m=length))

    pump_cv = round(pump_power_kw / 0.735499, 2)
    env_cfg = EnvironmentalConfig(
        lower_material_key=lower_mat,
        upper_material_key=upper_mat,
        upper_tank_vol_liters=upper_vol_l,
        upper_tank_used=upper_used,
        pipes=pipe_inputs,
        pump=PumpInput(power_cv=pump_cv),
        pump_count=pump_count,
        chlorine_dose_mg_l=chlorine_dose if chlorine_enabled else 0.0,
        chlorine_co2_kg_per_kg=chlorine_co2_kg,
        system_lifespan_years=analysis_years
    )

    v_map = [
        (r.lower_tank_vol, r.annual_pluvial_consumed_m3, econ["pump_kwh"])
        for r, econ in zip(sw_tech.results_by_volume, econ_sweep_records)
    ]
    sw_env = run_environmental_sweep(v_map, env_cfg)
    opt_env_vol = sw_env.best_lifetime_co2_vol_liters

    # 5. Otimização Multicritério TOPSIS (Etapa 7)
    candidates = []
    for r_tech, d_econ, d_env in zip(sw_tech.results_by_volume, econ_sweep_records, sw_env.sweep_details):
        candidates.append(TopsisCandidate(
            lower_tank_vol=r_tech.lower_tank_vol,
            water_saved_m3_yr=r_tech.annual_pluvial_consumed_m3,
            vpl_brl=d_econ["vpl"],
            co2_saved_kg_lifetime=d_env["lifetime_net_co2_saved_kg"],
            capex_brl=d_econ["capex"],
            upper_tank_vol=upper_vol_l,
            technical_threshold_met=(
                r_tech.lower_tank_vol > 0
                and r_tech.delta_potential_per_m3 <= delta_ideal
            ),
        ))
    topsis_res = calculate_topsis_scores(candidates, weights=(1.0/3.0, 1.0/3.0, 1.0/3.0))
    opt_topsis_vol = topsis_res.best_candidate.lower_tank_vol if topsis_res else opt_tech_vol

    # 6. Salva arquivo de projeto .triton
    proj_filename = f"estudo_caso_{case_id}_{rain_filename.split('.')[0].lower()}.triton"
    proj_filepath = os.path.join(base_dir, out_dir, proj_filename)
    
    # Monta dicionário de persistência
    proj_data = {
        "format_version": "5.0",
        "software_version": __version__,
        "case_id": case_id,
        "title": title,
        "typology": typology,
        "climate_city": rain_filename.replace('.csv', ''),
        "rain_file": rain_filename,
        "rain_sha256": rain_sha256,
        "area": area_m2,
        "runoff": runoff_c,
        "discard": discard_mm,
        "discard_mode": discard_mode,
        "discard_days": discard_days,
        "residents": residents,
        "demand": demand_l_hab_day,
        "share": share_pct,
        "upper_vol": upper_vol_l,
        "upper_used": upper_used,
        "pump_thresh_pct": pump_thresh_pct,
        "sweep_max": sweep_max_l,
        "sweep_step": sweep_step_l,
        "delta_ideal": delta_ideal,
        "lower_tank_material": lower_mat,
        "upper_tank_material": upper_mat,
        "pipes_list": pipes,
        "pump_power_kw": pump_power_kw,
        "pump_flow_rate": pump_flow_rate,
        "pump_efficiency": pump_efficiency,
        "pump_count": pump_count,
        "elec_tariff": elec_tariff,
        "chlorine_treatment_enabled": chlorine_enabled,
        "chlorine_dose_mg_l": chlorine_dose,
        "chlorine_cost_per_kg": chlorine_cost_kg,
        "water_tariffs": water_tariffs,
        "sewage_rate": sewage_rate,
        "sewage_mode": sewage_mode,
        "tma_annual": tma_annual,
        "inflation_annual": inflation_annual,
        "optima": {
            "technical_volume_l": opt_tech_vol,
            "economic_volume_l": best_vpl_vol,
            "environmental_volume_l": opt_env_vol,
            "topsis_recommended_l": opt_topsis_vol
        }
    }

    os.makedirs(os.path.dirname(proj_filepath), exist_ok=True)
    with open(proj_filepath, "w", encoding="utf-8") as f:
        json.dump(proj_data, f, indent=2, ensure_ascii=False)

    return {
        "case_id": case_id,
        "title": title,
        "typology": typology,
        "climate": rain_filename.replace('.csv', ''),
        "rain_file": rain_filename,
        "rain_sha256": rain_sha256,
        "area_m2": area_m2,
        "residents": residents,
        "daily_demand_l": tot_daily_demand,
        "materials": f"Cisterna: {lower_mat} | Caixa: {upper_mat}",
        "pipes_str": " + ".join([f"DN {p[0]} ({p[1]}m)" for p in pipes]),
        "pump_str": f"{pump_cv:.2f} CV ({pump_flow_rate:.0f} L/h, {pump_count} un)",
        "chlorine_str": f"{chlorine_dose:.1f} mg/L (R$ {chlorine_cost_kg:.2f}/kg)",
        "opt_tech_vol": opt_tech_vol,
        "opt_econ_vol": best_vpl_vol,
        "opt_env_vol": opt_env_vol,
        "opt_topsis_vol": opt_topsis_vol,
        "tech_sweep": sw_tech,
        "econ_sweep": econ_sweep_records,
        "env_sweep": sw_env,
        "environmental_config": env_cfg,
        "topsis_res": topsis_res,
        "proj_filepath": proj_filepath,
        "config": cfg,
        "precip_data": precip_data,
        "years_simulated": years_sim,
    }


def _pt(value, decimals=2):
    """Formatação numérica determinística para o relatório Markdown."""
    if value is None:
        return "—"
    raw = f"{float(value):,.{decimals}f}"
    return raw.replace(",", "§").replace(".", ",").replace("§", ".")


def _manual_interpolate_price(table, volume_l):
    """Reprodução explícita da interpolação para a auditoria documental."""
    volume_l = max(0.0, float(volume_l))
    if volume_l <= 0:
        return 0.0
    if volume_l <= table[0][0]:
        return table[0][1] * volume_l / table[0][0]
    if volume_l >= table[-1][0]:
        v1, p1 = table[-2]
        v2, p2 = table[-1]
        return p2 + (p2 - p1) * (volume_l - v2) / (v2 - v1)
    for (v1, p1), (v2, p2) in zip(table, table[1:]):
        if v1 <= volume_l <= v2:
            return p1 + (volume_l - v1) * (p2 - p1) / (v2 - v1)
    raise AssertionError("Volume não coberto pela tabela manual de preços.")


def _manual_tank_price(table, volume_l, material_key):
    return _manual_interpolate_price(table, volume_l) * MATERIAL_COST_MULTIPLIERS.get(material_key, 1.0)


def _append_cash_flow_table(lines, econ, discount_rate):
    lines.extend([
        "#### Fluxo de caixa: verificação termo a termo",
        "",
        "Em cada ano, a coluna manual recompõe `FC = −CAPEX + economia bruta − energia − O&M − cloro`; "
        "o fator é `(1 + TMA)^−t`. Os resíduos comparam essa substituição com o objeto retornado pelo motor.",
        "",
        "##### Fluxos nominais",
        "",
        "| Ano | CAPEX (R$) | Economia bruta (R$) | Energia (R$) | O&M (R$) | Cloro (R$) | FC sistema (R$) | FC manual (R$) | Resíduo FC (R$) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    audit_rows = []
    manual_cumulative = 0.0
    for cf in econ.annual_cash_flows:
        manual_net = (
            -cf.initial_investment
            + cf.total_gross_savings_brl
            - cf.pump_energy_cost_brl
            - cf.om_cost_brl
            - cf.chlorine_cost_brl
        )
        manual_factor = 1.0 / ((1.0 + discount_rate) ** cf.year)
        manual_discounted = manual_net * manual_factor
        manual_cumulative += manual_discounted
        lines.append(
            f"| {cf.year} | {_pt(cf.initial_investment)} | {_pt(cf.total_gross_savings_brl)} | "
            f"{_pt(cf.pump_energy_cost_brl)} | {_pt(cf.om_cost_brl)} | {_pt(cf.chlorine_cost_brl)} | "
            f"{_pt(cf.net_cash_flow_nominal_brl)} | {_pt(manual_net)} | "
            f"{_pt(abs(manual_net - cf.net_cash_flow_nominal_brl), 9)} |"
        )
        audit_rows.append(
            f"| {cf.year} | {_pt(manual_factor, 6)} | {_pt(cf.discounted_cash_flow_brl)} | "
            f"{_pt(abs(manual_discounted - cf.discounted_cash_flow_brl), 9)} | "
            f"{_pt(cf.cumulative_discounted_cash_flow_brl)} | "
            f"{_pt(abs(manual_cumulative - cf.cumulative_discounted_cash_flow_brl), 9)} |"
        )
    lines.extend([
        "",
        "##### Desconto e acumulado",
        "",
        "| Ano | Fator manual | FC descontado do sistema (R$) | Resíduo do desconto (R$) | Acumulado do sistema (R$) | Resíduo acumulado (R$) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        *audit_rows,
        "",
    ])


def _append_topsis_audit(lines, topsis):
    weights = np.divide(
        topsis.weighted_matrix,
        topsis.normalized_matrix,
        out=np.zeros_like(topsis.weighted_matrix),
        where=np.abs(topsis.normalized_matrix) > 1e-15,
    )
    inferred_weights = []
    for col in range(3):
        nonzero = weights[:, col][np.abs(weights[:, col]) > 1e-15]
        inferred_weights.append(float(nonzero[0]) if len(nonzero) else 0.0)

    lines.extend([
        "#### TOPSIS: conta completa por alternativa",
        "",
        "A matriz é transladada pelo pior observado em cada coluna, normalizada vetorialmente e ponderada. "
        f"Pesos efetivos: técnico `{_pt(inferred_weights[0], 6)}`, econômico `{_pt(inferred_weights[1], 6)}`, ambiental `{_pt(inferred_weights[2], 6)}`.",
        "",
        "##### Critérios e normalização",
        "",
        "| V (L) | Água (m³/a) | VPL (R$) | CO2 líquido (kg) | r técnico | r econômico | r ambiental |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    distance_rows = []
    gap_rows = []
    for i, candidate in enumerate(topsis.candidates):
        r = topsis.normalized_matrix[i]
        gaps = topsis.criterion_gap_to_best[i] * 100.0
        lines.append(
            f"| {_pt(candidate.lower_tank_vol, 0)} | {_pt(candidate.water_saved_m3_yr, 3)} | "
            f"{_pt(candidate.vpl_brl)} | {_pt(candidate.co2_saved_kg_lifetime, 2)} | "
            f"{_pt(r[0], 6)} | {_pt(r[1], 6)} | {_pt(r[2], 6)} |"
        )
        distance_rows.append(
            f"| {_pt(candidate.lower_tank_vol, 0)} | "
            f"{_pt(topsis.dist_best[i], 6)} | {_pt(topsis.dist_worst[i], 6)} | "
            f"{_pt(topsis.scores[i], 6)} | {int(topsis.rankings[i])} |"
        )
        gap_rows.append(
            f"| {_pt(candidate.lower_tank_vol, 0)} | {_pt(gaps[0], 1)}% | "
            f"{_pt(gaps[1], 1)}% | {_pt(gaps[2], 1)}% |"
        )
    lines.extend([
        "",
        "##### Distâncias e ranking",
        "",
        "| V (L) | D+ | D− | C | Rank |",
        "| ---: | ---: | ---: | ---: | ---: |",
        *distance_rows,
        "",
        "##### Distância relativa ao melhor de cada critério",
        "",
        "| V (L) | Gap técnico | Gap econômico | Gap ambiental |",
        "| ---: | ---: | ---: | ---: |",
        *gap_rows,
        "",
        "Para cada linha, `C = D- / (D+ + D-)`. Os três gaps são independentes dos pesos: "
        "0% é o ótimo observado no eixo e 100% é o pior valor observado.",
        "",
    ])


def write_reference_validation_report(results, output_path):
    """Gera o estudo rastreável diretamente dos objetos calculados pelo motor."""
    lines = [
        f"# Estudo de Caso e Verificação Manual — Três Modelos de Referência (Triton {__version__})",
        "",
        "> Documento gerado por `python scripts/generate_reference_case_studies.py`. "
        "Não edite os números manualmente: altere premissas/código, execute o script e revise os resíduos.",
        "",
        "## Escopo e cautelas",
        "",
        "Este relatório confronta, por substituição numérica, os resultados do motor com contas independentes "
        "das mesmas equações. Isso é verificação interna e reprodutibilidade computacional; não é validação "
        "externa, certificação normativa, orçamento executivo nem ensaio de qualidade da água.",
        "",
        "Decisões metodológicas essenciais:",
        "",
        "- O descarte é o **limiar diário legado do Netuno 4**: abaixo de `df`, a chuva aplicável é zerada; "
        "ao atingir o limiar, `P` entra integralmente. Não se usa `P-df`.",
        "- O balanço é YAS: limita estoque/extravasamento antes de retirar a demanda.",
        "- A alternativa de 0 L é a referência sem sistema: CAPEX e impactos ambientais iguais a zero.",
        "- CAPEX automático é triagem por interpolação da tabela interna; deve ser substituído por cotações locais.",
        "- O O&M variável do formato Netuno 4 depende do **volume pluvial consumido no mês**, não da capacidade da cisterna. "
        "Os três casos usam itens fixos; não se adotou o coeficiente não comprovado de R$ 15/m³ de cisterna.",
        "- A massa de cloro é consumo teórico em Cl2 equivalente. Demanda real de cloro exige ensaio e residual-alvo.",
        "- A ACV é de triagem: fatores de material, rede, água e cloro são editáveis e exigem calibração local/EPD.",
        "",
        "## Síntese dos ótimos recalculados",
        "",
        "| Caso | Ótimo técnico (L) | Maior VPL (L) | Maior CO2 líquido (L) | TOPSIS (L) | Score |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for case in results:
        topsis = case["topsis_res"]
        lines.append(
            f"| {case['case_id']} — {case['title']} | {_pt(case['opt_tech_vol'], 0)} | "
            f"{_pt(case['opt_econ_vol'], 0)} | {_pt(case['opt_env_vol'], 0)} | "
            f"{_pt(case['opt_topsis_vol'], 0)} | {_pt(topsis.scores[topsis.best_index], 6)} |"
        )
    lines.append("")

    for case in results:
        cfg = case["config"]
        precip = case["precip_data"]
        sweep = case["tech_sweep"]
        topsis = case["topsis_res"]
        selected_i = topsis.best_index
        technical = sweep.results_by_volume[selected_i]
        economic = case["econ_sweep"][selected_i]
        econ = economic["econ_obj"]
        environmental = case["env_sweep"].sweep_details[selected_i]
        lca = environmental["lca_result"]
        capex = economic["capex_breakdown"]
        years = case["years_simulated"]
        total_demand_day = cfg.residents_count * cfg.demand_value
        pluvial_demand_day = total_demand_day * cfg.rainwater_share
        annual_total_m3 = total_demand_day * 365.25 / 1000.0

        detailed = run_single_simulation(
            precip_data=precip,
            lower_tank_vol=technical.lower_tank_vol,
            area=cfg.area,
            runoff_coeff=cfg.runoff_coeff,
            discard_mm=cfg.discard,
            discard_mode=cfg.discard_mode,
            discard_days_interval=cfg.discard_days_interval,
            total_demand_per_day=total_demand_day,
            rainwater_share=cfg.rainwater_share,
            upper_tank_vol=cfg.upper_tank_vol if cfg.upper_tank_used else 0.0,
            upper_tank_used=bool(cfg.upper_tank_used),
            pumping_threshold=cfg.pumping_threshold,
            store_daily_details=True,
            start_date_str=cfg.start_date,
        )
        day = next(d for d in detailed.daily_results if d.harvested_liters > 0)
        day_i = day.day_index
        prev_lower = detailed.daily_results[day_i - 1].lower_tank_end_liters if day_i > 0 else 0.0
        prev_upper = detailed.daily_results[day_i - 1].upper_tank_end_liters if day_i > 0 else 0.0
        mass_lhs = prev_lower + prev_upper + day.harvested_liters
        mass_rhs = day.lower_tank_end_liters + day.upper_tank_end_liters + day.pluvial_consumed_liters + day.spilled_liters

        annual_pumped_l = technical.total_pumped_liters / years
        annual_cycles = technical.total_pump_cycles / years
        t_rec = annual_pumped_l / cfg.pump_flow_rate if cfg.pump_flow_rate > 0 else 0.0
        t_start = annual_cycles * cfg.pump_startup_time_h
        manual_kwh = cfg.pump_power_kw * (t_rec + t_start) / max(0.01, cfg.pump_efficiency / 100.0) if cfg.upper_tank_used else 0.0
        manual_cl2 = technical.annual_pluvial_consumed_m3 * cfg.chlorine_dose_mg_l / 1000.0 if cfg.chlorine_treatment_enabled else 0.0
        manual_cl2_cost = manual_cl2 * cfg.chlorine_cost_per_kg
        manual_capex = sum(capex[k] for k in ("lower", "upper", "pump", "piping", "accessories", "labor"))
        first = econ.annual_cash_flows[1]
        manual_gross = technical.annual_pluvial_consumed_m3 * (economic["water_tariff"] + economic["sewage_tariff"])
        manual_net = manual_gross - economic["annual_om"] - manual_kwh * cfg.elec_tariff - manual_cl2_cost
        manual_vpl = sum(cf.discounted_cash_flow_brl for cf in econ.annual_cash_flows)
        tir_rate = econ.tir_pct / 100.0
        manual_tir_residual = sum(
            cf.net_cash_flow_nominal_brl / ((1.0 + tir_rate) ** cf.year)
            for cf in econ.annual_cash_flows
        ) if tir_rate > -1.0 else float("nan")
        cum_simple = 0.0
        manual_payback_simple = None
        for cf in econ.annual_cash_flows:
            cum_simple += cf.net_cash_flow_nominal_brl
            if cf.year > 0 and manual_payback_simple is None and cum_simple >= 0.0:
                manual_payback_simple = cf.year
        manual_payback_discounted = next(
            (cf.year for cf in econ.annual_cash_flows if cf.year > 0 and cf.cumulative_discounted_cash_flow_brl >= 0.0),
            None,
        )
        manual_lifetime = (
            (lca.annual_avoided_co2_kg - lca.annual_pumping_co2_kg - lca.annual_treatment_co2_kg)
            * cfg.analysis_period_years - lca.total_embodied_co2_kg
        )
        manual_score = topsis.dist_worst[selected_i] / (
            topsis.dist_best[selected_i] + topsis.dist_worst[selected_i]
        ) if (topsis.dist_best[selected_i] + topsis.dist_worst[selected_i]) > 0 else 1.0

        # Auditoria item a item: estas expressões repetem de forma explícita
        # as equações documentadas, sem reutilizar os totais consolidados.
        previous_technical = sweep.results_by_volume[selected_i - 1] if selected_i > 0 else None
        manual_delta = 0.0
        if previous_technical is not None:
            delta_volume_m3 = (technical.lower_tank_vol - previous_technical.lower_tank_vol) / 1000.0
            if delta_volume_m3 > 0:
                manual_delta = (
                    technical.potential_potable_savings_pct
                    - previous_technical.potential_potable_savings_pct
                ) / delta_volume_m3

        manual_lower_capex = _manual_tank_price(
            LOWER_TANK_PRICE_TABLE, technical.lower_tank_vol, cfg.lower_tank_material
        )
        manual_upper_capex = (
            _manual_tank_price(UPPER_TANK_PRICE_TABLE, cfg.upper_tank_vol, cfg.upper_tank_material)
            if cfg.upper_tank_used else 0.0
        )
        manual_pump_unit = (
            max(280.0, 300.0 * (max(0.1, cfg.pump_power_kw) / 0.36775) ** 0.70)
            if cfg.upper_tank_used else 0.0
        )
        manual_pump_capex = manual_pump_unit * max(1, cfg.pump_count) if cfg.upper_tank_used else 0.0
        manual_piping_capex = max(
            350.0,
            1.25 * sum(float(p[1]) * PIPE_COST_PER_METER.get(int(p[0]), 38.0) for p in cfg.pipes_list),
        )
        manual_accessories_capex = max(500.0, 150.0 + 0.08 * (manual_lower_capex + manual_upper_capex))
        manual_labor_capex = max(
            1400.0,
            0.30 * (
                manual_lower_capex + manual_upper_capex + manual_pump_capex
                + manual_piping_capex + manual_accessories_capex
            ),
        )
        manual_capex_from_rules = sum((
            manual_lower_capex, manual_upper_capex, manual_pump_capex,
            manual_piping_capex, manual_accessories_capex, manual_labor_capex,
        ))
        manual_annual_om = sum(
            (12.0 / max(1.0, float(item[1])))
            * (float(item[2]) + float(item[3]) * technical.annual_pluvial_consumed_m3 / 12.0)
            for item in cfg.op_costs
            if len(item) >= 4
        )

        base_month_m3 = annual_total_m3 / 12.0
        pluvial_month_m3 = technical.annual_pluvial_consumed_m3 / 12.0
        post_month_m3 = max(0.0, base_month_m3 - pluvial_month_m3)
        water_without = calculate_water_bill(
            base_month_m3 * 1000.0, cfg.water_tariffs, sewage_mode=1, sewage_rate=0.0,
            water_tax_fixed=cfg.water_tax_fixed, water_tax_var=cfg.water_tax_var,
        )
        water_with = calculate_water_bill(
            post_month_m3 * 1000.0, cfg.water_tariffs, sewage_mode=1, sewage_rate=0.0,
            water_tax_fixed=cfg.water_tax_fixed, water_tax_var=cfg.water_tax_var,
        )
        total_without = calculate_water_bill(
            base_month_m3 * 1000.0, cfg.water_tariffs,
            sewage_mode=cfg.sewage_mode, sewage_rate=cfg.sewage_rate,
            water_tax_fixed=cfg.water_tax_fixed, water_tax_var=cfg.water_tax_var,
        )
        total_with = calculate_water_bill(
            post_month_m3 * 1000.0, cfg.water_tariffs,
            sewage_mode=cfg.sewage_mode, sewage_rate=cfg.sewage_rate,
            water_tax_fixed=cfg.water_tax_fixed, water_tax_var=cfg.water_tax_var,
        )
        manual_water_tariff = (
            max(0.0, water_without - water_with) / pluvial_month_m3 if pluvial_month_m3 > 0 else 0.0
        )
        manual_sewage_tariff = (
            max(0.0, (total_without - total_with) - (water_without - water_with)) / pluvial_month_m3
            if pluvial_month_m3 > 0 else 0.0
        )

        lower_preset = MATERIAL_PRESETS[normalize_material_key(cfg.lower_tank_material)]
        upper_preset = MATERIAL_PRESETS[normalize_material_key(cfg.upper_tank_material)]
        manual_lower_mass = technical.lower_tank_vol / 1000.0 * lower_preset.material_density_kg_per_m3_tank
        manual_upper_mass = (
            cfg.upper_tank_vol / 1000.0 * upper_preset.material_density_kg_per_m3_tank
            if cfg.upper_tank_used else 0.0
        )
        manual_pipe_co2 = sum(
            float(p[1]) * PIPE_EMISSION_FACTORS_PER_METER.get(int(p[0]), 3.92)
            for p in cfg.pipes_list
        )
        manual_pump_embodied = PUMP_EMBEDDED_CO2.get(round(cfg.pump_power_kw / 0.735499, 2), 18.0) * cfg.pump_count
        manual_embodied = (
            manual_lower_mass * lower_preset.co2_factor_kg_per_kg
            + manual_upper_mass * upper_preset.co2_factor_kg_per_kg
            + manual_pipe_co2 + manual_pump_embodied
        )
        manual_pump_co2 = manual_kwh * case["environmental_config"].grid_co2_factor_kg_kwh
        manual_treatment_co2 = manual_cl2 * cfg.chlorine_co2_kg_per_kg
        manual_avoided_co2 = (
            technical.annual_pluvial_consumed_m3
            * case["environmental_config"].potable_water_co2_kg_m3
        )
        manual_net_annual_co2 = manual_avoided_co2 - manual_pump_co2 - manual_treatment_co2
        manual_env_payback = manual_embodied / manual_net_annual_co2 if manual_net_annual_co2 > 0 else 999.0
        manual_lifetime = manual_net_annual_co2 * cfg.analysis_period_years - manual_embodied

        manual_d_plus = float(np.sqrt(np.sum((topsis.weighted_matrix[selected_i] - topsis.ideal_best) ** 2)))
        manual_d_minus = float(np.sqrt(np.sum((topsis.weighted_matrix[selected_i] - topsis.ideal_worst) ** 2)))
        raw_min = np.min(topsis.decision_matrix, axis=0)
        raw_max = np.max(topsis.decision_matrix, axis=0)
        raw_range = raw_max - raw_min
        manual_gaps = np.divide(
            raw_max - topsis.decision_matrix[selected_i], raw_range,
            out=np.zeros(3, dtype=float), where=raw_range > 0,
        )

        lines.extend([
            f"## Caso {case['case_id']} — {case['title']} ({case['climate']})",
            "",
            f"Projeto: [`{os.path.basename(case['proj_filepath'])}`]({os.path.basename(case['proj_filepath'])}). "
            f"Série: `{case['rain_file']}`, `{len(precip)}` dias (`{_pt(years, 4)}` anos de 365,25 dias), "
            f"precipitação média anual `{_pt(float(np.sum(precip)) / years, 2)} mm/ano`; "
            f"SHA-256 `{case['rain_sha256']}`.",
            "",
            "### 1. Entradas e demanda",
            "",
            f"- Demanda total: `{cfg.residents_count} × {_pt(cfg.demand_value, 1)} = {_pt(total_demand_day, 1)} L/dia`.",
            f"- Demanda pluvial-alvo: `{_pt(total_demand_day, 1)} × {_pt(cfg.rainwater_share, 3)} = {_pt(pluvial_demand_day, 1)} L/dia`.",
            f"- Demanda total anual equivalente: `{_pt(total_demand_day, 1)} × 365,25 / 1000 = {_pt(annual_total_m3, 3)} m³/ano`.",
            f"- Área `{_pt(cfg.area, 1)} m²`, coeficiente `{_pt(cfg.runoff_coeff, 3)}`, limiar `{_pt(cfg.discard, 2)} mm`, modo `{cfg.discard_mode}`.",
            "",
            "### 2. Um dia auditado e conservação de massa",
            "",
            f"No dia de índice `{day_i + 1}`, `P={_pt(day.precip_mm, 4)} mm` e `Pef={_pt(day.eff_precip_mm, 4)} mm`. "
            f"Logo, `Vcap = {_pt(day.eff_precip_mm, 4)} × {_pt(cfg.area, 1)} × {_pt(cfg.runoff_coeff, 3)} = {_pt(day.harvested_liters, 4)} L`.",
            "",
            f"Balanço dos dois reservatórios (o recalque é transferência interna): estoque inicial + captação = estoque final + consumo pluvial + extravasamento. "
            f"`{_pt(prev_lower + prev_upper, 4)} + {_pt(day.harvested_liters, 4)} = {_pt(day.lower_tank_end_liters + day.upper_tank_end_liters, 4)} + "
            f"{_pt(day.pluvial_consumed_liters, 4)} + {_pt(day.spilled_liters, 4)}`. Resíduo: `{_pt(mass_lhs - mass_rhs, 9)} L`.",
            "",
            "### 3. Indicadores técnicos do volume TOPSIS",
            "",
            f"Volume selecionado: `{_pt(technical.lower_tank_vol, 0)} L`. Consumo anual: "
            f"`{_pt(technical.avg_pluvial_consumed_l_day, 6)} × 365,25 / 1000 = {_pt(technical.annual_pluvial_consumed_m3, 6)} m³/ano`.",
            f"Potencial: `100 × {_pt(technical.avg_pluvial_consumed_l_day, 6)} / {_pt(total_demand_day, 1)} = {_pt(technical.potential_potable_savings_pct, 6)}%`.",
            f"Ganho marginal do ponto: `{_pt(technical.delta_potential_per_m3, 6)} %/m³`; limiar técnico: `{_pt(cfg.delta_ideal, 3)} %/m³`.",
            "",
            "### 4. CAPEX, bombeamento, cloro e O&M",
            "",
            f"CAPEX = cisterna `{_pt(capex['lower'])}` + caixa `{_pt(capex['upper'])}` + bombas `{_pt(capex['pump'])}` + "
            f"tubos `{_pt(capex['piping'])}` + acessórios `{_pt(capex['accessories'])}` + mão de obra `{_pt(capex['labor'])}` "
            f"= **R$ {_pt(manual_capex)}**.",
            f"Recalque anual: `{_pt(technical.total_pumped_liters, 3)} / {_pt(years, 4)} = {_pt(annual_pumped_l, 3)} L/ano`; "
            f"partidas: `{_pt(technical.total_pump_cycles, 0)} / {_pt(years, 4)} = {_pt(annual_cycles, 3)} /ano`.",
            f"Energia: `{_pt(cfg.pump_power_kw, 4)} × [({_pt(annual_pumped_l, 3)} / {_pt(cfg.pump_flow_rate, 1)}) + "
            f"({_pt(annual_cycles, 3)} × {_pt(cfg.pump_startup_time_h, 4)})] / {_pt(cfg.pump_efficiency / 100.0, 4)} "
            f"= {_pt(manual_kwh, 6)} kWh/ano`.",
            f"Cloro equivalente: `{_pt(technical.annual_pluvial_consumed_m3, 6)} × {_pt(cfg.chlorine_dose_mg_l, 3)} / 1000 "
            f"= {_pt(manual_cl2, 6)} kg Cl2-eq/ano`; custo `= {_pt(manual_cl2, 6)} × {_pt(cfg.chlorine_cost_per_kg)} = R$ {_pt(manual_cl2_cost)}/ano`.",
            f"O&M anualizado: **R$ {_pt(economic['annual_om'])}/ano**. Todos os itens deste caso têm coeficiente variável igual a zero; "
            "portanto, o valor não depende da capacidade nem do volume tratado.",
            "",
            "### 5. Economia e VPL",
            "",
            f"Tarifa marginal evitada: água `R$ {_pt(economic['water_tariff'], 6)}/m³` + esgoto `R$ {_pt(economic['sewage_tariff'], 6)}/m³`, "
            "obtida comparando a conta para a demanda total simulada com a conta após a economia pluvial.",
            f"Ano 1: economia bruta `{_pt(technical.annual_pluvial_consumed_m3, 6)} × ({_pt(economic['water_tariff'], 6)} + {_pt(economic['sewage_tariff'], 6)}) "
            f"= R$ {_pt(manual_gross)}`; fluxo líquido `= {_pt(manual_gross)} − {_pt(economic['annual_om'])} − "
            f"{_pt(manual_kwh * cfg.elec_tariff)} − {_pt(manual_cl2_cost)} = R$ {_pt(manual_net)}`.",
            f"VPL manual: soma dos 21 fluxos descontados (ano 0 a {cfg.analysis_period_years}) = **R$ {_pt(manual_vpl)}**.",
            f"TIR: com `r={_pt(econ.tir_pct, 6)}% a.a.`, `Σ FC_t/(1+r)^t = R$ {_pt(manual_tir_residual, 9)}`. "
            f"Paybacks obtidos pela primeira mudança do acumulado para valor não negativo: simples "
            f"`{manual_payback_simple}` ano(s) e descontado `{manual_payback_discounted}` ano(s).",
            "",
        ])
        _append_cash_flow_table(lines, econ, cfg.tma * 12.0 / 100.0)

        lines.extend([
            "### 6. ACV de triagem",
            "",
            f"Impacto incorporado total: `{_pt(lca.total_embodied_co2_kg, 6)} kg CO2e`; operação anual: bomba "
            f"`{_pt(lca.annual_pumping_co2_kg, 6)}` + cloro `{_pt(lca.annual_treatment_co2_kg, 6)}`; "
            f"crédito anual de água potável: `{_pt(lca.annual_avoided_co2_kg, 6)} kg CO2e`.",
            f"Saldo de vida: `({_pt(lca.annual_avoided_co2_kg, 6)} − {_pt(lca.annual_pumping_co2_kg, 6)} − "
            f"{_pt(lca.annual_treatment_co2_kg, 6)}) × {cfg.analysis_period_years} − {_pt(lca.total_embodied_co2_kg, 6)} "
            f"= **{_pt(manual_lifetime, 6)} kg CO2e**`.",
            "",
            "### 7. Comparação item a item: conta manual × sistema",
            "",
            "Cada linha abaixo possui substituição numérica própria. `Manual` é recomposto das entradas elementares; "
            "`Sistema` é o campo retornado pelo motor. O resíduo é `|Manual − Sistema|`, exceto nas identidades de fechamento.",
            "",
            "| Item | Equação/identidade manual | Manual | Sistema | Resíduo absoluto |",
            "| --- | --- | ---: | ---: | ---: |",
            f"| Demanda total (L/d) | `N × d` | {_pt(total_demand_day, 9)} | {_pt(day.total_demand_liters, 9)} | {_pt(abs(total_demand_day - day.total_demand_liters), 12)} |",
            f"| Demanda pluvial-alvo (L/d) | `D × f` | {_pt(pluvial_demand_day, 9)} | {_pt(day.pluvial_demand_liters, 9)} | {_pt(abs(pluvial_demand_day - day.pluvial_demand_liters), 12)} |",
            f"| Captação do dia (L) | `Pef × A × C` | {_pt(day.eff_precip_mm * cfg.area * cfg.runoff_coeff, 9)} | {_pt(day.harvested_liters, 9)} | {_pt(abs(day.eff_precip_mm * cfg.area * cfg.runoff_coeff - day.harvested_liters), 12)} |",
            f"| Conservação de massa do dia (L) | `estoque inicial + captação = estoque final + consumo + extravasamento` | {_pt(mass_lhs, 9)} | {_pt(mass_rhs, 9)} | {_pt(abs(mass_lhs - mass_rhs), 12)} |",
            f"| Água pluvial anual (m³/a) | `média diária × 365,25 / 1000` | {_pt(technical.avg_pluvial_consumed_l_day * 365.25 / 1000.0, 9)} | {_pt(technical.annual_pluvial_consumed_m3, 9)} | {_pt(abs(technical.avg_pluvial_consumed_l_day * 365.25 / 1000.0 - technical.annual_pluvial_consumed_m3), 12)} |",
            f"| Água potável anual (m³/a) | `média diária × 365,25 / 1000` | {_pt(technical.avg_potable_consumed_l_day * 365.25 / 1000.0, 9)} | {_pt(technical.annual_potable_consumed_m3, 9)} | {_pt(abs(technical.avg_potable_consumed_l_day * 365.25 / 1000.0 - technical.annual_potable_consumed_m3), 12)} |",
            f"| Extravasamento anual (m³/a) | `média diária × 365,25 / 1000` | {_pt(technical.avg_spilled_l_day * 365.25 / 1000.0, 9)} | {_pt(technical.annual_spill_m3, 9)} | {_pt(abs(technical.avg_spilled_l_day * 365.25 / 1000.0 - technical.annual_spill_m3), 12)} |",
            f"| Potencial de economia (%) | `100 × Qpluvial / Dtotal` | {_pt(100.0 * technical.avg_pluvial_consumed_l_day / total_demand_day, 9)} | {_pt(technical.potential_potable_savings_pct, 9)} | {_pt(abs(100.0 * technical.avg_pluvial_consumed_l_day / total_demand_day - technical.potential_potable_savings_pct), 12)} |",
            f"| Fechamento dos estados de atendimento (%) | `pleno + parcial + nulo = 100` | 100,000000000 | {_pt(technical.pct_days_full_satisfaction + technical.pct_days_partial_satisfaction + technical.pct_days_null_satisfaction, 9)} | {_pt(abs(100.0 - technical.pct_days_full_satisfaction - technical.pct_days_partial_satisfaction - technical.pct_days_null_satisfaction), 12)} |",
            f"| Ganho marginal (%/m³) | `Δpotencial / ΔV` | {_pt(manual_delta, 9)} | {_pt(technical.delta_potential_per_m3, 9)} | {_pt(abs(manual_delta - technical.delta_potential_per_m3), 12)} |",
            f"| CAPEX — cisterna inferior (R$) | `interpolação × μmaterial` | {_pt(manual_lower_capex, 9)} | {_pt(capex['lower'], 9)} | {_pt(abs(manual_lower_capex - capex['lower']), 12)} |",
            f"| CAPEX — reservatório superior (R$) | `interpolação × μmaterial` | {_pt(manual_upper_capex, 9)} | {_pt(capex['upper'], 9)} | {_pt(abs(manual_upper_capex - capex['upper']), 12)} |",
            f"| CAPEX — bombas (R$) | `preço unitário × quantidade` | {_pt(manual_pump_capex, 9)} | {_pt(capex['pump'], 9)} | {_pt(abs(manual_pump_capex - capex['pump']), 12)} |",
            f"| CAPEX — tubos e conexões (R$) | `max(350; 1,25 Σ L·preçoDN)` | {_pt(manual_piping_capex, 9)} | {_pt(capex['piping'], 9)} | {_pt(abs(manual_piping_capex - capex['piping']), 12)} |",
            f"| CAPEX — acessórios (R$) | `max(500; 150 + 0,08·tanques)` | {_pt(manual_accessories_capex, 9)} | {_pt(capex['accessories'], 9)} | {_pt(abs(manual_accessories_capex - capex['accessories']), 12)} |",
            f"| CAPEX — mão de obra (R$) | `max(1400; 0,30·subtotal)` | {_pt(manual_labor_capex, 9)} | {_pt(capex['labor'], 9)} | {_pt(abs(manual_labor_capex - capex['labor']), 12)} |",
            f"| CAPEX total (R$) | `Σ componentes` | {_pt(manual_capex_from_rules, 9)} | {_pt(economic['capex'], 9)} | {_pt(abs(manual_capex_from_rules - economic['capex']), 12)} |",
            f"| Horas equivalentes de bombeamento (h/a) | `(V/Q + n·tpartida)/η` | {_pt((t_rec + t_start) / max(0.01, cfg.pump_efficiency / 100.0), 9)} | {_pt(economic['pump_hrs'], 9)} | {_pt(abs((t_rec + t_start) / max(0.01, cfg.pump_efficiency / 100.0) - economic['pump_hrs']), 12)} |",
            f"| Energia da bomba (kWh/a) | `potência × horas equivalentes` | {_pt(manual_kwh, 9)} | {_pt(economic['pump_kwh'], 9)} | {_pt(abs(manual_kwh - economic['pump_kwh']), 12)} |",
            f"| Cloro equivalente (kg/a) | `m³ × mg/L / 1000` | {_pt(manual_cl2, 9)} | {_pt(lca.annual_chlorine_kg, 9)} | {_pt(abs(manual_cl2 - lca.annual_chlorine_kg), 12)} |",
            f"| Custo de cloro (R$/a) | `massa × preço/kg` | {_pt(manual_cl2_cost, 9)} | {_pt(economic['cl2_cost'], 9)} | {_pt(abs(manual_cl2_cost - economic['cl2_cost']), 12)} |",
            f"| O&M anual (R$/a) | `Σ 12/p · (fixo + variável·m³mês)` | {_pt(manual_annual_om, 9)} | {_pt(economic['annual_om'], 9)} | {_pt(abs(manual_annual_om - economic['annual_om']), 12)} |",
            f"| Tarifa efetiva de água (R$/m³) | `Δconta de água / m³ poupado` | {_pt(manual_water_tariff, 9)} | {_pt(economic['water_tariff'], 9)} | {_pt(abs(manual_water_tariff - economic['water_tariff']), 12)} |",
            f"| Tarifa efetiva de esgoto (R$/m³) | `(Δconta total − Δágua) / m³ poupado` | {_pt(manual_sewage_tariff, 9)} | {_pt(economic['sewage_tariff'], 9)} | {_pt(abs(manual_sewage_tariff - economic['sewage_tariff']), 12)} |",
            f"| Economia bruta ano 1 (R$) | `m³ × (Tágua + Tesgoto)` | {_pt(manual_gross, 9)} | {_pt(first.total_gross_savings_brl, 9)} | {_pt(abs(manual_gross - first.total_gross_savings_brl), 12)} |",
            f"| Fluxo líquido ano 1 (R$) | `bruta − energia − O&M − cloro` | {_pt(manual_net, 9)} | {_pt(first.net_cash_flow_nominal_brl, 9)} | {_pt(abs(manual_net - first.net_cash_flow_nominal_brl), 12)} |",
            f"| VPL (R$) | `Σ FCt/(1+i)^t` | {_pt(manual_vpl, 9)} | {_pt(econ.vpl, 9)} | {_pt(abs(manual_vpl - econ.vpl), 12)} |",
            f"| Resíduo da TIR (R$) | `Σ FCt/(1+TIR)^t` | {_pt(manual_tir_residual, 9)} | 0,000000000 | {_pt(abs(manual_tir_residual), 12)} |",
            f"| Payback simples (anos) | `primeiro acumulado nominal ≥ 0` | {manual_payback_simple} | {econ.payback_simple_years} | {_pt(abs((manual_payback_simple or 0) - (econ.payback_simple_years or 0)), 12)} |",
            f"| Payback descontado (anos) | `primeiro acumulado descontado ≥ 0` | {manual_payback_discounted} | {econ.payback_discounted_years} | {_pt(abs((manual_payback_discounted or 0) - (econ.payback_discounted_years or 0)), 12)} |",
            f"| Massa da cisterna inferior (kg) | `V × kg material/m³` | {_pt(manual_lower_mass, 9)} | {_pt(lca.lower_tank_mass_kg, 9)} | {_pt(abs(manual_lower_mass - lca.lower_tank_mass_kg), 12)} |",
            f"| Massa do reservatório superior (kg) | `Vsup × kg material/m³` | {_pt(manual_upper_mass, 9)} | {_pt(lca.upper_tank_mass_kg, 9)} | {_pt(abs(manual_upper_mass - lca.upper_tank_mass_kg), 12)} |",
            f"| CO2e incorporado dos tubos (kg) | `Σ L × fatorDN` | {_pt(manual_pipe_co2, 9)} | {_pt(lca.total_pipes_co2_kg, 9)} | {_pt(abs(manual_pipe_co2 - lca.total_pipes_co2_kg), 12)} |",
            f"| CO2e incorporado das bombas (kg) | `fator unitário × quantidade` | {_pt(manual_pump_embodied, 9)} | {_pt(lca.pump_embodied_co2_kg, 9)} | {_pt(abs(manual_pump_embodied - lca.pump_embodied_co2_kg), 12)} |",
            f"| CO2e incorporado total (kg) | `Σ materiais e equipamentos` | {_pt(manual_embodied, 9)} | {_pt(lca.total_embodied_co2_kg, 9)} | {_pt(abs(manual_embodied - lca.total_embodied_co2_kg), 12)} |",
            f"| CO2e do bombeamento (kg/a) | `kWh × fator da rede` | {_pt(manual_pump_co2, 9)} | {_pt(lca.annual_pumping_co2_kg, 9)} | {_pt(abs(manual_pump_co2 - lca.annual_pumping_co2_kg), 12)} |",
            f"| CO2e do tratamento (kg/a) | `kg Cl2 × fator do insumo` | {_pt(manual_treatment_co2, 9)} | {_pt(lca.annual_treatment_co2_kg, 9)} | {_pt(abs(manual_treatment_co2 - lca.annual_treatment_co2_kg), 12)} |",
            f"| CO2e evitado da rede (kg/a) | `m³ poupado × fator da água` | {_pt(manual_avoided_co2, 9)} | {_pt(lca.annual_avoided_co2_kg, 9)} | {_pt(abs(manual_avoided_co2 - lca.annual_avoided_co2_kg), 12)} |",
            f"| CO2e líquido anual (kg/a) | `evitado − bomba − tratamento` | {_pt(manual_net_annual_co2, 9)} | {_pt(lca.net_annual_avoided_co2_kg, 9)} | {_pt(abs(manual_net_annual_co2 - lca.net_annual_avoided_co2_kg), 12)} |",
            f"| Payback ambiental (anos) | `incorporado / líquido anual` | {_pt(manual_env_payback, 9)} | {_pt(lca.environmental_payback_years, 9)} | {_pt(abs(manual_env_payback - lca.environmental_payback_years), 12)} |",
            f"| CO2e líquido de vida (kg) | `líquido anual × vida − incorporado` | {_pt(manual_lifetime, 9)} | {_pt(lca.lifetime_net_co2_saved_kg, 9)} | {_pt(abs(manual_lifetime - lca.lifetime_net_co2_saved_kg), 12)} |",
            f"| TOPSIS D+ | `distância euclidiana ao ideal` | {_pt(manual_d_plus, 12)} | {_pt(topsis.dist_best[selected_i], 12)} | {_pt(abs(manual_d_plus - topsis.dist_best[selected_i]), 15)} |",
            f"| TOPSIS D− | `distância euclidiana ao anti-ideal` | {_pt(manual_d_minus, 12)} | {_pt(topsis.dist_worst[selected_i], 12)} | {_pt(abs(manual_d_minus - topsis.dist_worst[selected_i]), 15)} |",
            f"| Score TOPSIS | `D−/(D+ + D−)` | {_pt(manual_score, 12)} | {_pt(topsis.scores[selected_i], 12)} | {_pt(abs(manual_score - topsis.scores[selected_i]), 15)} |",
            f"| Gap técnico | `(máx − x)/(máx − mín)` | {_pt(manual_gaps[0], 12)} | {_pt(topsis.criterion_gap_to_best[selected_i, 0], 12)} | {_pt(abs(manual_gaps[0] - topsis.criterion_gap_to_best[selected_i, 0]), 15)} |",
            f"| Gap econômico | `(máx − x)/(máx − mín)` | {_pt(manual_gaps[1], 12)} | {_pt(topsis.criterion_gap_to_best[selected_i, 1], 12)} | {_pt(abs(manual_gaps[1] - topsis.criterion_gap_to_best[selected_i, 1]), 15)} |",
            f"| Gap ambiental | `(máx − x)/(máx − mín)` | {_pt(manual_gaps[2], 12)} | {_pt(topsis.criterion_gap_to_best[selected_i, 2], 12)} | {_pt(abs(manual_gaps[2] - topsis.criterion_gap_to_best[selected_i, 2]), 15)} |",
            "",
        ])
        _append_topsis_audit(lines, topsis)

    lines.extend([
        "## Referências e rastreabilidade",
        "",
        "- [Atlas de fluxogramas metodológicos](../triton/docs/fluxogramas_metodologicos.md): cadeia visual das equações e decisões implementadas.",
        "- GHISI, E.; CORDOVA, M. M. *Netuno 4 — Manual do Usuário*. UFSC, 2014. Cópia local em "
        "[`additional_material/documentation/Manual-Triton-4_Junho2014.pdf`](../additional_material/documentation/Manual-Triton-4_Junho2014.pdf).",
        "- ROCHA, V. L. *Validação do algoritmo do programa Triton para avaliação do potencial de economia de "
        "água potável e dimensionamento de reservatórios de sistemas de aproveitamento de água pluvial em "
        "edificações*. Dissertação (Mestrado em Engenharia Civil) — UFSC, 2009. "
        "[Registro institucional](https://repositorio.ufsc.br/handle/123456789/92966).",
        "- HWANG, C.-L.; YOON, K. *Multiple Attribute Decision Making*. Springer, 1981. "
        "[DOI](https://doi.org/10.1007/978-3-642-48318-9).",
        "- [MCTI/SIRENE — fatores de emissão](https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao). "
        "O fator deve ser escolhido para o período do estudo; "
        "o valor padrão do software é apenas uma hipótese editável de triagem.",
        "",
    ])

    with open(output_path, "w", encoding="utf-8", newline="\n") as stream:
        stream.write("\n".join(lines))


def _volume_markers(case, volume_l):
    markers = []
    if math.isclose(volume_l, case["opt_tech_vol"], abs_tol=1e-9):
        markers.append("T")
    if math.isclose(volume_l, case["opt_econ_vol"], abs_tol=1e-9):
        markers.append("E")
    if math.isclose(volume_l, case["opt_env_vol"], abs_tol=1e-9):
        markers.append("A")
    if math.isclose(volume_l, case["opt_topsis_vol"], abs_tol=1e-9):
        markers.append("M")
    return "/".join(markers) or "—"


def _case_point(case, volume_l):
    for index, technical in enumerate(case["tech_sweep"].results_by_volume):
        if math.isclose(technical.lower_tank_vol, volume_l, abs_tol=1e-9):
            return (
                index,
                technical,
                case["econ_sweep"][index],
                case["env_sweep"].sweep_details[index]["lca_result"],
            )
    raise ValueError(f"Volume {volume_l} L ausente no caso {case['case_id']}.")


def write_complete_detail_report(results, output_path):
    """Gera o detalhamento comparativo completo sem duplicação manual de números."""
    lines = [
        f"# Detalhamento completo dos três modelos — Triton {__version__}",
        "",
        "> Documento gerado por `python scripts/generate_reference_case_studies.py`. "
        "Entradas e resultados vêm dos mesmos objetos usados no estudo de verificação; não edite as tabelas à mão.",
        "",
        "Este relatório preserva a visão comparativa dos três modelos. O "
        "[`ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md`](ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md) "
        "faz a conta manual e mede resíduos; este arquivo fornece todos os dados de entrada e compara os resultados "
        "item a item, tanto entre os casos quanto entre os volumes de cada varredura.",
        "",
        "O [`atlas de fluxogramas metodológicos`](../triton/docs/fluxogramas_metodologicos.md) detalha a sequência "
        "das equações hidráulicas, econômicas, ambientais, multicritério e de verificação.",
        "",
        "## 1. Diagrama de influência do volume da cisterna",
        "",
        "O diagrama continua sendo parte da metodologia. Ele impede atribuir causalidade direta a parâmetros que "
        "são entradas independentes ou consequências endógenas da simulação.",
        "",
        "```mermaid",
        "flowchart LR",
        "    V[\"Capacidade inferior V\"] --> EST[\"Limite do estoque diário\"]",
        "    CH[\"Chuva, área, coeficiente e descarte\"] --> BAL[\"Balanço YAS diário\"]",
        "    DEM[\"Demanda e fração pluvial\"] --> BAL",
        "    EST --> BAL",
        "    BAL --> AT[\"Água pluvial atendida\"]",
        "    BAL --> EX[\"Extravasamento e falhas\"]",
        "    BAL --> REC[\"Recalque e partidas\"]",
        "    REC --> EN[\"Energia de bombeamento\"]",
        "    AT --> CL[\"Massa de cloro equivalente\"]",
        "    AT --> FAT[\"Conta de água e esgoto evitada\"]",
        "    AT --> CRED[\"Crédito ambiental da água evitada\"]",
        "    V --> PRE[\"Preço da cisterna\"]",
        "    V --> MASSA[\"Massa e CO2e incorporado da cisterna\"]",
        "    PRE --> CAPEX[\"CAPEX total\"]",
        "    EN --> OPEX[\"OPEX e CO2e operacional\"]",
        "    CL --> OPEX",
        "    FAT --> FLUXO[\"Fluxo de caixa, VPL e payback\"]",
        "    CAPEX --> FLUXO",
        "    MASSA --> ACV[\"Saldo de ciclo de vida\"]",
        "    OPEX --> ACV",
        "    CRED --> ACV",
        "    AT --> TOP[\"TOPSIS\"]",
        "    FLUXO --> TOP",
        "    ACV --> TOP",
        "    INDEP[\"Caixa superior, tubos, bomba e fatores locais\"] -. \"entradas do cenário\" .-> REC",
        "    INDEP -.-> CAPEX",
        "    INDEP -.-> ACV",
        "```",
        "",
        "| Classe de relação com `V` | Itens | Interpretação |",
        "| --- | --- | --- |",
        "| Direta | preço, massa e CO2e incorporado da cisterna inferior | função explícita da capacidade e do material |",
        "| Endógena | atendimento, extravasamento, falhas, recalque, energia, cloro, receita evitada e O&M variável por consumo | resultado do balanço repetido para cada `V` |",
        "| Independente | caixa superior, tubos, bomba, tarifas e fatores ambientais | entrada mantida fixa na varredura, salvo cenário explicitamente alterado |",
        "| Derivada | VPL, paybacks, ACV, ótimos e TOPSIS | combinação das três classes anteriores |",
        "",
        "## 2. Entradas dos três modelos — comparação item a item",
        "",
    ]

    case_headers = [f"Caso {case['case_id']} — {case['title']}" for case in results]
    def add_input_row(label, formatter):
        lines.append("| " + label + " | " + " | ".join(str(formatter(case)) for case in results) + " |")

    def begin_comparison_table(title):
        lines.extend([
            f"### {title}",
            "",
            "| Item | " + " | ".join(case_headers) + " |",
            "| --- | " + " | ".join("---" for _ in results) + " |",
        ])

    begin_comparison_table("2.1. Edificação, clima e demanda")
    add_input_row("Tipologia", lambda c: c["typology"])
    add_input_row("Clima / série", lambda c: f"{c['climate']} / `{c['rain_file']}`")
    add_input_row("Dias e anos simulados", lambda c: f"{len(c['precip_data'])} dias / {_pt(c['years_simulated'], 4)} anos")
    add_input_row("Precipitação média anual", lambda c: f"{_pt(float(np.sum(c['precip_data'])) / c['years_simulated'], 2)} mm/a")
    add_input_row("Área de captação", lambda c: f"{_pt(c['config'].area, 1)} m²")
    add_input_row("Coeficiente de escoamento", lambda c: _pt(c["config"].runoff_coeff, 3))
    add_input_row("Limiar de descarte", lambda c: f"{_pt(c['config'].discard, 2)} mm")
    add_input_row("Modo / intervalo de descarte", lambda c: f"modo {c['config'].discard_mode} / {c['config'].discard_days_interval} dias")
    add_input_row("Ocupantes", lambda c: c["config"].residents_count)
    add_input_row("Demanda unitária", lambda c: f"{_pt(c['config'].demand_value, 1)} L/pessoa·dia")
    add_input_row("Demanda total", lambda c: f"{_pt(c['daily_demand_l'], 1)} L/dia")
    add_input_row("Fração pluvial", lambda c: f"{_pt(c['config'].rainwater_share * 100.0, 1)}%")
    add_input_row("Demanda pluvial-alvo", lambda c: f"{_pt(c['daily_demand_l'] * c['config'].rainwater_share, 1)} L/dia")
    lines.extend(["", "Séries pluviométricas verificadas por SHA-256:", ""])
    for case in results:
        lines.append(f"- Caso {case['case_id']}: `{case['rain_sha256']}`")
    lines.append("")

    begin_comparison_table("2.2. Reservatórios, rede e bombeamento")
    add_input_row("Varredura inferior", lambda c: f"0–{_pt(c['config'].lower_tank_max, 0)} L; passo {_pt(c['config'].lower_tank_step, 0)} L")
    add_input_row("Limiar técnico marginal", lambda c: f"{_pt(c['config'].delta_ideal, 3)} %/m³")
    add_input_row("Reservatório superior", lambda c: f"{_pt(c['config'].upper_tank_vol, 0)} L")
    add_input_row("Gatilho de recalque", lambda c: f"{_pt(c['config'].pumping_threshold, 1)} L")
    add_input_row("Materiais inferior / superior", lambda c: f"{c['config'].lower_tank_material} / {c['config'].upper_tank_material}")
    add_input_row("Tubulações", lambda c: c["pipes_str"])
    add_input_row("Potência da bomba", lambda c: f"{_pt(c['config'].pump_power_kw, 3)} kW")
    add_input_row("Vazão / eficiência / quantidade", lambda c: f"{_pt(c['config'].pump_flow_rate, 0)} L/h / {_pt(c['config'].pump_efficiency, 1)}% / {c['config'].pump_count} un.")
    add_input_row("Tempo equivalente por partida", lambda c: f"{_pt(c['config'].pump_startup_time_h, 4)} h")
    lines.append("")

    begin_comparison_table("2.3. Premissas econômicas, operacionais e de tratamento")
    add_input_row("Tarifa de energia", lambda c: f"R$ {_pt(c['config'].elec_tariff, 2)}/kWh")
    add_input_row("Dose / preço / fator do cloro", lambda c: f"{_pt(c['config'].chlorine_dose_mg_l, 2)} mg/L / R$ {_pt(c['config'].chlorine_cost_per_kg, 2)}/kg / {_pt(c['config'].chlorine_co2_kg_per_kg, 2)} kg CO2e/kg")
    add_input_row("Esgoto", lambda c: f"modo {c['config'].sewage_mode}; {_pt(c['config'].sewage_rate, 1)}%")
    add_input_row("TMA / inflação", lambda c: f"{_pt(c['config'].tma * 12.0, 2)}% a.a. / {_pt(c['config'].inflation * 12.0, 2)}% a.a.")
    add_input_row("Horizonte", lambda c: f"{c['config'].analysis_period_years} anos")
    lines.append("")

    lines.extend(["### 2.4. Tarifas de água por caso", ""])
    for case in results:
        lines.extend([
            f"#### Caso {case['case_id']} — {case['title']}",
            "",
            "| Início (m³/mês) | Fim (m³/mês) | Valor (R$) | Regra |",
            "| ---: | ---: | ---: | --- |",
        ])
        for start, end, value, rule in case["config"].water_tariffs:
            lines.append(
                f"| {_pt(start, 0)} | {_pt(end, 0)} | {_pt(value, 2)} | "
                f"{'parcela fixa' if rule == -1 else 'faixa progressiva'} |"
            )
        lines.append("")

    lines.extend(["### 2.5. O&M por caso", ""])
    for case in results:
        lines.extend([
            f"#### Caso {case['case_id']} — {case['title']}",
            "",
            "| Item | Periodicidade (meses) | Parcela fixa (R$) | Variável (R$/m³ consumido no mês) |",
            "| --- | ---: | ---: | ---: |",
        ])
        for name, period, fixed, variable in case["config"].op_costs:
            lines.append(f"| {name} | {period} | {_pt(fixed)} | {_pt(variable)} |")
        lines.append("")

    lines.extend([
        "## 3. Síntese comparativa dos ótimos",
        "",
        "`T` = técnico; `E` = econômico; `A` = ambiental; `M` = multicritério TOPSIS.",
        "",
        "### Volumes selecionados",
        "",
        "| Caso | T (L) | E (L) | A (L) | M (L) |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    for case in results:
        lines.append(
            f"| Caso {case['case_id']} | {_pt(case['opt_tech_vol'], 0)} | {_pt(case['opt_econ_vol'], 0)} | "
            f"{_pt(case['opt_env_vol'], 0)} | {_pt(case['opt_topsis_vol'], 0)} |"
        )
    lines.extend([
        "",
        "### Diagnóstico da alternativa TOPSIS",
        "",
        "| Caso | Score M | Gap técnico M | Gap econômico M | Gap ambiental M |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    for case in results:
        topsis = case["topsis_res"]
        gaps = topsis.criterion_gap_to_best[topsis.best_index] * 100.0
        lines.append(
            f"| Caso {case['case_id']} | {_pt(topsis.scores[topsis.best_index], 6)} | "
            f"{_pt(gaps[0], 2)}% | {_pt(gaps[1], 2)}% | {_pt(gaps[2], 2)}% |"
        )
    lines.append("")

    for case in results:
        lines.extend([
            f"## 4.{case['case_id']}. Caso {case['case_id']} — {case['title']}",
            "",
            "### Comparação direta das quatro decisões",
            "",
            "Volumes coincidentes aparecem uma única vez com mais de um marcador. Esta tabela mostra diretamente "
            "o custo da concessão: quanto cada decisão entrega nos outros eixos.",
            "",
            "#### Desempenho hídrico e econômico",
            "",
            "| Marcador | V (L) | Água (m³/a) | Economia (%) | Extravasamento (m³/a) | CAPEX (R$) | VPL (R$) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        decision_volumes = []
        for volume_l in (case["opt_tech_vol"], case["opt_econ_vol"], case["opt_env_vol"], case["opt_topsis_vol"]):
            if not any(math.isclose(volume_l, existing, abs_tol=1e-9) for existing in decision_volumes):
                decision_volumes.append(volume_l)
        decision_points = []
        for volume_l in sorted(decision_volumes):
            i, tech, economic, lca = _case_point(case, volume_l)
            topsis = case["topsis_res"]
            gaps = topsis.criterion_gap_to_best[i] * 100.0
            decision_points.append((volume_l, i, tech, economic, lca, gaps))
            lines.append(
                f"| {_volume_markers(case, volume_l)} | {_pt(volume_l, 0)} | {_pt(tech.annual_pluvial_consumed_m3, 3)} | "
                f"{_pt(tech.potential_potable_savings_pct, 3)} | {_pt(tech.annual_spill_m3, 3)} | "
                f"{_pt(economic['capex'])} | {_pt(economic['vpl'])} |"
            )
        lines.extend([
            "",
            "#### Operação e desempenho ambiental",
            "",
            "| Marcador | V (L) | Energia (kWh/a) | Cloro (kg/a) | CO2e líquido de vida (kg) |",
            "| --- | ---: | ---: | ---: | ---: |",
        ])
        for volume_l, i, tech, economic, lca, gaps in decision_points:
            lines.append(
                f"| {_volume_markers(case, volume_l)} | {_pt(volume_l, 0)} | "
                f"{_pt(economic['pump_kwh'], 3)} | {_pt(economic['cl2_kg'], 4)} | "
                f"{_pt(lca.lifetime_net_co2_saved_kg, 2)} |"
            )
        lines.extend([
            "",
            "#### Diagnóstico TOPSIS",
            "",
            "| Marcador | V (L) | Score | Gap T | Gap E | Gap A | Rank |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        for volume_l, i, tech, economic, lca, gaps in decision_points:
            lines.append(
                f"| {_volume_markers(case, volume_l)} | {_pt(volume_l, 0)} | {_pt(topsis.scores[i], 6)} | "
                f"{_pt(gaps[0], 2)}% | {_pt(gaps[1], 2)}% | {_pt(gaps[2], 2)}% | "
                f"{int(topsis.rankings[i])} |"
            )
        lines.extend([
            "",
            "### Varredura técnica completa",
            "",
            "#### Balanço e economia de água",
            "",
            "| Ótimo | V (L) | Água pluvial (m³/a) | Água potável (m³/a) | Extravasamento (m³/a) | Economia (%) | Ganho marginal (%/m³) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        for tech in case["tech_sweep"].results_by_volume:
            lines.append(
                f"| {_volume_markers(case, tech.lower_tank_vol)} | {_pt(tech.lower_tank_vol, 0)} | "
                f"{_pt(tech.annual_pluvial_consumed_m3, 3)} | {_pt(tech.annual_potable_consumed_m3, 3)} | "
                f"{_pt(tech.annual_spill_m3, 3)} | {_pt(tech.potential_potable_savings_pct, 3)} | "
                f"{_pt(tech.delta_potential_per_m3, 4)} |"
            )
        lines.extend([
            "",
            "#### Atendimento e recalque",
            "",
            "| Ótimo | V (L) | Pleno (%) | Parcial (%) | Nulo (%) | Recalque (m³/a) | Partidas/a |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        for tech in case["tech_sweep"].results_by_volume:
            lines.append(
                f"| {_volume_markers(case, tech.lower_tank_vol)} | {_pt(tech.lower_tank_vol, 0)} | "
                f"{_pt(tech.pct_days_full_satisfaction, 2)} | {_pt(tech.pct_days_partial_satisfaction, 2)} | "
                f"{_pt(tech.pct_days_null_satisfaction, 2)} | "
                f"{_pt(tech.total_pumped_liters / case['years_simulated'] / 1000.0, 3)} | "
                f"{_pt(tech.total_pump_cycles / case['years_simulated'], 2)} |"
            )

        lines.extend([
            "",
            "### Varredura econômica completa",
            "",
            "#### CAPEX — reservatórios, bombas e tubos",
            "",
            "| Ótimo | V (L) | Cisterna (R$) | Superior (R$) | Bombas (R$) | Tubos (R$) |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ])
        for economic in case["econ_sweep"]:
            capex = economic["capex_breakdown"]
            lines.append(
                f"| {_volume_markers(case, economic['vol_l'])} | {_pt(economic['vol_l'], 0)} | {_pt(capex['lower'])} | "
                f"{_pt(capex['upper'])} | {_pt(capex['pump'])} | {_pt(capex['piping'])} |"
            )
        lines.extend([
            "",
            "#### CAPEX — complementos e total",
            "",
            "| Ótimo | V (L) | Acessórios (R$) | Mão de obra (R$) | CAPEX total (R$) |",
            "| --- | ---: | ---: | ---: | ---: |",
        ])
        for economic in case["econ_sweep"]:
            capex = economic["capex_breakdown"]
            lines.append(
                f"| {_volume_markers(case, economic['vol_l'])} | {_pt(economic['vol_l'], 0)} | "
                f"{_pt(capex['accessories'])} | {_pt(capex['labor'])} | {_pt(economic['capex'])} |"
            )
        lines.extend([
            "",
            "#### Operação e tarifas efetivas",
            "",
            "| Ótimo | V (L) | Energia (kWh/a) | Cloro (kg/a) | O&M (R$/a) | T água (R$/m³) | T esgoto (R$/m³) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        for economic in case["econ_sweep"]:
            lines.append(
                f"| {_volume_markers(case, economic['vol_l'])} | {_pt(economic['vol_l'], 0)} | "
                f"{_pt(economic['pump_kwh'], 3)} | {_pt(economic['cl2_kg'], 4)} | "
                f"{_pt(economic['annual_om'])} | {_pt(economic['water_tariff'], 4)} | "
                f"{_pt(economic['sewage_tariff'], 4)} |"
            )
        lines.extend([
            "",
            "#### Indicadores financeiros",
            "",
            "| Ótimo | V (L) | VPL (R$) | TIR (%) | PB simples (a) | PB descontado (a) |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ])
        for economic in case["econ_sweep"]:
            lines.append(
                f"| {_volume_markers(case, economic['vol_l'])} | {_pt(economic['vol_l'], 0)} | "
                f"{_pt(economic['vpl'])} | {_pt(economic['tir'], 3)} | "
                f"{_pt(economic['payback_s'], 0)} | {_pt(economic['payback_d'], 0)} |"
            )

        lines.extend([
            "",
            "### Varredura ambiental e multicritério completa",
            "",
            "#### Inventário e operação anual",
            "",
            "| Ótimo | V (L) | Massa inferior (kg) | CO2e incorporado (kg) | CO2e bomba (kg/a) | CO2e cloro (kg/a) | CO2e água evitada (kg/a) | CO2e líquido (kg/a) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        topsis = case["topsis_res"]
        for i, detail in enumerate(case["env_sweep"].sweep_details):
            lca = detail["lca_result"]
            lines.append(
                f"| {_volume_markers(case, detail['volume_l'])} | {_pt(detail['volume_l'], 0)} | "
                f"{_pt(lca.lower_tank_mass_kg, 2)} | {_pt(lca.total_embodied_co2_kg, 2)} | "
                f"{_pt(lca.annual_pumping_co2_kg, 3)} | {_pt(lca.annual_treatment_co2_kg, 3)} | "
                f"{_pt(lca.annual_avoided_co2_kg, 3)} | {_pt(lca.net_annual_avoided_co2_kg, 3)} |"
            )
        lines.extend([
            "",
            "#### Ciclo de vida e decisão TOPSIS",
            "",
            "| Ótimo | V (L) | CO2e líquido de vida (kg) | PB ambiental (a) | D+ | D− | Score | Rank |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        for i, detail in enumerate(case["env_sweep"].sweep_details):
            lca = detail["lca_result"]
            lines.append(
                f"| {_volume_markers(case, detail['volume_l'])} | {_pt(detail['volume_l'], 0)} | "
                f"{_pt(lca.lifetime_net_co2_saved_kg, 2)} | {_pt(lca.environmental_payback_years, 3)} | "
                f"{_pt(topsis.dist_best[i], 6)} | {_pt(topsis.dist_worst[i], 6)} | "
                f"{_pt(topsis.scores[i], 6)} | {int(topsis.rankings[i])} |"
            )
        lines.extend([
            "",
            "#### Distância relativa ao melhor por critério",
            "",
            "| Ótimo | V (L) | Gap técnico | Gap econômico | Gap ambiental |",
            "| --- | ---: | ---: | ---: | ---: |",
        ])
        for i, detail in enumerate(case["env_sweep"].sweep_details):
            gaps = topsis.criterion_gap_to_best[i] * 100.0
            lines.append(
                f"| {_volume_markers(case, detail['volume_l'])} | {_pt(detail['volume_l'], 0)} | "
                f"{_pt(gaps[0], 2)}% | {_pt(gaps[1], 2)}% | {_pt(gaps[2], 2)}% |"
            )
        lines.append("")

    lines.extend([
        "## 5. Cobertura e rastreabilidade",
        "",
        "| Grupo | Fornecido neste documento | Comparação manual × sistema |",
        "| --- | --- | --- |",
        "| Entradas hidrológicas e de demanda | comparação lado a lado dos três casos | seção 7 de cada caso no estudo de verificação |",
        "| Balanço e indicadores técnicos | todas as alternativas da varredura | captação, massa, consumos, extravasamento, economia, atendimento e ganho marginal |",
        "| CAPEX e OPEX | seis componentes de CAPEX, energia, cloro, O&M e tarifas em todos os volumes | componentes, totais e fluxo anual termo a termo |",
        "| ACV | massas, impactos incorporados e operacionais, crédito, saldo e payback em todos os volumes | inventário elementar, saldo anual e saldo de vida |",
        "| TOPSIS | D+, D−, score, três gaps e ranking em todos os volumes | distâncias, score e gaps recalculados |",
        "",
        "A concordância numérica verifica a implementação das equações escolhidas. Ela não transforma premissas de "
        "triagem em dados medidos nem substitui validação externa, cotações, EPDs, ensaios ou projeto executivo.",
        "",
        "Documentos associados:",
        "",
        "- [`ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md`](ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md): conta manual e resíduos.",
        "- [`PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md`](PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md): justificativa causal e equações.",
        "- [`../scripts/generate_reference_case_studies.py`](../scripts/generate_reference_case_studies.py): geração reprodutível.",
        "",
    ])

    with open(output_path, "w", encoding="utf-8", newline="\n") as stream:
        stream.write("\n".join(lines))


def main():
    print("=" * 80)
    print("TRITON 5 — ESTUDO DE CASO INTEGRADO DE 3 MODELOS DE REFERÊNCIA")
    print("=" * 80)

    # ──────────────────────────────────────────────────────────────────────────
    # CASO 1: RESIDENCIAL UNIFAMILIAR (FLORIANÓPOLIS - Florianopolis1.csv)
    # ──────────────────────────────────────────────────────────────────────────
    casan_tariffs = [
        (0.0, 0.0, 46.34, -1),
        (0.0, 10.0, 3.08, 1),
        (10.0, 25.0, 14.31, 1),
        (25.0, 50.0, 19.14, 1),
        (50.0, 999999.0, 24.08, 1),
    ]
    res1 = run_case_study(
        case_id="1",
        title="Residência Unifamiliar Sustentável",
        typology="Residencial Unifamiliar",
        rain_filename="Florianopolis1.csv",
        area_m2=180.0,
        runoff_c=0.85,
        discard_mm=2.0,
        discard_mode=1,
        discard_days=7,
        residents=4,
        demand_l_hab_day=180.0,
        share_pct=40.0,
        upper_vol_l=500.0,
        upper_used=True,
        pump_thresh_pct=10.0,
        sweep_max_l=10000.0,
        sweep_step_l=500.0,
        delta_ideal=5.0,
        lower_mat="PEAD",
        upper_mat="PEAD",
        pipes=[(100, 25.0), (50, 15.0)],
        pump_power_kw=0.368,
        pump_flow_rate=2280.0,
        pump_efficiency=55.0,
        pump_count=1,
        pump_startup_h=0.03,
        elec_tariff=0.95,
        chlorine_enabled=True,
        chlorine_dose=2.0,
        chlorine_cost_kg=25.0,
        chlorine_co2_kg=25.0,
        water_tariffs=casan_tariffs,
        sewage_rate=100.0,
        sewage_mode=1,
        tma_annual=10.0,
        inflation_annual=4.0
    )

    # ──────────────────────────────────────────────────────────────────────────
    # CASO 2: EDIFÍCIO COMERCIAL / CORPORATIVO (BRASÍLIA - Brasilia2.csv)
    # ──────────────────────────────────────────────────────────────────────────
    caesb_commercial_tariffs = [
        (0.0, 10.0, 7.80, 0),
        (10.0, 25.0, 15.60, 0),
        (25.0, 50.0, 22.40, 0),
        (50.0, 999999.0, 28.90, 0),
    ]
    res2 = run_case_study(
        case_id="2",
        title="Edifício Corporativo EcoOffice",
        typology="Comercial / Escritórios",
        rain_filename="Brasilia2.csv",
        area_m2=650.0,
        runoff_c=0.90,
        discard_mm=2.0,
        discard_mode=2,
        discard_days=7,
        residents=80,
        demand_l_hab_day=50.0,
        share_pct=65.0,
        upper_vol_l=3000.0,
        upper_used=True,
        pump_thresh_pct=15.0,
        sweep_max_l=50000.0,
        sweep_step_l=2500.0,
        delta_ideal=3.0,
        lower_mat="CONCRETO",
        upper_mat="PRFV",
        pipes=[(150, 40.0), (75, 35.0)],
        pump_power_kw=1.10,
        pump_flow_rate=7200.0,
        pump_efficiency=65.0,
        pump_count=2,
        pump_startup_h=0.04,
        elec_tariff=1.05,
        chlorine_enabled=True,
        chlorine_dose=3.0,
        chlorine_cost_kg=20.0,
        chlorine_co2_kg=25.0,
        water_tariffs=caesb_commercial_tariffs,
        sewage_rate=100.0,
        sewage_mode=1,
        tma_annual=12.0,
        inflation_annual=4.5
    )

    # ──────────────────────────────────────────────────────────────────────────
    # CASO 3: ESCOLA PÚBLICA INTEGRAL (MANAUS - Manaus3.csv)
    # ──────────────────────────────────────────────────────────────────────────
    manaus_public_tariffs = [
        (0.0, 20.0, 6.50, 0),
        (20.0, 50.0, 11.20, 0),
        (50.0, 100.0, 18.50, 0),
        (100.0, 999999.0, 25.30, 0),
    ]
    res3 = run_case_study(
        case_id="3",
        title="Escola Pública de Tempo Integral Amazonas",
        typology="Institucional / Escolar",
        rain_filename="Manaus3.csv",
        area_m2=1400.0,
        runoff_c=0.80,
        discard_mm=1.5,
        discard_mode=3,
        discard_days=3,
        residents=350,
        demand_l_hab_day=40.0,
        share_pct=50.0,
        upper_vol_l=5000.0,
        upper_used=True,
        pump_thresh_pct=20.0,
        sweep_max_l=60000.0,
        sweep_step_l=3000.0,
        delta_ideal=3.5,
        lower_mat="PRFV",
        upper_mat="PRFV",
        pipes=[(150, 60.0), (75, 25.0)],
        pump_power_kw=0.735,
        pump_flow_rate=5400.0,
        pump_efficiency=60.0,
        pump_count=2,
        pump_startup_h=0.03,
        elec_tariff=1.15,
        chlorine_enabled=True,
        chlorine_dose=2.5,
        chlorine_cost_kg=22.0,
        chlorine_co2_kg=25.0,
        water_tariffs=manaus_public_tariffs,
        sewage_rate=80.0,
        sewage_mode=1,
        tma_annual=10.0,
        inflation_annual=4.5
    )

    results = [res1, res2, res3]

    report_path = os.path.join(ROOT, "examples", "ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md")
    write_reference_validation_report(results, report_path)
    detail_path = os.path.join(ROOT, "examples", "DETALHAMENTO_COMPLETO_TRES_MODELOS.md")
    write_complete_detail_report(results, detail_path)

    # Imprime resumo comparativo
    for r in results:
        print(f"\n--- ESTUDO DE CASO {r['case_id']}: {r['title']} ({r['climate']}) ---")
        print(f"Tipologia: {r['typology']} | Area: {r['area_m2']} m2 | Ocupantes: {r['residents']} | Demanda: {r['daily_demand_l']} L/dia")
        print(f"Materiais: {r['materials']}")
        print(f"Tubulacoes: {r['pipes_str']}")
        print(f"Motobomba: {r['pump_str']}")
        print(f"Cloracao: {r['chlorine_str']}")
        print(f"  * Otimo Tecnico (Delta %/m3): {r['opt_tech_vol']:,.0f} L")
        print(f"  * Otimo Economico (VPL Max): {r['opt_econ_vol']:,.0f} L")
        print(f"  * Otimo Ambiental (ACV CO2e): {r['opt_env_vol']:,.0f} L")
        print(f"  * Decisao TOPSIS Global: {r['opt_topsis_vol']:,.0f} L")
        print(f"Projeto salvo em: {r['proj_filepath']}")

    print(f"\nRelatorio de verificacao manual regenerado em: {report_path}")
    print(f"Detalhamento comparativo regenerado em: {detail_path}")

    print("\n" + "=" * 80)
    print("TODOS OS 3 ESTUDOS DE CASO FORAM GERADOS SEM ERROS DE EXECUCAO.")
    print("=" * 80)


if __name__ == "__main__":
    main()
