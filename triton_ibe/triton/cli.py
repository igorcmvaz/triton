"""CLI reproduzível do Triton.

Aceita projetos CSV legados e projetos estruturados ``.triton``/JSON.  O
formato ``.triton`` é autocontido quando incorpora a série de chuva e também
guarda premissas ambientais e pesos TOPSIS usados pela linha de comando.
"""

from triton.core.taxas import anual_pct_para_mensal_pct
from triton.core.fracao_atendivel import conciliar_fracoes, percentual_para_fracao
from triton.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO, LAMINA_DE_DESCARTE_PADRAO_MM
import argparse
import copy
import csv
import glob
import json
import os
import shutil
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np

# No terminal, acentos em UTF-8. No executável de janela não há console (sys.stdout é None),
# e a interface importa este módulo (Modulação Probabilística): reconfigurar ali derrubava
# o programa ao abrir.
if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from triton.cli_textos import t as _t
from triton.core.edition import (
    configuracao_da_edicao, serie_de_exemplo_da_edicao, usa_dados_do_brasil, valor_de_partida_da_edicao,
)
from triton.core.economic import (
    calculate_effective_tariff,
    run_economic_analysis,
    run_robust_economic_analysis,
)
from triton.core.taxas import mensal_pct_para_anual_fracao
from triton.core.cost_estimates import (
    annualize_operational_costs,
    estimate_annual_chlorination_cost,
    estimate_preliminary_capex, precos_de_catalogo,
)
from triton.core.etap_integration import (
    capex_incremental_da_etap,
    opex_anual_incremental_da_etap,
)
from triton.core.chlorination import DOSE_PADRAO_MG_POR_LITRO, FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO, PUREZA_PADRAO
from triton.core.environmental import (
    EnvironmentalConfig, MATERIAL_PRESETS, PipeInput, PumpInput, calculate_lca,
    grid_factor_default,
)
from triton.core.pump_energy import compute_annual_pump_energy, consumo_especifico_padrao_kwh_por_m3
from triton.core.parser import (
    regra_operacional_efetiva,
    TritonConfig, export_triton_json, load_triton_project, load_precipitation, parse_netuno_csv,
)
from triton.core.simulation import SingleTankSimulationResult, run_single_simulation, run_sweep_simulation
from triton.core.topsis import PESOS_PADRAO, TopsisCandidate, calculate_topsis_scores, payback_do_criterio
from triton.core.mcdm_methods import AMOSTRAS_SMAA_PADRAO, run_smaa_vikor

ANALYSES = ("technical", "economic", "environmental", "topsis", "all")
FORMATS = ("text", "json", "csv", "html", "xlsx")
RAIN_RASTER_SUFFIXES = {".csv", ".txt", ".dat"}
CONFIG_OVERRIDES = {
    "area", "runoff_coeff", "discard", "discard_mode", "discard_days_interval", "start_date",
    "demand_value", "residents_count", "rainwater_share", "upper_tank_vol", "upper_tank_used",
    "pumping_threshold", "lower_tank_mode", "lower_tank_fixed", "lower_tank_max", "lower_tank_step",
    "delta_ideal", "phi_operation_rule", "analysis_period_years", "tma", "inflation", "sewage_rate", "sewage_mode",
    "water_tax_fixed", "water_tax_var", "tariff_escalation", "water_tariff_escalation",
    "sewage_tariff_escalation", "elec_tariff_escalation", "elec_tariff", "elec_tax_fixed",
    "elec_tax_var", "cost_lower_tank", "cost_upper_tank", "cost_labor", "cost_piping",
    "cost_accessories", "pump_count", "pump_power_kw", "pump_flow_rate", "pump_efficiency",
    "pump_startup_time_h", "pump_unit_cost", "pump_manometric_head_m", "pump_motor_efficiency",
    "lower_tank_material", "upper_tank_material", "supply_arrangement",
    "water_quality_target_class", "water_quality_disinfection", "water_quality_polishing",
    "etap_enabled", "precos_de_catalogo", "chlorine_treatment_enabled", "chlorine_dose_mg_l",
    "chlorine_product_purity", "sewage_volume_factor",
    "chlorine_cost_per_kg", "chlorine_co2_kg_per_kg", "iptu_green_enabled", "iptu_annual_value",
    "iptu_discount_pct", "tariff_flag", "building_template_id", "irrigation_liters_per_day",
    "irrigation_rain_threshold_mm", "irrigation_potable_backup", "potable_indoor_share",
    "non_potable_indoor_share", "num_economias",
}


def _json_default(value: Any) -> Any:
    """Converte escalares NumPy produzidos pelo motor para JSON nativo."""
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Tipo não serializável: {type(value).__name__}")


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=_json_default)


def _number_or_text(value: str) -> Any:
    low = value.strip().lower()
    if low in {"true", "yes", "sim"}:
        return True
    if low in {"false", "no", "não", "nao"}:
        return False
    try:
        number = float(value.replace(",", "."))
        return int(number) if number.is_integer() else number
    except ValueError:
        return value


def _parse_weights(raw: str) -> Tuple[float, float, float]:
    try:
        values = tuple(float(value.strip()) for value in raw.split(","))
        if len(values) == 3 and all(value >= 0 for value in values) and sum(values) > 0:
            return values
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("Use três pesos não negativos separados por vírgula; a soma deve ser positiva.")


def _positive_int(raw: str) -> int:
    try:
        value = int(raw)
        if value > 0:
            return value
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("Informe um inteiro positivo.")


def _apply_overrides(cfg: TritonConfig, raw_overrides: Iterable[str]) -> None:
    for item in raw_overrides or []:
        if "=" not in item:
            raise ValueError(f"Sobrescrita inválida: '{item}'. Use --set chave=valor.")
        key, value = (part.strip() for part in item.split("=", 1))
        if key not in CONFIG_OVERRIDES:
            available = ", ".join(sorted(CONFIG_OVERRIDES))
            raise ValueError(f"Campo '{key}' não pode ser sobrescrito. Campos aceitos: {available}")
        if key == "phi_operation_rule":
            # "triton" (ou vazio) volta à regra do Triton; um número em [0, 1] escolhe a família de Fewkes.
            if value.lower() in ("", "triton", "none", "nenhum"):
                cfg.phi_operation_rule = None
                continue
            try:
                phi = float(value.replace(",", "."))
            except ValueError:
                raise ValueError("phi_operation_rule aceita 'triton' ou um número entre 0 e 1.") from None
            if not 0.0 <= phi <= 1.0:
                raise ValueError("phi_operation_rule fora de [0, 1]: use 0 (YAS estrita), 1 (YBS) ou 'triton'.")
            cfg.phi_operation_rule = phi
            continue
        setattr(cfg, key, _number_or_text(value))


def _as_float(value: Any, default: float) -> float:
    try:
        return float(str(value).replace(".", "").replace(",", ".")) if "," in str(value) else float(value)
    except (TypeError, ValueError):
        return default


def _analysis_from_ui_state(ui_state: Dict[str, Any]) -> Dict[str, Any]:
    """Converte o estado salvo pela GUI em premissas explícitas para a CLI.

    Projetos antigos guardam a ACV e os pesos em ``ui_state``. Esta adaptação
    conserva a paridade sem obrigar o usuário a recriar o arquivo .triton.
    """
    ui_state = ui_state or {}
    output: Dict[str, Any] = {}
    topsis = ui_state.get("topsis", {})
    if topsis:
        output["topsis_weights"] = [
            _as_float(topsis.get("technical_weight"), 33.3),
            _as_float(topsis.get("economic_weight"), 33.3),
            _as_float(topsis.get("environmental_weight"), 33.4),
        ]
    env = ui_state.get("environmental", {})
    if not env:
        return output
    text, combos, checks = env.get("text", {}), env.get("combos", {}), env.get("checks", {})
    material_keys = list(MATERIAL_PRESETS)
    def material(combo_name: str, default: str) -> str:
        index = combos.get(combo_name)
        return material_keys[index] if isinstance(index, int) and 0 <= index < len(material_keys) else default
    def value(name: str, default: float) -> float:
        return _as_float(text.get(name), default)
    # A tubulação não sai do estado da tela: ele só guarda as quatro bitolas
    # antigas (50, 75, 100 e 150 mm) e perdia as demais. A ACV lê os
    # comprimentos do próprio projeto, como a aba ambiental da interface.
    legacy_treatment_factor = value("txt_treatment_co2", 0.0)
    chlorine_dose = value("txt_chlorine_dose", DOSE_PADRAO_MG_POR_LITRO)
    # Estados de interface anteriores guardavam apenas kg CO2e/m³. Ao ler
    # esses projetos, convertemos o fator para manter a emissão equivalente.
    if "txt_chlorine_co2" in text:
        chlorine_factor = value("txt_chlorine_co2", FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO)
    elif legacy_treatment_factor > 0 and chlorine_dose > 0:
        chlorine_factor = legacy_treatment_factor / (chlorine_dose / 1000.0)
    else:
        chlorine_factor = FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    from triton.core.environmental import valor_personalizado_ou_none
    baixo, alto = material("combo_lower_mat", "PEAD"), material("combo_upper_mat", "PEAD")
    output["environmental"] = {
        "lower_material_key": baixo,
        "upper_material_key": alto,
        "custom_lower_density_kg_m3": valor_personalizado_ou_none(
            baixo, value("txt_lower_density", 0.0) or None, "material_density_kg_per_m3_tank"),
        "custom_lower_co2_per_kg": valor_personalizado_ou_none(
            baixo, value("txt_lower_co2_kg", 0.0) or None, "co2_factor_kg_per_kg"),
        "custom_upper_density_kg_m3": valor_personalizado_ou_none(
            alto, value("txt_upper_density", 0.0) or None, "material_density_kg_per_m3_tank"),
        "custom_upper_co2_per_kg": valor_personalizado_ou_none(
            alto, value("txt_upper_co2_kg", 0.0) or None, "co2_factor_kg_per_kg"),
        "grid_co2_factor_kg_kwh": value("txt_grid_co2", _fator_de_rede_de_partida()),
        "potable_water_co2_kg_m3": value("txt_potable_co2", _emissao_da_agua_de_partida()),
        "chlorine_dose_mg_l": chlorine_dose,
        "chlorine_co2_kg_per_kg": chlorine_factor,
        "system_lifespan_years": value("txt_lifespan", 20.0),
        "pump": {"power_cv": value("txt_pump_cv", 0.5),
                 "specific_kwh_per_m3": value("txt_pump_kwh", consumo_especifico_padrao_kwh_por_m3()),
                 "custom_embodied_co2": value("txt_pump_co2", 0.0) or None},
        "upper_tank_used": bool(checks.get("chk_upper_used", True)),
    }
    return output


def _prefill_preliminary_capex(cfg: TritonConfig) -> None:
    """Preenche estimativas preliminares de CAPEX/OPEX quando zeradas no projeto.

    A interface gráfica preenche estes valores automaticamente (`tab_economic_integrated.py`).
    Sem esta paridade, projetos .triton recém-criados ou com custos zerados rodavam sem mão de
    obra, tubulação ou acessórios na linha de comando.
    """
    vol_used = float(cfg.lower_tank_fixed if cfg.lower_tank_mode == 0 else (getattr(cfg, "econ_lower_tank_vol", 0.0) or 2000.0))
    upper_used = bool(cfg.upper_tank_used)
    estimates = estimate_preliminary_capex(
        vol_used, getattr(cfg, "upper_tank_vol", 500.0), upper_used,
        cfg.pump_power_kw, cfg.pump_count,
        lower_material=getattr(cfg, "lower_tank_material", "PEAD"),
        upper_material=getattr(cfg, "upper_tank_material", "PEAD"),
            catalogo=precos_de_catalogo(cfg)
        )
    if cfg.cost_lower_tank <= 0 and cfg.lower_tank_mode == 0:
        cfg.cost_lower_tank = estimates["lower"]
    if cfg.cost_upper_tank <= 0:
        cfg.cost_upper_tank = estimates["upper"]
    if cfg.cost_piping <= 0:
        cfg.cost_piping = estimates["piping"]
    if cfg.cost_accessories <= 0:
        cfg.cost_accessories = estimates["accessories"]
    if cfg.cost_labor <= 0:
        cfg.cost_labor = estimates["labor"]
    if cfg.pump_unit_cost <= 0:
        cfg.pump_unit_cost = estimates["pump_unit"]
    if not cfg.op_costs:
        from triton.core.cost_estimates import default_maintenance_items
        cfg.op_costs = default_maintenance_items(upper_used)
        # Os custos de referência são em reais: fora do catálogo ficam as rotinas, a custo
        # zero, como a interface faz (paridade interface × CLI).
        if not precos_de_catalogo(cfg):
            cfg.op_costs = [(nome, meses, 0.0, 0.0) for nome, meses, *_ in cfg.op_costs]


def _load_bundle(project_file: str) -> Dict[str, Any]:
    """Carrega CSV legado ou projeto estruturado sem perder a chuva incorporada."""
    path = Path(project_file).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    if path.suffix.lower() in {".triton", ".json"}:
        with path.open("r", encoding="utf-8") as stream:
            raw = json.load(stream)
        if not isinstance(raw, dict) or raw.get("schema", {}).get("name") != "triton-project":
            raise ValueError("JSON inválido: esperado schema.name = 'triton-project'. Use `triton.cli init` para criar um modelo.")
        bundle = load_triton_project(str(path))
        if bundle.get("aviso_fracoes"):
            print(f"Aviso: {bundle['aviso_fracoes']}", file=sys.stderr)
        explicit_analysis = bundle.get("analysis", {}) or {}
        legacy_analysis = _analysis_from_ui_state(bundle.get("ui_state", {}))
        # Campos explícitos do schema mais novo sempre vencem o estado legado.
        if not explicit_analysis:
            bundle["analysis"] = legacy_analysis
        else:
            bundle["analysis"] = {**legacy_analysis, **explicit_analysis}
            if legacy_analysis.get("environmental") and explicit_analysis.get("environmental"):
                bundle["analysis"]["environmental"] = {
                    **legacy_analysis["environmental"], **explicit_analysis["environmental"],
                }
        bundle["raw"] = raw
        bundle["source_path"] = str(path)
        # Permite arquivo de chuva relativo ao .triton quando ele não incorporou a série.
        cfg = bundle["config"]
        _prefill_preliminary_capex(cfg)
        if bundle.get("precip_data") is None and cfg.precip_file:
            relative_rainfall = path.parent / cfg.precip_file
            if relative_rainfall.is_file():
                cfg.precip_file = str(relative_rainfall)
        return bundle

    cfg = parse_netuno_csv(str(path))
    _prefill_preliminary_capex(cfg)
    return {
        "config": cfg, "precip_data": None, "analysis": {}, "raw": {},
        "source_path": str(path), "is_json": False,
    }


def _validate_config(cfg: TritonConfig, precip: Optional[Any] = None) -> List[str]:
    errors: List[str] = []
    if cfg.area <= 0:
        errors.append("area deve ser maior que zero")
    if not 0 <= cfg.runoff_coeff <= 1:
        errors.append("runoff_coeff deve estar entre 0 e 1")
    if not 0 <= cfg.rainwater_share <= 1:
        errors.append("rainwater_share deve estar entre 0 e 1 (por exemplo, 0.40)")
    if cfg.demand_value < 0 or cfg.residents_count < 0:
        errors.append("demanda e moradores não podem ser negativos")
    if cfg.lower_tank_mode == 1 and (cfg.lower_tank_max <= 0 or cfg.lower_tank_step <= 0):
        errors.append("no modo de varredura, lower_tank_max e lower_tank_step devem ser maiores que zero")
    if cfg.lower_tank_mode != 1 and cfg.lower_tank_fixed < 0:
        errors.append("lower_tank_fixed não pode ser negativo")
    if bool(cfg.upper_tank_used) and cfg.upper_tank_vol < 0:
        errors.append("upper_tank_vol não pode ser negativo")
    if cfg.analysis_period_years <= 0:
        errors.append("analysis_period_years deve ser maior que zero")
    for label, values in (("demand_monthly", cfg.demand_monthly), ("residents_monthly", cfg.residents_monthly)):
        if values and len(values) != 12:
            errors.append(f"{label} deve conter exatamente 12 valores")
    if bool(cfg.demand_monthly) != bool(cfg.residents_monthly):
        errors.append("demand_monthly e residents_monthly devem ser informados juntos")
    if precip is not None and len(precip) == 0:
        errors.append("a série de precipitação está vazia")
    return errors


def _validate_analysis_config(raw: Optional[Dict[str, Any]]) -> List[str]:
    raw = raw or {}
    errors: List[str] = []
    weights = raw.get("topsis_weights")
    if weights is not None:
        if not isinstance(weights, list) or len(weights) != 3:
            errors.append("analysis.topsis_weights deve ser uma lista com três valores")
        else:
            try:
                if any(float(value) < 0 for value in weights) or sum(float(value) for value in weights) <= 0:
                    errors.append("analysis.topsis_weights deve conter valores não negativos com soma positiva")
            except (TypeError, ValueError):
                errors.append("analysis.topsis_weights deve conter números")
    environmental = raw.get("environmental", {})
    if environmental and not isinstance(environmental, dict):
        errors.append("analysis.environmental deve ser um objeto JSON")
    elif environmental:
        for key in ("lower_material_key", "upper_material_key"):
            material = environmental.get(key)
            if material is not None and material not in MATERIAL_PRESETS:
                errors.append(f"analysis.environmental.{key} deve ser um dos materiais: {', '.join(MATERIAL_PRESETS)}")
        for pipe in environmental.get("pipes", []):
            try:
                valid_pipe = isinstance(pipe, dict) and float(pipe.get("length_m", 0)) >= 0
            except (TypeError, ValueError):
                valid_pipe = False
            if not valid_pipe:
                errors.append("cada analysis.environmental.pipes deve conter length_m numérico e não negativo")
    return errors


def _get_precipitation(bundle: Dict[str, Any]) -> Any:
    precipitation = bundle.get("precip_data")
    if precipitation is not None and len(precipitation):
        return precipitation
    cfg = bundle["config"]
    if not cfg.precip_file:
        raise ValueError("O projeto não possui série de precipitação incorporada nem arquivo de chuva configurado.")
    return load_precipitation(cfg.precip_file)


def _total_demand(cfg: TritonConfig) -> float:
    return cfg.demand_value * (cfg.residents_count if cfg.residents_count > 0 else 1)


