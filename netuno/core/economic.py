import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from netuno.core.parser import NetunoConfig
from netuno.core.pump_energy import compute_annual_pump_energy
from netuno.core.supply_arrangement import GRAVIDADE, arranjo_de
from netuno.core.pump_hydraulics import (
    ALTURA_MANOMETRICA_PADRAO_M,
    energia_especifica_a_partir_da_vazao,
    energia_especifica_kwh_por_m3,
    rendimento_do_motor,
    rendimento_tipico,
    vazao_l_por_h,
)
from netuno.core.chlorination import Cloracao, DOSE_PADRAO_MG_POR_LITRO, PUREZA_PADRAO
from netuno.core.etap_integration import (
    capex_incremental_da_etap,
    dimensionar_etap_do_projeto,
    opex_anual_incremental_da_etap,
)
from netuno.core.simulation import SingleTankSimulationResult


def _calculate_irr(cash_flows: List[float], periods_per_year: int = 1) -> Optional[float]:
    """Calcula a TIR anual efetiva por busca de raiz com bracket.

    Para fluxos não convencionais (mais de uma mudança de sinal), a TIR pode
    ter múltiplas soluções e não é um indicador unívoco; nesse caso retorna
    ``None`` em vez de escolher uma raiz arbitrária.
    """
    values = np.asarray(cash_flows, dtype=float)
    if values.size < 2 or not np.all(np.isfinite(values)):
        return None
    nonzero = values[np.abs(values) > 1e-12]
    if nonzero.size < 2 or not (np.any(nonzero < 0) and np.any(nonzero > 0)):
        return None
    if np.count_nonzero(np.sign(nonzero[1:]) != np.sign(nonzero[:-1])) != 1:
        if periods_per_year > 1 and len(cash_flows) >= periods_per_year:
            annual_cfs = [float(cash_flows[0])]
            for y_start in range(1, len(cash_flows), periods_per_year):
                y_sum = float(sum(cash_flows[y_start:y_start + periods_per_year]))
                annual_cfs.append(y_sum)
            return _calculate_irr(annual_cfs, periods_per_year=1)
        return None

    indices = np.arange(values.size, dtype=float)

    def npv(rate: float) -> float:
        try:
            if rate <= -1.0:
                return float('-inf')
            log_terms = -indices * math.log1p(rate)
            if np.any(log_terms > 650.0):
                dom_idx = int(np.argmax(log_terms))
                return float('inf') if values[dom_idx] > 0 else float('-inf')
            factors = np.exp(log_terms)
            val = float(np.dot(values, factors))
            return val if math.isfinite(val) else float('inf')
        except (ValueError, OverflowError):
            return float('inf')

    # Grade logarítmica: resolve TIRs negativas próximas de -100% e projetos
    # de retorno muito alto sem depender de um chute inicial de Newton.
    rates = np.concatenate((
        np.linspace(-0.999999, -0.01, 240),
        np.array([0.0]),
        np.geomspace(1e-8, 1e4, 420),
    ))
    previous_rate = float(rates[0])
    previous_value = npv(previous_rate)
    bracket = None
    for rate in rates[1:]:
        rate = float(rate)
        value = npv(rate)
        if abs(value) <= 1e-9:
            period_rate = rate
            return ((1.0 + period_rate) ** periods_per_year - 1.0) * 100.0
        if np.isfinite(previous_value) and np.isfinite(value) and previous_value * value < 0:
            bracket = (previous_rate, rate)
            break
        previous_rate, previous_value = rate, value
    if bracket is None:
        return None

    low, high = bracket
    f_low = npv(low)
    for _ in range(160):
        mid = (low + high) / 2.0
        f_mid = npv(mid)
        if abs(f_mid) <= 1e-10 or high - low <= 1e-12:
            period_rate = mid
            return ((1.0 + period_rate) ** periods_per_year - 1.0) * 100.0
        if f_low * f_mid <= 0:
            high = mid
        else:
            low, f_low = mid, f_mid
    period_rate = (low + high) / 2.0
    return ((1.0 + period_rate) ** periods_per_year - 1.0) * 100.0

@dataclass
class MonthlyCashFlowItem:
    month: int
    year: int
    water_bill_without_pluvial: float
    water_bill_with_pluvial: float
    water_savings: float
    pump_energy_kwh: float
    pump_cost: float
    om_cost: float
    chlorine_cost: float = 0.0
    iptu_savings: float = 0.0
    net_savings: float = 0.0
    discounted_net_savings: float = 0.0
    cumulative_discounted: float = 0.0

@dataclass
class EconomicAnalysisResult:
    vpl: float  # Valor Presente Líquido (R$)
    tir_monthly_pct: float  # Taxa Interna de Retorno (% ao mês)
    tir_annual_pct: float  # Taxa Interna de Retorno (% ao ano)
    payback_months: Optional[int]  # Tempo de retorno (meses)
    payback_years: Optional[float]  # Tempo de retorno (anos)
    capex_total: float  # Custo inicial total (R$)
    annual_water_savings_brl: float
    annual_opex_brl: float
    monthly_pump_kwh: float = 0.0
    annual_pump_kwh: float = 0.0
    monthly_pump_cost_brl: float = 0.0
    annual_pump_cost_brl: float = 0.0
    annual_chlorine_cost_brl: float = 0.0
    # Linha de tratamento (ETAP). O investimento entra no CAPEX e o custeio
    # anual, descontada a cloracao ja contabilizada, entra no fluxo de caixa.
    etap_capex_brl: float = 0.0
    annual_etap_opex_brl: float = 0.0
    etap_disinfection_method: str = ""
    etap_disinfection_stages: List[str] = field(default_factory=list)
    annual_iptu_savings_brl: float = 0.0
    annual_chlorine_kg: float = 0.0
    monthly_cash_flows: List[MonthlyCashFlowItem] = field(default_factory=list)


