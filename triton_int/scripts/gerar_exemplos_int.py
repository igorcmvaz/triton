# -*- coding: utf-8 -*-
"""Generates the three example projects of the International Edition.

New York, London and Cape Town. The building is the manual's tutorial house (150 m² of roof,
four residents, 150 L/person.day, 28% non-potable), the same in the three cities, so the
results compare. What changes is the place:

- rainfall: the 1991-2020 daily series in ``data/rainfall`` (Open-Meteo / ERA5 reanalysis),
  embedded in the project;
- water and sewer tariff: the official 2026 figures below, each with its source and its date
  (see ``examples/LEIA.md``);
- currency: US$, GBP, ZAR, stored in the project (``ui_state.stage3``).

Costs of works, pump and maintenance are NOT invented: they stay at zero, and the project says
so. The user enters their own (stage 5); without them the analysis shows only the bill saving.

    python scripts/gerar_exemplos_int.py

Reproducible: same inputs, same files (apart from the creation timestamp).
"""

from __future__ import annotations

import os
import sys
from decimal import Decimal

os.environ["TRITON_EDITION"] = "INT"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from triton.core.edition import configuracao_da_edicao  # noqa: E402
from triton.core.parser import export_triton_json, load_precipitation  # noqa: E402

PASTA_EXEMPLOS = os.path.join(RAIZ, "examples")
PASTA_CHUVA = os.path.join(RAIZ, "data", "rainfall")

#: The manual's tutorial house (manual/gerar_tabelas.py, TUTORIAL), copied here so that this script
#: does not depend on the manual sources.
TUTORIAL = {
    "area": 150.0,            # m² of roof, horizontal projection
    "runoff_coeff": 0.85,     # clay tile
    "discard_mm": 2.0,
    "discard_mode": 1,        # every rain event
    "residents": 4,
    "per_capita": 150.0,      # L/person.day
    "rainwater_share": 0.28,  # toilet flushing and outdoor uses
}

M3_POR_CCF = Decimal("2.8316847")        # 1 CCF = 100 ft³ = 2.8316847 m³
DIAS_POR_MES = Decimal("30.4375")                # 365.25 / 12, the engine's month
SEM_TETO = 999999.0

AVISO_DE_CUSTOS = ("Costs of works, pump and maintenance are not set: enter your own "
                   "(stage 5). Until then the analysis shows only the saving on the bill.")


def _r(x, casas=6) -> float:
    return float(round(Decimal(x), casas))


def _nova_york():
    agua_m3 = Decimal("5.35") / M3_POR_CCF          # US$ per m³
    minima_mes = Decimal("0.49") * DIAS_POR_MES     # US$ per month
    return dict(
        pasta="new_york", arquivo="new_york.triton", serie="NewYork.csv",
        nome="Example - tutorial house in New York (ERA5 1991-2020) [costs to be entered by the user]",
        cidade="New York", pais="USA", moeda="USD",
        tarifa_cidade="New York City", tarifa_pais="USA",
        entidade="NYC Water Board / NYC DEP", vigencia="01/07/2026",
        fonte=("NYC Water Board and NYC Department of Environmental Protection (DEP), "
               "Water and Sewer Rates FY2027, in force from 1 July 2026: water US$ 5.35 per CCF "
               "(100 ft3 = 2.8316847 m3), sewer 159% of the water charge, minimum charge US$ 0.49 per day."),
        campos=dict(
            water_tariffs=[(0.0, 0.0, _r(minima_mes), -3), (0.0, SEM_TETO, _r(agua_m3), 1)],
            sewage_mode=1, sewage_rate=159.0, sewage_tariffs=[], sewage_volume_factor=1.0,
            water_tax_fixed=0.0, water_tax_var=0.0),
        hipoteses=[
            "US$ 5.35 per CCF converted at 1 CCF = 2.8316847 m3 (US$ 1.8894 per m3).",
            "Sewer = 159% of the water charge (percentage of the water parcel, mode 1).",
            "The US$ 0.49 per day minimum charge is entered as a monthly floor on the water parcel "
            "(US$ 0.49 x 30.4375 days = US$ 14.91 per month); it does not bind at the example's consumption.",
        ])