def _run_technical(cfg: TritonConfig, precip: Any, volume: Optional[float] = None) -> Tuple[List[SingleTankSimulationResult], Dict[str, Any]]:
    # Uma alteração da fração total (--share, --set, cenários) recalcula a
    # interna, e vice-versa; ver triton/core/fracao_atendivel.py.
    aviso = conciliar_fracoes(cfg)
    if aviso:
        print(f"Aviso: {aviso}", file=sys.stderr)
    b_cfg = {
        "area": cfg.area,
        "runoff": cfg.runoff_coeff,
        "runoff_coeff": cfg.runoff_coeff,
        "residents": cfg.residents_count,
        "demand": cfg.demand_value,
        "share": cfg.rainwater_share,
        "potable_indoor_share": cfg.potable_indoor_share,
        "non_potable_indoor_share": cfg.non_potable_indoor_share,
        "irrigation_liters_per_day": float(cfg.irrigation_liters_per_day or 0.0),
        "irrigation_rain_threshold_mm": getattr(cfg, "irrigation_rain_threshold_mm", 2.0),
        "irrigation_potable_backup": getattr(cfg, "irrigation_potable_backup", True),
        "num_economias": max(1, int(getattr(cfg, "num_economias", 1))),
        "demand_mode": getattr(cfg, "demand_mode", "constant") or "constant",
        "template_id": getattr(cfg, "building_template_id", "res_medio"),
        "monthly_demands": cfg.demand_monthly or None,
        "monthly_residents": cfg.residents_monthly or None,
        "monthly_shares": cfg.monthly_shares or None,
        "weekly_demands": cfg.weekly_demands or None,
        "weekly_residents": cfg.weekly_residents or None,
        "weekly_shares": cfg.weekly_shares or None,
        "daily_demands": cfg.daily_demands or None,
        "daily_residents": cfg.daily_residents or None,
        "daily_shares": cfg.daily_shares or None,
        "phi_operation_rule": regra_operacional_efetiva(cfg),
    }
    common = dict(
        precip_data=precip, area=cfg.area, runoff_coeff=cfg.runoff_coeff,
        discard_mm=cfg.discard, discard_mode=cfg.discard_mode,
        discard_days_interval=cfg.discard_days_interval, total_demand_per_day=_total_demand(cfg),
        rainwater_share=cfg.rainwater_share, upper_tank_vol=cfg.upper_tank_vol,
        upper_tank_used=bool(cfg.upper_tank_used), pumping_threshold=cfg.pumping_threshold,
        monthly_demands=cfg.demand_monthly or None, monthly_residents=cfg.residents_monthly or None,
        # O modo de demanda e as listas semanais e diarias nao eram repassados:
        # a simulacao caia em "constant" e a modulacao do projeto era ignorada,
        # inclusive as listas mensais, que chegavam aqui e nao eram usadas.
        demand_mode=getattr(cfg, "demand_mode", "constant") or "constant",
        monthly_shares=cfg.monthly_shares or None,
        weekly_demands=cfg.weekly_demands or None,
        weekly_residents=cfg.weekly_residents or None,
        weekly_shares=cfg.weekly_shares or None,
        daily_demands=cfg.daily_demands or None,
        daily_residents=cfg.daily_residents or None,
        daily_shares=cfg.daily_shares or None,
        start_date_str=cfg.start_date,
        building_config=b_cfg,
    )
    if volume is not None:
        if volume < 0:
            raise ValueError("--volume não pode ser negativo")
        result = run_single_simulation(lower_tank_vol=volume, **common)
        return [result], {"mode": "fixed", "selected_volume_l": volume}
    if cfg.lower_tank_mode == 1:
        sweep = run_sweep_simulation(
            lower_tank_max=cfg.lower_tank_max, lower_tank_step=cfg.lower_tank_step,
            delta_ideal_threshold=cfg.delta_ideal, **common,
        )
        return list(sweep.results_by_volume), {
            "mode": "sweep", "optimal_volume_l": sweep.optimal_lower_tank_vol,
            "optimal_potential_pct": sweep.optimal_potential_pct,
            "sweep_grid": {
                "requested_step_l": sweep.requested_step_l,
                "effective_step_l": sweep.effective_step_l,
                "step_adjusted": sweep.step_adjusted,
                "positive_volume_count": max(0, len(sweep.results_by_volume) - 1),
                "zero_l_reference_included": True,
                "maximum_volume_l": sweep.results_by_volume[-1].lower_tank_vol if sweep.results_by_volume else cfg.lower_tank_max,
            },
        }
    result = run_single_simulation(lower_tank_vol=cfg.lower_tank_fixed, **common)
    return [result], {"mode": "fixed", "selected_volume_l": cfg.lower_tank_fixed}


def _technical_row(result: SingleTankSimulationResult) -> Dict[str, float]:
    return {
        "lower_tank_volume_l": result.lower_tank_vol,
        "potable_savings_pct": result.potential_potable_savings_pct,
        "annual_rainwater_m3": result.annual_pluvial_consumed_m3,
        "annual_potable_consumed_m3": result.annual_potable_consumed_m3,
        "annual_overflow_m3": result.annual_spill_m3,
        "full_supply_days_pct": result.pct_days_full_satisfaction,
        "partial_supply_days_pct": result.pct_days_partial_satisfaction,
        "no_supply_days_pct": result.pct_days_null_satisfaction,
        "marginal_gain_pct_per_m3": result.delta_potential_per_m3,
    }


def _environmental_config(cfg: TritonConfig, result: SingleTankSimulationResult, annual_pump_kwh: float,
                          raw: Optional[Dict[str, Any]]) -> EnvironmentalConfig:
    raw = raw or {}
    # O arranjo 3D define a tubulação e acrescenta conexões, peças e cabos.
    from triton.core.quantitativo_do_arranjo import itens_de_acv_do_projeto
    itens_do_arranjo = itens_de_acv_do_projeto(cfg)
    if "pipes" in raw and isinstance(raw["pipes"], list):
        pipes = [PipeInput(
            diameter_mm=int(item.get("diameter_mm", 100)), length_m=float(item.get("length_m", 0)),
            custom_co2_per_m=item.get("custom_co2_per_m"),
        ) for item in raw["pipes"] if isinstance(item, dict)]
    elif hasattr(cfg, "get_pipe_lengths_dict") and cfg.get_pipe_lengths_dict():
        pipes = [PipeInput(diameter_mm=int(d), length_m=float(l))
                 for d, l in sorted(cfg.get_pipe_lengths_dict().items()) if float(l) > 0]
    elif hasattr(cfg, "pipes_list") and cfg.pipes_list:
        pipes = [PipeInput(diameter_mm=int(d), length_m=float(l)) for d, l in cfg.pipes_list if float(l) > 0]
    else:
        pipes = None

    pump_raw = raw.get("pump", {}) if isinstance(raw.get("pump", {}), dict) else {}
    # Potência e consumo específico saem da mesma função que a aba ambiental da
    # interface usa (compute_annual_pump_energy); a conversão direta de
    # pump_power_kw dava 0,5 cv onde a interface via 0,25 cv, e o carbono
    # incorporado da motobomba divergia entre as duas para o mesmo projeto.
    energia = compute_annual_pump_energy(cfg, result, upper_tank_used=bool(cfg.upper_tank_used))
    cv_padrao = energia.pump_power_cv if energia.pump_power_cv > 0 else max(0.25, round(cfg.pump_power_kw / 0.7355, 2))
    power_cv = float(pump_raw.get("power_cv", cv_padrao))
    pump = PumpInput(
        power_cv=power_cv, custom_embodied_co2=pump_raw.get("custom_embodied_co2"),
        # 0,40 kWh/m3 era o valor anterior a correcao da hidraulica, que dividia
        # pelo rendimento duas vezes e implicava 67 m de altura manometrica. O
        # padrao do programa passou a sair de rho.g.H/eta com altura de casa, e a
        # linha de comando ficou com o numero antigo: 3,7 vezes maior, de modo que
        # a mesma configuracao dava emissao diferente na tela e no terminal.
        specific_kwh_per_m3=float(
            pump_raw.get("specific_kwh_per_m3",
                         energia.specific_kwh_per_m3 if energia.specific_kwh_per_m3 > 0
                         else consumo_especifico_padrao_kwh_por_m3())
        ),
        material=str(pump_raw.get("material", "Ferro Fundido, Cobre & Alumínio")),
    )
    has_explicit_chlorine = "chlorine_dose_mg_l" in raw or "chlorine_co2_kg_per_kg" in raw
    if "chlorine_dose_mg_l" in raw:
        chlorine_dose = float(raw["chlorine_dose_mg_l"])
    elif not getattr(cfg, "chlorine_treatment_enabled", True):
        chlorine_dose = 0.0
    else:
        chlorine_dose = float(getattr(cfg, "chlorine_dose_mg_l", DOSE_PADRAO_MG_POR_LITRO))

    # A sobreposicao legada de intensidade de tratamento vale SO quando o projeto
    # a declara. Antes desta revisao ela era aplicada sempre que o projeto nao trazia
    # parametros de cloro - a maioria - e, com a linha de tratamento ligada, isso
    # passou a ter efeito novo: o campo legado tem precedencia sobre a ETAP e a
    # DESLIGAVA. Escolher ozonio cobrava o ozonizador no fluxo de caixa e nao
    # emitia por ele. Projetos que a declaram continuam reproduzindo o resultado
    # historico; os demais passam a usar a cadeia atual, como a interface ja faz.
    legacy_treatment = (
        float(raw["chemical_treatment_co2_m3"])
        if (not has_explicit_chlorine and "chemical_treatment_co2_m3" in raw)
        else None
    )
    if has_explicit_chlorine:
        chlorine_factor = float(raw.get("chlorine_co2_kg_per_kg", FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO))
    elif legacy_treatment is not None and chlorine_dose > 0:
        # Projeto legado: reconstroi o fator que reproduz a intensidade declarada.
        chlorine_factor = legacy_treatment / (chlorine_dose / 1000.0)
    else:
        chlorine_factor = float(getattr(cfg, "chlorine_co2_kg_per_kg", FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO))

    lower_mat = raw.get("lower_material_key", getattr(cfg, "lower_tank_material", "PEAD"))
    upper_mat = raw.get("upper_material_key", getattr(cfg, "upper_tank_material", "PEAD"))

    values = {
        "lower_material_key": lower_mat,
        "custom_lower_density_kg_m3": raw.get("custom_lower_density_kg_m3"),
        "custom_lower_co2_per_kg": raw.get("custom_lower_co2_per_kg"),
        "upper_material_key": upper_mat,
        "custom_upper_density_kg_m3": raw.get("custom_upper_density_kg_m3"),
        "custom_upper_co2_per_kg": raw.get("custom_upper_co2_per_kg"),
        "pipes": pipes,
        "pump": pump,
        "pump_count": int(raw.get("pump_count", cfg.pump_count)),
        "pump_material": str(raw.get("pump_material", pump.material)),
        **fatores_de_emissao(raw),
        "chlorine_dose_mg_l": chlorine_dose,
        "chlorine_co2_kg_per_kg": chlorine_factor,
        "chemical_treatment_co2_m3": legacy_treatment,
        "system_lifespan_years": float(raw.get("system_lifespan_years", cfg.analysis_period_years)),
    }
    if values["pipes"] is None:
        values.pop("pipes")
    return EnvironmentalConfig(
        lower_tank_vol=result.lower_tank_vol, annual_water_saved_m3=result.annual_pluvial_consumed_m3,
        annual_pump_kwh=annual_pump_kwh, upper_tank_used=bool(cfg.upper_tank_used),
        supply_arrangement=str(getattr(cfg, "supply_arrangement", "") or ""),
        upper_tank_vol_liters=cfg.upper_tank_vol,
        # A escolha da linha de tratamento tem de atravessar TAMBEM pela linha de
        # comando. `run_economic_analysis` recebe o TritonConfig inteiro e ja a
        # honrava; a ACV montava a propria configuracao sem estes campos e caia
        # nos padroes. A mesma rodada cobrava o ozonizador no fluxo de caixa e
        # emitia como se fosse so cloracao.
        water_quality_target_class=getattr(cfg, "water_quality_target_class", "classe_1"),
        water_quality_disinfection=getattr(cfg, "water_quality_disinfection", "cloro"),
        water_quality_polishing=bool(getattr(cfg, "water_quality_polishing", False)),
        etap_enabled=bool(getattr(cfg, "etap_enabled", True)),
        roof_area_m2=float(getattr(cfg, "area", 100.0) or 100.0),
        # O dispositivo de descarte declarado no projeto entra no carbono
        # incorporado, como na interface; a linha de comando o omitia.
        first_flush_system_enabled=bool(getattr(cfg, "first_flush_system_enabled", False)),
        discard=float(getattr(cfg, "discard", LAMINA_DE_DESCARTE_PADRAO_MM) or LAMINA_DE_DESCARTE_PADRAO_MM),
        chlorine_product_purity=float(getattr(cfg, "chlorine_product_purity", PUREZA_PADRAO) or PUREZA_PADRAO),
        itens_do_arranjo=itens_do_arranjo,
        **values,
    )


def _preco_da_cisterna(cfg: TritonConfig, volume_l: float) -> float:
    """Preço da cisterna inferior para um volume da varredura.

    É a mesma estimativa que a aba econômica da interface usa em cada linha da
    varredura (`tab_economic_integrated.py`): interpolação da tabela de preços
    pelo volume e pelo material. Sem ela, a linha de comando cobrava o mesmo
    preço de uma cisterna de 1.000 L e de uma de 20.000 L, o VPL só crescia com
    o volume, e as duas interfaces davam ótimos econômicos diferentes para o
    mesmo projeto.
    """
    from triton.core.cost_estimates import preco_da_cisterna_do_volume
    return preco_da_cisterna_do_volume(cfg, volume_l)


def _fator_sorteado(cfg: TritonConfig, atributo: str) -> float:
    """Fator que a modulação probabilística põe no projeto; 1 fora dela."""
    valor = getattr(cfg, atributo, 1.0)
    return 1.0 if valor is None else float(valor)


#: Emissão da água potável da rede quando a avaliação ambiental não a declara, kg CO₂e/m³ (o valor do Brasil).
EMISSAO_DA_AGUA_POTAVEL_BRASIL = 0.35


def _emissao_da_agua_de_partida() -> float:
    """Zero fora da Brasil: o usuário informa o fator da água da rede do seu local."""
    return valor_de_partida_da_edicao(EMISSAO_DA_AGUA_POTAVEL_BRASIL)


def _fator_de_rede_de_partida() -> float:
    """O fator da rede quando o projeto não o declara: o do Brasil na Brasil, zero nas outras edições.

    Nas outras edições o usuário informa o fator da rede do seu local; gravar 0,085 (o do
    sistema interligado brasileiro) num modelo de INT ou IBE seria dar-lhe um dado de outro país.
    """
    return valor_de_partida_da_edicao(grid_factor_default())


def fatores_de_emissao(raw: Optional[Dict[str, Any]]) -> Dict[str, float]:
    """Os fatores de emissão da avaliação ambiental: os declarados ou os padrões."""
    raw = raw or {}
    return {"grid_co2_factor_kg_kwh": float(raw.get("grid_co2_factor_kg_kwh", _fator_de_rede_de_partida())),
            "potable_water_co2_kg_m3": float(raw.get("potable_water_co2_kg_m3", _emissao_da_agua_de_partida()))}


def _economic_row(cfg: TritonConfig, result: SingleTankSimulationResult,
                  preco_por_volume: bool = False) -> Tuple[Dict[str, Any], Any]:
    v_vol = result.lower_tank_vol
    vol_m3_val = result.annual_pluvial_consumed_m3 if v_vol > 0 else 0.0
    sim_days = getattr(result, 'total_days', getattr(result, 'n_days_simulated', 365))
    upper_used = bool(getattr(cfg, 'upper_tank_used', 1))

    if preco_por_volume:
        c_low = _preco_da_cisterna(cfg, v_vol) if v_vol > 0 else 0.0
    else:
        c_low = float(cfg.cost_lower_tank) if v_vol > 0 else 0.0
    # Modulação probabilística: o fator sorteado do preço da cisterna (1 fora dela). Entra
    # antes da mão de obra, que, automática, acompanha o custo da cisterna.
    c_low *= _fator_sorteado(cfg, "fator_da_cisterna_estocastico")

    etap_c_inc = capex_incremental_da_etap(cfg, vol_m3_val) if getattr(cfg, 'etap_enabled', True) else 0.0
    # Arranjo e mão de obra de cada volume, pela mesma regra da interface.
    from triton.core.quantitativo_do_arranjo import capex_do_volume
    from triton.core.supply_arrangement import arranjo_de, usa_bomba
    tub_v, acc_v, mao_v = capex_do_volume(cfg, v_vol, c_low)
    capex_v = 0.0 if v_vol <= 0 else (
        c_low + float(cfg.cost_upper_tank) +
        (float(cfg.pump_unit_cost) * int(getattr(cfg, "pump_count", 1)) if usa_bomba(arranjo_de(cfg)) else 0.0) +
        tub_v + acc_v + mao_v +
        etap_c_inc
    )
    # Modulação probabilística: o fator sorteado do investimento (1 fora dela).
    capex_v *= _fator_sorteado(cfg, "fator_de_investimento_estocastico")

    annual_total_demand = (result.annual_pluvial_consumed_m3 + result.annual_potable_consumed_m3) if v_vol > 0 else 0.0
    tw_v, ts_v = calculate_effective_tariff(cfg, vol_m3_val, annual_total_demand_m3=annual_total_demand)

    tma_annual = mensal_pct_para_anual_fracao(cfg.tma)
    inf_annual = mensal_pct_para_anual_fracao(cfg.inflation)
    n_readj_per_year = 12.0 / max(1.0, float(cfg.tariff_escalation))
    w_esc_annual = (1.0 + float(getattr(cfg, 'water_tariff_escalation', 5.0)) / 100.0) ** n_readj_per_year - 1.0
    s_esc_annual = (1.0 + float(getattr(cfg, 'sewage_tariff_escalation', 5.0)) / 100.0) ** n_readj_per_year - 1.0
    e_esc_annual = (1.0 + float(getattr(cfg, 'elec_tariff_escalation', 5.0)) / 100.0) ** n_readj_per_year - 1.0

    flag_sel = getattr(cfg, "tariff_flag", "verde")
    flag_add = 0.0
    if flag_sel == "amarela":
        flag_add = 0.01885
    elif flag_sel == "vermelha_1":
        flag_add = 0.04463
    elif flag_sel == "vermelha_2":
        flag_add = 0.07877
    elif flag_sel == "branca":
        flag_add = -0.15 * float(cfg.elec_tariff)
    eff_elec_tariff = max(0.0, float(cfg.elec_tariff) + flag_add)

    p_hrs_v = 0.0
    if upper_used and float(cfg.pump_flow_rate) > 0 and v_vol > 0:
        if hasattr(result, 'total_pumped_liters') and result.total_pumped_liters > 0:
            t_rec_v = (result.total_pumped_liters / max(1.0, sim_days / 365.25)) / float(cfg.pump_flow_rate)
            ann_cyc_v = result.total_pump_cycles / max(1.0, sim_days / 365.25)
            t_part_v = ann_cyc_v * float(cfg.pump_startup_time_h)
            p_hrs_v = t_rec_v + t_part_v
        else:
            p_hrs_v = (vol_m3_val * 1000.0) / float(cfg.pump_flow_rate)

    cl2_enabled = getattr(cfg, "chlorine_treatment_enabled", True)
    cl2_dose = float(getattr(cfg, "chlorine_dose_mg_l", 2.0))
    cl2_cost_kg = float(getattr(cfg, "chlorine_cost_per_kg", 25.0))
    ann_cl_cost_v = 0.0
    if upper_used and v_vol > 0:
        _, ann_cl_cost_v = estimate_annual_chlorination_cost(
            vol_m3_val, cl2_dose if cl2_enabled else 0.0, cl2_cost_kg
        )

    annual_om_v = annualize_operational_costs(cfg.op_costs, vol_m3_val) if v_vol > 0 else 0.0
    if v_vol > 0 and getattr(cfg, 'etap_enabled', True):
        annual_om_v += opex_anual_incremental_da_etap(cfg, vol_m3_val)
    # Modulação probabilística: o fator sorteado do custeio anual (O&M declarado, custeio
    # da linha de tratamento e cloro). A energia do bombeamento tem variável própria.
    fator_om = _fator_sorteado(cfg, "fator_de_om_estocastico")
    annual_om_v *= fator_om
    ann_cl_cost_v *= fator_om

    iptu_enabled = getattr(cfg, "iptu_green_enabled", False)
    ann_iptu_savings = 0.0
    if iptu_enabled and v_vol > 0:
        ann_iptu_savings = float(getattr(cfg, "iptu_annual_value", 0.0)) * (float(getattr(cfg, "iptu_discount_pct", 0.0)) / 100.0)

    econ_res = run_robust_economic_analysis(
        initial_investment=capex_v,
        annual_water_saved_m3=vol_m3_val,
        water_tariff_per_m3=tw_v,
        sewage_tariff_per_m3=ts_v,
        sewage_mode=int(cfg.sewage_mode),
        water_tariff_escalation_rate=w_esc_annual,
        sewage_tariff_escalation_rate=s_esc_annual,
        elec_tariff_escalation_rate=e_esc_annual,
        inflation_rate=inf_annual,
        discount_rate=tma_annual,
        annual_om_cost_base=annual_om_v,
        pump_power_kw=float(cfg.pump_power_kw),
        pump_hours_year=p_hrs_v,
        elec_tariff_kwh=eff_elec_tariff,
        analysis_period_years=int(cfg.analysis_period_years),
        annual_chlorine_cost=ann_cl_cost_v,
        annual_iptu_savings=ann_iptu_savings,
    )

    if v_vol > 0 and len(econ_res.annual_cash_flows) > 1:
        cf1 = econ_res.annual_cash_flows[1]
        annual_opex_v = cf1.pump_energy_cost_brl + cf1.om_cost_brl + getattr(cf1, "chlorine_cost_brl", 0.0)
        annual_water_savings_brl = cf1.total_gross_savings_brl
    else:
        annual_opex_v = 0.0
        annual_water_savings_brl = 0.0

    pump_energy_res = compute_annual_pump_energy(cfg, result, upper_tank_used=upper_used)
    annual_pump_kwh = pump_energy_res.annual_kwh if v_vol > 0 else 0.0

    pb_m = (econ_res.payback_discounted_years * 12.0) if econ_res.payback_discounted_years is not None else None
    tir_m = anual_pct_para_mensal_pct(econ_res.tir_pct) if np.isfinite(econ_res.tir_pct) else 0.0

    econ_res.capex_total = capex_v
    econ_res.tir_annual_pct = econ_res.tir_pct
    econ_res.tir_monthly_pct = tir_m
    econ_res.payback_months = pb_m
    econ_res.annual_water_savings_brl = annual_water_savings_brl
    econ_res.annual_opex_brl = annual_opex_v
    econ_res.annual_pump_kwh = annual_pump_kwh

    row_dict = {
        "lower_tank_volume_l": v_vol,
        "capex_brl": capex_v,
        "npv_brl": econ_res.vpl,
        "irr_monthly_pct": tir_m,
        "irr_annual_pct": econ_res.tir_pct,
        "discounted_payback_months": pb_m,
        "annual_water_savings_brl": annual_water_savings_brl,
        "annual_opex_brl": annual_opex_v,
        "annual_pump_kwh": annual_pump_kwh,
    }
    return row_dict, econ_res