def calculate_water_bill(
    vol_liters: float,
    tariffs: List[Tuple[float, float, float, int]],
    sewage_mode: int = 1,
    sewage_rate: float = 100.0,
    water_tax_fixed: float = 0.0,
    water_tax_var: float = 0.0,
    num_units: int = 1,
) -> float:
    """
    Calcula a conta mensal de água e esgoto em R$ para um determinado volume em Litros.
    Suporta Micromedição Individualizada em Edifícios Multifamiliares e Condomínios (num_units >= 1).
    Quando num_units > 1, o consumo é avaliado no patamar de 1 unidade habitacional e multiplicado
    pelo número de economias, evitando distorções nas faixas progressivas residenciais.
    """
    n_units = max(1, int(num_units))
    vol_m3_unit = (vol_liters / 1000.0) / float(n_units)
    c_agua_unit = 0.0
    
    effective_tariffs = tariffs if tariffs else [
        (0.0, 0.0, 46.34, -1),
        (0.0, 10.0, 3.08, 1),
        (10.0, 25.0, 14.31, 1),
        (25.0, 50.0, 19.14, 1),
        (50.0, 999999.0, 24.08, 1),
    ]
    
    # 1. Identifica se existe franquia de consumo mínimo com taxa fixa inclusa (is_fix == -2)
    # Ex: DAE Americana: até 6 m³ = R$ 14,30 fixo; excedendo 6 m³, todo o volume desde 0 m³ é cobrado pela tarifa da faixa correspondente
    min_franchise = None
    for t in effective_tariffs:
        min_v, max_v, rate_or_fix, is_fix = t
        if is_fix == -2:
            min_franchise = (max_v, rate_or_fix)
            break

    if min_franchise is not None:
        franchise_vol, franchise_cost = min_franchise
        if vol_m3_unit <= franchise_vol:
            c_agua_unit = franchise_cost
        else:
            for t in effective_tariffs:
                min_v, max_v, rate_or_fix, is_fix = t
                if is_fix in (0, 1):
                    eff_min = 0.0 if min_v <= franchise_vol else min_v
                    if vol_m3_unit > eff_min:
                        v_in_tier = min(vol_m3_unit, max_v) - eff_min
                        if v_in_tier > 0:
                            c_agua_unit += v_in_tier * rate_or_fix
    else:
        # Calcula a tarifa de água nas faixas progressivas padrão para 1 unidade habitacional
        for t in effective_tariffs:
            min_v, max_v, rate_or_fix, is_fix = t
            if is_fix == -1:
                # Custo fixo / disponibilidade por unidade
                c_agua_unit += rate_or_fix
            elif is_fix == -3:
                # Piso: aplicado depois, sobre o total tarifado.
                continue
            elif vol_m3_unit > min_v:
                v_in_tier = min(vol_m3_unit, max_v) - min_v
                if v_in_tier > 0:
                    c_agua_unit += v_in_tier * rate_or_fix

    # 2. Piso de pagamento (is_fix == -3)
    #
    # Regime distinto do custo fixo, e o motor nao o tinha. O custo fixo SOMA por
    # cima do consumo medido; o piso nao soma, LIMITA por baixo. Com piso de
    # R$ 40 e consumo tarifado de R$ 55, economizar ate R$ 15 nao reduz nada -
    # e e justamente isso que um estudo de aproveitamento pluvial precisa
    # enxergar. Ver netuno/core/tariff_regimes.py.
    piso = 0.0
    for t in effective_tariffs:
        if int(t[3]) == -3:
            piso = max(piso, float(t[2]))
    if piso > 0.0:
        c_agua_unit = max(c_agua_unit, piso)

    # Cálculo do esgoto
    if sewage_mode == 0:  # Custo fixo de esgoto
        c_sewage_unit = sewage_rate
    else:  # Percentual sobre o valor da água
        c_sewage_unit = c_agua_unit * (sewage_rate / 100.0)
        
    # Impostos e taxas por unidade
    c_tax_var_unit = c_agua_unit * (water_tax_var / 100.0)
    c_total_unit = c_agua_unit + c_sewage_unit + c_tax_var_unit + water_tax_fixed
    
    return float(c_total_unit * n_units)


