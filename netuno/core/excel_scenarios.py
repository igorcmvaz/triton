import os
from netuno.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
import itertools
import io
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional, Union
import numpy as np
import pandas as pd

from netuno.core.parser import load_precipitation, parse_float, parse_int
from netuno.core.fracao_atendivel import percentual_para_fracao, aviso_percentual_pequeno
from netuno.core.simulation import run_single_simulation, run_sweep_simulation, SingleTankSimulationResult, SweepSimulationResult
from netuno.core.scenarios import ScenarioItem, ScenarioOutput, MultiScenarioMatrixResult

def generate_sample_scenario_excel(output_path: str = "cenarios_modelo_netuno.xlsx") -> str:
    """
    Generates a sample Excel file (.xlsx) with pre-populated scenario parameters.
    User can open this template, edit values, and re-upload to Netuno.
    """
    sample_data = [
        {
            "Cenario": "Residência Florianópolis 3 hab",
            "Chuva_Arquivo": "precFpolis_2002_2011.csv",
            "Area_m2": 100,
            "Moradores": 3,
            "Demanda_L_hab_dia": 100,
            "Substituicao_Percentual": 40,
            "Descarte_mm": 1.0,
            "Coef_Escoamento": 0.9,
            "Modo_Reservatorio": "Varredura",
            "Reservatorio_Inferior_L": 10000,
            "Passo_Varredura_L": 250,
            "Reservatorio_Superior_L": 500,
            "Limiar_Recalque_L": 375
        },
        {
            "Cenario": "Residência Santos 4 hab",
            "Chuva_Arquivo": "precSantos_1994_2003.csv",
            "Area_m2": 150,
            "Moradores": 4,
            "Demanda_L_hab_dia": 120,
            "Substituicao_Percentual": 50,
            "Descarte_mm": 1.0,
            "Coef_Escoamento": 0.9,
            "Modo_Reservatorio": "Varredura",
            "Reservatorio_Inferior_L": 10000,
            "Passo_Varredura_L": 250,
            "Reservatorio_Superior_L": 500,
            "Limiar_Recalque_L": 375
        },
        {
            "Cenario": "Escola Santana do Ipanema",
            "Chuva_Arquivo": "precSantanaDoIpanema_2002_2011.csv",
            "Area_m2": 300,
            "Moradores": 10,
            "Demanda_L_hab_dia": 50,
            "Substituicao_Percentual": 30,
            "Descarte_mm": 2.0,
            "Coef_Escoamento": COEFICIENTE_DE_ESCOAMENTO_PADRAO,
            "Modo_Reservatorio": "Fixo",
            "Reservatorio_Inferior_L": 5000,
            "Passo_Varredura_L": 0,
            "Reservatorio_Superior_L": 0,
            "Limiar_Recalque_L": 0
        }
    ]
    df = pd.DataFrame(sample_data)
    df.to_excel(output_path, index=False, engine='openpyxl')
    return output_path