def _environmental_row(cfg: TritonConfig, result: SingleTankSimulationResult, annual_pump_kwh: float,
                       raw: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], Any]:
    lca = calculate_lca(result.lower_tank_vol, result.annual_pluvial_consumed_m3,
                        _environmental_config(cfg, result, annual_pump_kwh, raw))
    return {
        "lower_tank_volume_l": result.lower_tank_vol, "embodied_co2_kg": lca.total_embodied_co2_kg,
        "annual_avoided_co2_kg": lca.annual_avoided_co2_kg,
        "annual_operational_co2_kg": lca.annual_pumping_co2_kg + lca.annual_treatment_co2_kg,
        "annual_chlorine_kg": lca.annual_chlorine_kg,
        "chlorine_dose_mg_l": lca.chlorine_dose_mg_l,
        "treatment_co2_kg_per_m3": lca.treatment_co2_kg_per_m3,
        "annual_treatment_co2_kg": lca.annual_treatment_co2_kg,
        "lifetime_net_co2_saved_kg": lca.lifetime_net_co2_saved_kg,
        "environmental_payback_years": lca.environmental_payback_years,
        "environmentally_viable": lca.is_environmentally_viable,
    }, lca


def run_analysis(cfg: TritonConfig, precip: Any, analysis_type: str = "technical", volume: Optional[float] = None,
                 weights: Tuple[float, float, float] = PESOS_PADRAO,
                 environmental: Optional[Dict[str, Any]] = None, source: str = "",
                 weight_sensitivity: int = 0, seed: int = 42, smaa: bool = True) -> Dict[str, Any]:
    """Executa a cadeia técnica → econômica → ambiental → TOPSIS de forma rastreável.

    ``smaa=False`` dispensa a aceitabilidade SMAA-VIKOR (20.000 vetores de pesos), que
    responde por quase todo o tempo da cadeia; a modulação probabilística, que roda a cadeia
    centenas de vezes e só usa o vencedor do TOPSIS, a desliga.
    """
    technical_results, technical_summary = _run_technical(cfg, precip, volume)
    output: Dict[str, Any] = {
        "schema": {"name": "triton-analysis", "version": 2},
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "provenance": {"source_project": source, "rainfall_days": len(precip), "start_date": cfg.start_date},
        "technical": {"summary": technical_summary, "alternatives": [_technical_row(row) for row in technical_results]},
    }
    if analysis_type == "technical":
        return output
    economic_rows, economic_results = zip(*[
        _economic_row(cfg, result, preco_por_volume=(volume is None and cfg.lower_tank_mode == 1))
        for result in technical_results
    ])
    output["economic"] = {"alternatives": list(economic_rows)}
    if analysis_type == "economic":
        return output
    environmental_rows, environmental_results = zip(*[
        _environmental_row(cfg, result, econ.annual_pump_kwh, environmental)
        for result, econ in zip(technical_results, economic_results)
    ])
    output["environmental"] = {"alternatives": list(environmental_rows)}
    if analysis_type == "environmental":
        return output
    opt_tech_vol = technical_summary.get("optimal_volume_l")
    candidates = [TopsisCandidate(
        lower_tank_vol=result.lower_tank_vol, water_saved_m3_yr=result.annual_pluvial_consumed_m3,
        vpl_brl=econ.vpl, co2_saved_kg_lifetime=lca.lifetime_net_co2_saved_kg,
        capex_brl=econ.capex_total, upper_tank_vol=cfg.upper_tank_vol if cfg.upper_tank_used else 0.0,
        technical_threshold_met=(result.lower_tank_vol > 0 and result.delta_potential_per_m3 <= cfg.delta_ideal),
        is_technical_optimum=(opt_tech_vol is not None and abs(result.lower_tank_vol - opt_tech_vol) < 1.0),
        potential_savings_pct=result.potential_potable_savings_pct,
        overflow_m3_yr=result.annual_spill_m3,
        discounted_payback_years=payback_do_criterio(
            econ.payback_months / 12.0 if econ.payback_months is not None else None, econ.vpl),
        irr_pct=econ.tir_annual_pct,
        potable_consumed_m3_yr=result.annual_potable_consumed_m3,
    ) for result, econ, lca in zip(technical_results, economic_results, environmental_results)]
    topsis = calculate_topsis_scores(candidates, weights=weights)
    output["topsis"] = {
        "weights": dict(zip(("technical", "economic", "environmental"), weights)),
        "criteria": [{
            "key": key, "label": label, "weight": float(weight),
            "direction": "maximize" if benefit else "minimize",
        } for key, label, weight, benefit in zip(
            topsis.criterion_keys, topsis.criterion_labels, topsis.criterion_weights,
            (True, False, True, False, True, False, False),
        )] if topsis else [],
        "best_volume_l": topsis.best_candidate.lower_tank_vol if topsis else None,
        "best_score": float(topsis.scores[topsis.best_index]) if topsis else None,
        "technical_best_volume_l": topsis.candidates[topsis.technical_best_index].lower_tank_vol if topsis else None,
        "economic_best_volume_l": topsis.candidates[topsis.financial_best_index].lower_tank_vol if topsis else None,
        "environmental_best_volume_l": topsis.candidates[topsis.environmental_best_index].lower_tank_vol if topsis else None,
        "ranking": [{
            "lower_tank_volume_l": candidate.lower_tank_vol,
            "score": float(topsis.scores[index]),
            "rank": int(topsis.rankings[index]),
            "distance_to_ideal": float(topsis.dist_best[index]),
            "distance_from_anti_ideal": float(topsis.dist_worst[index]),
            "criterion_values": {
                key: float(topsis.decision_matrix[index, col])
                for col, key in enumerate(topsis.criterion_keys)
            },
            "criterion_gap_pct": {
                key: float(topsis.criterion_gap_to_best[index, col] * 100.0)
                for col, key in enumerate(topsis.criterion_keys)
            },
            "technical_gap_pct": float((1.0 - topsis.group_proximity_to_best[index, 0]) * 100.0),
            "economic_gap_pct": float((1.0 - topsis.group_proximity_to_best[index, 1]) * 100.0),
            "environmental_gap_pct": float((1.0 - topsis.group_proximity_to_best[index, 2]) * 100.0),
        } for index, candidate in enumerate(topsis.candidates)] if topsis else [],
    }
    smaa = (run_smaa_vikor(candidates, v_param=0.5, num_samples=AMOSTRAS_SMAA_PADRAO, random_seed=seed)
            if candidates and smaa else None)
    if smaa:
        output["smaa_vikor"] = {
            "samples": AMOSTRAS_SMAA_PADRAO,
            "seed": seed,
            "best_volume_l": smaa.best_candidate.lower_tank_vol,
            "best_acceptability_pct": float(smaa.first_rank_probs[smaa.best_index]),
            "acceptabilities": [
                {
                    "lower_tank_volume_l": cand.lower_tank_vol,
                    "first_rank_pct": float(smaa.first_rank_probs[idx]),
                }
                for idx, cand in enumerate(candidates)
            ],
        }
    if weight_sensitivity:
        rng = np.random.default_rng(seed)
        winners: Dict[str, int] = {}
        for sampled_weights in rng.dirichlet((1.0, 1.0, 1.0), size=weight_sensitivity):
            sampled = calculate_topsis_scores(candidates, weights=tuple(sampled_weights))
            winner = f"{sampled.best_candidate.lower_tank_vol:.0f}"
            winners[winner] = winners.get(winner, 0) + 1
        output["topsis"]["weight_sensitivity"] = {
            "samples": weight_sensitivity, "seed": seed,
            "winner_frequency_pct": {volume: count * 100.0 / weight_sensitivity for volume, count in winners.items()},
        }
    return output


def _moeda_do_bundle(bundle: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """A moeda que o projeto grava (Etapa 3); ``None`` quando o arquivo não a declara."""
    from triton.core.dados_do_relatorio import moeda_do_projeto
    return moeda_do_projeto((bundle or {}).get("ui_state"))


def _simbolo(report: Dict[str, Any]) -> str:
    """O símbolo da moeda do relatório, ou «(moeda do projeto)» quando não declarada."""
    moeda = (report.get("provenance") or {}).get("currency") or {}
    return moeda.get("symbol") or "(moeda do projeto)"


def _flat_rows(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = {row["lower_tank_volume_l"]: dict(row) for row in report["technical"]["alternatives"]}
    for section in ("economic", "environmental"):
        for row in report.get(section, {}).get("alternatives", []):
            rows.setdefault(row["lower_tank_volume_l"], {}).update(row)
    ranks = {row["lower_tank_volume_l"]: row for row in report.get("topsis", {}).get("ranking", [])}
    moeda = (report.get("provenance") or {}).get("currency") or {}
    for volume, row in rows.items():
        row.update({f"topsis_{key}": value for key, value in ranks.get(volume, {}).items() if key != "lower_tank_volume_l"})
        if "economic" in report:
            # Os valores «_brl» são na moeda do projeto, não necessariamente o real.
            row["currency"] = moeda.get("code") or "não declarada"
    return list(rows.values())


def _render_html(report: Dict[str, Any]) -> str:
    rows = _flat_rows(report)
    columns = sorted({key for row in rows for key in row})
    header = "".join(f"<th>{column}</th>" for column in columns)
    body = "".join("<tr>" + "".join(f"<td>{row.get(column, '')}</td>" for column in columns) + "</tr>" for row in rows)
    return ("<!doctype html><meta charset='utf-8'><title>Triton analysis</title><style>"
            "body{font:14px Segoe UI,Arial;margin:32px;color:#172033}table{border-collapse:collapse;width:100%}"
            "th{background:#0284c7;color:white}td,th{padding:8px;border:1px solid #cbd5e1;text-align:right}th:first-child,td:first-child{text-align:left}</style>"
            f"<h1>Triton — relatório de análise</h1><p>Gerado: {report['generated_at_utc']}</p>"
            + (f"<p>Valores monetários em: {_simbolo(report)}</p>" if "economic" in report else "")
            + f"<table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>")


def _write_report(report: Dict[str, Any], output_format: str, output_file: Optional[str]) -> None:
    if output_format == "text":
        technical = report["technical"]
        summary = technical["summary"]
        print(f"=== Triton | {summary['mode']} | {len(technical['alternatives'])} {_t('alternativa(s)')} ===")
        if summary.get("optimal_volume_l") is not None:
            print(f"{_t('Volume técnico indicado:')} {summary['optimal_volume_l']:.0f} L ({summary['optimal_potential_pct']:.2f}% {_t('de economia')})")
        if "economic" in report:
            econ_alts = [row for row in report["economic"]["alternatives"] if row["lower_tank_volume_l"] > 0]
            if econ_alts:
                viable_pb = [row for row in econ_alts if row.get("discounted_payback_months") is not None and row["discounted_payback_months"] > 0 and row.get("npv_brl", 0) > 0]
                if viable_pb:
                    best_econ = min(viable_pb, key=lambda row: (row["discounted_payback_months"], -row["npv_brl"]))
                else:
                    best_econ = max(econ_alts, key=lambda row: row["npv_brl"])
                pb_yrs = best_econ.get("discounted_payback_months") / 12.0 if best_econ.get("discounted_payback_months") else None
                pb_txt = f" | Payback: {pb_yrs:.1f}a" if pb_yrs else ""
                print(f"{_t('Melhor alternativa econômica (Menor Payback):')} {best_econ['lower_tank_volume_l']:.0f} L | {_t('VPL')} {_simbolo(report)} {best_econ['npv_brl']:.2f}{pb_txt}")
        if "environmental" in report:
            env_alts = [row for row in report["environmental"]["alternatives"] if row["lower_tank_volume_l"] > 0]
            if env_alts:
                best_env = max(env_alts, key=lambda row: row["lifetime_net_co2_saved_kg"])
                print(f"{_t('Melhor alternativa ambiental:')} {best_env['lower_tank_volume_l']:.0f} L | {best_env['lifetime_net_co2_saved_kg']:.2f} kg CO2e")
        if "topsis" in report:
            print(f"TOPSIS: {report['topsis']['best_volume_l']:.0f} L | score {report['topsis']['best_score']:.3f}")
        if "smaa_vikor" in report:
            sv = report["smaa_vikor"]
            print(f"SMAA-VIKOR: {sv['best_volume_l']:.0f} L | {sv['best_acceptability_pct']:.1f}% {_t('em')} {sv['samples']} {_t('simulações')}")
        return
    if not output_file:
        raise ValueError(f"--output é obrigatório quando --format {output_format} é usado")
    target = Path(output_file)
    target.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "json":
        target.write_text(_json_dump(report), encoding="utf-8")
    elif output_format == "html":
        target.write_text(_render_html(report), encoding="utf-8")
    elif output_format == "csv":
        rows = _flat_rows(report)
        with target.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=sorted({key for row in rows for key in row}), delimiter=";")
            writer.writeheader(); writer.writerows(rows)
    elif output_format == "xlsx":
        try:
            import pandas as pd
            with pd.ExcelWriter(target, engine="openpyxl") as writer:
                pd.DataFrame(_flat_rows(report)).to_excel(writer, sheet_name="alternatives", index=False)
                for name in ("technical", "economic", "environmental", "topsis"):
                    if name in report:
                        pd.DataFrame([report[name].get("summary", report[name])]).to_excel(writer, sheet_name=name[:31], index=False)
                prov = dict(report.get("provenance") or {})
                moeda = prov.pop("currency", None) or {}
                prov["currency"] = moeda.get("code") or "não declarada"
                pd.DataFrame([prov]).to_excel(writer, sheet_name="provenance", index=False)
        except ImportError as exc:
            raise RuntimeError("A exportação XLSX requer pandas e openpyxl instalados.") from exc
    print(f"Resultado salvo em: {target.resolve()}")


def _template_analysis() -> Dict[str, Any]:
    return {
        "topsis_weights": list(PESOS_PADRAO),
        "environmental": {
            "lower_material_key": "PEAD", "upper_material_key": "PEAD",
            "grid_co2_factor_kg_kwh": _fator_de_rede_de_partida(),
            "potable_water_co2_kg_m3": _emissao_da_agua_de_partida(),
            "chlorine_dose_mg_l": DOSE_PADRAO_MG_POR_LITRO,
            "chlorine_co2_kg_per_kg": FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
            "system_lifespan_years": 20,
            "pipes": [{"diameter_mm": 100, "length_m": 20}, {"diameter_mm": 32, "length_m": 20}, {"diameter_mm": 40, "length_m": 5}],
            "pump": {"power_cv": 0.5, "specific_kwh_per_m3": consumo_especifico_padrao_kwh_por_m3()},
        },
    }


def _create_template(path: str, rainfall_file: str, embed_rainfall: bool) -> Path:
    # Os padrões da edição: na Brasil, os históricos; nas outras, sem tarifa, preço nem localidade do Brasil.
    cfg = configuracao_da_edicao()
    for campo, valor in dict(precip_file=rainfall_file, area=100.0, demand_value=120.0, residents_count=4,
                             rainwater_share=0.40, runoff_coeff=COEFICIENTE_DE_ESCOAMENTO_PADRAO, lower_tank_max=10000.0,
                             lower_tank_step=500.0, upper_tank_vol=500.0, upper_tank_used=1).items():
        setattr(cfg, campo, valor)
    if not usa_dados_do_brasil():
        # o IPTU Verde é incentivo municipal do Brasil: o valor venal e o desconto de partida não vão no modelo
        cfg.iptu_annual_value = 0.0
        cfg.iptu_discount_pct = 0.0
    precipitation = load_precipitation(rainfall_file) if embed_rainfall else None
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    export_triton_json(cfg, str(target), precip_data=precipitation, analysis=_template_analysis())
    # Bloco opcional e inerte até receber valores.  Ele documenta a forma
    # reproduzível de declarar uma matriz diretamente no projeto.
    content = json.loads(target.read_text(encoding="utf-8"))
    content["cli_factorial"] = {"factors": {}, "rainfall_files": []}
    target.write_text(_json_dump(content), encoding="utf-8")
    return target


def _clima_de_exemplo() -> Dict[str, Any]:
    """A série de chuva de exemplo da edição: a de Florianópolis na Brasil, a que a edição distribui nas outras."""
    from triton.core.edition import cidade_de_exemplo_da_edicao
    serie = serie_de_exemplo_da_edicao()
    if usa_dados_do_brasil():
        return {"id": "florianopolis-1", "name": "Florianópolis — série 1",
                "rainfall_file": serie, "start_date": "01/01/2002"}
    local = cidade_de_exemplo_da_edicao().split(",")[0]
    return {"id": local.lower().replace(" ", "-") + "-1", "name": f"{local} — 1",
            "rainfall_file": serie, "start_date": "01/01/1991"}


def _create_catalog(kind: str, path: str) -> Path:
    if kind == "premises":
        content = {
            "schema": {"name": "triton-premises-catalog", "version": 1},
            "premises": [{
                "id": "residencia-base", "name": _t("Residência base"),
                "config": {"area": 100.0, "demand_value": 120.0, "residents_count": 4,
                           "rainwater_share": 0.40, "runoff_coeff": COEFICIENTE_DE_ESCOAMENTO_PADRAO, "discard": 1.0,
                           "lower_tank_mode": 1, "lower_tank_max": 10000.0, "lower_tank_step": 500.0,
                           "upper_tank_used": 1, "upper_tank_vol": 500.0, "pumping_threshold": 250.0,
                           "analysis_period_years": 20},
                "analysis": _template_analysis(),
            }],
        }
    else:
        content = {
            "schema": {"name": "triton-climate-catalog", "version": 1},
            "climates": [_clima_de_exemplo()],
        }
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_json_dump(content), encoding="utf-8")
    return target


