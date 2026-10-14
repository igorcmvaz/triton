"""Módulo de execução paralela e varredura multi-cenário para dimensionamento de reservatórios."""
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional, Union, Callable
from triton.core.fracao_atendivel import validar_fracao
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from triton.core.parser import load_precipitation
from triton.core.simulation import run_single_simulation, run_sweep_simulation, SingleTankSimulationResult, SweepSimulationResult
from triton.core.hydrology_defaults import LAMINA_DE_DESCARTE_PADRAO_MM

@dataclass
class ScenarioItem:
    scenario_id: str
    city_name: str
    precip_file: str
    area: float
    residents: int
    demand_per_capita: float
    total_demand_l_day: float
    rainwater_share: float
    runoff_coeff: float
    lower_tank_vol: float
    is_sweep: bool = False
    lower_tank_max: float = 10000.0
    lower_tank_step: float = 250.0


@dataclass
class ScenarioOutput:
    scenario: ScenarioItem
    result: Optional[SingleTankSimulationResult] = None
    sweep_result: Optional[SweepSimulationResult] = None


@dataclass
class MultiScenarioMatrixResult:
    total_scenarios_run: int
    outputs: List[ScenarioOutput] = field(default_factory=list)
    summary_matrix: List[Dict[str, Any]] = field(default_factory=list)


def _worker_run_scenario_sweep(task_tuple: Tuple) -> Tuple[ScenarioOutput, Dict[str, Any]]:
    (
        scen_id, city_label, p_path, p_data, area, res, d_cap, tot_demand, r_share, runoff,
        max_vol, sweep_step, upper_vol, upper_used, p_thresh, discard, delta_ideal, discard_mode, discard_days_interval
    ) = task_tuple

    scen_item = ScenarioItem(
        scenario_id=scen_id,
        city_name=city_label,
        precip_file=p_path,
        area=area,
        residents=res,
        demand_per_capita=d_cap,
        total_demand_l_day=tot_demand,
        rainwater_share=r_share,
        runoff_coeff=runoff,
        lower_tank_vol=max_vol,
        is_sweep=True,
        lower_tank_max=max_vol,
        lower_tank_step=sweep_step
    )

    sw_res = run_sweep_simulation(
        precip_data=p_data,
        lower_tank_max=max_vol,
        lower_tank_step=sweep_step,
        area=area,
        runoff_coeff=runoff,
        discard_mm=discard,
        total_demand_per_day=tot_demand,
        rainwater_share=r_share,
        upper_tank_vol=upper_vol,
        upper_tank_used=upper_used,
        pumping_threshold=p_thresh,
        discard_mode=discard_mode,
        discard_days_interval=discard_days_interval,
        delta_ideal_threshold=delta_ideal,
        store_daily_details=False
    )

    opt_single_res = None
    if sw_res.results_by_volume:
        for r_vol in sw_res.results_by_volume:
            if r_vol.lower_tank_vol == sw_res.optimal_lower_tank_vol:
                opt_single_res = r_vol
                break
        if opt_single_res is None:
            opt_single_res = sw_res.results_by_volume[-1]

    matrix_row = {
        "id": scen_id,
        "city": city_label,
        "area_m2": area,
        "residents": res,
        "demand_l_capita_day": d_cap,
        "total_demand_l_day": tot_demand,
        "rainwater_share_pct": r_share * 100.0,
        "runoff_coeff": runoff,
        "optimal_lower_tank_l": sw_res.optimal_lower_tank_vol,
        "optimal_potential_pct": sw_res.optimal_potential_pct,
        "avg_pluvial_l_day": opt_single_res.avg_pluvial_consumed_l_day if opt_single_res else 0.0,
        "avg_spilled_l_day": opt_single_res.avg_spilled_l_day if opt_single_res else 0.0
    }

    return ScenarioOutput(scenario=scen_item, result=opt_single_res, sweep_result=sw_res), matrix_row