def calculate_effective_tariff(
    cfg: Any,
    annual_m3_saved: float,
    annual_total_demand_m3: Optional[float] = None,
) -> Tuple[float, float]:
    """Calcula a tarifa marginal evitada com a tabela completa de faixas.

    Quando a demanda total anual é informada, a conta sem aproveitamento usa
    exatamente esse consumo médio mensal e a conta com aproveitamento subtrai
    o volume pluvial simulado. O fallback histórico só é mantido para chamadas
    legadas que não fornecem a demanda total.
    """
    if not hasattr(cfg, 'water_tariffs') or not cfg.water_tariffs or annual_m3_saved <= 0:
        return 0.0, 0.0

    pluv_monthly_m3 = annual_m3_saved / 12.0
    if annual_total_demand_m3 is not None and annual_total_demand_m3 > 0:
        base_monthly_m3 = annual_total_demand_m3 / 12.0
    else:
        base_monthly_m3 = max(15.0, pluv_monthly_m3 * 1.5)

    num_units = max(1, int(getattr(cfg, 'num_economias', getattr(cfg, 'num_units', 1))))

    water_bill_without = calculate_water_bill(
        base_monthly_m3 * 1000.0,
        cfg.water_tariffs,
        sewage_mode=1,
        sewage_rate=0.0,
        water_tax_fixed=getattr(cfg, 'water_tax_fixed', 0.0),
        water_tax_var=getattr(cfg, 'water_tax_var', 0.0),
        num_units=num_units
    )

    water_bill_with = calculate_water_bill(
        max(0.0, (base_monthly_m3 - pluv_monthly_m3) * 1000.0),
        cfg.water_tariffs,
        sewage_mode=1,
        sewage_rate=0.0,
        water_tax_fixed=getattr(cfg, 'water_tax_fixed', 0.0),
        water_tax_var=getattr(cfg, 'water_tax_var', 0.0),
        num_units=num_units
    )

    water_monthly_savings = max(0.0, water_bill_without - water_bill_with)
    eff_tariff = water_monthly_savings / pluv_monthly_m3 if pluv_monthly_m3 > 0 else 0.0

    sewage_mode = getattr(cfg, 'sewage_mode', 1)
    sewage_rate = getattr(cfg, 'sewage_rate', 100.0)
    total_bill_without = calculate_water_bill(
        base_monthly_m3 * 1000.0,
        cfg.water_tariffs,
        sewage_mode=sewage_mode,
        sewage_rate=sewage_rate,
        water_tax_fixed=getattr(cfg, 'water_tax_fixed', 0.0),
        water_tax_var=getattr(cfg, 'water_tax_var', 0.0),
        num_units=num_units
    )
    total_bill_with = calculate_water_bill(
        max(0.0, (base_monthly_m3 - pluv_monthly_m3) * 1000.0),
        cfg.water_tariffs,
        sewage_mode=sewage_mode,
        sewage_rate=sewage_rate,
        water_tax_fixed=getattr(cfg, 'water_tax_fixed', 0.0),
        water_tax_var=getattr(cfg, 'water_tax_var', 0.0),
        num_units=num_units
    )
    total_monthly_savings = max(0.0, total_bill_without - total_bill_with)
    sewage_monthly_savings = max(0.0, total_monthly_savings - water_monthly_savings)
    eff_sewage = sewage_monthly_savings / pluv_monthly_m3 if pluv_monthly_m3 > 0 else 0.0

    return eff_tariff, eff_sewage