def _run_project(args: argparse.Namespace) -> None:
    bundle = _load_bundle(args.file)
    cfg = bundle["config"]
    _apply_overrides(cfg, args.set_values)
    if args.rainfall:
        cfg.precip_file = args.rainfall
        bundle["precip_data"] = None
    if args.start_date:
        cfg.start_date = args.start_date
    precipitation = _get_precipitation(bundle)
    errors = _validate_config(cfg, precipitation)
    errors.extend(_validate_analysis_config(bundle.get("analysis")))
    if errors:
        raise ValueError("Projeto inválido:\n- " + "\n- ".join(errors))
    analysis_config = bundle.get("analysis", {}) or {}
    weights = args.weights or tuple(analysis_config.get("topsis_weights", PESOS_PADRAO))
    report = run_analysis(cfg, precipitation, args.analysis, args.volume, weights,
                          analysis_config.get("environmental", {}), bundle.get("source_path", args.file),
                          args.weight_sensitivity, args.seed)
    report["provenance"]["currency"] = _moeda_do_bundle(bundle)
    _write_report(report, args.format, args.output)


def _run_batch(args: argparse.Namespace) -> None:
    from triton.core.excel_scenarios import parse_excel_scenarios
    scenarios = parse_excel_scenarios(args.file)
    if not scenarios:
        raise ValueError("Nenhum cenário válido foi encontrado no arquivo.")
    for scenario in scenarios:
        for aviso in scenario.get("avisos", []):
            print(f"aviso: {aviso}", file=sys.stderr)
    base_bundle = _load_bundle(args.base) if args.base else {"config": configuracao_da_edicao(), "analysis": {}}
    base_cfg = base_bundle["config"]
    base_analysis = base_bundle.get("analysis", {}) or {}
    reports = []
    for scenario in scenarios:
        cfg = copy.deepcopy(base_cfg)
        cfg.precip_file = scenario["precip_file"]
        cfg.area, cfg.residents_count = scenario["area"], scenario["residents"]
        cfg.demand_value, cfg.rainwater_share = scenario["demand_per_capita"], scenario["rainwater_share"]
        cfg.discard, cfg.runoff_coeff = scenario["discard"], scenario["runoff_coeff"]
        cfg.lower_tank_mode = 1 if scenario.get("is_sweep", True) else 0
        cfg.lower_tank_max = scenario["lower_tank_vol"]; cfg.lower_tank_fixed = scenario["lower_tank_vol"]
        cfg.lower_tank_step = scenario.get("lower_tank_step", 250.0)
        cfg.upper_tank_vol = scenario["upper_tank_vol"]; cfg.upper_tank_used = int(cfg.upper_tank_vol > 0)
        cfg.pumping_threshold = scenario["pumping_threshold"]
        precipitation = load_precipitation(cfg.precip_file)
        errors = _validate_config(cfg, precipitation) + _validate_analysis_config(base_analysis)
        if errors:
            raise ValueError(f"Cenário '{scenario['scenario_name']}' inválido: {'; '.join(errors)}")
        report = run_analysis(
            cfg, precipitation, args.analysis,
            weights=args.weights or tuple(base_analysis.get("topsis_weights", PESOS_PADRAO)),
            environmental=base_analysis.get("environmental", {}), source=args.file,
            weight_sensitivity=args.weight_sensitivity, seed=args.seed,
        )
        report["scenario_name"] = scenario["scenario_name"]
        report["provenance"]["currency"] = _moeda_do_bundle(base_bundle)
        reports.append(report)
    combined = {"schema": {"name": "triton-batch-analysis", "version": 1}, "reports": reports}
    if args.format == "text":
        for report in reports:
            print(f"\n[{report['scenario_name']}]")
            _write_report(report, "text", None)
    elif args.format == "json":
        if not args.output:
            raise ValueError("--output é obrigatório para exportar o lote")
        Path(args.output).write_text(_json_dump(combined), encoding="utf-8")
        print(f"Resultado salvo em: {Path(args.output).resolve()}")
    else:
        flat = []
        for report in reports:
            flat.extend([{"scenario_name": report["scenario_name"], **row} for row in _flat_rows(report)])
        compact = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "technical": {"alternatives": flat}}
        _write_report(compact, args.format, args.output)


class _Progress:
    """Progresso determinístico com média móvel simples e estimativa de término."""
    def __init__(self, total: int, quiet: bool = False) -> None:
        import time
        self.total, self.quiet, self.started = max(1, total), quiet, time.perf_counter()
        self.last_print = -1

    @staticmethod
    def _duration(seconds: float) -> str:
        seconds = max(0, int(round(seconds)))
        return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"

    def update(self, completed: int, label: str = "") -> None:
        if self.quiet:
            return
        import time
        elapsed = time.perf_counter() - self.started
        average = elapsed / max(1, completed)
        eta = average * (self.total - completed)
        ratio = completed / self.total
        filled = int(28 * ratio)
        message = (f"[{('=' * filled).ljust(28, '·')}] {completed}/{self.total} "
                   f"{ratio:6.1%} | decorrido {self._duration(elapsed)} | ETA {self._duration(eta)} | {label}")
        if sys.stderr is not None and sys.stderr.isatty():
            print("\r" + message[:180], end="", file=sys.stderr, flush=True)
            if completed == self.total:
                print(file=sys.stderr)
        elif completed == self.total or completed - self.last_print >= max(1, self.total // 20):
            print(message, file=sys.stderr)
            self.last_print = completed


def _load_catalog(file_path: str, expected_schema: str) -> Dict[str, Any]:
    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Catálogo não encontrado: {path}")
    with path.open(encoding="utf-8") as stream:
        catalog = json.load(stream)
    if not isinstance(catalog, dict) or catalog.get("schema", {}).get("name") != expected_schema:
        raise ValueError(f"Catálogo inválido em {path.name}: esperado schema.name = '{expected_schema}'.")
    catalog["_path"] = path
    return catalog


def _config_from_premise(raw: Dict[str, Any]) -> Tuple[TritonConfig, Dict[str, Any]]:
    if not isinstance(raw, dict):
        raise ValueError("Cada premissa deve ser um objeto JSON.")
    data = raw.get("config", {})
    if not isinstance(data, dict):
        raise ValueError(f"Premissa '{raw.get('id', '?')}' deve conter um objeto config.")
    cfg = configuracao_da_edicao()
    invalid = set(data) - set(TritonConfig.__dataclass_fields__)
    if invalid:
        raise ValueError(f"Premissa '{raw.get('id', '?')}' contém campos inválidos: {', '.join(sorted(invalid))}")
    for key, value in data.items():
        setattr(cfg, key, value)
    analysis = raw.get("analysis", {}) or {}
    errors = _validate_config(cfg) + _validate_analysis_config(analysis)
    if errors:
        raise ValueError(f"Premissa '{raw.get('id', '?')}' inválida: {'; '.join(errors)}")
    return cfg, analysis


def _climate_data(raw: Dict[str, Any], catalog_dir: Path) -> Tuple[Any, str, str]:
    if not isinstance(raw, dict):
        raise ValueError("Cada clima deve ser um objeto JSON.")
    identifier = str(raw.get("id", "clima-sem-id"))
    start_date = str(raw.get("start_date", "01/01/2002"))
    embedded = raw.get("precipitation_mm")
    if embedded:
        values = np.asarray(embedded, dtype=float)
    else:
        file_name = raw.get("rainfall_file")
        if not file_name:
            raise ValueError(f"Clima '{identifier}' precisa de rainfall_file ou precipitation_mm.")
        local_file = catalog_dir / str(file_name)
        values = load_precipitation(str(local_file) if local_file.is_file() else str(file_name))
    if not len(values):
        raise ValueError(f"Clima '{identifier}' possui uma série de chuva vazia.")
    return values, identifier, start_date


def _matrix_best_row(report: Dict[str, Any]) -> Dict[str, Any]:
    rows = _flat_rows(report)
    if not rows:
        return {}
    selected = report.get("topsis", {}).get("best_volume_l")
    if selected is None:
        selected = report["technical"]["summary"].get("optimal_volume_l")
    if selected is None:
        selected = max(rows, key=lambda row: row.get("potable_savings_pct", 0)).get("lower_tank_volume_l")
    return next((row for row in rows if row.get("lower_tank_volume_l") == selected), rows[0])


def _write_matrix_outputs(output_dir: str, summaries: List[Dict[str, Any]], alternatives: List[Dict[str, Any]],
                          detailed: List[Dict[str, Any]]) -> None:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
        fields = sorted({key for row in rows for key in row})
        with path.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, delimiter=";")
            writer.writeheader(); writer.writerows(rows)
    write_csv(target / "triton-matriz-resumo.csv", summaries)
    write_csv(target / "triton-matriz-alternativas.csv", alternatives)
    (target / "triton-matriz-detalhado.json").write_text(_json_dump({
        "schema": {"name": "triton-matrix-analysis", "version": 1},
        "generated_at_utc": datetime.now(timezone.utc).isoformat(), "reports": detailed,
    }), encoding="utf-8")
    columns = ["premise_id", "premise_name", "climate_id", "climate_name", "selected_volume_l",
               "potable_savings_pct", "annual_rainwater_m3", "npv_brl", "lifetime_net_co2_saved_kg", "topsis_score"]
    columns = [column for column in columns if any(column in row for row in summaries)]
    head = "".join(f"<th>{column}</th>" for column in columns)
    body = "".join("<tr>" + "".join(f"<td>{row.get(column, '')}</td>" for column in columns) + "</tr>" for row in summaries)
    (target / "triton-matriz-painel.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>Triton | matriz consolidada</title><style>"
        "body{font:14px Segoe UI,Arial;background:#f8fafc;color:#172033;margin:32px}.hero{background:#0f3b5b;color:#fff;padding:24px;border-radius:12px}"
        ".cards{display:flex;gap:12px;margin:18px 0}.card{background:#fff;padding:14px 20px;border-radius:10px;border:1px solid #cbd5e1}table{border-collapse:collapse;width:100%;background:#fff}th{background:#0284c7;color:#fff}td,th{padding:9px;border:1px solid #cbd5e1;text-align:right}td:nth-child(-n+4),th:nth-child(-n+4){text-align:left}</style>"
        f"<div class='hero'><h1>Triton — matriz consolidada</h1><p>{len(summaries)} combinações de premissas e climas</p></div>"
        f"<div class='cards'><div class='card'><b>Combinações</b><br>{len(summaries)}</div><div class='card'><b>Alternativas avaliadas</b><br>{len(alternatives)}</div></div>"
        f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>", encoding="utf-8")
    print("Saídas consolidadas:", target.resolve())
    print("- triton-matriz-resumo.csv (uma decisão por combinação)")
    print("- triton-matriz-alternativas.csv (todos os volumes)")
    print("- triton-matriz-detalhado.json (resultados auditáveis completos)")
    print("- triton-matriz-painel.html (visualização consolidada)")


def _run_matrix(args: argparse.Namespace) -> None:
    premises = _load_catalog(args.premises, "triton-premises-catalog")
    climates = _load_catalog(args.climates, "triton-climate-catalog")
    premise_rows = premises.get("premises", [])
    climate_rows = climates.get("climates", [])
    if not premise_rows or not climate_rows:
        raise ValueError("Os dois catálogos precisam conter ao menos um item.")
    progress = _Progress(len(premise_rows) * len(climate_rows), args.quiet)
    summaries, alternatives, detailed = [], [], []
    completed = 0
    for premise in premise_rows:
        cfg_base, analysis = _config_from_premise(premise)
        for climate in climate_rows:
            cfg = copy.deepcopy(cfg_base)
            precipitation, climate_id, start_date = _climate_data(climate, climates["_path"].parent)
            cfg.start_date = start_date
            report = run_analysis(
                cfg, precipitation, args.analysis,
                weights=args.weights or tuple(analysis.get("topsis_weights", PESOS_PADRAO)),
                environmental=analysis.get("environmental", {}),
                source=f"{premises['_path'].name} × {climates['_path'].name}",
                weight_sensitivity=args.weight_sensitivity, seed=args.seed,
            )
            premise_id, climate_name = str(premise.get("id", "premissa")), str(climate.get("name", climate_id))
            context = {"premise_id": premise_id, "premise_name": str(premise.get("name", premise_id)),
                       "climate_id": climate_id, "climate_name": climate_name, "rainfall_days": len(precipitation)}
            best = _matrix_best_row(report)
            summaries.append({**context, "selected_volume_l": best.get("lower_tank_volume_l"), **best})
            alternatives.extend([{**context, **row} for row in _flat_rows(report)])
            detailed.append({**context, "report": report})
            completed += 1
            progress.update(completed, f"{premise_id} × {climate_id}")
    _write_matrix_outputs(args.output_dir, summaries, alternatives, detailed)


def _discover_project_files(entries: Iterable[str], recursive: bool) -> List[Path]:
    """Resolve arquivos .triton individuais e diretórios de projetos."""
    files: List[Path] = []
    for entry in entries:
        path = Path(entry).expanduser().resolve()
        if path.is_file():
            if path.suffix.lower() not in {".triton", ".json"}:
                raise ValueError(f"Projeto '{path.name}' deve ter extensão .triton ou .json.")
            files.append(path)
        elif path.is_dir():
            pattern = "**/*.triton" if recursive else "*.triton"
            files.extend(sorted(item for item in path.glob(pattern) if item.is_file()))
        else:
            raise FileNotFoundError(f"Projeto ou pasta não encontrado: {path}")
    unique = list(dict.fromkeys(files))
    if not unique:
        raise ValueError("Nenhum arquivo .triton foi encontrado nos caminhos informados.")
    return unique


def _discover_rainfall_files(folder: str, recursive: bool) -> List[Path]:
    """Lista séries diárias de chuva em uma pasta, em ordem determinística."""
    path = Path(folder).expanduser().resolve()
    if not path.is_dir():
        raise NotADirectoryError(f"Pasta de precipitações não encontrada: {path}")
    candidates = path.rglob("*") if recursive else path.glob("*")
    files = sorted(item for item in candidates if item.is_file() and item.suffix.lower() in RAIN_RASTER_SUFFIXES)
    if not files:
        accepted = ", ".join(sorted(RAIN_RASTER_SUFFIXES))
        raise ValueError(f"Nenhuma série de chuva ({accepted}) foi encontrada em {path}.")
    return files


def _project_factorial_spec(bundle: Dict[str, Any]) -> Dict[str, Any]:
    raw = bundle.get("raw", {}) or {}
    spec = raw.get("cli_factorial", {}) or {}
    if not isinstance(spec, dict):
        raise ValueError("cli_factorial deve ser um objeto JSON.")
    factors = spec.get("factors", {}) or {}
    if not isinstance(factors, dict):
        raise ValueError("cli_factorial.factors deve ser um objeto {campo: [valores]}.")
    invalid = set(factors) - CONFIG_OVERRIDES
    if invalid:
        raise ValueError("cli_factorial.factors contém campos não permitidos: " + ", ".join(sorted(invalid)))
    for field, values in factors.items():
        if not isinstance(values, list) or not values:
            raise ValueError(f"cli_factorial.factors.{field} deve ser uma lista não vazia.")
    rainfall_files = spec.get("rainfall_files", []) or []
    if not isinstance(rainfall_files, list) or any(not isinstance(value, str) or not value.strip() for value in rainfall_files):
        raise ValueError("cli_factorial.rainfall_files deve ser uma lista de caminhos de arquivos.")
    return {"factors": factors, "rainfall_files": rainfall_files}


def _factorial_overrides(factors: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """Expande {campo: [a, b]} em todas as combinações de configuração."""
    if not factors:
        return [{}]
    fields, values = list(factors), list(factors.values())
    return [dict(zip(fields, combination)) for combination in product(*values)]


def _project_rainfall_files(bundle: Dict[str, Any], spec: Dict[str, Any], args: argparse.Namespace) -> List[Optional[Path]]:
    """A pasta fornecida na CLI prevalece; sem ela, usa lista interna ou a chuva nativa."""
    if args.rainfall_dir:
        return _discover_rainfall_files(args.rainfall_dir, args.recursive)
    if spec["rainfall_files"]:
        project_dir = Path(bundle["source_path"]).parent
        files = []
        for value in spec["rainfall_files"]:
            candidate = Path(value)
            candidate = candidate if candidate.is_absolute() else project_dir / candidate
            candidate = candidate.resolve()
            if not candidate.is_file():
                raise FileNotFoundError(f"Série declarada em cli_factorial.rainfall_files não encontrada: {candidate}")
            files.append(candidate)
        return files
    return [None]


def _run_project_matrix(args: argparse.Namespace) -> None:
    """Executa projetos reais em lista ou em produto cartesiano com séries de chuva.

    - somente --projects: cada .triton roda com sua chuva própria, sem cruzamento;
    - --rainfall-dir: cada projeto é combinado com todas as séries da pasta;
    - cli_factorial no .triton expande os campos declarados em produto cartesiano.
    """
    project_files = _discover_project_files(args.projects, args.recursive)
    bundles = [_load_bundle(str(path)) for path in project_files]
    plans: List[Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]], List[Optional[Path]]]] = []
    total = 0
    for bundle in bundles:
        spec = _project_factorial_spec(bundle) if not args.ignore_project_factors else {"factors": {}, "rainfall_files": []}
        combinations = _factorial_overrides(spec["factors"])
        rainfalls = _project_rainfall_files(bundle, spec, args)
        plans.append((bundle, spec, combinations, rainfalls))
        total += len(combinations) * len(rainfalls)

    progress = _Progress(total, args.quiet)
    summaries: List[Dict[str, Any]] = []
    alternatives: List[Dict[str, Any]] = []
    detailed: List[Dict[str, Any]] = []
    completed = 0
    for bundle, _spec, combinations, rainfalls in plans:
        project_path = Path(bundle["source_path"])
        project_id = project_path.stem
        analysis_config = bundle.get("analysis", {}) or {}
        for factor_index, override in enumerate(combinations, start=1):
            for rainfall_path in rainfalls:
                cfg = copy.deepcopy(bundle["config"])
                for field, value in override.items():
                    setattr(cfg, field, value)
                if rainfall_path is None:
                    precipitation = _get_precipitation(bundle)
                    rainfall_name = "série incorporada" if bundle.get("precip_data") is not None else Path(cfg.precip_file).name
                    rainfall_source = str(cfg.precip_file or "embedded")
                else:
                    precipitation = load_precipitation(str(rainfall_path))
                    cfg.precip_file = str(rainfall_path)
                    rainfall_name, rainfall_source = rainfall_path.stem, str(rainfall_path)
                errors = _validate_config(cfg, precipitation) + _validate_analysis_config(analysis_config)
                if errors:
                    raise ValueError(f"Projeto '{project_path.name}' inválido: " + "; ".join(errors))
                weights = args.weights or tuple(analysis_config.get("topsis_weights", PESOS_PADRAO))
                report = run_analysis(
                    cfg, precipitation, args.analysis, weights=weights,
                    environmental=analysis_config.get("environmental", {}),
                    source=f"{project_path.name} × {rainfall_name} × f{factor_index:03d}",
                    weight_sensitivity=args.weight_sensitivity, seed=args.seed + completed,
                )
                context = {
                    "scenario_id": f"{project_id}--{rainfall_name}--f{factor_index:03d}",
                    "project_id": project_id, "project_file": str(project_path),
                    "project_name": str(getattr(cfg, "project_name", project_id) or project_id),
                    "rainfall_name": rainfall_name, "rainfall_file": rainfall_source,
                    "rainfall_days": len(precipitation), "factor_index": factor_index,
                    **{f"factor_{field}": value for field, value in override.items()},
                }
                best = _matrix_best_row(report)
                summaries.append({**context, "selected_volume_l": best.get("lower_tank_volume_l"), **best})
                alternatives.extend([{**context, **row} for row in _flat_rows(report)])
                detailed.append({**context, "report": report})
                completed += 1
                progress.update(completed, context["scenario_id"])
    _write_matrix_outputs(args.output_dir, summaries, alternatives, detailed)


