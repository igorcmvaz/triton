"""Sincronização de parâmetros da ACV com os dados explícitos do projeto.

Materiais nunca são inferidos a partir do preço: custo e composição física são
premissas independentes. A sincronização usa as escolhas persistidas no
``NetunoConfig`` e recorre a padrões seguros somente quando elas não existem.
"""

import math
from typing import Dict, Optional, Tuple

from netuno.core.environmental import (
    MATERIAL_PRESETS,
    PIPE_EMISSION_FACTORS_PER_METER,
    PUMP_EMBEDDED_CO2,
)
from netuno.core.parser import NetunoConfig
from netuno.core.pump_energy import compute_annual_pump_energy, nearest_pump_cv
from netuno.core.simulation import SingleTankSimulationResult


def infer_tank_material(volume_l: float, total_cost: float, default: str = "PEAD") -> str:
    """
    Heurística legada, mantida apenas para importadores que a chamam de forma
    explícita. Não é usada pela sincronização automática da ACV.

    Infere material provável do reservatório a partir do custo unitário (R$/L).
    Referência: PEAD prefabricado ~0,4–0,8; concreto in loco ~1,2+; inox ~2,0+.
    """
    if volume_l <= 0 or total_cost <= 0:
        return default
    cost_per_l = total_cost / volume_l
    if cost_per_l >= 2.0:
        return "ACO_INOX"
    if cost_per_l >= 1.2:
        return "CONCRETO"
    if cost_per_l >= 0.65:
        return "FIBRA"
    return "PEAD"


def estimate_pipe_lengths_m(
    capture_area_m2: float,
    upper_used: bool,
    lower_vol_l: float,
    pump_suc_dn: int = 32,
    pump_rec_dn: int = 25,
) -> Dict[int, float]:
    """
    Estima comprimentos de tubulação PVC por DN com base na área de captação,
    porte do sistema e especificações da motobomba (5m sucção e 20m recalque).
    """
    area = max(1.0, capture_area_m2)
    lower_vol = max(0.0, lower_vol_l)

    capture_run = max(8.0, min(40.0, 4.0 * math.sqrt(area) + 6.0))
    distribution_dn75 = 0.0
    main_dn100 = max(10.0, min(30.0, capture_run * 0.6 + lower_vol / 2000.0))
    large_dn150 = 6.0 if lower_vol >= 10000 else 0.0

    res = {
        20: 0.0, 25: 0.0, 32: 0.0, 40: 0.0, 50: 0.0, 60: 0.0, 75: round(distribution_dn75, 1),
        85: 0.0, 100: round(main_dn100, 1), 110: 0.0, 150: round(large_dn150, 1),
    }
    if upper_used:
        res[int(pump_rec_dn)] = res.get(int(pump_rec_dn), 0.0) + 20.0
        res[int(pump_suc_dn)] = res.get(int(pump_suc_dn), 0.0) + 5.0
    return res


def material_preset_values(material_key: str) -> Tuple[float, float]:
    """Retorna (densidade kg/m³ útil, CO2 kg/kg) do preset de material."""
    preset = MATERIAL_PRESETS.get(material_key, MATERIAL_PRESETS["PEAD"])
    return preset.material_density_kg_per_m3_tank, preset.co2_factor_kg_per_kg


def pipe_co2_factor(diameter_mm: int) -> float:
    return PIPE_EMISSION_FACTORS_PER_METER.get(diameter_mm, 3.92)


def pump_embodied_co2(power_cv: float) -> float:
    key = nearest_pump_cv(power_cv)
    return PUMP_EMBEDDED_CO2.get(key, 18.0)


def build_sync_snapshot(
    config: NetunoConfig,
    sim_result: Optional[SingleTankSimulationResult],
    *,
    upper_used: bool = True,
    upper_vol_l: float = 500.0,
    lower_vol_l: float = 5000.0,
    capture_area_m2: float = 100.0,
) -> Dict[str, object]:
    """
    Monta dicionário de valores sugeridos para a ACV a partir do projeto.
    """
    pump_energy = compute_annual_pump_energy(config, sim_result, upper_tank_used=upper_used)
    power_cv = pump_energy.pump_power_cv if pump_energy.pump_power_cv > 0 else 0.5

    lower_material = str(getattr(config, "lower_tank_material", "PEAD") or "PEAD").upper()
    upper_material = str(getattr(config, "upper_tank_material", "PEAD") or "PEAD").upper()
    aliases = {"PRFV": "FIBRA", "FIBERGLASS": "FIBRA", "INOX": "ACO_INOX"}
    lower_material = aliases.get(lower_material, lower_material)
    upper_material = aliases.get(upper_material, upper_material)
    if lower_material not in MATERIAL_PRESETS:
        lower_material = "PEAD"
    if upper_material not in MATERIAL_PRESETS:
        upper_material = "PEAD"

    lower_density, lower_co2 = material_preset_values(lower_material)
    upper_density, upper_co2 = material_preset_values(upper_material)
    if hasattr(config, "get_pipe_lengths_dict"):
        pipes = config.get_pipe_lengths_dict()
    elif hasattr(config, "pipes_list") and config.pipes_list:
        pipes = {20: 0.0, 25: 0.0, 32: 0.0, 40: 0.0, 50: 0.0, 60: 0.0, 75: 0.0, 85: 0.0, 100: 0.0, 110: 0.0, 150: 0.0}
        for d, l in config.pipes_list:
            pipes[int(d)] = float(l)
    else:
        pipes = estimate_pipe_lengths_m(capture_area_m2, upper_used, lower_vol_l)

    specific_kwh = pump_energy.specific_kwh_per_m3
    if specific_kwh <= 0 and sim_result and sim_result.annual_pluvial_consumed_m3 > 0:
        ann_m3 = sim_result.annual_pluvial_consumed_m3
        if pump_energy.annual_kwh > 0:
            specific_kwh = pump_energy.annual_kwh / ann_m3

    return {
        "lower_material_key": lower_material,
        "lower_density": lower_density,
        "lower_co2_kg": lower_co2,
        "upper_material_key": upper_material,
        "upper_density": upper_density,
        "upper_co2_kg": upper_co2,
        "upper_used": upper_used,
        "upper_vol_l": upper_vol_l,
        "pump_cv": power_cv,
        "pump_co2": pump_embodied_co2(power_cv),
        "pump_count": max(1, config.pump_count),
        "specific_kwh_per_m3": specific_kwh,
        "annual_pump_kwh": pump_energy.annual_kwh,
        "lifespan_years": config.analysis_period_years,
        "pipes_m": pipes,
        "pipe_co2": {dn: pipe_co2_factor(dn) for dn in pipes},
        "annual_pumped_m3": pump_energy.annual_pumped_m3,
        "annual_cycles": pump_energy.annual_cycles,
    }