def _londres():
    return dict(
        pasta="london", arquivo="london.triton", serie="London.csv",
        nome="Example - tutorial house in London (ERA5 1991-2020) [costs to be entered by the user]",
        cidade="London", pais="United Kingdom", moeda="GBP",
        tarifa_cidade="London", tarifa_pais="United Kingdom",
        entidade="Thames Water", vigencia="01/04/2026",
        fonte=("Thames Water, charges 2026-27, metered household: water GBP 2.7346 per m3 and "
               "wastewater GBP 1.4721 per m3; standing charges GBP 66.87 per year (water) and "
               "GBP 128.13 per year (wastewater; GBP 80.43 with the surface-water drainage rebate). "
               "No VAT on household water and sewerage."),
        campos=dict(
            water_tariffs=[(0.0, 0.0, _r(Decimal("66.87") / 12), -1), (0.0, SEM_TETO, 2.7346, 1)],
            sewage_mode=2, sewage_rate=1.4721, sewage_tariffs=[], sewage_volume_factor=1.0,
            water_tax_fixed=_r(Decimal("128.13") / 12), water_tax_var=0.0),
        hipoteses=[
            "Water standing charge GBP 66.87/12 per month on the water parcel; wastewater standing "
            "charge GBP 128.13/12 per month as a fixed amount (it cancels in the saving).",
            "Wastewater charged on 100% of the metered volume (no return-to-sewer allowance applied: "
            "none was supplied). The GBP 80.43 rebate case is not applied.",
            "Charging year 2026-27 taken to start on 1 April 2026 (inferred; confirm).",
        ])


def _cidade_do_cabo():
    return dict(
        pasta="cape_town", arquivo="cape_town.triton", serie="CapeTown.csv",
        nome="Example - tutorial house in Cape Town (ERA5 1991-2020) [costs to be entered by the user]",
        cidade="Cape Town", pais="South Africa", moeda="ZAR",
        tarifa_cidade="Cape Town", tarifa_pais="South Africa",
        entidade="City of Cape Town", vigencia="01/07/2026",
        fonte=("City of Cape Town, Tariffs 2026/27, domestic (non-indigent), no restrictions, "
               "VAT included, R/kl: water 0-6 kl 25.05; 6-10.5 kl 34.42; 10.5-35 kl 54.60; >35 kl 109.98. "
               "Sanitation: 70% of the water consumption, up to 35 kl: 0-4.2 kl 18.28; 4.2-7.35 kl 25.11; "
               "7.35-24.5 kl 42.18; 24.5-35 kl 73.91."),
        campos=dict(
            water_tariffs=[(0.0, 6.0, 25.05, 1), (6.0, 10.5, 34.42, 1),
                           (10.5, 35.0, 54.60, 1), (35.0, SEM_TETO, 109.98, 1)],
            sewage_mode=3, sewage_rate=0.0,
            sewage_tariffs=[(0.0, 4.2, 18.28), (4.2, 7.35, 25.11), (7.35, 24.5, 42.18), (24.5, 35.0, 73.91)],
            sewage_volume_factor=0.7, water_tax_fixed=0.0, water_tax_var=0.0),
        hipoteses=[
            "1 kl = 1 m3; prices already include VAT (no extra tax is added).",
            "Sanitation volume = 70% of the water consumed, charged by the four steps up to 35 kl "
            "of sanitation volume; above that nothing more is charged (the cap is read from "
            "'up to 35 kl'; confirm).",
            "No fixed monthly charge was supplied, so none is entered.",
            "Tariff year 2026/27 taken to start on 1 July 2026 (inferred; confirm).",
        ])


CIDADES = (_nova_york, _londres, _cidade_do_cabo)