def _emit(texto: str, destino: Optional[str]) -> None:
    """Imprime na tela, ou grava no arquivo pedido."""
    if not destino:
        print(texto)
        return
    alvo = Path(destino)
    alvo.write_text(texto + "\n", encoding="utf-8")
    print(f"Resultado salvo em: {alvo.resolve()}")


def _parametros_de_simulacao(cfg) -> Dict[str, Any]:
    """Os parâmetros hídricos do projeto, no formato que o motor pede."""
    return dict(
        area=float(cfg.area),
        runoff_coeff=float(cfg.runoff_coeff),
        discard_mm=float(getattr(cfg, "discard", 2.0)),
        discard_mode=int(getattr(cfg, "discard_mode", 1)),
        total_demand_per_day=float(cfg.demand_value) * float(getattr(cfg, "residents_count", 1) or 1),
        rainwater_share=float(cfg.rainwater_share),
        phi_rule=regra_operacional_efetiva(cfg),
    )


def _run_series_length(args: argparse.Namespace) -> None:
    """Responde de quantos anos de chuva este projeto precisa."""
    from triton.core.comprimento_de_serie import analisar

    bundle = _load_bundle(args.file)
    cfg = bundle["config"]
    _apply_overrides(cfg, args.set_values)
    precipitation = _get_precipitation(bundle)
    errors = _validate_config(cfg, precipitation)
    if errors:
        raise ValueError("Projeto inválido:\n- " + "\n- ".join(errors))

    resultado = analisar(
        precipitation, _parametros_de_simulacao(cfg),
        volume_maximo_l=args.max_volume, passo_l=args.step,
        limiar_ganho_pct_m3=args.threshold, tolerancia_pp=args.tolerance,
        tolerancia_passos=args.tolerance_steps, confianca_pct=args.confidence,
        amostra_por_comprimento=args.windows, semente=args.seed,
    )
    dados = {
        "anos_da_serie": resultado.anos_da_serie,
        "volume_ideal_l": resultado.volume_ideal_l,
        "potencial_no_ideal_pct": resultado.potencial_no_ideal_pct,
        "comprimento_representativo_anos": resultado.comprimento_representativo_anos,
        "serie_e_representativa": resultado.serie_e_representativa,
        "confianca_pct": resultado.confianca_pct,
        "tolerancia_pp": resultado.tolerancia_pp,
        "limiar_ganho_pct_m3": resultado.limiar_ganho_pct_m3,
        "amostra_por_comprimento": resultado.amostra_por_comprimento,
        "semente": resultado.semente,
        "frequencia_por_comprimento": resultado.frequencia_por_comprimento,
        "janelas_por_comprimento": resultado.janelas_por_comprimento,
        "resumo": resultado.resumo(),
    }
    if args.format == "json":
        texto = json.dumps(dados, ensure_ascii=False, indent=2)
    elif args.format == "csv":
        linhas = ["anos;frequencia_pct;janelas"]
        linhas += [f"{a};{f};{resultado.janelas_por_comprimento[a]}"
                   for a, f in sorted(resultado.frequencia_por_comprimento.items())]
        texto = "\n".join(linhas)
    else:
        linhas = [resultado.resumo(), "",
                  f"Volume ideal com a série inteira: {resultado.volume_ideal_l:,.0f} L".replace(",", "."),
                  f"Potencial nesse volume: {resultado.potencial_no_ideal_pct:.2f}%",
                  f"Critério: {resultado.confianca_pct:.0f}% das janelas com o mesmo volume ideal "
                  f"e potencial dentro de {resultado.tolerancia_pp:.1f} pontos", ""]
        linhas.append("anos  janelas  resultados semelhantes")
        for anos_, freq in sorted(resultado.frequencia_por_comprimento.items()):
            marca = " <-" if anos_ == resultado.comprimento_representativo_anos else ""
            linhas.append(f"{anos_:>4}  {resultado.janelas_por_comprimento[anos_]:>7}  {freq:>6.1f}%{marca}")
        texto = "\n".join(linhas)
    _emit(texto, args.output)


def _distribuicao_da_linha(texto: str, base):
    """«normal:média:desvio», «lognormal:média:desvio», «triangular:mín:moda:máx»,
    «uniforme:mín:máx» ou «fixo». Os limites de truncagem vêm dos padrões do projeto."""
    from dataclasses import replace
    partes = [p.strip() for p in str(texto).split(":")]
    tipo = partes[0].lower()
    if tipo == "fixo":
        return replace(base, variar=False)
    numeros = [float(x.replace(",", ".")) for x in partes[1:]]
    precisa = {"normal": 2, "lognormal": 2, "triangular": 3, "uniforme": 2}
    if tipo not in precisa or len(numeros) != precisa[tipo]:
        raise ValueError(f"Distribuição inválida «{texto}»: use normal:média:desvio, lognormal:média:desvio, "
                         "triangular:mín:moda:máx, uniforme:mín:máx ou fixo.")
    if tipo in ("normal", "lognormal"):
        return replace(base, tipo=tipo, media=numeros[0], desvio=numeros[1], variar=True)
    if tipo == "triangular":
        return replace(base, tipo=tipo, minimo=numeros[0], moda=numeros[1], maximo=numeros[2], variar=True)
    return replace(base, tipo=tipo, minimo=numeros[0], maximo=numeros[1], variar=True)


def _parametros_estocasticos(bundle: Dict[str, Any], cfg: TritonConfig, args: argparse.Namespace):
    """As distribuições salvas no projeto (ou os padrões), com o que a linha de comando sobrepõe."""
    from triton.core.modulacao_estocastica import ParametrosIncertos, padroes_do_projeto
    analysis_cfg = bundle.get("analysis", {}) or {}
    salvos = (analysis_cfg.get("modulacao_estocastica")
              or (bundle.get("ui_state") or {}).get("modulacao_estocastica") or {})
    parametros = (ParametrosIncertos.de_dict(salvos["parametros"]) if salvos.get("parametros")
                  else padroes_do_projeto(cfg))
    from triton.core.modulacao_estocastica import CATALOGO, distribuicao_de_triagem
    pedidos = [("per_capita_l_dia", args.per_capita), ("pessoas", args.people),
               ("fracao_nao_potavel_pct", args.non_potable)]
    for item in args.variables or []:
        nome, _, spec = item.partition("=")
        pedidos.append((nome.strip(), spec.strip()))
    for nome, valor in pedidos:
        if not valor:
            continue
        if nome not in CATALOGO:
            raise ValueError(f"Variável desconhecida «{nome}»; use uma de: {', '.join(CATALOGO)}.")
        base = parametros.variaveis.get(nome) or distribuicao_de_triagem(cfg, nome)
        parametros.variaveis[nome] = _distribuicao_da_linha(valor, base)
    if args.daily_cv is not None:
        parametros.cv_diario_pct = float(args.daily_cv)
    if args.climate_models:
        from triton.core.climate_database import CLIMATE_MODELS
        pedido = args.climate_models.strip()
        if pedido.lower() in ("todos", "all"):
            parametros.modelos_climaticos = list(CLIMATE_MODELS)
        elif pedido.lower() in ("nenhum", "none"):
            parametros.modelos_climaticos = []
        else:
            parametros.modelos_climaticos = [m.strip() for m in pedido.split(",") if m.strip()]
    amostras = args.samples or int(salvos.get("amostras", 1000))
    semente = args.seed if args.seed is not None else int(salvos.get("semente", 42))
    return parametros, amostras, semente


def _run_stochastic_study(args: argparse.Namespace) -> None:
    """Modulação probabilística: o estudo inteiro refeito com as premissas escolhidas sorteadas."""
    from triton.core.modulacao_estocastica import CATALOGO, simular

    if args.list_variables:
        for v in CATALOGO.values():
            print(f"{v.chave:<24} {v.grupo:<14} {v.rotulo} ({v.unidade}){' — ligada por padrão' if v.padrao else ''}")
        from triton.core.climate_database import CLIMATE_MODELS
        print(f"\nModelos climáticos (--climate-models): {', '.join(CLIMATE_MODELS)}")
        return
    if not args.file:
        raise ValueError("Informe o projeto (ou use --list-variables).")

    bundle = _load_bundle(args.file)
    cfg = bundle["config"]
    _apply_overrides(cfg, args.set_values)
    precipitation = _get_precipitation(bundle)
    errors = _validate_config(cfg, precipitation) + _validate_analysis_config(bundle.get("analysis"))
    if errors:
        raise ValueError("Projeto inválido:\n- " + "\n- ".join(errors))
    analysis_cfg = bundle.get("analysis", {}) or {}
    parametros, amostras, semente = _parametros_estocasticos(bundle, cfg, args)
    weights = args.weights or tuple(analysis_cfg.get("topsis_weights", PESOS_PADRAO))

    def progresso(feitas: int, total: int) -> None:
        if args.format == "text" and not args.quiet:
            print(f"\r{feitas}/{total} realizações", end="", file=sys.stderr, flush=True)

    dados = simular(cfg, precipitation, parametros, amostras=amostras, semente=semente,
                    ao_progredir=progresso, pesos=weights, ambiental=analysis_cfg.get("environmental"))
    if args.format == "text" and not args.quiet:
        print(file=sys.stderr)

    # Os VPL («vpl_brl») estão na moeda do projeto; o arquivo diz qual.
    dados["moeda"] = _moeda_do_bundle(bundle)
    if args.format == "json":
        _emit(json.dumps(dados, ensure_ascii=False, indent=2, default=_json_default), args.output)
        return
    if args.format == "csv":
        if not args.output:
            raise ValueError("--output é obrigatório para o formato csv")
        with Path(args.output).open("w", newline="", encoding="utf-8-sig") as stream:
            campos = list(dados["amostras"][0].keys()) if dados["amostras"] else []
            writer = csv.DictWriter(stream, fieldnames=campos, delimiter=";")
            writer.writeheader()
            writer.writerows(dados["amostras"])
        print(f"Amostras salvas em: {Path(args.output).resolve()}")
        return

    def br(x, casas=0):
        return "—" if x is None else f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ref = dados["volume_de_referencia_l"]
    linha = next((v for v in dados["por_volume"] if v["volume_l"] == ref), None)
    # Moeda do projeto (o «R$» era fixo, também em projeto em euro).
    rs = (_moeda_do_bundle(bundle) or {}).get("symbol") or "(moeda do projeto)"
    texto = [f"Modulação probabilística: {dados['realizacoes_feitas']} realizações, semente {dados['semente']}",
             f"Volume de referência (escolhido pelo estudo): {br(ref)} L"]
    if linha:
        p, v = linha["potencial_pct"], linha["vpl_brl"]
        texto += [f"Potencial de economia: caso-base {br(linha['base']['potencial_pct'], 1)}%, "
                  f"P5–P50–P95 {br(p['p5'], 1)}–{br(p['p50'], 1)}–{br(p['p95'], 1)}%",
                  f"VPL: caso-base {rs} {br(linha['base']['vpl_brl'])}; P5 {rs} {br(v['p5'])}, mediana {rs} {br(v['p50'])}, "
                  f"P95 {rs} {br(v['p95'])}; P(VPL > 0) = {br(linha['prob_vpl_positivo_pct'], 0)}%"]
    texto.append("Variáveis sorteadas: " + ", ".join(CATALOGO[k].rotulo for k in dados["variaveis_ativas"]))
    if dados.get("por_modelo"):
        eta = dados["sensibilidade_modelo_eta2"]
        texto.append(f"Modelo climático sorteado entre {len(dados['por_modelo'])}; η² com o VPL "
                     f"{br(eta.get('vpl_brl'), 2)}, com o potencial {br(eta.get('potencial_pct'), 2)}")
        for m in dados["por_modelo"]:
            texto.append(f"  {m['modelo']}: {m['realizacoes']} realizações, potencial médio "
                         f"{br(m['potencial_pct']['media'], 1)}%, VPL médio {rs} {br(m['vpl_brl']['media'])}")
    for nome, rho in sorted(dados["sensibilidade_spearman"].items(),
                            key=lambda kv: -abs(kv[1]["vpl_brl"] or 0.0)):
        texto.append(f"  ρ de Spearman com o VPL, {CATALOGO[nome].rotulo}: {br(rho['vpl_brl'], 2)}")
    for chave, rotulo in (("ideal_tecnico", "Ideal técnico"), ("otimo_economico", "Ótimo econômico (payback)"),
                          ("vencedor_topsis", "Vencedor TOPSIS")):
        freq = dados["frequencia_pct"][chave]
        texto.append(f"{rotulo}: " + ", ".join(
            (f"{k} L {br(f, 0)}%" if k != "nenhum" else f"nenhum {br(f, 0)}%") for k, f in freq.items()))
    _emit("\n".join(texto), args.output)


def _run_stochastic_demand(args: argparse.Namespace) -> None:
    """Propaga a incerteza do consumo diário sobre o desempenho e sobre o volume."""
    from triton.core.demanda_estocastica import (
        PerfilDeConsumo, simular, volume_ideal_por_realizacao)

    bundle = _load_bundle(args.file)
    cfg = bundle["config"]
    _apply_overrides(cfg, args.set_values)
    precipitation = _get_precipitation(bundle)
    errors = _validate_config(cfg, precipitation)
    if errors:
        raise ValueError("Projeto inválido:\n- " + "\n- ".join(errors))

    parametros = _parametros_de_simulacao(cfg)
    perfil = PerfilDeConsumo(
        media_l_dia=parametros["total_demand_per_day"], cv_pct=args.daily_cv,
        distribuicao=args.distribution,
        probabilidade_de_ausencia_pct=args.absence,
        incerteza_da_media_pct=args.level_uncertainty,
    )
    volume = args.volume
    if volume is None:
        baseline, summary = _run_technical(cfg, precipitation)
        volume = summary.get("optimal_volume_l") or (baseline[-1].lower_tank_vol if baseline else 0.0)

    dados = simular(precipitation, float(volume), perfil, parametros,
                    realizacoes=args.samples, semente=args.seed)
    if args.ideal_volume:
        volumes = [float(v) for v in np.arange(args.step, args.max_volume + args.step / 2, args.step)]
        dados["volume_ideal"] = volume_ideal_por_realizacao(
            precipitation, perfil, parametros, volumes_l=volumes,
            limiar_ganho_pct_m3=args.threshold,
            realizacoes=min(args.samples, args.ideal_volume_samples), semente=args.seed)

    if args.format == "json":
        texto = json.dumps(dados, ensure_ascii=False, indent=2)
    else:
        p = dados["potencial_pct"]
        linhas = [
            f"Volume analisado: {dados['volume_l']:,.0f} L".replace(",", "."),
            f"Demanda média: {perfil.media_l_dia:,.0f} L/dia".replace(",", "."),
            f"Sorteio: {args.samples} realizações, {perfil.distribuicao}, "
            f"CV diário de {perfil.cv_pct:.0f}%, incerteza da média de "
            f"{perfil.incerteza_da_media_pct:.0f}%, ausência em {perfil.probabilidade_de_ausencia_pct:.0f}% dos dias",
            "",
            f"Potencial de economia   determinístico {dados['deterministico']['potencial_pct']:.2f}%"
            f"   sorteado {p['p5']:.2f}% a {p['p95']:.2f}% (mediana {p['p50']:.2f}%)",
            f"Dias plenamente atendidos  {dados['dias_plenos_pct']['p5']:.1f}% a {dados['dias_plenos_pct']['p95']:.1f}%",
            f"Extravasamento médio       {dados['extravasado_l_dia']['p5']:.0f} a "
            f"{dados['extravasado_l_dia']['p95']:.0f} L/dia",
        ]
        if "volume_ideal" in dados:
            vi = dados["volume_ideal"]["volume_ideal_l"]
            distintos = ", ".join(f"{v:,.0f}".replace(",", ".") for v in dados["volume_ideal"]["volumes_distintos"])
            linhas += ["", f"Volume ideal por realização: {vi['p5']:,.0f} a {vi['p95']:,.0f} L".replace(",", "."),
                       f"Volumes eleitos: {distintos} L"]
        texto = "\n".join(linhas)
    _emit(texto, args.output)