def parse_excel_scenarios(file_input: Union[str, bytes, io.BytesIO]) -> List[Dict[str, Any]]:
    """
    Parses an Excel (.xlsx/.xls) or CSV file containing explicit scenario rows.
    """
    if isinstance(file_input, bytes):
        file_input = io.BytesIO(file_input)
        
    try:
        df = pd.read_excel(file_input, engine='openpyxl')
    except Exception:
        if isinstance(file_input, io.BytesIO):
            file_input.seek(0)
        df = pd.read_csv(file_input, sep=None, engine='python')
        
    scenarios = []
    
    # Normalize column names (strip, lowercase)
    cols_map = {col: str(col).strip().lower() for col in df.columns}
    
    for idx, row in df.iterrows():
        # Alias helper
        def get_val(aliases: List[str], default: Any) -> Any:
            for alias in aliases:
                for orig_col, norm_col in cols_map.items():
                    if alias in norm_col:
                        val = row[orig_col]
                        if pd.notna(val):
                            return val
            return default
            
        c_name = get_val(["cenario", "nome", "scenario", "name"], f"Cenario_{idx+1}")
        c_file = get_val(["chuva", "arquivo", "precip", "file", "cidade"], "precFpolis_2002_2011.csv")
        area = parse_float(get_val(["area"], 100.0), 100.0)
        residents = parse_int(get_val(["moradores", "habitants", "residents"], 3), 3)
        demand_capita = parse_float(get_val(["demanda", "demand"], 100.0), 100.0)
        
        # A coluna é sempre percentual, de 0 a 100: 40 é 40%, e 0,4 é 0,4%.
        share_val = parse_float(get_val(["substituicao", "share", "percentual"], 40.0), 40.0)
        share = percentual_para_fracao(f"Substituição da linha {idx + 2}", share_val)
        aviso = aviso_percentual_pequeno(share_val)
            
        discard = parse_float(get_val(["descarte", "discard"], 1.0), 1.0)
        runoff = parse_float(get_val(["coef", "runoff", "escoamento"], COEFICIENTE_DE_ESCOAMENTO_PADRAO), COEFICIENTE_DE_ESCOAMENTO_PADRAO)
        
        mode_str = str(get_val(["modo", "mode"], "varredura")).lower()
        is_sweep = "varredura" in mode_str or "sweep" in mode_str or "range" in mode_str
        
        tank_lower = parse_float(get_val(["inferior", "lower", "reservatorio"], 10000.0 if is_sweep else 2000.0))
        tank_step = parse_float(get_val(["passo", "step"], 250.0), 250.0)
        
        tank_upper = parse_float(get_val(["superior", "upper"], 0.0), 0.0)
        limiar = parse_float(get_val(["limiar", "recalque", "threshold"], 0.0), 0.0)
        
        scenarios.append({
            "scenario_name": str(c_name),
            "precip_file": str(c_file),
            "area": area,
            "residents": residents,
            "demand_per_capita": demand_capita,
            "rainwater_share": share,
            "discard": discard,
            "runoff_coeff": runoff,
            "is_sweep": is_sweep,
            "lower_tank_vol": tank_lower,
            "lower_tank_step": tank_step,
            "upper_tank_vol": tank_upper,
            "pumping_threshold": limiar,
            "avisos": [f"{c_name}: {aviso}"] if aviso else [],
        })
        
    return scenarios


def generate_factorial_grid(
    precip_files: List[Tuple[str, str]], # (label, file_path)
    areas: List[float],
    residents_list: List[int],
    demands_per_capita: List[float],
    rainwater_shares: List[float],
    lower_tanks: List[float],
    upper_tank_vol: float = 0.0,
    pumping_threshold: float = 0.0,
    discard_mm: float = 1.0,
    runoff_coeff: float = COEFICIENTE_DE_ESCOAMENTO_PADRAO,
    is_sweep: bool = True,
    sweep_step: float = 250.0
) -> List[Dict[str, Any]]:
    """
    Generates full Cartesian Factorial combinations (X * Y * Z ...) of scenario parameters.
    """
    factorial_scenarios = []
    combo_idx = 0
    
    for (c_label, c_file), area, res, d_cap, r_share in itertools.product(
        precip_files, areas, residents_list, demands_per_capita, rainwater_shares
    ):
        combo_idx += 1
        name = f"Fat_{combo_idx:03d}_{c_label}_A{int(area)}_R{res}"
        
        if is_sweep:
            max_tank = max(lower_tanks) if lower_tanks else 10000.0
            factorial_scenarios.append({
                "scenario_name": name,
                "city_label": c_label,
                "precip_file": c_file,
                "area": area,
                "residents": res,
                "demand_per_capita": d_cap,
                "rainwater_share": r_share,
                "discard": discard_mm,
                "runoff_coeff": runoff_coeff,
                "is_sweep": True,
                "lower_tank_vol": max_tank,
                "lower_tank_step": sweep_step,
                "upper_tank_vol": upper_tank_vol,
                "pumping_threshold": pumping_threshold
            })
        else:
            for t_vol in lower_tanks:
                sub_name = f"{name}_V{int(t_vol)}"
                factorial_scenarios.append({
                    "scenario_name": sub_name,
                    "city_label": c_label,
                    "precip_file": c_file,
                    "area": area,
                    "residents": res,
                    "demand_per_capita": d_cap,
                    "rainwater_share": r_share,
                    "discard": discard_mm,
                    "runoff_coeff": runoff_coeff,
                    "is_sweep": False,
                    "lower_tank_vol": t_vol,
                    "lower_tank_step": 0.0,
                    "upper_tank_vol": upper_tank_vol,
                    "pumping_threshold": pumping_threshold
                })
                
    return factorial_scenarios