def run_economic_analysis(
    config: NetunoConfig,
    sim_result: SingleTankSimulationResult
) -> EconomicAnalysisResult:
    """
    Executes full financial cash flow, VPL, TIR, and Payback analysis.
    """
    # 1. Initial Investment Cost (CAPEX)
    capex = (
        config.cost_lower_tank +
        config.cost_upper_tank +
        config.cost_labor +
        config.cost_piping +
        config.cost_accessories +
        # Arranjo por gravidade não tem motobomba a comprar.
        (0.0 if arranjo_de(config) == GRAVIDADE else config.pump_unit_cost * config.pump_count)
    )
    
    # Average monthly consumption volumes
    avg_pluv_l_day = sim_result.avg_pluvial_consumed_l_day
    avg_pot_l_day = sim_result.avg_potable_consumed_l_day
    avg_tot_l_day = avg_pluv_l_day + avg_pot_l_day
    
    days_in_month = 30.4375  # 365.25 / 12
    
    vol_tot_liters_month = avg_tot_l_day * days_in_month
    vol_pot_liters_month = avg_pot_l_day * days_in_month
    vol_pluv_liters_month = avg_pluv_l_day * days_in_month
    vol_pluv_m3_month = vol_pluv_liters_month / 1000.0
    
    num_units = max(1, int(getattr(config, 'num_economias', getattr(config, 'num_units', 1))))

    bill_without = calculate_water_bill(
        vol_tot_liters_month, config.water_tariffs,
        config.sewage_mode, config.sewage_rate,
        config.water_tax_fixed, config.water_tax_var,
        num_units=num_units
    )
    
    bill_with = calculate_water_bill(
        vol_pot_liters_month, config.water_tariffs,
        config.sewage_mode, config.sewage_rate,
        config.water_tax_fixed, config.water_tax_var,
        num_units=num_units
    )
    
    monthly_water_savings_base = max(0.0, bill_without - bill_with)
    
    # 2. Pump Operational Cost (Eq 5.6 - 5.10)
    monthly_pump_cost_base = 0.0
    monthly_pump_kwh_base = 0.0
    
    # A energia vem da função única de netuno/core/pump_energy.py, conforme o
    # arranjo de abastecimento. Até setembro de 2026 esta conta era uma cópia
    # que só existia com caixa superior, enquanto a ACV cobrava bombeamento em
    # qualquer arranjo.
    energia_de_abastecimento = compute_annual_pump_energy(config, sim_result)
    if energia_de_abastecimento.annual_kwh > 0:
        monthly_pump_kwh_base = energia_de_abastecimento.annual_kwh / 12.0

        # Ajuste por bandeira tarifária ANEEL ou Tarifa Branca
        tariff_flag = getattr(config, 'tariff_flag', 'verde')
        flag_add = 0.0
        if tariff_flag == 'amarela':
            flag_add = 0.01885
        elif tariff_flag == 'vermelha_1':
            flag_add = 0.04463
        elif tariff_flag == 'vermelha_2':
            flag_add = 0.07877
        elif tariff_flag == 'branca':
            flag_add = -0.15 * config.elec_tariff  # Desconto fora de ponta

        effective_elec_tariff = max(0.0, config.elec_tariff + flag_add)

        monthly_pump_cost_base = (
            monthly_pump_kwh_base * effective_elec_tariff * (1.0 + config.elec_tax_var / 100.0) +
            config.elec_tax_fixed
        )
        
    # Volume pluvial anual efetivamente aproveitado, base de dimensionamento da
    # linha de tratamento e da dosagem.
    annual_pluvial_m3 = vol_pluv_m3_month * 12.0

    # 2.1 Chlorination / Chemical Treatment Cost (OPEX)
    chlorine_enabled = getattr(config, 'chlorine_treatment_enabled', True)
    dose_mg_l = getattr(config, 'chlorine_dose_mg_l', DOSE_PADRAO_MG_POR_LITRO)
    cost_per_kg_cl2 = getattr(config, 'chlorine_cost_per_kg', 25.0)

    # O que se compra e o PRODUTO (pastilha a 65% de cloro ativo), nao o cloro
    # puro, e o preco em R$/kg e do produto. Antes desta revisao a conta usava a massa
    # de cloro ativo, subestimando o custo em 1/0,65 - cerca de 35%. A conversao
    # vem da cadeia unica em netuno/core/chlorination.py.
    _cloracao = Cloracao(
        dose_mg_por_litro=max(0.0, float(dose_mg_l)),
        pureza=max(1e-6, float(getattr(config, 'chlorine_product_purity', PUREZA_PADRAO))),
    )
    monthly_cl2_kg = _cloracao.massa_anual_de_produto_kg(vol_pluv_m3_month) if chlorine_enabled else 0.0
    monthly_cl2_cost_base = monthly_cl2_kg * cost_per_kg_cl2
    annual_cl2_kg = monthly_cl2_kg * 12.0
    annual_cl2_cost = monthly_cl2_cost_base * 12.0

    # 2.1.1 Linha de tratamento (ETAP)
    #
    # A escolha feita na aba de Qualidade da Agua - classe alvo, desinfeccao e
    # filtro de polimento - chega aqui pela configuracao. O investimento entra no
    # CAPEX; do custeio anual desconta-se a cloracao, que as linhas acima ja
    # custeiam, de modo que o hipoclorito e pago uma vez so.
    etap = dimensionar_etap_do_projeto(config, annual_pluvial_m3=annual_pluvial_m3, sim_result=sim_result)
    # A regra incremental - descontar a verba generica de «Acessorios» do CAPEX e
    # a cloracao do custeio - vive em netuno/core/etap_integration.py, e nao aqui:
    # a aba economica integrada monta o proprio fluxo de caixa e precisa da mesma
    # regra. Duas copias divergiriam, e foi assim que o cloro chegou a ter cinco
    # convencoes.
    etap_capex = capex_incremental_da_etap(config, annual_pluvial_m3, sim_result)
    annual_etap_opex = opex_anual_incremental_da_etap(config, annual_pluvial_m3, sim_result)
    monthly_etap_opex_base = annual_etap_opex / 12.0
    capex += etap_capex

    # 2.2 Benefício Fiscal do IPTU Verde
    iptu_enabled = getattr(config, 'iptu_green_enabled', False)
    iptu_val_yr = getattr(config, 'iptu_annual_value', 0.0)
    iptu_disc_pct = getattr(config, 'iptu_discount_pct', 0.0)
    annual_iptu_savings_base = (iptu_val_yr * (iptu_disc_pct / 100.0)) if iptu_enabled else 0.0
    monthly_iptu_savings_base = annual_iptu_savings_base / 12.0

    # 3. Monthly Cash Flow projection
    total_months = config.analysis_period_years * 12
    tma_monthly = config.tma / 100.0
    inf_monthly = config.inflation / 100.0
    
    cash_flows: List[MonthlyCashFlowItem] = []
    cumulative_disc = -capex
    payback_month: Optional[int] = None
    
    net_cf_list = [-capex]
    
    w_esc = getattr(config, 'water_tariff_escalation', 5.0)
    s_esc = getattr(config, 'sewage_tariff_escalation', 5.0)
    e_esc = getattr(config, 'elec_tariff_escalation', 5.0)
    esc_interval = max(1, config.tariff_escalation)

    bill_without_base = calculate_water_bill(
        vol_tot_liters_month, config.water_tariffs,
        config.sewage_mode, config.sewage_rate,
        config.water_tax_fixed, config.water_tax_var,
        num_units=num_units
    )
    
    bill_with_base = calculate_water_bill(
        vol_pot_liters_month, config.water_tariffs,
        config.sewage_mode, config.sewage_rate,
        config.water_tax_fixed, config.water_tax_var,
        num_units=num_units
    )

    # Separa água (incluindo taxas vinculadas a ela) e esgoto para aplicar os
    # dois reajustes configurados sem indexar a conta agregada pelo índice errado.
    water_only_without_base = calculate_water_bill(
        vol_tot_liters_month, config.water_tariffs, 1, 0.0,
        config.water_tax_fixed, config.water_tax_var, num_units=num_units
    )
    water_only_with_base = calculate_water_bill(
        vol_pot_liters_month, config.water_tariffs, 1, 0.0,
        config.water_tax_fixed, config.water_tax_var, num_units=num_units
    )
    base_water_savings = max(0.0, water_only_without_base - water_only_with_base)
    base_total_savings = max(0.0, bill_without_base - bill_with_base)
    base_sewage_savings = max(0.0, base_total_savings - base_water_savings)

    for m in range(1, total_months + 1):
        year = math.ceil(m / 12.0)
        
        # Inflation factor for O&M costs ONLY
        inf_factor = (1.0 + inf_monthly) ** (m - 1)
        
        # Separate tariff escalation factors (applied every config.tariff_escalation months)
        escalation_steps = (m - 1) // int(esc_interval)

        w_tariff_factor = (1.0 + w_esc / 100.0) ** escalation_steps
        s_tariff_factor = (1.0 + s_esc / 100.0) ** escalation_steps
        e_tariff_factor = (1.0 + e_esc / 100.0) ** escalation_steps
        
        water_without_m = water_only_without_base * w_tariff_factor
        water_with_m = water_only_with_base * w_tariff_factor
        sewage_without_base = max(0.0, bill_without_base - water_only_without_base)
        sewage_with_base = max(0.0, bill_with_base - water_only_with_base)
        bill_without_m = water_without_m + sewage_without_base * s_tariff_factor
        bill_with_m = water_with_m + sewage_with_base * s_tariff_factor
        w_savings = base_water_savings * w_tariff_factor + base_sewage_savings * s_tariff_factor
        p_cost = monthly_pump_cost_base * e_tariff_factor
        
        # Additional O&M costs indexed to inflation
        om_cost = 0.0
        for op in config.op_costs:
            name, period_m, fix_cost, var_cost_m3 = op
            if m % max(1, period_m) == 0:
                om_cost += (fix_cost + var_cost_m3 * vol_pluv_m3_month) * inf_factor
                
        # Chlorination chemical consumable cost indexed to inflation
        cl2_cost = monthly_cl2_cost_base * inf_factor

        # Custeio da ETAP sem a cloracao: lampada germicida, energia do reator,
        # refil do filtro de polimento. Indexado a inflacao como os demais O&M.
        etap_cost = monthly_etap_opex_base * inf_factor
        
        # IPTU Verde savings
        iptu_s = monthly_iptu_savings_base * inf_factor
        
        net_s = w_savings - p_cost - om_cost - cl2_cost - etap_cost + iptu_s
        disc_net_s = net_s / ((1.0 + tma_monthly) ** m)
        cumulative_disc += disc_net_s
        
        if payback_month is None and cumulative_disc >= 0:
            payback_month = m
            
        net_cf_list.append(net_s)
        
        cash_flows.append(MonthlyCashFlowItem(
            month=m,
            year=year,
            water_bill_without_pluvial=bill_without_m,
            water_bill_with_pluvial=bill_with_m,
            water_savings=w_savings,
            pump_energy_kwh=monthly_pump_kwh_base,
            pump_cost=p_cost,
            om_cost=om_cost + etap_cost,
            chlorine_cost=cl2_cost,
            iptu_savings=iptu_s,
            net_savings=net_s,
            discounted_net_savings=disc_net_s,
            cumulative_discounted=cumulative_disc
        ))
        
    # VPL calculation
    vpl = cumulative_disc  # At month total_months
    
    tir_a_pct_value = _calculate_irr(net_cf_list, periods_per_year=12)
    tir_a_pct = tir_a_pct_value if tir_a_pct_value is not None else 0.0
    tir_m_pct = (((1.0 + tir_a_pct / 100.0) ** (1.0 / 12.0)) - 1.0) * 100.0 if tir_a_pct > -100.0 else 0.0
        
    payback_yrs = (payback_month / 12.0) if payback_month is not None else None
    
    return EconomicAnalysisResult(
        vpl=vpl,
        tir_monthly_pct=tir_m_pct,
        tir_annual_pct=tir_a_pct,
        payback_months=payback_month,
        payback_years=payback_yrs,
        capex_total=capex,
        annual_water_savings_brl=monthly_water_savings_base * 12.0,
        annual_opex_brl=(monthly_pump_cost_base * 12.0) + annual_cl2_cost + annual_etap_opex,
        monthly_pump_kwh=monthly_pump_kwh_base,
        annual_pump_kwh=monthly_pump_kwh_base * 12.0,
        monthly_pump_cost_brl=monthly_pump_cost_base,
        annual_pump_cost_brl=monthly_pump_cost_base * 12.0,
        annual_chlorine_cost_brl=annual_cl2_cost,
        annual_iptu_savings_brl=annual_iptu_savings_base,
        annual_chlorine_kg=annual_cl2_kg,
        monthly_cash_flows=cash_flows,
        etap_capex_brl=etap_capex,
        annual_etap_opex_brl=annual_etap_opex,
        etap_disinfection_method=etap.metodo,
        etap_disinfection_stages=etap.estagios,
    )