def _run_uncertainty(args: argparse.Namespace) -> None:
    """Propaga incerteza independente nas premissas principais por Monte Carlo."""
    if any(value < 0 for value in (args.rainfall_cv, args.area_cv, args.demand_cv, args.capex_cv)):
        raise ValueError("Os coeficientes de variação (CV) não podem ser negativos.")
    bundle = _load_bundle(args.file)
    cfg = bundle["config"]
    _apply_overrides(cfg, args.set_values)
    precipitation = _get_precipitation(bundle)
    errors = _validate_config(cfg, precipitation) + _validate_analysis_config(bundle.get("analysis"))
    if errors:
        raise ValueError("Projeto inválido:\n- " + "\n- ".join(errors))
    analysis_cfg = bundle.get("analysis", {}) or {}
    weights = args.weights or tuple(analysis_cfg.get("topsis_weights", PESOS_PADRAO))

    # Sem volume explícito, a referência é o ótimo técnico do caso-base; isso
    # mede a robustez de uma decisão de projeto concreta, não de toda a varredura.
    if args.volume is None:
        baseline, summary = _run_technical(cfg, precipitation)
        volume = summary.get("optimal_volume_l") or (baseline[-1].lower_tank_vol if baseline else cfg.lower_tank_fixed)
    else:
        volume = args.volume
    rng = np.random.default_rng(args.seed)
    samples: List[Dict[str, Any]] = []
    capex_fields = ("cost_lower_tank", "cost_upper_tank", "cost_labor", "cost_piping", "cost_accessories", "pump_unit_cost")
    for index in range(args.samples):
        scenario = copy.deepcopy(cfg)
        rainfall_factor = max(0.0, rng.normal(1.0, args.rainfall_cv / 100.0))
        scenario.area = max(0.01, scenario.area * rng.normal(1.0, args.area_cv / 100.0))
        scenario.demand_value = max(0.0, scenario.demand_value * rng.normal(1.0, args.demand_cv / 100.0))
        for field in capex_fields:
            setattr(scenario, field, max(0.0, getattr(scenario, field) * rng.normal(1.0, args.capex_cv / 100.0)))
        report = run_analysis(
            scenario, precipitation * rainfall_factor, args.analysis, volume, weights,
            analysis_cfg.get("environmental", {}), bundle.get("source_path", args.file), 0, args.seed + index,
        )
        technical = report["technical"]["alternatives"][0]
        row = {"sample": index + 1, "rainfall_factor": rainfall_factor, "area_m2": scenario.area,
               "demand_l_person_day": scenario.demand_value, **technical}
        if "economic" in report:
            row.update(report["economic"]["alternatives"][0])
        if "environmental" in report:
            row.update(report["environmental"]["alternatives"][0])
        samples.append(row)

    def quantiles(key: str) -> Dict[str, float]:
        values = np.array([float(row[key]) for row in samples if row.get(key) is not None], dtype=float)
        return {"p05": float(np.quantile(values, .05)), "p50": float(np.quantile(values, .50)), "p95": float(np.quantile(values, .95))}
    summary = {
        "samples": args.samples, "seed": args.seed, "selected_volume_l": volume,
        "uncertainty_cv_pct": {"rainfall": args.rainfall_cv, "area": args.area_cv, "demand": args.demand_cv, "capex": args.capex_cv},
        "potable_savings_pct": quantiles("potable_savings_pct"),
    }
    if "npv_brl" in samples[0]:
        summary["npv_brl"] = quantiles("npv_brl")
        summary["probability_npv_positive_pct"] = 100.0 * sum(row["npv_brl"] > 0 for row in samples) / len(samples)
    if "lifetime_net_co2_saved_kg" in samples[0]:
        summary["lifetime_net_co2_saved_kg"] = quantiles("lifetime_net_co2_saved_kg")
        summary["probability_environmentally_viable_pct"] = 100.0 * sum(bool(row["environmentally_viable"]) for row in samples) / len(samples)
    output = {"schema": {"name": "triton-uncertainty", "version": 1},
              "generated_at_utc": datetime.now(timezone.utc).isoformat(), "summary": summary, "samples": samples}
    if args.format == "text":
        print(f"=== Triton | incerteza Monte Carlo | {args.samples} amostras ===")
        print(f"Volume analisado: {volume:.0f} L")
        print(f"Economia potável (%), P05/P50/P95: {summary['potable_savings_pct']}")
        if "npv_brl" in summary:
            print(f"VPL, P05/P50/P95: {summary['npv_brl']} | P(VPL > 0): {summary['probability_npv_positive_pct']:.1f}%")
        return
    if not args.output:
        raise ValueError("--output é obrigatório para exportar a análise de incerteza")
    target = Path(args.output)
    if args.format == "json":
        target.write_text(_json_dump(output), encoding="utf-8")
    elif args.format == "csv":
        with target.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=sorted({key for row in samples for key in row}), delimiter=";")
            writer.writeheader(); writer.writerows(samples)
    else:
        raise ValueError("A análise de incerteza suporta os formatos text, json e csv")
    print(f"Resultado salvo em: {target.resolve()}")


MASS_TEST_CASES = [
    {"name": "Caso 1 (S1)", "sup": 150.0, "inf": 310.0, "ref_file": "150_310_consolidado_final.csv"},
    {"name": "Caso 2 (S2)", "sup": 250.0, "inf": 500.0, "ref_file": "250_500_consolidado_final.csv"},
    {"name": "Caso 3 (S3)", "sup": 500.0, "inf": 1000.0, "ref_file": "500_1000_consolidado_final.csv"},
    {"name": "Caso 4 (S4)", "sup": 1000.0, "inf": 2000.0, "ref_file": "1000_2000_consolidado_final.csv"},
]

KNOWN_MODELS = [
    "ACCESS-CM2", "ACCESS-ESM1-5", "CMCC-ESM2", "EC-EARTH3", "GFDL-CM4",
    "GFDL-ESM4", "HadGEM3-GC31-LL", "INM-CM4_8", "INM-CM5", "IPSL-CM6A-LR",
    "KACE", "KIOST", "MIROC6", "MPI-ESM1-2", "MRI-ESM2", "NESM3",
    "NorESM2-MM", "TaiESM1", "UKESM1-0-LL"
]

def _parse_filename_meta(fname: str) -> Tuple[str, str, str]:
    raw = fname.replace("(Triton)", "").rsplit(".", 1)[0]
    matched_model = None
    for m in KNOWN_MODELS:
        if f"_{m}_" in raw or raw.endswith(f"_{m}"):
            matched_model = m
            break
    if matched_model:
        idx = raw.find(matched_model)
        city = raw[:idx].rstrip("_")
        scen = raw[idx + len(matched_model):].lstrip("_")
        return city, matched_model, scen
    parts = raw.split("_")
    if len(parts) >= 3 and parts[-1] in ("Near", "Far"):
        return "_".join(parts[:-3]), parts[-3], f"{parts[-2]}_{parts[-1]}"
    elif len(parts) >= 2:
        return "_".join(parts[:-2]), parts[-2], parts[-1]
    return raw, "Unknown", "Unknown"


def _worker_mass_compare_file(task_tuple: Tuple) -> Dict[str, Any]:
    (
        file_path,
        sup_vol,
        inf_vol,
        area,
        residents,
        demand_per_capita,
        share,
        runoff,
        discard_mm,
        pumping_threshold,
    ) = task_tuple

    fname = os.path.basename(file_path)
    city, model, scenario = _parse_filename_meta(fname)

    try:
        precip_data = load_precipitation(file_path)
        tot_demand = demand_per_capita * residents

        sim_res = run_single_simulation(
            precip_data=precip_data,
            lower_tank_vol=inf_vol,
            upper_tank_vol=sup_vol,
            upper_tank_used=True,
            pumping_threshold=pumping_threshold,
            area=area,
            runoff_coeff=runoff,
            discard_mm=discard_mm,
            total_demand_per_day=tot_demand,
            rainwater_share=share,
        )

        return {
            "success": True,
            "city": city,
            "model": model,
            "scenario": scenario,
            "metrics": {
                "potential_savings": round(sim_res.potential_potable_savings_pct, 2),
                "average_rainwater_consumption": round(sim_res.avg_pluvial_consumed_l_day, 3),
                "average_drinking_water_consumption": round(sim_res.avg_potable_consumed_l_day, 3),
                "average_rainwater_overflow": round(sim_res.avg_spilled_l_day, 3),
                "period_when_demand_is_fully_met": round(sim_res.pct_days_full_satisfaction, 2),
                "period_when_demand_is_partially_met": round(sim_res.pct_days_partial_satisfaction, 2),
                "period_when_demand_is_not_met": round(sim_res.pct_days_null_satisfaction, 2),
            },
            "error": "",
        }
    except Exception as exc:
        return {
            "success": False,
            "city": city,
            "model": model,
            "scenario": scenario,
            "error": str(exc),
        }