def projeto(c: dict):
    """The configuration, the rainfall series, the interface state and the notes of one city."""
    cfg = configuracao_da_edicao()
    t = TUTORIAL
    cfg.project_name = c["nome"]
    cfg.area = t["area"]
    cfg.runoff_coeff = t["runoff_coeff"]
    cfg.discard = t["discard_mm"]
    cfg.discard_mode = t["discard_mode"]
    cfg.residents_count = t["residents"]
    cfg.demand_value = t["per_capita"]
    cfg.rainwater_share = t["rainwater_share"]
    cfg.first_flush_system_enabled = True
    # Volume sweep, as in the tutorial chapter: the curve is what is shown.
    cfg.lower_tank_mode = 1
    cfg.lower_tank_max = 20000.0
    cfg.lower_tank_step = 1000.0
    cfg.delta_ideal = 1.0
    cfg.supply_arrangement = "pressurizacao"
    cfg.pressurizer_model = "personalizado"   # no brand: the user enters the booster's data
    cfg.upper_tank_used = 0
    cfg.upper_tank_vol = 0.0
    cfg.pump_count = 1
    # Rainfall: the series file of the edition, embedded in the project.
    cfg.climate_source_mode = "custom_file"
    cfg.climate_city_name, cfg.climate_city_uf = c["cidade"], c["pais"]
    cfg.climate_model, cfg.climate_scenario = "ERA5 reanalysis (Open-Meteo)", "Reanalysis"
    cfg.climate_start_date, cfg.climate_end_date = "01/01/1991", "31/12/2020"
    cfg.start_date = "01/01/1991"
    cfg.precip_file = c["serie"]
    chuva = load_precipitation(os.path.join(PASTA_CHUVA, c["serie"]))
    # Tariff.
    for campo, valor in c["campos"].items():
        setattr(cfg, campo, valor)
    cfg.tariff_city_name, cfg.tariff_city_uf = c["tarifa_cidade"], c["tarifa_pais"]
    cfg.elec_city_name, cfg.elec_city_uf = c["tarifa_cidade"], c["tarifa_pais"]
    cfg.tariff_vigencia = c["vigencia"]
    cfg.tariff_category = "residencial"
    cfg.data_base_estudo = "14/10/2026"   # date the tariffs were collected: keeps the file reproducible
    cfg.created_at = "14/10/2026 00:00"
    estado = {
        "project": {"source_mode": "custom_file", "start_date": "01/01/1991", "end_date": "31/12/2020"},
        "stage3": {"currency_code": c["moeda"]},
    }
    notas = {
        "example": c["nome"],
        "costs": AVISO_DE_CUSTOS,
        "tariff_entity": c["entidade"],
        "tariff_validity": c["vigencia"],
        "tariff_source": c["fonte"],
        "tariff_assumptions": c["hipoteses"],
        "tariffs_collected_on": "14/10/2026",
        "rainfall": f"{c['serie']}: Open-Meteo / ERA5 reanalysis, 1991-2020, 10,958 days (data/rainfall/LEIA.md).",
    }
    return cfg, chuva, estado, notas


def _curto(caminho: str) -> str:
    """O caminho relativo à raiz, ou o absoluto se estiver noutra unidade (pasta temporária)."""
    try:
        return os.path.relpath(caminho, RAIZ)
    except ValueError:
        return caminho


def gerar(destino: str = PASTA_EXEMPLOS):
    os.makedirs(destino, exist_ok=True)
    feitos = []
    for fabrica in CIDADES:
        c = fabrica()
        cfg, chuva, estado, notas = projeto(c)
        caminho = os.path.join(destino, c["arquivo"])
        export_triton_json(cfg, caminho, precip_data=chuva, ui_state=estado, analysis=notas)
        print(f"{_curto(caminho)}: {len(chuva)} days, {chuva.sum() / 30:.0f} mm/year, {c['moeda']}")
        feitos.append(caminho)
    return feitos


if __name__ == "__main__":
    gerar()
