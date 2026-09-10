import math
from netuno.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from netuno.core.parser import NetunoConfig

@dataclass
class SimulationDayResult:
    day_index: int
    precip_mm: float
    eff_precip_mm: float
    harvested_liters: float
    total_demand_liters: float
    pluvial_demand_liters: float
    pluvial_consumed_liters: float
    potable_consumed_liters: float
    spilled_liters: float
    lower_tank_end_liters: float
    upper_tank_end_liters: float
    pumped_liters: float
    pump_cycles: int
    satisfaction_type: int  # 2 = full, 1 = partial, 0 = null
    potable_indoor_consumed_liters: float = 0.0
    pluvial_indoor_consumed_liters: float = 0.0
    pluvial_irrigation_consumed_liters: float = 0.0
    irrigation_demand_liters: float = 0.0
    irrigation_suppressed: bool = False

@dataclass
class SingleTankSimulationResult:
    lower_tank_vol: float
    potential_potable_savings_pct: float  # Epot %
    avg_pluvial_consumed_l_day: float
    avg_potable_consumed_l_day: float
    avg_spilled_l_day: float
    pct_days_full_satisfaction: float
    pct_days_partial_satisfaction: float
    pct_days_null_satisfaction: float
    delta_potential_per_m3: float = 0.0  # %/m3
    
    # Detailed time series
    daily_results: List[SimulationDayResult] = field(default_factory=list)
    monthly_results: List[Dict[str, Any]] = field(default_factory=list)
    n_days_simulated: int = 365
    
    # Dual tank pump metrics
    total_pumped_liters: float = 0.0
    total_pump_cycles: int = 0
    max_pump_batch_liters: float = 0.0
    monthly_pump_hours: List[float] = field(default_factory=list)

    # Discretized consumption metrics (indoor potable, indoor non-potable, irrigation)
    avg_pluvial_indoor_consumed_l_day: float = 0.0
    avg_pluvial_irrigation_consumed_l_day: float = 0.0
    avg_irrigation_suppressed_l_day: float = 0.0
    # Demanda que nao foi atendida por ninguem: acontece quando o suprimento
    # de reserva da irrigacao esta desligado e a cisterna nao da conta. Sem
    # este campo o balanco nao fecha as claras, porque a demanda total deixa
    # de ser a soma do pluvial com o potavel.
    avg_unmet_demand_l_day: float = 0.0
    total_irrigation_days_suppressed: int = 0
    total_irrigation_days_active: int = 0

    @property
    def annual_pluvial_consumed_m3(self) -> float:
        return (self.avg_pluvial_consumed_l_day * 365.25) / 1000.0

    @property
    def annual_pluvial_indoor_consumed_m3(self) -> float:
        if self.avg_pluvial_indoor_consumed_l_day > 0:
            return (self.avg_pluvial_indoor_consumed_l_day * 365.25) / 1000.0
        return self.annual_pluvial_consumed_m3

    @property
    def annual_pluvial_irrigation_consumed_m3(self) -> float:
        return (self.avg_pluvial_irrigation_consumed_l_day * 365.25) / 1000.0

    @property
    def annual_irrigation_volume_suppressed_m3(self) -> float:
        return (self.avg_irrigation_suppressed_l_day * 365.25) / 1000.0

    @property
    def annual_potable_consumed_m3(self) -> float:
        return (self.avg_potable_consumed_l_day * 365.25) / 1000.0

    @property
    def annual_spill_m3(self) -> float:
        return (self.avg_spilled_l_day * 365.25) / 1000.0

    @property
    def total_overflow_liters(self) -> float:
        return self.annual_spill_m3 * 1000.0

    @property
    def total_days(self) -> int:
        if self.daily_results:
            return len(self.daily_results)
        return self.n_days_simulated if self.n_days_simulated > 0 else 365

    @property
    def average_pumped_liters_per_cycle(self) -> float:
        """Volume médio transferido em cada partida da motobomba."""
        if self.total_pump_cycles <= 0:
            return 0.0
        return self.total_pumped_liters / self.total_pump_cycles


@dataclass
class SweepSimulationResult:
    optimal_lower_tank_vol: Optional[float]
    optimal_potential_pct: Optional[float]
    results_by_volume: List[SingleTankSimulationResult] = field(default_factory=list)
    requested_step_l: float = 0.0
    effective_step_l: float = 0.0
    step_adjusted: bool = False


SWEEP_STEP_QUANTUM_L = 250.0
MAX_SWEEP_POSITIVE_VOLUMES = 40


@dataclass
class SweepVolumeGrid:
    """Plano auditavel da grade discreta usada pela varredura.

    ``positive_volume_count`` nao inclui a alternativa de referencia de 0 L.
    O volume maximo informado sempre e preservado como ultimo ponto; portanto,
    apenas o ultimo intervalo pode ser menor que o passo efetivo.
    """

    volumes_l: List[float]
    requested_step_l: float
    effective_step_l: float
    step_adjusted: bool

    @property
    def positive_volume_count(self) -> int:
        return max(0, len(self.volumes_l) - 1)


def _round_step_up_to_quantum(step_l: float, quantum_l: float) -> float:
    """Round a positive increment upward to the next manufacturing quantum."""
    units = math.ceil((step_l / quantum_l) - 1e-12)
    return max(quantum_l, float(units) * quantum_l)