def _run_compare_mass(args: argparse.Namespace) -> None:
    import glob
    import time
    from concurrent.futures import ProcessPoolExecutor, as_completed

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = args.input_dir or os.path.join(base_dir, "TesteMassivo", "Triton_future_files_split")
    reference_dir = args.reference_dir or os.path.join(base_dir, "TesteMassivo")
    output_dir = args.output_dir or os.path.join(base_dir, "TesteMassivo", "nova_versao")

    os.makedirs(output_dir, exist_ok=True)

    climate_files = sorted(glob.glob(os.path.join(input_dir, "*.csv")) + glob.glob(os.path.join(input_dir, "*.txt")))
    if not climate_files:
        raise ValueError(f"Nenhum arquivo climático encontrado em: {input_dir}")

    workers = args.workers or os.cpu_count() or 4

    print("=" * 80)
    print("TRITON -- EXECUÇÃO PARALELA MASSIVA E COMPARAÇÃO COM TESTEMASSIVO")
    print("=" * 80)
    print(f" [+] Pasta de Séries Climáticas: {input_dir}")
    print(f" [+] Pasta de Referência: {reference_dir}")
    print(f" [+] Pasta de Resultados e Relatórios: {output_dir}")
    print(f" [*] Séries Climáticas Encontradas: {len(climate_files):,}")
    print(f" [*] Casos de Cisternas Combinadas: {len(MASS_TEST_CASES)}")
    print(f" [*] Total de Simulações: {len(climate_files) * len(MASS_TEST_CASES):,}")
    print(f" [*] Processamento Multi-Core: {workers} núcleos")
    print("=" * 80)

    metric_info = [
        ("potential_savings", "Potencial de economia (%)", "%"),
        ("average_rainwater_consumption", "Volume consumido médio de água pluvial (litros/dia)", "liters/day"),
        ("average_drinking_water_consumption", "Volume consumido médio de água potável (litros/dia)", "liters/day"),
        ("average_rainwater_overflow", "Volume médio de água pluvial extravasado (litros/dia)", "liters/day"),
        ("period_when_demand_is_fully_met", "Dias em que a demanda de água pluvial é atendida completamente", "days"),
        ("period_when_demand_is_partially_met", "Dias em que a demanda de água pluvial é atendida parcialmente (%)", "%"),
        ("period_when_demand_is_not_met", "Dias em que a demanda de água pluvial não é atendida (%)", "%"),
    ]

    summary_rows = []
    start_total_time = time.time()

    for case in MASS_TEST_CASES:
        c_name = case["name"]
        sup_vol = case["sup"]
        inf_vol = case["inf"]
        ref_fname = case["ref_file"]

        print(f"\n---> Processando {c_name}: Reservatório Superior = {sup_vol:.0f} L | Reservatório Inferior = {inf_vol:.0f} L")
        t0 = time.time()

        tasks = [
            (fpath, sup_vol, inf_vol, args.area, args.residents, args.demand, percentual_para_fracao("--share", args.share), args.runoff, args.discard, 0.0)
            for fpath in climate_files
        ]

        sim_results = []
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(_worker_mass_compare_file, task) for task in tasks]
            for idx, fut in enumerate(as_completed(futures), start=1):
                res = fut.result()
                if res.get("success"):
                    sim_results.append(res)
                if idx % 10 == 0 or idx == len(tasks):
                    elapsed = time.time() - t0
                    speed = idx / elapsed if elapsed > 0 else 0
                    sys.stdout.write(f"\r Progresso {c_name}: {idx:,}/{len(tasks):,} [{idx/len(tasks)*100:.1f}%] | {speed:.1f} sim/s")
                    sys.stdout.flush()

        sys.stdout.write("\n")
        elapsed_sim = time.time() - t0
        print(f" [OK] {len(sim_results):,} simulações de {c_name} concluídas em {elapsed_sim:.2f}s")

        out_csv_path = os.path.join(output_dir, ref_fname)
        print(f" [+] Salvando novo arquivo consolidado em: {out_csv_path}")

        lines = ["city,model,scenario,metric,label,value,unit"]
        sorted_results = sorted(sim_results, key=lambda x: (x["city"], x["model"], x["scenario"]))

        for r in sorted_results:
            c = r["city"]
            m = r["model"]
            s = r["scenario"]
            m_dict = r["metrics"]

            for m_key, m_label, m_unit in metric_info:
                val = m_dict.get(m_key, 0.0)
                lines.append(f"{c},{m},{s},{m_key},{m_label},{val},{m_unit}")

        with open(out_csv_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        ref_csv_path = os.path.join(reference_dir, ref_fname)
        if os.path.exists(ref_csv_path):
            print(f" [*] Comparando resultados com a referência: {ref_csv_path}")
            ref_dict = {}
            with open(ref_csv_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = (row["city"], row["model"], row["scenario"], row["metric"])
                    try:
                        ref_dict[key] = float(row["value"])
                    except (ValueError, TypeError):
                        pass

            exact_matches = 0
            minor_diffs = 0
            discrepancies = 0
            max_diff = 0.0
            sum_diff = 0.0
            total_compared = 0

            for r in sorted_results:
                c = r["city"]
                m = r["model"]
                s = r["scenario"]
                for m_key, _, _ in metric_info:
                    new_val = r["metrics"][m_key]
                    ref_val = ref_dict.get((c, m, s, m_key))
                    if ref_val is not None:
                        total_compared += 1
                        diff = abs(new_val - ref_val)
                        sum_diff += diff
                        if diff > max_diff:
                            max_diff = diff

                        if diff <= 0.01:
                            exact_matches += 1
                        elif diff <= 0.1:
                            minor_diffs += 1
                        else:
                            discrepancies += 1

            mae = sum_diff / total_compared if total_compared > 0 else 0.0
            pct_exact = (exact_matches / total_compared * 100.0) if total_compared > 0 else 0.0

            print(f"     Métricas comparadas: {total_compared:,}")
            print(f"     Concordância Exata (diff <= 0.01): {exact_matches:,} ({pct_exact:.2f}%)")
            print(f"     Diferença Mínima (diff <= 0.10): {minor_diffs:,}")
            print(f"     Discrepâncias (> 0.10): {discrepancies:,}")
            print(f"     Erro Médio Absoluto (MAE): {mae:.4f}")
            print(f"     Diferença Máxima Absoluta: {max_diff:.4f}")

            summary_rows.append({
                "caso": c_name,
                "superior_l": sup_vol,
                "inferior_l": inf_vol,
                "total_comparado": total_compared,
                "exatos_pct": round(pct_exact, 2),
                "diferencas_menores": minor_diffs,
                "discrepancias": discrepancies,
                "mae": round(mae, 4),
                "max_diff": round(max_diff, 4),
            })
        else:
            print(f" ⚠️ Arquivo de referência não encontrado: {ref_csv_path}")

    total_elapsed = time.time() - start_total_time

    md_report_path = os.path.join(output_dir, "relatorio_comparativo_massivo.md")
    csv_report_path = os.path.join(output_dir, "relatorio_comparativo_massivo.csv")

    md_lines = [
        "# Relatório Comparativo de Simulações Massivas — Triton Nova Versão",
        "",
        f"**Data da Execução:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de Simulações Executadas:** {len(climate_files) * len(MASS_TEST_CASES):,}",
        f"**Tempo Total de Execução:** {total_elapsed:.2f} segundos",
        "",
        "---",
        "",
        "## 1. Resumo Consolidado por Caso de Reservatórios",
        "",
        "| Caso | Reservatório Superior | Reservatório Inferior | Métricas Comparadas | Equivalência Exata (≤0.01) | Dif. Menor (≤0.10) | Discrepâncias (>0.10) | MAE (Erro Médio) | Dif. Máxima |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for sr in summary_rows:
        md_lines.append(
            f"| {sr['caso']} | {sr['superior_l']:.0f} L | {sr['inferior_l']:.0f} L | {sr['total_comparado']:,} | {sr['exatos_pct']:.2f}% | {sr['diferencas_menores']:,} | {sr['discrepancias']:,} | {sr['mae']:.4f} | {sr['max_diff']:.4f} |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 2. Significado Prático do Limiar de Tolerância (diff ≤ 0,10)",
        "",
        "O parâmetro `diff` representa a diferença absoluta entre o valor calculado na nova versão e o valor do arquivo de referência (`abs(valor_novo - valor_ref)`):",
        "",
        "- **Nas Variáveis Percentuais (`%`)** (ex: `% de Economia Potável` e `% de Atendimento`):",
        "  - `diff ≤ 0,10` significa **menos de 0,10%** (menos de 1 décimo de ponto percentual).",
        "  - *Exemplo de unidade:* referência **19,97%**, nova versão **19,98%** → `diff` = **0,01 ponto percentual**.",
        "",
        "- **Nas Variáveis Volumétricas Diárias (`L/dia`)** (ex: `Consumo Pluvial`, `Consumo Potável` e `Extravasamento`):",
        "  - `diff ≤ 0,10` significa **menos de 0,10 Litros por dia** (menos de **100 mL/dia** de água em uma demanda total de 600 L/dia).",
        "  - *Exemplo de unidade:* referência **119,837 L/dia**, nova versão **119,864 L/dia** → `diff` = **0,027 L/dia**.",
        "",
        "---",
        "",
        "## 3. Limites de interpretação",
        "",
        "Somente a tabela da Seção 1 é calculada a partir desta execução. Estatísticas históricas fixas foram removidas para impedir que resultados de outro conjunto de arquivos sejam atribuídos ao lote atual.",
        "",
        "A concordância mede regressão contra os CSVs fornecidos em `--reference-dir`; ela não prova que o baseline representa a realidade física. Divergências devem ser investigadas por métrica, unidade, série, versão e equação antes de serem classificadas como erro de qualquer implementação.",
        "",
        "A comparação também não substitui conservação de massa, validação com dados medidos, análise de incerteza ou revisão independente.",
    ])

    with open(md_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    with open(csv_report_path, "w", encoding="utf-8") as f:
        f.write("caso;superior_l;inferior_l;total_comparado;exatos_pct;diferencas_menores;discrepancias;mae;max_diff\n")
        for sr in summary_rows:
            f.write(f"{sr['caso']};{sr['superior_l']};{sr['inferior_l']};{sr['total_comparado']};{sr['exatos_pct']};{sr['diferencas_menores']};{sr['discrepancias']};{sr['mae']};{sr['max_diff']}\n")

    print("\n" + "=" * 80)
    print(f"[OK] EXECUÇÃO MASSIVA CONCLUÍDA COM SUCESSO EM {total_elapsed:.2f} SEGUNDOS!")
    print(f"     Relatório Markdown salvo em: {md_report_path}")
    print(f"     Relatório CSV salvo em: {csv_report_path}")
    print("=" * 80)


def _parse_filename_meta_vaz(fname: str) -> Tuple[str, str, str, str]:
    cleaned = fname.replace("(Triton)", "").replace(".csv", "").replace(".txt", "")
    horizon = "Histórico"
    if "_Near" in cleaned:
        horizon = "Near"
        cleaned = cleaned.replace("_Near", "")
    elif "_Middle" in cleaned:
        horizon = "Middle"
        cleaned = cleaned.replace("_Middle", "")
    elif "_Far" in cleaned:
        horizon = "Far"
        cleaned = cleaned.replace("_Far", "")

    scenario = "Histórico"
    if "_SSP245" in cleaned:
        scenario = "SSP245"
        if horizon == "Histórico":
            horizon = "Futuro (2015-2100)"
        cleaned = cleaned.replace("_SSP245", "")
    elif "_SSP585" in cleaned:
        scenario = "SSP585"
        if horizon == "Histórico":
            horizon = "Futuro (2015-2100)"
        cleaned = cleaned.replace("_SSP585", "")

    model = "Desconhecido"
    for m in KNOWN_MODELS:
        if m in cleaned:
            model = m
            break

    city = cleaned
    if model != "Desconhecido":
        city = cleaned.replace(f"_{model}", "").replace(model, "")
    city = city.strip("_")

    return city, model, scenario, horizon


VAZ_BUILDING_MODELS = {
    "UTI": {
        "name": "Casa Unifamiliar Térrea",
        "residents": 4,
        "roof_area": 60.19,
        "floors": 1,
        "material": "PEAD",
        "pipe_len": 25.0,
        "pipe_dn": 75,
        "accessories": 600.0,
        "pump_kw": 0.37,
        "om": 600.0,
    },
    "UTG": {
        "name": "Casa Unifamiliar Geminada",
        "residents": 8,
        "roof_area": 115.43,
        "floors": 1,
        "material": "PEAD",
        "pipe_len": 40.0,
        "pipe_dn": 75,
        "accessories": 1000.0,
        "pump_kw": 0.55,
        "om": 900.0,
    },
    "MSG": {
        "name": "Sobrado Multifamiliar Geminado",
        "residents": 16,
        "roof_area": 132.53,
        "floors": 2,
        "material": "CONCRETO",
        "pipe_len": 70.0,
        "pipe_dn": 100,
        "accessories": 1800.0,
        "pump_kw": 0.75,
        "om": 1500.0,
    },
    "MFH": {
        "name": "Bloco Multifamiliar H",
        "residents": 64,
        "roof_area": 158.70,
        "floors": 4,
        "material": "CONCRETO",
        "pipe_len": 140.0,
        "pipe_dn": 100,
        "accessories": 4200.0,
        "pump_kw": 3.0,
        "om": 3800.0,
    },
    "MFL": {
        "name": "Bloco Multifamiliar Retangular",
        "residents": 128,
        "roof_area": 421.52,
        "floors": 4,
        "material": "CONCRETO",
        "pipe_len": 270.0,
        "pipe_dn": 150,
        "accessories": 8500.0,
        "pump_kw": 4.5,
        "om": 7200.0,
    },
}


def _worker_vaz_study_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Worker por arquivo climático (450 simulações em memória por arquivo).
    Lê o arquivo de precipitação UMA ÚNICA VEZ e executa todas as tipologias/cenários.
    Executa com prioridade de CPU em segundo plano (BELOW_NORMAL) para garantir fluidez total do PC.
    """
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.SetPriorityClass(
                ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
            )  # BELOW_NORMAL_PRIORITY_CLASS
        except Exception:
            pass

    fname = os.path.basename(file_path)
    city, model, scenario, horizon = _parse_filename_meta_vaz(fname)

    try:
        rain = load_precipitation(file_path)
    except Exception:
        return []

    records = []

    for bcode, bspec in VAZ_BUILDING_MODELS.items():
        tot_demand = bspec["residents"] * 150.0
        for share in [0.30, 0.40, 0.50]:
            pluvial_demand = tot_demand * share
            for dmode in [1, 2, 3]:
                candidates = []
                cand_data = []
                v_list = [500, 1000, 2000, 3000, 5000, 7500, 10000, 15000, 20000, 30000]

                for v_low in v_list:
                    cfg = TritonConfig()
                    cfg.area = bspec["roof_area"]
                    cfg.residents_count = bspec["residents"]
                    cfg.demand_value = 150.0
                    cfg.rainwater_share = share
                    cfg.discard = 2.0
                    cfg.discard_mode = dmode
                    cfg.upper_tank_used = True
                    cfg.upper_tank_vol = 0.5 * pluvial_demand
                    cfg.lower_tank_fixed = float(v_low)
                    # Cada volume do estudo e uma cisterna diferente: sem isto o
                    # TritonConfig novo cobrava o mesmo preco-padrao de 500 L a
                    # 30.000 L, e o VPL so crescia com o volume.
                    cfg.cost_lower_tank = _preco_da_cisterna(cfg, float(v_low))
                    # O projeto guarda % ao mês. O valor 0,12 aqui significava
                    # 0,12% ao mês, e não os 12% ao ano pretendidos.
                    cfg.tma = anual_pct_para_mensal_pct(12.0)
                    cfg.inflation = anual_pct_para_mensal_pct(4.5)
                    cfg.analysis_period_years = 30

                    sim_res = run_single_simulation(
                        precip_data=rain,
                        lower_tank_vol=float(v_low),
                        area=bspec["roof_area"],
                        runoff_coeff=0.80,
                        discard_mm=2.0,
                        discard_mode=dmode,
                        total_demand_per_day=tot_demand,
                        rainwater_share=share,
                        upper_tank_vol=cfg.upper_tank_vol,
                        upper_tank_used=True,
                        pumping_threshold=0.0
                    )
                    
                    econ_res = run_economic_analysis(cfg, sim_res)

                    pipes = [PipeInput(length_m=bspec["pipe_len"], diameter_mm=bspec["pipe_dn"])]
                    pump_obj = PumpInput(power_cv=bspec["pump_kw"] / 0.735)
                    env_cfg = EnvironmentalConfig(
                        lower_tank_vol=float(v_low),
                        annual_water_saved_m3=sim_res.annual_pluvial_consumed_m3,
                        annual_pump_kwh=econ_res.annual_pump_kwh,
                        lower_material_key=bspec["material"],
                        upper_tank_used=True,
                        upper_tank_vol_liters=cfg.upper_tank_vol,
                        upper_material_key="PEAD",
                        pipes=pipes,
                        pump=pump_obj,
                        system_lifespan_years=30
                    )
                    lca_res = calculate_lca(env_cfg)

                    cand = TopsisCandidate(
                        lower_tank_vol=float(v_low),
                        water_saved_m3_yr=sim_res.annual_pluvial_consumed_m3,
                        vpl_brl=econ_res.vpl,
                        co2_saved_kg_lifetime=lca_res.lifetime_net_co2_saved_kg,
                        potential_savings_pct=sim_res.potential_potable_savings_pct,
                        overflow_m3_yr=sim_res.annual_spill_m3,
                        discounted_payback_years=(econ_res.payback_months / 12.0 if econ_res.payback_months is not None else None),
                        irr_pct=econ_res.tir_annual_pct,
                        potable_consumed_m3_yr=sim_res.annual_potable_consumed_m3,
                    )
                    candidates.append(cand)
                    cand_data.append((v_low, sim_res, econ_res, lca_res))

                top_res = calculate_topsis_scores(candidates, weights=(0.333333, 0.333333, 0.333333))

                for idx, (v_low, sim_res, econ_res, lca_res) in enumerate(cand_data):
                    t_score = float(top_res.scores[idx]) if top_res is not None else 0.0
                    t_rank = int(top_res.rankings[idx]) if top_res is not None else idx + 1
                    is_best = bool(top_res.best_index == idx) if top_res is not None else False

                    records.append({
                        "city": city,
                        "model": model,
                        "scenario": scenario,
                        "horizon": horizon,
                        "building_code": bcode,
                        "building_name": bspec["name"],
                        "residents": bspec["residents"],
                        "roof_area_m2": bspec["roof_area"],
                        "demand_per_capita_l": 150.0,
                        "total_demand_l_day": tot_demand,
                        "rainwater_share_pct": share * 100.0,
                        "discard_rule_mode": dmode,
                        "discard_mm": 2.0,
                        "lower_tank_vol_l": float(v_low),
                        "upper_tank_vol_l": float(cfg.upper_tank_vol),
                        "potential_savings_pct": float(sim_res.potential_potable_savings_pct),
                        "avg_pluvial_consumed_l_day": float(sim_res.avg_pluvial_consumed_l_day),
                        "annual_pluvial_consumed_m3": float(sim_res.annual_pluvial_consumed_m3),
                        "avg_potable_consumed_l_day": float(sim_res.avg_potable_consumed_l_day),
                        "annual_potable_consumed_m3": float(sim_res.annual_potable_consumed_m3),
                        "avg_spilled_l_day": float(sim_res.avg_spilled_l_day),
                        "annual_spill_m3": float(sim_res.annual_spill_m3),
                        "fully_met_pct": float(sim_res.pct_days_full_satisfaction),
                        "partially_met_pct": float(sim_res.pct_days_partial_satisfaction),
                        "not_met_pct": float(sim_res.pct_days_null_satisfaction),
                        "capex_total_brl": float(econ_res.capex_total),
                        "annual_opex_brl": float(econ_res.annual_opex_brl),
                        "annual_water_savings_brl": float(econ_res.annual_water_savings_brl),
                        "vpl_brl": float(econ_res.vpl),
                        "tir_annual_pct": float(econ_res.tir_annual_pct) if econ_res.tir_annual_pct is not None else 0.0,
                        "payback_years": float(econ_res.payback_years) if econ_res.payback_years is not None else -1.0,
                        "embodied_co2_kg": float(lca_res.total_embodied_co2_kg),
                        "annual_avoided_co2_kg": float(lca_res.annual_avoided_co2_kg),
                        "lifetime_net_co2_saved_kg": float(lca_res.lifetime_net_co2_saved_kg),
                        "pump_energy_kwh_yr": float(econ_res.annual_pump_kwh),
                        "topsis_score": t_score,
                        "topsis_rank": t_rank,
                        "is_topsis_best": is_best
                    })

    return records


def _run_vaz_study(args: argparse.Namespace) -> None:
    import pandas as pd
    import gc
    import shutil

    input_dir = args.input_dir or os.path.join("TesteMassivo", "Triton_vaz_files_split")
    output_dir = args.output_dir or os.path.join("TesteMassivo", "estudo_vaz")

    if not os.path.exists(input_dir):
        print(f"[ERRO] Pasta de entrada não encontrada: {input_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    climate_files = sorted(glob.glob(os.path.join(input_dir, "*.csv")) + glob.glob(os.path.join(input_dir, "*.txt")))
    if not climate_files:
        print(f"[ERRO] Nenhum arquivo climático encontrado em: {input_dir}")
        return

    cpu_cores = os.cpu_count() or 4
    num_workers = args.workers or max(1, cpu_cores - 1)
    total_simulations = len(climate_files) * len(VAZ_BUILDING_MODELS) * 90  # 5 tipologias * 3 shares * 3 dmodes * 10 volumes = 450 sim por arquivo

    print("=" * 80)
    print("ESTUDO MASSIVO COMPLETO DE TIPOLOGIAS DE VAZ — TRITON (PARQUET STREAMING)")
    print("=" * 80)
    print(f" [+] Pasta de Séries Climáticas: {input_dir}")
    print(f" [+] Pasta de Resultados e Parquet: {output_dir}")
    print(f" [*] Séries Climáticas Encontradas: {len(climate_files):,}")
    print(f" [*] Tipologias de Edificação (Vaz): {len(VAZ_BUILDING_MODELS)} (UTI, UTG, MSG, MFH, MFL)")
    print(f" [*] Total de Simulações Diárias a Executar: {total_simulations:,}")
    print(f" [*] Processamento em Segundo Plano: {num_workers} núcleos (Headroom OS: {max(0, cpu_cores - num_workers)} núcleos)")
    print("=" * 80)

    start_total_time = time.time()
    tasks = climate_files

    simulations_completed = 0
    total_tasks = len(tasks)

    # Pasta temporária para salvamento em Parquet intermediário
    chunks_dir = os.path.join(output_dir, f"_tmp_vaz_chunks_{int(time.time())}")
    os.makedirs(chunks_dir, exist_ok=True)
    print(f" [+] Salvamento incremental otimizado em Parquet em: {chunks_dir}")

    chunk_buffer: List[Dict[str, Any]] = []
    parquet_chunk_paths: List[str] = []
    chunk_index = 0
    batch_records_threshold = 20000

    def flush_vaz_chunk():
        nonlocal chunk_buffer, chunk_index, parquet_chunk_paths
        if not chunk_buffer:
            return
        chunk_index += 1
        chunk_file = os.path.join(chunks_dir, f"part_{chunk_index:05d}.parquet")
        df_chunk = pd.DataFrame(chunk_buffer)
        df_chunk.to_parquet(chunk_file, engine="pyarrow", index=False, compression="snappy")
        parquet_chunk_paths.append(chunk_file)
        chunk_buffer.clear()
        gc.collect()

    import concurrent.futures

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        max_pending = num_workers * 2
        task_iter = iter(tasks)
        futures = {}

        # Preenche a fila inicial de submissão preguiçosa
        for _ in range(max_pending):
            try:
                fpath = next(task_iter)
                fut = executor.submit(_worker_vaz_study_file, fpath)
                futures[fut] = fpath
            except StopIteration:
                break

        last_print_time = time.time()

        while futures:
            done_set, _ = concurrent.futures.wait(set(futures.keys()), return_when=concurrent.futures.FIRST_COMPLETED)
            for fut in done_set:
                fpath_arg = futures.pop(fut)
                f_name = os.path.basename(fpath_arg)
                res_list = fut.result()

                if res_list:
                    simulations_completed += len(res_list)
                    chunk_buffer.extend(res_list)

                    if len(chunk_buffer) >= batch_records_threshold:
                        flush_vaz_chunk()

                now = time.time()
                if now - last_print_time >= 0.15 or simulations_completed == total_simulations:
                    elapsed = now - start_total_time
                    pct = (simulations_completed / total_simulations) * 100.0 if total_simulations > 0 else 0.0
                    rate = simulations_completed / elapsed if elapsed > 0 else 0
                    eta_sec = (total_simulations - simulations_completed) / rate if rate > 0 else 0
                    sys.stdout.write(
                        f"\r Progresso Simulações: {simulations_completed:,}/{total_simulations:,} [{pct:.1f}%] | "
                        f"Velocidade: {rate:,.1f} sim/s | ETA: {eta_sec:.0f}s | "
                        f"Arquivo: {f_name}"
                    )
                    sys.stdout.flush()
                    last_print_time = now

                # Submete a próxima tarefa preguiçosamente
                try:
                    next_fpath = next(task_iter)
                    next_fut = executor.submit(_worker_vaz_study_file, next_fpath)
                    futures[next_fut] = next_fpath
                except StopIteration:
                    pass

        sys.stdout.write("\n")

    # Descarrega o último lote em RAM
    flush_vaz_chunk()

    total_elapsed = time.time() - start_total_time

    parquet_file_path = os.path.join(output_dir, "estudo_vaz_consolidado.parquet")
    print(f"\n [+] Unificando {len(parquet_chunk_paths)} arquivos Parquet intermediários em streaming: {parquet_file_path}...")

    total_records = 0
    if parquet_chunk_paths:
        import pyarrow.parquet as pq
        import pyarrow.dataset as ds
        writer = None
        for cp in parquet_chunk_paths:
            table = pq.read_table(cp)
            total_records += table.num_rows
            if writer is None:
                writer = pq.ParquetWriter(parquet_file_path, table.schema, compression="snappy")
            writer.write_table(table)
            del table
            gc.collect()
        if writer is not None:
            writer.close()
        del writer
        gc.collect()

        # Remove a pasta temporária de chunks
        if os.path.exists(chunks_dir):
            shutil.rmtree(chunks_dir, ignore_errors=True)

        # Lê apenas os registros com is_topsis_best para o relatório leve em memória
        try:
            dataset = ds.dataset(parquet_file_path, format="parquet")
            table_best = dataset.to_table(filter=ds.field("is_topsis_best") == True)
            df_best = table_best.to_pandas()
        except Exception:
            df_best = pd.DataFrame()
    else:
        df_best = pd.DataFrame()

    # Remove qualquer arquivo CSV gigante legado da pasta de saída
    legacy_csv = os.path.join(output_dir, "estudo_vaz_incremental.csv")
    if os.path.exists(legacy_csv):
        try:
            os.remove(legacy_csv)
        except Exception:
            pass

    md_report_path = os.path.join(output_dir, "relatorio_estudo_vaz.md")
    csv_report_path = os.path.join(output_dir, "relatorio_estudo_vaz.csv")

    md_lines = [
        "# Relatório Sintético do Estudo Massivo de Tipologias de Vaz — Triton",
        "",
        f"**Data da Execução:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de Séries Climáticas Analisadas:** {len(climate_files):,}",
        f"**Total de Registros no Arquivo Parquet:** {len(df):,}",
        f"**Arquivo Parquet Consolidado Único:** [`{os.path.abspath(parquet_file_path)}`](file:///{os.path.abspath(parquet_file_path).replace(os.sep, '/')})",
        f"**Tempo Total de Processamento:** {total_elapsed:.2f} segundos ({total_elapsed/60:.2f} minutos)",
        "",
        "---",
        "",
        "## Resumo de Resultados Médios das Soluções Vencedoras TOPSIS por Tipologia",
        "",
        "| Código | Nome da Tipologia | Moradores | Cobertura (m²) | Economia Médial Pluvial (%) | Volume Ótimo Médio (L) | VPL Médio (R$) | CO2 Evitado Vida Útil (kg) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for bcode, bspec in VAZ_BUILDING_MODELS.items():
        if not df_best.empty:
            sub_b = df_best[df_best["building_code"] == bcode]
            if len(sub_b) > 0:
                avg_sav = sub_b["potential_savings_pct"].mean()
                avg_vol = sub_b["lower_tank_vol_l"].mean()
                avg_vpl = sub_b["vpl_brl"].mean()
                avg_co2 = sub_b["lifetime_net_co2_saved_kg"].mean()
                md_lines.append(
                    f"| {bcode} | {bspec['name']} | {bspec['residents']} | {bspec['roof_area']:.2f} | {avg_sav:.2f}% | {avg_vol:.0f} L | R$ {avg_vpl:,.2f} | {avg_co2:,.1f} kg |"
                )

    with open(md_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    # Salvar resumo CSV sintético (apenas as melhores por TOPSIS, poucas linhas)
    df_best.to_csv(csv_report_path, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 80)
    print(f"[OK] ESTUDO VAZ CONCLUÍDO COM SUCESSO EM {total_elapsed:.2f} SEGUNDOS!")
    print(f"     * Arquivo Parquet Único Consolidado: {parquet_file_path}")
    print(f"     * Relatório Markdown Sintético: {md_report_path}")
    print(f"     * Resumo TOPSIS (CSV pequeno): {csv_report_path}")
    print("=" * 80)


class _AnalisadorDaEdicao(argparse.ArgumentParser):
    """``ArgumentParser`` cuja ajuda sai no idioma da edição (``cli_textos.t``): igual ao original na Brasil."""

    def __init__(self, *args, **kwargs):
        if isinstance(kwargs.get("description"), str):
            kwargs["description"] = _t(kwargs["description"])
        super().__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        if isinstance(kwargs.get("help"), str):
            kwargs["help"] = _t(kwargs["help"])
        return super().add_argument(*args, **kwargs)


def main() -> None:
    parser = _AnalisadorDaEdicao(description="Triton CLI: simulação, economia, ACV, TOPSIS e automação reproduzível.")
    subparsers = parser.add_subparsers(dest="command", required=True, parser_class=_AnalisadorDaEdicao)
    _adicionar = subparsers.add_parser

    def _adicionar_traduzido(nome, **kwargs):
        if isinstance(kwargs.get("help"), str):
            kwargs["help"] = _t(kwargs["help"])
        return _adicionar(nome, **kwargs)

    subparsers.add_parser = _adicionar_traduzido

    def add_analysis_arguments(command_parser: argparse.ArgumentParser, default_analysis: str) -> None:
        command_parser.add_argument("file", help="Projeto CSV legado, .triton ou JSON estruturado")
        command_parser.add_argument("--analysis", choices=ANALYSES, default=default_analysis)
        command_parser.add_argument("--volume", type=float, help="Força um volume de cisterna inferior (L)")
        command_parser.add_argument("--weights", type=_parse_weights, help="Pesos TOPSIS: técnico,econômico,ambiental")
        command_parser.add_argument("--rainfall", help="Substitui a chuva do projeto por este arquivo")
        command_parser.add_argument("--start-date", help="Data inicial dd/mm/aaaa; necessária para sazonalidade mensal")
        command_parser.add_argument("--set", dest="set_values", action="append", default=[], metavar="CAMPO=VALOR",
                                    help="Sobrescreve campo do projeto; pode ser repetido")
        command_parser.add_argument("--format", choices=FORMATS, default="text")
        command_parser.add_argument("--output", help="Arquivo de saída obrigatório para json/csv/html/xlsx")
        command_parser.add_argument("--weight-sensitivity", type=_positive_int, default=0, metavar="N",
                                    help="Amostra N combinações de pesos TOPSIS e informa a frequência vencedora")
        command_parser.add_argument("--seed", type=int, default=42, help="Semente para análises estocásticas")

    add_analysis_arguments(subparsers.add_parser("run", help="Simula; padrão técnico compatível com o legado"), "technical")
    add_analysis_arguments(subparsers.add_parser("analyze", help="Executa cadeia completa de análises"), "all")
    add_analysis_arguments(subparsers.add_parser("econ", help="Atalho legado para análise econômica"), "economic")

    validate_parser = subparsers.add_parser("validate", help="Valida a estrutura e as premissas de um projeto")
    validate_parser.add_argument("file")
    validate_parser.add_argument("--rainfall")

    init_parser = subparsers.add_parser("init", help="Cria um template .triton estruturado e editável")
    init_parser.add_argument("file", help="Destino .triton")
    init_parser.add_argument("--rainfall", default=serie_de_exemplo_da_edicao(), help="Arquivo de chuva de referência")
    init_parser.add_argument("--embed-rainfall", action="store_true", help="Incorpora a série no .triton")

    catalog_parser = subparsers.add_parser("init-catalog", help="Cria catálogo JSON de premissas ou de climas")
    catalog_parser.add_argument("kind", choices=("premises", "climates"))
    catalog_parser.add_argument("file", help="Destino JSON do catálogo")

    matrix_parser = subparsers.add_parser("matrix", help="Combina premissas de edifício com catálogo climático")
    matrix_parser.add_argument("premises", help="Catálogo JSON com schema triton-premises-catalog")
    matrix_parser.add_argument("climates", help="Catálogo JSON com schema triton-climate-catalog")
    matrix_parser.add_argument("--analysis", choices=ANALYSES, default="all")
    matrix_parser.add_argument("--weights", type=_parse_weights)
    matrix_parser.add_argument("--weight-sensitivity", type=_positive_int, default=0)
    matrix_parser.add_argument("--seed", type=int, default=42)
    matrix_parser.add_argument("--output-dir", default="triton-matriz-resultados")
    matrix_parser.add_argument("--quiet", action="store_true", help="Oculta a barra de progresso e ETA")

    project_matrix_parser = subparsers.add_parser(
        "matrix-projects",
        help="Executa arquivos .triton em lista, pasta de chuva ou matriz fatorial declarada no projeto",
    )
    project_matrix_parser.add_argument("--projects", nargs="+", required=True,
                                       help="Arquivos .triton/.json ou pastas contendo arquivos .triton")
    project_matrix_parser.add_argument("--rainfall-dir",
                                       help="Pasta de séries CSV/TXT/DAT; combina cada projeto com cada série")
    project_matrix_parser.add_argument("--ignore-project-factors", action="store_true",
                                       help="Ignora o bloco cli_factorial dos projetos")
    project_matrix_parser.add_argument("--recursive", action="store_true",
                                       help="Procura projetos e séries também nas subpastas")
    project_matrix_parser.add_argument("--analysis", choices=ANALYSES, default="all")
    project_matrix_parser.add_argument("--weights", type=_parse_weights)
    project_matrix_parser.add_argument("--weight-sensitivity", type=_positive_int, default=0)
    project_matrix_parser.add_argument("--seed", type=int, default=42)
    project_matrix_parser.add_argument("--output-dir", default="triton-matriz-projetos")
    project_matrix_parser.add_argument("--quiet", action="store_true", help="Oculta a barra de progresso e ETA")

    batch_parser = subparsers.add_parser("batch", help="Executa cenários de uma planilha CSV/XLSX")
    batch_parser.add_argument("file", help="Planilha de cenários")
    batch_parser.add_argument("--base", help="Projeto .triton/CSV com parâmetros econômicos e ambientais base")
    batch_parser.add_argument("--analysis", choices=ANALYSES, default="all")
    batch_parser.add_argument("--weights", type=_parse_weights)
    batch_parser.add_argument("--format", choices=FORMATS, default="csv")
    batch_parser.add_argument("--output", help="Arquivo de saída")
    batch_parser.add_argument("--weight-sensitivity", type=_positive_int, default=0)
    batch_parser.add_argument("--seed", type=int, default=42)

    uncertainty_parser = subparsers.add_parser("uncertainty", help="Propaga incertezas por Monte Carlo para uma decisão de volume")
    uncertainty_parser.add_argument("file", help="Projeto CSV, .triton ou JSON")
    uncertainty_parser.add_argument("--analysis", choices=("technical", "economic", "environmental", "all"), default="all")
    uncertainty_parser.add_argument("--volume", type=float, help="Volume analisado; padrão: ótimo técnico do caso-base")
    uncertainty_parser.add_argument("--samples", type=_positive_int, default=200)
    uncertainty_parser.add_argument("--seed", type=int, default=42)
    uncertainty_parser.add_argument("--rainfall-cv", type=float, default=10.0, help="CV percentual da chuva")
    uncertainty_parser.add_argument("--area-cv", type=float, default=0.0, help="CV percentual da área")
    uncertainty_parser.add_argument("--demand-cv", type=float, default=10.0, help="CV percentual da demanda")
    uncertainty_parser.add_argument("--capex-cv", type=float, default=15.0, help="CV percentual de CAPEX")
    uncertainty_parser.add_argument("--weights", type=_parse_weights)
    uncertainty_parser.add_argument("--set", dest="set_values", action="append", default=[], metavar="CAMPO=VALOR")
    uncertainty_parser.add_argument("--format", choices=("text", "json", "csv"), default="text")
    uncertainty_parser.add_argument("--output")

    series_parser = subparsers.add_parser(
        "series-length",
        help="Responde de quantos anos de chuva este projeto precisa (Geraldi e Ghisi)")
    series_parser.add_argument("file", help="Projeto CSV, .triton ou JSON")
    series_parser.add_argument("--max-volume", type=float, default=20000.0,
                               help="Maior volume da grade, em litros")
    series_parser.add_argument("--step", type=float, default=1000.0, help="Passo da grade, em litros")
    series_parser.add_argument("--threshold", type=float, default=1.0,
                               help="Limiar de ganho marginal que define o volume ideal, em %%/m³")
    series_parser.add_argument("--tolerance", type=float, default=2.0,
                               help="Tolerância do potencial, em pontos percentuais")
    series_parser.add_argument("--tolerance-steps", type=int, default=0,
                               help="Tolerância do volume ideal, em passos da grade")
    series_parser.add_argument("--confidence", type=float, default=90.0,
                               help="Frequência mínima de resultados semelhantes, em %%")
    series_parser.add_argument("--windows", type=_positive_int, default=None,
                               help="Janelas sorteadas por comprimento; sem isto, usa todas")
    series_parser.add_argument("--seed", type=int, default=42)
    series_parser.add_argument("--set", dest="set_values", action="append", default=[], metavar="CAMPO=VALOR")
    series_parser.add_argument("--format", choices=("text", "json", "csv"), default="text")
    series_parser.add_argument("--output")

    stochastic_parser = subparsers.add_parser(
        "stochastic-demand",
        help="Sorteia o consumo diário e devolve o desempenho como faixa (Silva e Ghisi)")
    stochastic_parser.add_argument("file", help="Projeto CSV, .triton ou JSON")
    stochastic_parser.add_argument("--volume", type=float,
                                   help="Volume analisado; padrão: ótimo técnico do caso-base")
    stochastic_parser.add_argument("--samples", type=_positive_int, default=100)
    stochastic_parser.add_argument("--daily-cv", type=float, default=20.0,
                                   help="CV do consumo de um dia para o outro, em %%")
    stochastic_parser.add_argument("--level-uncertainty", type=float, default=0.0,
                                   help="Incerteza do nível médio do consumo, em %%; é o que move o resultado")
    stochastic_parser.add_argument("--absence", type=float, default=0.0,
                                   help="Probabilidade de dia sem consumo, em %%")
    stochastic_parser.add_argument("--distribution",
                                   choices=("normal", "lognormal", "uniforme", "triangular"),
                                   default="lognormal")
    stochastic_parser.add_argument("--ideal-volume", action="store_true",
                                   help="Também apura o volume ideal de cada realização")
    stochastic_parser.add_argument("--ideal-volume-samples", type=_positive_int, default=30)
    stochastic_parser.add_argument("--max-volume", type=float, default=20000.0)
    stochastic_parser.add_argument("--step", type=float, default=1000.0)
    stochastic_parser.add_argument("--threshold", type=float, default=1.0)
    stochastic_parser.add_argument("--seed", type=int, default=42)
    stochastic_parser.add_argument("--set", dest="set_values", action="append", default=[], metavar="CAMPO=VALOR")
    stochastic_parser.add_argument("--format", choices=("text", "json"), default="text")
    stochastic_parser.add_argument("--output")

    study_parser = subparsers.add_parser(
        "probabilistic-study", aliases=["stochastic-study"],
        help="Modulação probabilística: refaz o estudo com as premissas escolhidas sorteadas")
    study_parser.add_argument("file", nargs="?", help="Projeto CSV, .triton ou JSON")
    study_parser.add_argument("--samples", type=_positive_int, help="Realizações; padrão: o salvo no projeto ou 1000")
    study_parser.add_argument("--seed", type=int, help="Semente; padrão: a salva no projeto ou 42")
    for opcao, ajuda in (("--per-capita", "consumo per capita, L/hab.dia"), ("--people", "número de pessoas"),
                         ("--non-potable", "fração não potável interna, %%")):
        study_parser.add_argument(opcao, help=f"{_t(f'Distribuição do {ajuda}')}: "
                                              + _t("normal:média:desvio, lognormal:média:desvio, "
                                                   "triangular:mín:moda:máx, uniforme:mín:máx ou fixo"))
    study_parser.add_argument("--var", dest="variables", action="append", default=[], metavar="VARIÁVEL=DISTRIBUIÇÃO",
                              help="Qualquer variável do catálogo (per_capita_l_dia, pessoas, fracao_nao_potavel_pct, "
                                   "demanda_externa_l_dia, area_m2, coef_escoamento, descarte_mm, fator_chuva, "
                                   "fator_tarifa, reajuste_tarifa_pct, tma_pct_mes, fator_investimento, tarifa_energia); "
                                   "pode ser repetida. Ex.: --var fator_chuva=normal:1:0,1")
    study_parser.add_argument("--list-variables", action="store_true", help="Lista o catálogo e sai")
    study_parser.add_argument("--climate-models", metavar="MODELO,MODELO,…",
                              help=(argparse.SUPPRESS if not usa_dados_do_brasil() else "Modelos CLIMBra entre os quais cada realização sorteia a chuva (mesma cidade, "
                                   "cenário e recorte do projeto); «todos» usa os 19; «nenhum» desliga"))
    study_parser.add_argument("--daily-cv", type=float, help="Variação de um dia para o outro, em %% (padrão 0)")
    study_parser.add_argument("--weights", type=_parse_weights)
    study_parser.add_argument("--set", dest="set_values", action="append", default=[], metavar="CAMPO=VALOR")
    study_parser.add_argument("--format", choices=("text", "json", "csv"), default="text")
    study_parser.add_argument("--output")
    study_parser.add_argument("--quiet", action="store_true", help="Oculta o progresso")

    # Estudos da replicação do Brasil (TesteMassivo, estudo de Vaz): só existem na Edição Brasil.
    if usa_dados_do_brasil():
        compare_mass_parser = subparsers.add_parser(
            "compare-mass",
            help="Executa simulação paralela em massa dos 4 casos de reservatórios combinados e compara com TesteMassivo",
        )
        compare_mass_parser.add_argument("--input-dir", help="Pasta com os arquivos de chuva divididos (Triton_future_files_split)")
        compare_mass_parser.add_argument("--reference-dir", help="Pasta com os CSVs consolidados de referência (TesteMassivo)")
        compare_mass_parser.add_argument("--output-dir", help="Pasta para gravar novos resultados e relatório (TesteMassivo/nova_versao)")
        compare_mass_parser.add_argument("--area", type=float, default=60.0, help="Área de captação em m² (padrão Tabela 2: 60)")
        compare_mass_parser.add_argument("--residents", type=int, default=4, help="Número de moradores (padrão Tabela 2: 4)")
        compare_mass_parser.add_argument("--demand", type=float, default=150.0, help="Demanda diária per capita L/hab/dia (padrão Tabela 2: 150)")
        compare_mass_parser.add_argument("--share", type=float, default=30.0, help="Percentual não potável, de 0 a 100: 30 é 30%% (padrão Tabela 2: 30)")
        compare_mass_parser.add_argument("--runoff", type=float, default=0.80, help="Coeficiente de escoamento (padrão Tabela 2: 0.80)")
        compare_mass_parser.add_argument("--discard", type=float, default=2.0, help="Descarte inicial first-flush em mm (padrão Tabela 2: 2.0)")
        compare_mass_parser.add_argument("--workers", "-w", type=int, default=None, help="Número de núcleos de CPU para execução paralela")

        run_vaz_parser = subparsers.add_parser(
            "run-vaz-study",
            help="Executa estudo massivo de tipologias residenciais de Vaz em Parquet com ACV, Financeiro e TOPSIS",
        )
        run_vaz_parser.add_argument("--input-dir", help="Pasta com as 86.716 séries climáticas divididas (TesteMassivo/Triton_vaz_files_split)")
        run_vaz_parser.add_argument("--output-dir", help="Pasta para gravar arquivo Parquet e relatórios (TesteMassivo/estudo_vaz)")
        run_vaz_parser.add_argument("--workers", "-w", type=int, default=None, help="Número de núcleos de CPU para execução paralela")

    args = parser.parse_args()
    try:
        if args.command == "init":
            target = _create_template(args.file, args.rainfall, args.embed_rainfall)
            print(f"{_t('Template .triton criado em:')} {target.resolve()}")
        elif args.command == "init-catalog":
            target = _create_catalog(args.kind, args.file)
            print(f"{_t('Catálogo de')} {args.kind} {_t('criado em:')} {target.resolve()}")
        elif args.command == "matrix":
            _run_matrix(args)
        elif args.command == "matrix-projects":
            _run_project_matrix(args)
        elif args.command == "validate":
            bundle = _load_bundle(args.file)
            if args.rainfall:
                bundle["config"].precip_file = args.rainfall; bundle["precip_data"] = None
            errors = _validate_config(bundle["config"], _get_precipitation(bundle))
            errors.extend(_validate_analysis_config(bundle.get("analysis")))
            if errors:
                raise ValueError("Projeto inválido:\n- " + "\n- ".join(errors))
            print(_t("Projeto válido: estrutura, chuva e premissas essenciais verificadas."))
        elif args.command == "batch":
            _run_batch(args)
        elif args.command == "uncertainty":
            _run_uncertainty(args)
        elif args.command == "series-length":
            _run_series_length(args)
        elif args.command == "stochastic-demand":
            _run_stochastic_demand(args)
        elif args.command in ("probabilistic-study", "stochastic-study"):
            _run_stochastic_study(args)
        elif args.command == "compare-mass" and usa_dados_do_brasil():
            _run_compare_mass(args)
        elif args.command == "run-vaz-study" and usa_dados_do_brasil():
            _run_vaz_study(args)
        else:
            _run_project(args)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        parser.exit(2, f"{_t('Erro:')} {exc}\n")



if __name__ == "__main__":
    main()