@dataclass
class SimpleEconomicResult:
    npv: float
    payback_simple_years: Optional[float]
    payback_discounted_years: Optional[float]
    total_net_savings: float


def calculate_economic_indicators(
    initial_investment: float,
    annual_water_saved_m3: float,
    water_tariff_per_m3: float,
    tariff_escalation_rate: float = 0.05,
    discount_rate: float = 0.08,
    annual_om_cost: float = 100.0,
    analysis_period_years: int = 20
) -> SimpleEconomicResult:
    """
    Calcula VPL, Payback Simples, Payback Descontado (com precisão mensal) e Economia Líquida Acumulada.
    """
    if initial_investment <= 0:
        return SimpleEconomicResult(
            npv=0.0,
            payback_simple_years=0.0,
            payback_discounted_years=0.0,
            total_net_savings=0.0
        )

    cum_discounted = -initial_investment
    cum_simple = -initial_investment

    cur_cum_simple = -initial_investment
    cur_cum_discounted = -initial_investment

    payback_simple = None
    payback_discounted = None

    total_net_savings = 0.0
    current_tariff = water_tariff_per_m3

    for yr in range(1, analysis_period_years + 1):
        gross_savings = annual_water_saved_m3 * current_tariff
        net_savings = gross_savings - annual_om_cost
        total_net_savings += net_savings

        disc_factor_yr = 1.0 / ((1.0 + discount_rate) ** yr)
        discounted_net = net_savings * disc_factor_yr

        cum_simple += net_savings
        cum_discounted += discounted_net

        # Progresso mensal detalhado para precisão exata do tempo de retorno
        monthly_net = net_savings / 12.0
        for m in range(1, 13):
            overall_m = (yr - 1) * 12 + m
            m_disc_factor = 1.0 / ((1.0 + discount_rate) ** (overall_m / 12.0))
            m_disc_net = monthly_net * m_disc_factor

            prev_s = cur_cum_simple
            cur_cum_simple += monthly_net
            if payback_simple is None and cur_cum_simple >= 0:
                if monthly_net > 0:
                    frac = (-prev_s) / monthly_net
                    payback_simple = ((overall_m - 1) + frac) / 12.0
                else:
                    payback_simple = overall_m / 12.0

            prev_d = cur_cum_discounted
            cur_cum_discounted += m_disc_net
            if payback_discounted is None and cur_cum_discounted >= 0:
                if m_disc_net > 0:
                    frac_d = (-prev_d) / m_disc_net
                    payback_discounted = ((overall_m - 1) + frac_d) / 12.0
                else:
                    payback_discounted = overall_m / 12.0

        current_tariff *= (1.0 + tariff_escalation_rate)

    return SimpleEconomicResult(
        npv=cum_discounted,
        payback_simple_years=round(payback_simple, 2) if payback_simple is not None else None,
        payback_discounted_years=round(payback_discounted, 2) if payback_discounted is not None else None,
        total_net_savings=total_net_savings
    )