def build_sweep_volume_grid(
    lower_tank_max: float,
    requested_step_l: float,
    *,
    max_positive_volumes: int = MAX_SWEEP_POSITIVE_VOLUMES,
    step_quantum_l: float = SWEEP_STEP_QUANTUM_L,
) -> SweepVolumeGrid:
    """Build a bounded sweep grid without discarding the requested maximum.

    The step is first rounded upward to a multiple of ``step_quantum_l``. If
    the resulting grid would contain more than ``max_positive_volumes`` tank
    capacities, the step is doubled until the limit is met. The 0-L baseline
    is additional to that limit. When the maximum is not a step multiple it is
    appended explicitly, allowing an auditable shorter terminal interval.
    """
    maximum_l = float(lower_tank_max)
    requested_l = float(requested_step_l)
    quantum_l = float(step_quantum_l)

    if not math.isfinite(maximum_l) or maximum_l < 0:
        raise ValueError("O volume maximo da varredura deve ser finito e nao negativo.")
    if not math.isfinite(requested_l) or requested_l <= 0:
        raise ValueError("O passo de varredura deve ser finito e maior que zero.")
    if not math.isfinite(quantum_l) or quantum_l <= 0:
        raise ValueError("O multiplo-base do passo deve ser maior que zero.")
    if max_positive_volumes <= 0:
        raise ValueError("O limite de volumes positivos deve ser maior que zero.")

    effective_l = _round_step_up_to_quantum(requested_l, quantum_l)
    positive_count = int(math.ceil((maximum_l / effective_l) - 1e-12)) if maximum_l > 0 else 0
    while positive_count > max_positive_volumes:
        effective_l = _round_step_up_to_quantum(effective_l * 2.0, quantum_l)
        positive_count = int(math.ceil((maximum_l / effective_l) - 1e-12))

    volumes_l = [0.0]
    for index in range(1, positive_count):
        volumes_l.append(float(index) * effective_l)
    if maximum_l > 0:
        volumes_l.append(maximum_l)

    tolerance = max(1e-9, abs(requested_l) * 1e-12)
    return SweepVolumeGrid(
        volumes_l=volumes_l,
        requested_step_l=requested_l,
        effective_step_l=effective_l,
        step_adjusted=abs(effective_l - requested_l) > tolerance,
    )


from datetime import datetime, timedelta