def run_parsed_scenarios(scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Executes simulations for a list of parsed scenario dicts.
    Returns list of result summary dicts suitable for tables/Excel export.
    """
    precip_cache: Dict[str, np.ndarray] = {}
    results = []
    
    for idx, sc in enumerate(scenarios):
        fpath = sc["precip_file"]
        if fpath not in precip_cache:
            try:
                precip_cache[fpath] = load_precipitation(fpath)
            except Exception:
                precip_cache[fpath] = load_precipitation("precFpolis_2002_2011.csv")
                
        prec = precip_cache[fpath]
        tot_demand = sc["demand_per_capita"] * sc["residents"]
        
        if sc.get("is_sweep", True):
            sw = run_sweep_simulation(
                precip_data=prec,
                lower_tank_max=sc["lower_tank_vol"],
                lower_tank_step=sc.get("lower_tank_step", 250.0),
                area=sc["area"],
                runoff_coeff=sc["runoff_coeff"],
                discard_mm=sc["discard"],
                total_demand_per_day=tot_demand,
                rainwater_share=sc["rainwater_share"],
                upper_tank_vol=sc["upper_tank_vol"],
                upper_tank_used=bool(sc["upper_tank_vol"] > 0),
                pumping_threshold=sc["pumping_threshold"]
            )
            
            # Find optimal volume metrics
            opt_v = sw.optimal_lower_tank_vol
            opt_pot = sw.optimal_potential_pct
            avg_pluv = 0.0
            avg_spill = 0.0
            if sw.results_by_volume:
                for r in sw.results_by_volume:
                    if r.lower_tank_vol == opt_v:
                        avg_pluv = r.avg_pluvial_consumed_l_day
                        avg_spill = r.avg_spilled_l_day
                        break
                if avg_pluv == 0.0:
                    avg_pluv = sw.results_by_volume[-1].avg_pluvial_consumed_l_day
                    avg_spill = sw.results_by_volume[-1].avg_spilled_l_day
                    
            results.append({
                "ID": f"SCEN_{idx+1:03d}",
                "Nome_Cenario": sc["scenario_name"],
                "Arquivo_Chuva": os.path.basename(sc["precip_file"]),
                "Area_m2": sc["area"],
                "Moradores": sc["residents"],
                "Demanda_L_hab_dia": sc["demand_per_capita"],
                "Demanda_Total_L_dia": tot_demand,
                "Substituicao_Pluvial_%": round(sc["rainwater_share"] * 100.0, 1),
                "Descarte_mm": sc["discard"],
                "Volume_Ideal_L": opt_v if opt_v is not None else "Indeterminado",
                "Economia_Potencial_%": round(opt_pot, 2) if opt_pot else 0.0,
                "Consumo_Pluvial_L_dia": round(avg_pluv, 2),
                "Volume_Extravasado_L_dia": round(avg_spill, 2)
            })
        else:
            s_res = run_single_simulation(
                precip_data=prec,
                lower_tank_vol=sc["lower_tank_vol"],
                area=sc["area"],
                runoff_coeff=sc["runoff_coeff"],
                discard_mm=sc["discard"],
                total_demand_per_day=tot_demand,
                rainwater_share=sc["rainwater_share"],
                upper_tank_vol=sc["upper_tank_vol"],
                upper_tank_used=bool(sc["upper_tank_vol"] > 0),
                pumping_threshold=sc["pumping_threshold"]
            )
            results.append({
                "ID": f"SCEN_{idx+1:03d}",
                "Nome_Cenario": sc["scenario_name"],
                "Arquivo_Chuva": os.path.basename(sc["precip_file"]),
                "Area_m2": sc["area"],
                "Moradores": sc["residents"],
                "Demanda_L_hab_dia": sc["demand_per_capita"],
                "Demanda_Total_L_dia": tot_demand,
                "Substituicao_Pluvial_%": round(sc["rainwater_share"] * 100.0, 1),
                "Descarte_mm": sc["discard"],
                "Volume_Reservatorio_L": sc["lower_tank_vol"],
                "Economia_Potencial_%": round(s_res.potential_potable_savings_pct, 2),
                "Consumo_Pluvial_L_dia": round(s_res.avg_pluvial_consumed_l_day, 2),
                "Volume_Extravasado_L_dia": round(s_res.avg_spilled_l_day, 2)
            })
            
    return results


def export_scenarios_to_excel_bytes(results: List[Dict[str, Any]]) -> bytes:
    """
    Exports scenario results into formatted Excel (.xlsx) file bytes.
    """
    df = pd.DataFrame(results)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Resultados_Cenarios", index=False)
    return output.getvalue()