@dataclass
class AnnualCashFlowItem:
    year: int
    initial_investment: float
    water_saved_m3: float
    water_tariff_readjusted: float
    sewage_tariff_readjusted: float
    gross_water_savings_brl: float
    gross_sewage_savings_brl: float
    total_gross_savings_brl: float
    pump_energy_cost_brl: float
    om_cost_brl: float
    chlorine_cost_brl: float = 0.0
    iptu_green_savings_brl: float = 0.0
    net_cash_flow_nominal_brl: float = 0.0
    discount_factor: float = 1.0
    discounted_cash_flow_brl: float = 0.0
    cumulative_discounted_cash_flow_brl: float = 0.0


@dataclass
class RobustEconomicAnalysisResult:
    vpl: float
    tir_pct: float
    payback_simple_years: Optional[float]
    payback_discounted_years: Optional[float]
    total_investment: float
    total_gross_savings_brl: float
    total_opex_brl: float
    annual_chlorine_cost_brl: float = 0.0
    annual_iptu_savings_brl: float = 0.0
    annual_cash_flows: List[AnnualCashFlowItem] = field(default_factory=list)


def run_robust_economic_analysis(
    initial_investment: float,
    annual_water_saved_m3: float,
    water_tariff_per_m3: float,
    sewage_tariff_per_m3: float = 0.0,
    sewage_mode: int = 1,
    water_tariff_escalation_rate: float = 0.05,
    sewage_tariff_escalation_rate: float = 0.05,
    elec_tariff_escalation_rate: float = 0.05,
    tariff_escalation_rate: Optional[float] = None,
    inflation_rate: float = 0.04,
    discount_rate: float = 0.08,
    annual_om_cost_base: float = 120.0,
    pump_power_kw: float = 0.75,
    pump_hours_year: float = 150.0,
    elec_tariff_kwh: float = 1.0,
    analysis_period_years: int = 20,
    annual_chlorine_cost: float = 0.0,
    annual_iptu_savings: float = 0.0,
) -> RobustEconomicAnalysisResult:
    """
    Executa projeção anual detalhada de fluxo de caixa, VPL, TIR e Payback com OPEX de cloração e IPTU Verde.
    """
    numeric_inputs = {
        "initial_investment": initial_investment,
        "annual_water_saved_m3": annual_water_saved_m3,
        "water_tariff_per_m3": water_tariff_per_m3,
        "sewage_tariff_per_m3": sewage_tariff_per_m3,
        "annual_om_cost_base": annual_om_cost_base,
        "pump_power_kw": pump_power_kw,
        "pump_hours_year": pump_hours_year,
        "elec_tariff_kwh": elec_tariff_kwh,
        "annual_chlorine_cost": annual_chlorine_cost,
        "annual_iptu_savings": annual_iptu_savings,
    }
    rotulos = {
        "initial_investment": "O investimento inicial",
        "annual_water_saved_m3": "O volume anual de água economizada",
        "water_tariff_per_m3": "A tarifa de água",
        "sewage_tariff_per_m3": "A tarifa de esgoto",
        "annual_om_cost_base": "O custo anual de operação e manutenção",
        "pump_power_kw": "A potência da motobomba",
        "pump_hours_year": "O tempo anual de funcionamento da motobomba",
        "elec_tariff_kwh": "A tarifa de energia elétrica",
        "annual_chlorine_cost": "O custo anual de cloração",
        "annual_iptu_savings": "O desconto anual de IPTU",
    }
    for name, value in numeric_inputs.items():
        if not math.isfinite(float(value)) or float(value) < 0:
            raise ValueError(f"{rotulos.get(name, name)} deve ser um número finito "
                             f"e não negativo; recebido {value!r}.")
    if int(analysis_period_years) != analysis_period_years or analysis_period_years <= 0:
        raise ValueError("O período de análise deve ser um número inteiro de anos, "
                         f"maior que zero; recebido {analysis_period_years!r}.")
    if initial_investment <= 0 and annual_water_saved_m3 <= 0 and annual_iptu_savings <= 0:
        cfs_zero = [
            AnnualCashFlowItem(
                year=yr,
                initial_investment=0.0,
                water_saved_m3=0.0,
                water_tariff_readjusted=water_tariff_per_m3,
                sewage_tariff_readjusted=sewage_tariff_per_m3,
                gross_water_savings_brl=0.0,
                gross_sewage_savings_brl=0.0,
                total_gross_savings_brl=0.0,
                pump_energy_cost_brl=0.0,
                om_cost_brl=0.0,
                chlorine_cost_brl=0.0,
                iptu_green_savings_brl=0.0,
                net_cash_flow_nominal_brl=0.0,
                discount_factor=1.0,
                discounted_cash_flow_brl=0.0,
                cumulative_discounted_cash_flow_brl=0.0
            ) for yr in range(analysis_period_years + 1)
        ]
        return RobustEconomicAnalysisResult(
            vpl=0.0,
            tir_pct=0.0,
            payback_simple_years=0.0,
            payback_discounted_years=0.0,
            total_investment=0.0,
            total_gross_savings_brl=0.0,
            total_opex_brl=0.0,
            annual_chlorine_cost_brl=0.0,
            annual_iptu_savings_brl=0.0,
            annual_cash_flows=cfs_zero
        )

    cash_flows = []
    cum_discounted = -initial_investment
    cum_simple = -initial_investment
    
    cur_cum_simple = -initial_investment
    cur_cum_discounted = -initial_investment

    payback_simple = None
    payback_discounted = None

    if initial_investment <= 0:
        payback_simple = 0.0
        payback_discounted = 0.0

    net_cfs_for_tir = [-initial_investment]

    # Reajustes tarifários
    w_esc = tariff_escalation_rate if tariff_escalation_rate is not None else water_tariff_escalation_rate
    s_esc = tariff_escalation_rate if tariff_escalation_rate is not None else sewage_tariff_escalation_rate
    e_esc = tariff_escalation_rate if tariff_escalation_rate is not None else elec_tariff_escalation_rate

    # As taxas chegam como fração decimal ao ano, sempre. Antes a função
    # adivinhava a unidade: módulo até 0,5 era fração, acima disso percentual.
    # Uma TMA de 0,5% ao mês chegava como 0,5 e era lida como 50% ao ano. A
    # convenção está em netuno/core/taxas.py.
    from netuno.core.taxas import validar_fracao_anual
    w_esc = validar_fracao_anual("O reajuste da tarifa de água", w_esc)
    s_esc = validar_fracao_anual("O reajuste da tarifa de esgoto", s_esc)
    e_esc = validar_fracao_anual("O reajuste da tarifa de energia", e_esc)
    inf_r = validar_fracao_anual("A inflação", inflation_rate)
    disc_r = validar_fracao_anual("A taxa de desconto", discount_rate)

    # Ano 0
    cash_flows.append(AnnualCashFlowItem(
        year=0,
        initial_investment=initial_investment,
        water_saved_m3=0.0,
        water_tariff_readjusted=water_tariff_per_m3,
        sewage_tariff_readjusted=sewage_tariff_per_m3,
        gross_water_savings_brl=0.0,
        gross_sewage_savings_brl=0.0,
        total_gross_savings_brl=0.0,
        pump_energy_cost_brl=0.0,
        om_cost_brl=0.0,
        chlorine_cost_brl=0.0,
        net_cash_flow_nominal_brl=-initial_investment,
        discount_factor=1.0,
        discounted_cash_flow_brl=-initial_investment,
        cumulative_discounted_cash_flow_brl=-initial_investment
    ))

    curr_water_tariff = water_tariff_per_m3
    curr_sewage_tariff = sewage_tariff_per_m3
    curr_om_cost = annual_om_cost_base
    curr_elec_tariff = elec_tariff_kwh
    curr_cl2_cost = annual_chlorine_cost

    total_gross_savings = 0.0
    total_opex = 0.0

    for yr in range(1, analysis_period_years + 1):
        if yr > 1:
            curr_water_tariff *= (1.0 + w_esc)
            curr_sewage_tariff *= (1.0 + s_esc)
            curr_elec_tariff *= (1.0 + e_esc)
            curr_om_cost *= (1.0 + inf_r)
            curr_cl2_cost *= (1.0 + inf_r)

        w_savings = annual_water_saved_m3 * curr_water_tariff
        s_savings = (annual_water_saved_m3 * curr_sewage_tariff) if sewage_mode == 1 else 0.0
        curr_iptu_savings = annual_iptu_savings * ((1.0 + inf_r) ** (yr - 1)) if yr > 1 else annual_iptu_savings
        tot_savings = w_savings + s_savings + curr_iptu_savings
        
        pump_cost = pump_power_kw * pump_hours_year * curr_elec_tariff
        tot_opex_yr = curr_om_cost + pump_cost + curr_cl2_cost

        net_cf = tot_savings - tot_opex_yr
        net_cfs_for_tir.append(net_cf)

        disc_factor = 1.0 / ((1.0 + disc_r) ** yr)
        disc_cf = net_cf * disc_factor

        cum_simple += net_cf
        cum_discounted += disc_cf

        # Cálculo com resolução e precisão mensal para os Paybacks
        monthly_net_cf = net_cf / 12.0
        for m in range(1, 13):
            overall_month = (yr - 1) * 12 + m
            m_disc_factor = 1.0 / ((1.0 + disc_r) ** (overall_month / 12.0))
            m_disc_cf = monthly_net_cf * m_disc_factor

            prev_s = cur_cum_simple
            cur_cum_simple += monthly_net_cf
            if payback_simple is None and cur_cum_simple >= 0:
                if monthly_net_cf > 0:
                    frac_s = (-prev_s) / monthly_net_cf
                    payback_simple = ((overall_month - 1) + frac_s) / 12.0
                else:
                    payback_simple = overall_month / 12.0

            prev_d = cur_cum_discounted
            cur_cum_discounted += m_disc_cf
            if payback_discounted is None and cur_cum_discounted >= 0:
                if m_disc_cf > 0:
                    frac_d = (-prev_d) / m_disc_cf
                    payback_discounted = ((overall_month - 1) + frac_d) / 12.0
                else:
                    payback_discounted = overall_month / 12.0

        total_gross_savings += tot_savings
        total_opex += tot_opex_yr

        cash_flows.append(AnnualCashFlowItem(
            year=yr,
            initial_investment=0.0,
            water_saved_m3=annual_water_saved_m3,
            water_tariff_readjusted=curr_water_tariff,
            sewage_tariff_readjusted=curr_sewage_tariff,
            gross_water_savings_brl=w_savings,
            gross_sewage_savings_brl=s_savings,
            total_gross_savings_brl=tot_savings,
            pump_energy_cost_brl=pump_cost,
            om_cost_brl=curr_om_cost,
            chlorine_cost_brl=curr_cl2_cost,
            iptu_green_savings_brl=curr_iptu_savings,
            net_cash_flow_nominal_brl=net_cf,
            discount_factor=disc_factor,
            discounted_cash_flow_brl=disc_cf,
            cumulative_discounted_cash_flow_brl=cum_discounted
        ))

    tir_result = _calculate_irr(net_cfs_for_tir, periods_per_year=1)
    tir_val = tir_result if tir_result is not None else 0.0

    return RobustEconomicAnalysisResult(
        vpl=cum_discounted,
        tir_pct=tir_val,
        payback_simple_years=payback_simple,
        payback_discounted_years=payback_discounted,
        total_investment=initial_investment,
        total_gross_savings_brl=total_gross_savings,
        total_opex_brl=total_opex,
        annual_chlorine_cost_brl=annual_chlorine_cost,
        annual_iptu_savings_brl=annual_iptu_savings,
        annual_cash_flows=cash_flows
    )