def build_detailed_daily_demand_vectors(
    n_days: int,
    start_date_str: str = "01/01/1980",
    demand_mode: str = "constant",
    demand_value: float = 200.0,
    residents_count: float = 4.0,
    rainwater_share: float = 0.4,
    weekly_demands: Optional[List[float]] = None,
    weekly_residents: Optional[List[float]] = None,
    weekly_shares: Optional[List[float]] = None,
    monthly_demands: Optional[List[float]] = None,
    monthly_residents: Optional[List[float]] = None,
    monthly_shares: Optional[List[float]] = None,
    daily_demands: Optional[List[float]] = None,
    daily_residents: Optional[List[float]] = None,
    daily_shares: Optional[List[float]] = None,
    building_config: Optional[dict] = None,
    precip_data: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Constrói séries diárias completas e discretizadas dos componentes de demanda:
    - tot_arr: Demanda total diária após supressão por chuva (L/dia)
    - pluv_arr: Demanda pluvial diária desejada (não-potável interno + irrigação ativa) (L/dia)
    - pot_in_arr: Demanda de potável interno (chuveiros, lavatórios, cozinha) (L/dia)
    - non_pot_in_arr: Demanda de não-potável interno (bacias, lavagem de roupas) (L/dia)
    - irr_arr: Demanda de irrigação após verificação de chuva (L/dia)
    - irr_suppressed_mask: Vetor booleano indicando dias em que a irrigação foi suprimida por chuva
    """
    if building_config is not None:
        demand_mode = building_config.get("demand_mode", demand_mode)
        demand_value = building_config.get("demand", demand_value)
        residents_count = building_config.get("residents", residents_count)
        rainwater_share = building_config.get("share", rainwater_share)
        if "weekly_demands" in building_config:
            weekly_demands = building_config["weekly_demands"]
        if "weekly_residents" in building_config:
            weekly_residents = building_config["weekly_residents"]
        if "weekly_shares" in building_config:
            weekly_shares = building_config["weekly_shares"]
        if "monthly_demands" in building_config:
            monthly_demands = building_config["monthly_demands"]
        if "monthly_residents" in building_config:
            monthly_residents = building_config["monthly_residents"]
        if "monthly_shares" in building_config:
            monthly_shares = building_config["monthly_shares"]
        if "daily_demands" in building_config:
            daily_demands = building_config["daily_demands"]
        if "daily_residents" in building_config:
            daily_residents = building_config["daily_residents"]
        if "daily_shares" in building_config:
            daily_shares = building_config["daily_shares"]

    irr_vol_base = float(building_config.get("irrigation_liters_per_day", 0.0)) if building_config else 0.0
    irr_rain_thresh = float(building_config.get("irrigation_rain_threshold_mm", 2.0)) if building_config else 2.0
    non_pot_indoor_share = building_config.get("non_potable_indoor_share", None) if building_config else None

    try:
        start_dt = datetime.strptime(start_date_str.strip(), "%d/%m/%Y")
    except Exception:
        start_dt = datetime(1980, 1, 1)

    tot_in_arr = np.zeros(n_days, dtype=np.float64)
    sh_in_arr = np.zeros(n_days, dtype=np.float64)

    base_sh = (rainwater_share / 100.0) if rainwater_share > 1.0 else rainwater_share
    base_sh = max(0.0, min(1.0, float(base_sh)))

    if demand_mode == "weekly" and weekly_demands and len(weekly_demands) >= 7:
        w_d = [float(v) if v is not None and float(v) > 0 else float(demand_value) for v in weekly_demands[:7]]
        w_r = [float(v) if v is not None and float(v) > 0 else float(residents_count) for v in (weekly_residents[:7] if weekly_residents and len(weekly_residents) >= 7 else [residents_count]*7)]
        w_s_raw = weekly_shares[:7] if weekly_shares and len(weekly_shares) >= 7 else [base_sh]*7
        w_s = [(float(v)/100.0 if float(v) > 1.0 else float(v)) if v is not None and float(v) >= 0 else base_sh for v in w_s_raw]
        for i in range(n_days):
            cur_dt = start_dt + timedelta(days=i)
            w_idx = cur_dt.weekday()
            tot_in_arr[i] = w_d[w_idx] * w_r[w_idx]
            sh_in_arr[i] = max(0.0, min(1.0, w_s[w_idx]))
    elif (demand_mode == "monthly" or (monthly_demands and len(monthly_demands) >= 12 and demand_mode != "daily")) and monthly_demands and len(monthly_demands) >= 12:
        m_d = [float(v) if v is not None and float(v) > 0 else float(demand_value) for v in monthly_demands[:12]]
        m_r = [float(v) if v is not None and float(v) > 0 else float(residents_count) for v in (monthly_residents[:12] if monthly_residents and len(monthly_residents) >= 12 else [residents_count]*12)]
        m_s_raw = monthly_shares[:12] if monthly_shares and len(monthly_shares) >= 12 else [base_sh]*12
        m_s = [(float(v)/100.0 if float(v) > 1.0 else float(v)) if v is not None and float(v) >= 0 else base_sh for v in m_s_raw]
        for i in range(n_days):
            cur_dt = start_dt + timedelta(days=i)
            m_idx = cur_dt.month - 1
            tot_in_arr[i] = m_d[m_idx] * m_r[m_idx]
            sh_in_arr[i] = max(0.0, min(1.0, m_s[m_idx]))
    elif demand_mode == "daily" and daily_demands and len(daily_demands) > 0:
        len_d = len(daily_demands)
        len_r = len(daily_residents) if daily_residents else 0
        len_s = len(daily_shares) if daily_shares else 0
        for i in range(n_days):
            d_val = float(daily_demands[i % len_d])
            r_val = float(daily_residents[i % len_r]) if len_r > 0 else float(residents_count)
            s_raw = float(daily_shares[i % len_s]) if len_s > 0 else base_sh
            s_val = (s_raw / 100.0) if s_raw > 1.0 else s_raw
            tot_in_arr[i] = max(0.0, d_val * r_val)
            sh_in_arr[i] = max(0.0, min(1.0, s_val))
    else:
        tot_in_arr[:] = float(demand_value) * float(residents_count)
        sh_in_arr[:] = base_sh

    # Determinação das frações internas
    if demand_mode in ("weekly", "monthly", "daily"):
        non_pot_in_arr = tot_in_arr * sh_in_arr
    elif non_pot_indoor_share is not None:
        np_sh = float(non_pot_indoor_share)
        if np_sh > 1.0:
            np_sh /= 100.0
        np_sh = max(0.0, min(1.0, np_sh))
        non_pot_in_arr = tot_in_arr * np_sh
    else:
        non_pot_in_arr = tot_in_arr * sh_in_arr

    pot_in_arr = np.maximum(0.0, tot_in_arr - non_pot_in_arr)

    # Irrigação e supressão por chuva
    irr_arr = np.zeros(n_days, dtype=np.float64)
    irr_suppressed_mask = np.zeros(n_days, dtype=bool)

    if irr_vol_base > 0:
        for i in range(n_days):
            p_val = float(precip_data[i]) if (precip_data is not None and i < len(precip_data)) else 0.0
            if p_val >= irr_rain_thresh:
                irr_suppressed_mask[i] = True
                irr_arr[i] = 0.0
            else:
                irr_suppressed_mask[i] = False
                irr_arr[i] = irr_vol_base

    pluv_arr = non_pot_in_arr + irr_arr
    tot_arr = pot_in_arr + pluv_arr

    return tot_arr, pluv_arr, pot_in_arr, non_pot_in_arr, irr_arr, irr_suppressed_mask


def build_daily_demand_vectors(
    n_days: int,
    start_date_str: str = "01/01/1980",
    demand_mode: str = "constant",
    demand_value: float = 200.0,
    residents_count: float = 4.0,
    rainwater_share: float = 0.4,
    weekly_demands: Optional[List[float]] = None,
    weekly_residents: Optional[List[float]] = None,
    weekly_shares: Optional[List[float]] = None,
    monthly_demands: Optional[List[float]] = None,
    monthly_residents: Optional[List[float]] = None,
    monthly_shares: Optional[List[float]] = None,
    daily_demands: Optional[List[float]] = None,
    daily_residents: Optional[List[float]] = None,
    daily_shares: Optional[List[float]] = None,
    building_config: Optional[dict] = None,
    precip_data: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Constrói vetores diários de demanda total (L/dia) e demanda pluvial (L/dia)
    para o período de simulação de n_days a partir de start_date_str.
    """
    tot_arr, pluv_arr, _, _, _, _ = build_detailed_daily_demand_vectors(
        n_days=n_days,
        start_date_str=start_date_str,
        demand_mode=demand_mode,
        demand_value=demand_value,
        residents_count=residents_count,
        rainwater_share=rainwater_share,
        weekly_demands=weekly_demands,
        weekly_residents=weekly_residents,
        weekly_shares=weekly_shares,
        monthly_demands=monthly_demands,
        monthly_residents=monthly_residents,
        monthly_shares=monthly_shares,
        daily_demands=daily_demands,
        daily_residents=daily_residents,
        daily_shares=daily_shares,
        building_config=building_config,
        precip_data=precip_data,
    )
    return tot_arr, pluv_arr


try:
    import numba
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

if HAS_NUMBA:
    @numba.njit(fastmath=True)
    def _numba_sim_single(
        precip_data, lower_tank_vol, area, runoff_coeff, discard_mm, discard_mode, discard_days_interval, tot_demands_arr, pluvial_demands_arr, non_pot_in_arr, irr_arr, pot_in_arr, irr_backup
    ):
        n_days = len(precip_data)
        v_lower = 0.0
        total_pluvial_consumed = 0.0
        total_potable_consumed = 0.0
        total_spilled = 0.0
        # A repartição entre uso interno e irrigação é acumulada dia a dia, como no
        # kernel Python de referência. Derivá-la dos totais anuais introduziria viés
        # sistemático, pois Σ min(aᵢ,bᵢ) ≤ min(Σaᵢ, Σbᵢ).
        total_pluvial_indoor = 0.0
        total_pluvial_irrigation = 0.0
        total_unmet = 0.0

        days_full = 0
        days_partial = 0
        days_null = 0
        last_discard_day = -999999
        
        for i in range(n_days):
            p_i = precip_data[i]
            tot_demand_day = tot_demands_arr[i]
            pluvial_demand_per_day = pluvial_demands_arr[i]

            apply_discard = False
            if p_i > 0.0:
                if discard_mode == 1:
                    apply_discard = True
                elif discard_mode == 2:
                    prev_p = precip_data[i-1] if i > 0 else 0.0
                    if prev_p < 1.0:
                        apply_discard = True
                elif discard_mode == 3:
                    if (i - last_discard_day) >= discard_days_interval:
                        apply_discard = True

            if apply_discard:
                p_eff = p_i - discard_mm if p_i > discard_mm else 0.0
                last_discard_day = i
            else:
                p_eff = p_i

            v_ac = p_eff * area * runoff_coeff
            v_available_before_c = v_lower + v_ac
            if v_available_before_c > lower_tank_vol:
                v_spill_today = v_available_before_c - lower_tank_vol
                v_in_tank = lower_tank_vol
            else:
                v_spill_today = 0.0
                v_in_tank = v_available_before_c

            v_c = min(pluvial_demand_per_day, v_in_tank)
            v_lower = v_in_tank - v_c

            # A reparticao precisa vir ANTES do potavel: o deficit de irrigacao
            # so vira consumo de rede se o suprimento de reserva estiver ligado.
            c_pluv_in = min(v_c, non_pot_in_arr[i])
            residual = v_c - c_pluv_in
            if residual < 0.0:
                residual = 0.0
            c_pluv_irr = min(residual, irr_arr[i])
            deficit_in = non_pot_in_arr[i] - c_pluv_in
            if deficit_in < 0.0:
                deficit_in = 0.0
            deficit_irr = irr_arr[i] - c_pluv_irr
            if deficit_irr < 0.0:
                deficit_irr = 0.0
            if irr_backup:
                potable_used = pot_in_arr[i] + deficit_in + deficit_irr
                unmet_today = 0.0
            else:
                potable_used = pot_in_arr[i] + deficit_in
                unmet_today = deficit_irr
            if v_c >= pluvial_demand_per_day - 1e-5:
                days_full += 1
            elif v_c > 1e-5:
                days_partial += 1
            else:
                days_null += 1

            total_pluvial_consumed += v_c
            total_potable_consumed += potable_used
            total_spilled += v_spill_today
            total_pluvial_indoor += c_pluv_in
            total_pluvial_irrigation += c_pluv_irr
            total_unmet += unmet_today

        return total_pluvial_consumed, total_potable_consumed, total_spilled, 0.0, 0, 0.0, days_full, days_partial, days_null, total_pluvial_indoor, total_pluvial_irrigation, total_unmet


    @numba.njit(fastmath=True)
    def _numba_sim_dual(
        precip_data, lower_tank_vol, area, runoff_coeff, discard_mm, discard_mode, discard_days_interval, tot_demands_arr, pluvial_demands_arr, upper_tank_vol, pumping_threshold, non_pot_in_arr, irr_arr, pot_in_arr, irr_backup
    ):
        n_days = len(precip_data)
        v_lower = 0.0
        v_upper = 0.0
        total_pluvial_consumed = 0.0
        total_potable_consumed = 0.0
        total_spilled = 0.0
        total_pumped = 0.0
        total_pump_cycles = 0
        max_pump_batch = 0.0
        # Ver a nota em _numba_sim_single: a repartição é acumulada dia a dia.
        total_pluvial_indoor = 0.0
        total_pluvial_irrigation = 0.0
        total_unmet = 0.0

        days_full = 0
        days_partial = 0
        days_null = 0
        last_discard_day = -999999

        for i in range(n_days):
            p_i = precip_data[i]
            tot_demand_day = tot_demands_arr[i]
            pluvial_demand_per_day = pluvial_demands_arr[i]

            apply_discard = False
            if p_i > 0.0:
                if discard_mode == 1:
                    apply_discard = True
                elif discard_mode == 2:
                    prev_p = precip_data[i-1] if i > 0 else 0.0
                    if prev_p < 1.0:
                        apply_discard = True
                elif discard_mode == 3:
                    if (i - last_discard_day) >= discard_days_interval:
                        apply_discard = True

            if apply_discard:
                p_eff = p_i - discard_mm if p_i > discard_mm else 0.0
                last_discard_day = i
            else:
                p_eff = p_i

            v_ac = p_eff * area * runoff_coeff
            v_c = 0.0
            v_spill_today = 0.0
            v_rec_today = 0.0
            cycles_today = 0

            v_available_before_c = v_lower + v_ac
            if v_available_before_c > lower_tank_vol:
                v_spill_today = v_available_before_c - lower_tank_vol
                v_lower = lower_tank_vol
            else:
                v_lower = v_available_before_c

            needed = pluvial_demand_per_day
            while needed > 1e-6:
                if v_upper > pumping_threshold:
                    draw = min(needed, v_upper - pumping_threshold)
                    v_c += draw
                    v_upper -= draw
                    needed -= draw
                    if needed <= 1e-6:
                        break

                if v_lower > 1e-6 and v_upper < upper_tank_vol:
                    pump_capacity_needed = upper_tank_vol - v_upper
                    pump_vol = min(v_lower, pump_capacity_needed)
                    v_lower -= pump_vol
                    v_upper += pump_vol
                    v_rec_today += pump_vol
                    cycles_today += 1
                    if pump_vol > max_pump_batch:
                        max_pump_batch = pump_vol
                    draw = min(needed, v_upper)
                    v_c += draw
                    v_upper -= draw
                    needed -= draw
                else:
                    if v_upper > 1e-6:
                        draw = min(needed, v_upper)
                        v_c += draw
                        v_upper -= draw
                        needed -= draw
                    else:
                        break

            # A reparticao precisa vir ANTES do potavel: o deficit de irrigacao
            # so vira consumo de rede se o suprimento de reserva estiver ligado.
            c_pluv_in = min(v_c, non_pot_in_arr[i])
            residual = v_c - c_pluv_in
            if residual < 0.0:
                residual = 0.0
            c_pluv_irr = min(residual, irr_arr[i])
            deficit_in = non_pot_in_arr[i] - c_pluv_in
            if deficit_in < 0.0:
                deficit_in = 0.0
            deficit_irr = irr_arr[i] - c_pluv_irr
            if deficit_irr < 0.0:
                deficit_irr = 0.0
            if irr_backup:
                potable_used = pot_in_arr[i] + deficit_in + deficit_irr
                unmet_today = 0.0
            else:
                potable_used = pot_in_arr[i] + deficit_in
                unmet_today = deficit_irr
            if v_c >= pluvial_demand_per_day - 1e-5:
                days_full += 1
            elif v_c > 1e-5:
                days_partial += 1
            else:
                days_null += 1

            total_pluvial_consumed += v_c
            total_potable_consumed += potable_used
            total_spilled += v_spill_today
            total_pumped += v_rec_today
            total_pump_cycles += cycles_today
            total_pluvial_indoor += c_pluv_in
            total_pluvial_irrigation += c_pluv_irr
            total_unmet += unmet_today

        return total_pluvial_consumed, total_potable_consumed, total_spilled, total_pumped, total_pump_cycles, max_pump_batch, days_full, days_partial, days_null, total_pluvial_indoor, total_pluvial_irrigation, total_unmet


def validar_parametros_fisicos(
    lower_tank_vol: float,
    area: float,
    runoff_coeff: float,
    discard_mm: float,
    total_demand_per_day: float,
    rainwater_share: float,
    upper_tank_vol: float = 0.0,
) -> None:
    """Rejeita entrada fisicamente impossivel, antes de simular.

    Ate a versao 5.0.8 area negativa, coeficiente negativo e volume negativo
    passavam sem erro e produziam potencial de economia NEGATIVO - de -166% no
    caso do volume. Um percentual assim nao significa nada e atravessa o
    programa inteiro: vira economia de agua no economico, emissao evitada na
    ACV e numero no relatorio.

    Nao se cala o valor: area negativa e erro de digitacao, e quem digitou
    precisa ver. Levanta-se `ValueError` nomeando o campo.

    Volume ZERO e valido: e a referencia "sem sistema" da varredura.
    """
    if lower_tank_vol < 0:
        raise ValueError(
            f"Volume do reservatorio inferior negativo ({lower_tank_vol:g} L). "
            "Zero e valido e representa o cenario sem sistema; negativo, nao."
        )
    if upper_tank_vol < 0:
        raise ValueError(f"Volume do reservatorio superior negativo ({upper_tank_vol:g} L).")
    if area < 0:
        raise ValueError(f"Area de captacao negativa ({area:g} m2).")
    if not 0.0 <= runoff_coeff <= 1.0:
        raise ValueError(
            f"Coeficiente de escoamento fora de [0, 1]: {runoff_coeff:g}. "
            "Acima de 1 a cobertura entregaria mais agua do que a chuva traz; "
            "abaixo de 0, captacao negativa. Telhados usuais ficam entre 0,80 e 0,95."
        )
    if discard_mm < 0:
        raise ValueError(
            f"Lamina de descarte negativa ({discard_mm:g} mm): o descarte retira "
            "agua da captacao, nao acrescenta."
        )
    if total_demand_per_day < 0:
        raise ValueError(f"Demanda diaria negativa ({total_demand_per_day:g} L/dia).")
    if not 0.0 <= rainwater_share <= 1.0:
        raise ValueError(
            f"Fracao atendivel por agua pluvial fora de [0, 1]: {rainwater_share:g}. "
            "Informe 0,4 para 40%, nao 40."
        )

def run_single_simulation(
    precip_data: np.ndarray,
    lower_tank_vol: float,
    area: float = 100.0,
    runoff_coeff: float = COEFICIENTE_DE_ESCOAMENTO_PADRAO,
    discard_mm: float = 1.0,
    discard_mode: int = 1,  # 1 = Todos os eventos, 2 = 1º evento pós estiagem (1 dia sem chuva), 3 = A cada X dias
    discard_days_interval: int = 7,  # Intervalo de dias para o modo 3
    total_demand_per_day: float = 300.0,  # 100 L/capita * 3 residents = 300 L/day
    rainwater_share: float = 0.4,  # 40% -> 120 L/day pluvial demand
    upper_tank_vol: float = 0.0,
    upper_tank_used: bool = False,
    pumping_threshold: float = 0.0,
    store_daily_details: bool = False,
    monthly_demands: Optional[List[float]] = None,
    monthly_residents: Optional[List[float]] = None,
    monthly_shares: Optional[List[float]] = None,
    weekly_demands: Optional[List[float]] = None,
    weekly_residents: Optional[List[float]] = None,
    weekly_shares: Optional[List[float]] = None,
    daily_demands: Optional[List[float]] = None,
    daily_residents: Optional[List[float]] = None,
    daily_shares: Optional[List[float]] = None,
    demand_mode: str = "constant",
    start_date_str: str = "01/01/1980",
    building_config: Optional[dict] = None,
    tot_demands_arr: Optional[np.ndarray] = None,
    pluvial_demands_arr: Optional[np.ndarray] = None,
) -> SingleTankSimulationResult:
    """
    Executes daily water balance simulation for a specific lower tank volume.
    Replicates Netuno 4.0 exact daily water balance equations.
    Supports constant, weekly, monthly and full daily modulated demand series.
    """
    # Entrada fisicamente impossivel produz resultado sem sentido que atravessa
    # o programa inteiro sem erro. Barra-se aqui, nomeando o campo.
    validar_parametros_fisicos(
        lower_tank_vol=float(lower_tank_vol),
        area=float(area),
        runoff_coeff=float(runoff_coeff),
        discard_mm=float(discard_mm),
        total_demand_per_day=float(total_demand_per_day),
        rainwater_share=float(rainwater_share),
        upper_tank_vol=float(upper_tank_vol),
    )

    n_days = len(precip_data)
    pumping_threshold = max(0.0, min(float(pumping_threshold), max(0.0, float(upper_tank_vol))))

    if tot_demands_arr is None or pluvial_demands_arr is None:
        tot_demands_arr, pluvial_demands_arr, pot_in_arr, non_pot_in_arr, irr_arr, irr_suppressed_mask = build_detailed_daily_demand_vectors(
            n_days=n_days,
            start_date_str=start_date_str,
            demand_mode=demand_mode,
            demand_value=total_demand_per_day / (float(building_config.get("residents", 4)) if building_config else 1.0) if building_config is None and monthly_demands is None else (building_config.get("demand", 200.0) if building_config else total_demand_per_day),
            residents_count=float(building_config.get("residents", 4)) if building_config else 1.0,
            rainwater_share=rainwater_share,
            weekly_demands=weekly_demands,
            weekly_residents=weekly_residents,
            weekly_shares=weekly_shares,
            monthly_demands=monthly_demands,
            monthly_residents=monthly_residents,
            monthly_shares=monthly_shares,
            daily_demands=daily_demands,
            daily_residents=daily_residents,
            daily_shares=daily_shares,
            building_config=building_config,
            precip_data=precip_data,
        )
    else:
        pot_in_arr = None
        non_pot_in_arr = None
        irr_arr = None
        irr_suppressed_mask = None

    if HAS_NUMBA and not store_daily_details:
        p_arr = np.ascontiguousarray(precip_data, dtype=np.float64)
        t_arr = np.ascontiguousarray(tot_demands_arr, dtype=np.float64)
        pl_arr = np.ascontiguousarray(pluvial_demands_arr, dtype=np.float64)

        # Vetores da repartição interno/irrigação. Quando a edificação não define
        # irrigação, usar a própria demanda pluvial como teto do uso interno faz o
        # kernel reproduzir exatamente o caso sem repartição: como
        # v_c = min(demanda_pluvial, disponível) ≤ demanda_pluvial, o mínimo diário
        # devolve v_c inteiro ao uso interno e zero à irrigação.
        if non_pot_in_arr is not None and irr_arr is not None:
            np_in_arr = np.ascontiguousarray(non_pot_in_arr, dtype=np.float64)
            ir_arr = np.ascontiguousarray(irr_arr, dtype=np.float64)
        else:
            np_in_arr = pl_arr
            ir_arr = np.zeros(len(p_arr), dtype=np.float64)

        # A bandeira do suprimento de reserva atravessa ate o kernel: sem ela,
        # desligar a reserva nao mudava um litro no resumo.
        irr_backup = bool(building_config.get("irrigation_potable_backup", True)) \
            if building_config else True
        if pot_in_arr is not None:
            pt_arr = np.ascontiguousarray(pot_in_arr, dtype=np.float64)
        else:
            pt_arr = np.ascontiguousarray(
                np.maximum(0.0, t_arr - pl_arr), dtype=np.float64)

        if not upper_tank_used or upper_tank_vol <= 0:
            res_tup = _numba_sim_single(
                p_arr, float(lower_tank_vol), float(area), float(runoff_coeff), float(discard_mm), int(discard_mode), int(discard_days_interval), t_arr, pl_arr, np_in_arr, ir_arr, pt_arr, irr_backup
            )
        else:
            res_tup = _numba_sim_dual(
                p_arr, float(lower_tank_vol), float(area), float(runoff_coeff), float(discard_mm), int(discard_mode), int(discard_days_interval), t_arr, pl_arr, float(upper_tank_vol), float(pumping_threshold), np_in_arr, ir_arr, pt_arr, irr_backup
            )

        tot_pluv, tot_pot, tot_spill, tot_pump, tot_cycles, max_batch, d_full, d_part, d_null, pluv_indoor, pluv_irrigation, tot_unmet = res_tup
        total_demand_period = float(np.sum(tot_demands_arr))
        potential_savings_pct = (tot_pluv / total_demand_period) * 100.0 if total_demand_period > 0 else 0.0
        # O potavel vem do acumulador, e nao da diferenca: com o suprimento de
        # reserva desligado, a irrigacao nao atendida nao e comprada da rede.
        avg_potable_kernel = tot_pot / len(p_arr)
        avg_unmet_kernel = tot_unmet / len(p_arr)
        
        days_supp = int(np.sum(irr_suppressed_mask)) if irr_suppressed_mask is not None else 0
        irr_vol_nominal = float(building_config.get("irrigation_liters_per_day", 0.0)) if building_config else 0.0
        vol_supp = days_supp * irr_vol_nominal

        # Valores exatos, acumulados dia a dia dentro do kernel. Até a versão 5.0.7
        # estes eram estimados a partir dos totais anuais, o que superestimava o uso
        # interno e subestimava a irrigação em até 26%.
        pluv_in_est = pluv_indoor
        pluv_irr_est = pluv_irrigation

        return SingleTankSimulationResult(
            lower_tank_vol=lower_tank_vol,
            potential_potable_savings_pct=potential_savings_pct,
            avg_pluvial_consumed_l_day=tot_pluv / n_days,
            avg_potable_consumed_l_day=avg_potable_kernel,
            avg_spilled_l_day=tot_spill / n_days,
            pct_days_full_satisfaction=(d_full / n_days) * 100.0,
            pct_days_partial_satisfaction=(d_part / n_days) * 100.0,
            pct_days_null_satisfaction=(d_null / n_days) * 100.0,
            daily_results=[],
            n_days_simulated=n_days,
            total_pumped_liters=tot_pump,
            total_pump_cycles=tot_cycles,
            max_pump_batch_liters=max_batch,
            avg_pluvial_indoor_consumed_l_day=pluv_in_est / n_days,
            avg_pluvial_irrigation_consumed_l_day=pluv_irr_est / n_days,
            avg_irrigation_suppressed_l_day=vol_supp / n_days,
            total_irrigation_days_suppressed=days_supp,
            total_irrigation_days_active=n_days - days_supp,
            avg_unmet_demand_l_day=avg_unmet_kernel,
        )

    # State variables (Pure Python fallback and detailed daily results)
    v_lower = 0.0  # Lower reservoir starts empty
    v_upper = 0.0  # Upper reservoir starts empty

    total_pluvial_consumed = 0.0
    total_pluvial_indoor_consumed = 0.0
    total_pluvial_irrigation_consumed = 0.0
    total_potable_consumed = 0.0
    total_unmet_demand = 0.0
    total_spilled = 0.0
    total_pumped = 0.0
    total_pump_cycles = 0
    max_pump_batch = 0.0
    
    days_full = 0
    days_partial = 0
    days_null = 0
    days_irr_suppressed = 0
    vol_irr_suppressed = 0.0
    
    daily_list: List[SimulationDayResult] = []
    total_demand_period = 0.0
    last_discard_day = -999999

    irr_backup_enabled = bool(building_config.get("irrigation_potable_backup", True)) if building_config else True
    irr_nominal_rate = float(building_config.get("irrigation_liters_per_day", 0.0)) if building_config else 0.0

    for i in range(n_days):
        p_i = precip_data[i]
        tot_demand_day = tot_demands_arr[i]
        pluvial_demand_per_day = pluvial_demands_arr[i]
        total_demand_period += tot_demand_day

        pot_in_day = pot_in_arr[i] if pot_in_arr is not None else max(0.0, tot_demand_day - pluvial_demand_per_day)
        non_pot_in_day = non_pot_in_arr[i] if non_pot_in_arr is not None else pluvial_demand_per_day
        irr_day = irr_arr[i] if irr_arr is not None else 0.0
        is_suppressed = bool(irr_suppressed_mask[i]) if irr_suppressed_mask is not None else False

        if is_suppressed:
            days_irr_suppressed += 1
            vol_irr_suppressed += irr_nominal_rate
        
        # 1. Effective rainfall & harvested volume (Abordagens de Descarte Inicial / First Flush)
        apply_discard = False
        if p_i > 0.0:
            if discard_mode == 1:
                apply_discard = True
            elif discard_mode == 2:
                prev_p = precip_data[i-1] if i > 0 else 0.0
                if prev_p < 1.0:
                    apply_discard = True
            elif discard_mode == 3:
                if (i - last_discard_day) >= discard_days_interval:
                    apply_discard = True

        if apply_discard:
            p_eff = p_i - discard_mm if p_i > discard_mm else 0.0
            last_discard_day = i
        else:
            p_eff = p_i

        v_ac = p_eff * area * runoff_coeff  # Liters
        
        v_c = 0.0  # Pluvial consumed today
        v_spill_today = 0.0
        v_rec_today = 0.0
        cycles_today = 0
        
        if not upper_tank_used or upper_tank_vol <= 0:
            # === SINGLE TANK SYSTEM (Only Lower Reservoir) ===
            v_available_before_c = v_lower + v_ac
            if v_available_before_c > lower_tank_vol:
                v_spill_today = v_available_before_c - lower_tank_vol
                v_in_tank = lower_tank_vol
            else:
                v_in_tank = v_available_before_c
                
            v_c = min(pluvial_demand_per_day, v_in_tank)
            v_lower = v_in_tank - v_c
            v_upper = 0.0
            
        else:
            # === DUAL TANK SYSTEM (Lower + Upper Reservoir) ===
            v_available_before_c = v_lower + v_ac
            if v_available_before_c > lower_tank_vol:
                v_spill_today = v_available_before_c - lower_tank_vol
                v_lower = lower_tank_vol
            else:
                v_lower = v_available_before_c
                
            needed = pluvial_demand_per_day
            
            while needed > 1e-6:
                if v_upper > pumping_threshold:
                    draw = min(needed, v_upper - pumping_threshold)
                    v_c += draw
                    v_upper -= draw
                    needed -= draw
                    if needed <= 1e-6:
                        break
                        
                if v_lower > 1e-6 and v_upper < upper_tank_vol:
                    pump_capacity_needed = upper_tank_vol - v_upper
                    pump_vol = min(v_lower, pump_capacity_needed)
                    v_lower -= pump_vol
                    v_upper += pump_vol
                    v_rec_today += pump_vol
                    cycles_today += 1
                    max_pump_batch = max(max_pump_batch, pump_vol)
                    
                    draw = min(needed, v_upper)
                    v_c += draw
                    v_upper -= draw
                    needed -= draw
                else:
                    if v_upper > 1e-6:
                        draw = min(needed, v_upper)
                        v_c += draw
                        v_upper -= draw
                        needed -= draw
                    else:
                        break
                        
        # Discretização do atendimento pluvial (Prioridade 1: Não-Potável Interno, Prioridade 2: Irrigação)
        c_pluv_in = min(v_c, non_pot_in_day)
        c_pluv_irr = min(max(0.0, v_c - c_pluv_in), irr_day)
        total_pluvial_indoor_consumed += c_pluv_in
        total_pluvial_irrigation_consumed += c_pluv_irr

        deficit_in = max(0.0, non_pot_in_day - c_pluv_in)
        deficit_irr = max(0.0, irr_day - c_pluv_irr) if irr_backup_enabled else 0.0
        potable_used = pot_in_day + deficit_in + deficit_irr
        # Sem suprimento de reserva, o deficit de irrigacao nao e comprado da
        # rede: fica como demanda nao atendida, e o balanco precisa mostra-la.
        unmet_today = 0.0 if irr_backup_enabled else max(0.0, irr_day - c_pluv_irr)
        
        # Satisfaction metric
        if v_c >= pluvial_demand_per_day - 1e-5:
            sat_type = 2  # Full
            days_full += 1
        elif v_c > 1e-5:
            sat_type = 1  # Partial
            days_partial += 1
        else:
            sat_type = 0  # Null
            days_null += 1
            
        total_pluvial_consumed += v_c
        total_potable_consumed += potable_used
        total_unmet_demand += unmet_today
        total_spilled += v_spill_today
        total_pumped += v_rec_today
        total_pump_cycles += cycles_today
        
        if store_daily_details:
            daily_list.append(SimulationDayResult(
                day_index=i,
                precip_mm=p_i,
                eff_precip_mm=p_eff,
                harvested_liters=v_ac,
                total_demand_liters=tot_demand_day,
                pluvial_demand_liters=pluvial_demand_per_day,
                pluvial_consumed_liters=v_c,
                potable_consumed_liters=potable_used,
                spilled_liters=v_spill_today,
                lower_tank_end_liters=v_lower,
                upper_tank_end_liters=v_upper,
                pumped_liters=v_rec_today,
                pump_cycles=cycles_today,
                satisfaction_type=sat_type,
                potable_indoor_consumed_liters=pot_in_day,
                pluvial_indoor_consumed_liters=c_pluv_in,
                pluvial_irrigation_consumed_liters=c_pluv_irr,
                irrigation_demand_liters=irr_day,
                irrigation_suppressed=is_suppressed,
            ))
        
    # Summary Metrics
    potential_savings_pct = (total_pluvial_consumed / total_demand_period) * 100.0 if total_demand_period > 0 else 0.0
    
    avg_pluvial = total_pluvial_consumed / n_days
    # Vem do acumulador dia a dia, que respeita o suprimento de reserva. Ate a
    # versao 5.0.8 era recalculado por diferenca, o que atribuia ao potavel toda
    # a demanda nao atendida pela chuva - inclusive a irrigacao que a regra manda
    # nao fazer. Com a reserva ligada, que e o padrao, as duas formulas coincidem.
    avg_potable = total_potable_consumed / n_days
    avg_spilled = total_spilled / n_days
    
    pct_full = (days_full / n_days) * 100.0
    pct_partial = (days_partial / n_days) * 100.0
    pct_null = (days_null / n_days) * 100.0
    
    return SingleTankSimulationResult(
        lower_tank_vol=lower_tank_vol,
        potential_potable_savings_pct=potential_savings_pct,
        avg_pluvial_consumed_l_day=avg_pluvial,
        avg_potable_consumed_l_day=avg_potable,
        avg_spilled_l_day=avg_spilled,
        pct_days_full_satisfaction=pct_full,
        pct_days_partial_satisfaction=pct_partial,
        pct_days_null_satisfaction=pct_null,
        daily_results=daily_list,
        n_days_simulated=n_days,
        total_pumped_liters=total_pumped,
        total_pump_cycles=total_pump_cycles,
        max_pump_batch_liters=max_pump_batch,
        avg_pluvial_indoor_consumed_l_day=total_pluvial_indoor_consumed / n_days,
        avg_pluvial_irrigation_consumed_l_day=total_pluvial_irrigation_consumed / n_days,
        avg_irrigation_suppressed_l_day=vol_irr_suppressed / n_days,
        total_irrigation_days_suppressed=days_irr_suppressed,
        total_irrigation_days_active=n_days - days_irr_suppressed,
        avg_unmet_demand_l_day=total_unmet_demand / n_days,
    )


def run_sweep_simulation(
    precip_data: np.ndarray,
    lower_tank_max: float = 10000.0,
    lower_tank_step: float = 250.0,
    area: float = 100.0,
    runoff_coeff: float = COEFICIENTE_DE_ESCOAMENTO_PADRAO,
    discard_mm: float = 1.0,
    discard_mode: int = 1,
    discard_days_interval: int = 7,
    total_demand_per_day: float = 300.0,
    rainwater_share: float = 0.4,
    upper_tank_vol: float = 0.0,
    upper_tank_used: bool = False,
    pumping_threshold: float = 0.0,
    delta_ideal_threshold: float = 5.0,  # %/m3
    store_daily_details: bool = False,
    monthly_demands: Optional[List[float]] = None,
    monthly_residents: Optional[List[float]] = None,
    monthly_shares: Optional[List[float]] = None,
    weekly_demands: Optional[List[float]] = None,
    weekly_residents: Optional[List[float]] = None,
    weekly_shares: Optional[List[float]] = None,
    daily_demands: Optional[List[float]] = None,
    daily_residents: Optional[List[float]] = None,
    daily_shares: Optional[List[float]] = None,
    demand_mode: str = "constant",
    start_date_str: str = "01/01/1980",
    building_config: Optional[dict] = None,
) -> SweepSimulationResult:
    """
    Runs simulations on a bounded lower-reservoir grid.
    Supports constant, weekly, monthly and full daily modulated demand series.
    Calculates marginal delta potential (%/m3) and determines Optimal Reservoir Volume (V_ideal).
    """
    grid = build_sweep_volume_grid(lower_tank_max, lower_tank_step)
    vols = grid.volumes_l
        
    n_days = len(precip_data)
    tot_demands_arr, pluvial_demands_arr = build_daily_demand_vectors(
        n_days=n_days,
        start_date_str=start_date_str,
        demand_mode=demand_mode,
        demand_value=total_demand_per_day / (float(building_config.get("residents", 4)) if building_config else 1.0) if building_config is None and monthly_demands is None else (building_config.get("demand", 200.0) if building_config else total_demand_per_day),
        residents_count=float(building_config.get("residents", 4)) if building_config else 1.0,
        rainwater_share=rainwater_share,
        weekly_demands=weekly_demands,
        weekly_residents=weekly_residents,
        weekly_shares=weekly_shares,
        monthly_demands=monthly_demands,
        monthly_residents=monthly_residents,
        monthly_shares=monthly_shares,
        daily_demands=daily_demands,
        daily_residents=daily_residents,
        daily_shares=daily_shares,
        building_config=building_config,
        precip_data=precip_data,
    )

    results: List[SingleTankSimulationResult] = []
    
    for v in vols:
        res = run_single_simulation(
            precip_data=precip_data,
            lower_tank_vol=v,
            area=area,
            runoff_coeff=runoff_coeff,
            discard_mm=discard_mm,
            discard_mode=discard_mode,
            discard_days_interval=discard_days_interval,
            total_demand_per_day=total_demand_per_day,
            rainwater_share=rainwater_share,
            upper_tank_vol=upper_tank_vol,
            upper_tank_used=upper_tank_used,
            pumping_threshold=pumping_threshold,
            store_daily_details=store_daily_details,
            monthly_demands=monthly_demands,
            monthly_residents=monthly_residents,
            monthly_shares=monthly_shares,
            weekly_demands=weekly_demands,
            weekly_residents=weekly_residents,
            weekly_shares=weekly_shares,
            daily_demands=daily_demands,
            daily_residents=daily_residents,
            daily_shares=daily_shares,
            demand_mode=demand_mode,
            start_date_str=start_date_str,
            building_config=building_config,
            tot_demands_arr=tot_demands_arr,
            pluvial_demands_arr=pluvial_demands_arr,
        )
        results.append(res)
        
    # Calculate marginal delta (%/m3)
    # delta = (pot[i] - pot[i-1]) / ((v[i] - v[i-1]) / 1000.0)
    optimal_vol: Optional[float] = None
    optimal_pot: Optional[float] = None
    
    for i in range(len(results)):
        if i == 0:
            results[i].delta_potential_per_m3 = 0.0
        else:
            delta_pot = results[i].potential_potable_savings_pct - results[i-1].potential_potable_savings_pct
            delta_vol_m3 = (results[i].lower_tank_vol - results[i-1].lower_tank_vol) / 1000.0
            if delta_vol_m3 > 0:
                results[i].delta_potential_per_m3 = delta_pot / delta_vol_m3
            else:
                results[i].delta_potential_per_m3 = 0.0
                
            # Optimal volume criteria (Eq 4.8 from Netuno manual):
            # V_ideal = menor volume onde delta_potential / delta_vol_m3 <= threshold (%/m3)
            if optimal_vol is None and results[i].lower_tank_vol > 0 and results[i].delta_potential_per_m3 <= delta_ideal_threshold:
                optimal_vol = results[i].lower_tank_vol
                optimal_pot = results[i].potential_potable_savings_pct
                
    # Fallback if range was too small to reach delta threshold: take the maximum volume in sweep
    if optimal_vol is None and len(results) > 1:
        optimal_vol = results[-1].lower_tank_vol
        optimal_pot = results[-1].potential_potable_savings_pct

    return SweepSimulationResult(
        optimal_lower_tank_vol=optimal_vol,
        optimal_potential_pct=optimal_pot,
        results_by_volume=results,
        requested_step_l=grid.requested_step_l,
        effective_step_l=grid.effective_step_l,
        step_adjusted=grid.step_adjusted,
    )