def run_multi_scenario_matrix(
    precip_files: List[Tuple[str, str]],
    areas: List[float],
    residents_list: List[int],
    demands_per_capita: List[float],
    rainwater_shares: List[float],
    lower_tanks: List[float],
    runoff_coeffs: Union[float, List[float]] = 0.9,
    upper_tank_vol: float = 500.0,
    upper_tank_used: bool = False,
    pumping_threshold: float = 375.0,
    discard_mm: float = LAMINA_DE_DESCARTE_PADRAO_MM,
    discard_mode: int = 1,
    discard_days_interval: int = 7,
    delta_ideal: float = 2.0,
    run_as_sweeps: bool = True,
    sweep_step: float = 500.0,
    parallel: bool = True,
    progress_callback: Optional[Callable[[int, int, ScenarioOutput, Dict[str, Any]], None]] = None
) -> MultiScenarioMatrixResult:
    """
    Executa simulação de matriz fatorial multi-cenários usando o motor oficial triton.core.simulation.

    `rainwater_shares` são frações de 0 a 1; quem recebe percentual da tela converte antes.
    Suporta computação paralela multi-core para alta performance e notificação de progresso via callback.
    """
    precip_cache: Dict[str, np.ndarray] = {}
    for label, path in precip_files:
        precip_cache[label] = load_precipitation(path)

    if isinstance(runoff_coeffs, (int, float)):
        r_coeffs_list = [float(runoff_coeffs)]
    else:
        r_coeffs_list = [float(c) for c in runoff_coeffs]

    max_vol = max(lower_tanks) if lower_tanks else 10000.0

    tasks = []
    scen_counter = 0

    for city_label, p_path in precip_files:
        p_data = precip_cache[city_label]
        for area in areas:
            for res in residents_list:
                for d_cap in demands_per_capita:
                    for r_share in rainwater_shares:
                        for runoff in r_coeffs_list:
                            scen_counter += 1
                            scen_id = f"SCEN_{scen_counter:04d}"
                            tot_demand = d_cap * res
                            r_share_val = validar_fracao("A fração atendível do cenário", r_share)
                            
                            tasks.append((
                                scen_id, city_label, p_path, p_data, area, res, d_cap, tot_demand, r_share_val, runoff,
                                max_vol, sweep_step, upper_tank_vol, upper_tank_used, pumping_threshold, discard_mm, delta_ideal, discard_mode, discard_days_interval
                            ))

    outputs: List[ScenarioOutput] = []
    matrix_rows: List[Dict[str, Any]] = []
    total_tasks = len(tasks)
    completed = 0

    if parallel and total_tasks > 1:
        cpu_cores = os.cpu_count() or 4
        num_workers = max(1, cpu_cores - 1)
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(_worker_run_scenario_sweep, t) for t in tasks]
            for f in as_completed(futures):
                scen_out, m_row = f.result()
                outputs.append(scen_out)
                matrix_rows.append(m_row)
                completed += 1
                if progress_callback:
                    progress_callback(completed, total_tasks, scen_out, m_row)
    else:
        for t in tasks:
            scen_out, m_row = _worker_run_scenario_sweep(t)
            outputs.append(scen_out)
            matrix_rows.append(m_row)
            completed += 1
            if progress_callback:
                progress_callback(completed, total_tasks, scen_out, m_row)

    return MultiScenarioMatrixResult(
        total_scenarios_run=len(outputs),
        outputs=outputs,
        summary_matrix=matrix_rows
    )


def export_matrix_planilha_csv(matrix_res: MultiScenarioMatrixResult, file_path: str) -> str:
    """
    Exports MultiScenarioMatrixResult to a Planilha.csv file matching Netuno 4.0 exact matrix format.
    """
    from triton.core.parser import format_triton_float
    
    header = "Simulação;Dados de precipitação;Descarte precipitação;Área de captação;Demanda de água potável;Número de habitantes;Percentual de substituição;Coeficiente de escoamento superficial;Reservatório superior;Reservatório inferior;Potencial de economia de água potável;"
    lines = [header]
    
    for idx, out in enumerate(matrix_res.outputs, start=1):
        scen = out.scenario
        opt_v = scen.lower_tank_vol
        opt_v_str = f"{opt_v:g} L" if opt_v and opt_v > 0 else "Vol ideal: não encontrado"
        
        row = (
            f"{idx};"
            f"{os.path.basename(scen.precip_file)};"
            f"{format_triton_float(1.0)};"
            f"{format_triton_float(scen.area, 0)};"
            f"{format_triton_float(scen.demand_per_capita, 0)};"
            f"{scen.residents};"
            f"{format_triton_float(scen.rainwater_share * 100.0, 0)};"
            f"{format_triton_float(scen.runoff_coeff, 1)};"
            f"0 | 0%;"
            f"{opt_v_str};"
            f"{format_triton_float(out.result.potential_potable_savings_pct if out.result else 0.0, 2)}"
        )
        lines.append(row)
        
    with open(file_path, 'w', encoding='latin1', errors='replace') as f:
        f.write("\n".join(lines) + "\n")
        
    return file_path