def run_sensitivity_analysis(
    base_params: Dict[str, Any],
    variations_pct: List[float] = [-30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0]
) -> Dict[str, List[Tuple[float, float]]]:
    """
    Calcula a variação do VPL em relação a percentuais de variação para cada variável.
    """
    sensitivity_results = {}
    var_keys = [
        ('water_tariff_per_m3',          'Tarifa de Água (R$/m³)'),
        ('initial_investment',            'Investimento Inicial (CAPEX)'),
        ('annual_water_saved_m3',         'Volume de Água Pluvial Captada'),
        ('water_tariff_escalation_rate',  'Reajuste Tarifário Água'),
        ('annual_om_cost_base',           'Custos de O&M'),
        ('discount_rate',                 'TMA (Taxa de Desconto)'),
        ('inflation_rate',                'Taxa de Inflação'),
        ('sewage_tariff_per_m3',          'Tarifa de Esgoto (R$/m³)'),
        ('elec_tariff_escalation_rate',   'Reajuste Tarifário Energia'),
        ('analysis_period_years',         'Período de Análise (anos)'),
    ]

    for key, label in var_keys:
        curve = []
        for v_pct in variations_pct:
            params = base_params.copy()
            base_val = params.get(key, 1.0)
            if key == 'analysis_period_years':
                # Período deve ser inteiro positivo
                new_val = max(1, round(base_val * (1.0 + v_pct / 100.0)))
                params[key] = new_val
            else:
                params[key] = base_val * (1.0 + v_pct / 100.0)
            res = run_robust_economic_analysis(**params)
            curve.append((v_pct, res.vpl))
        sensitivity_results[label] = curve

    return sensitivity_results
