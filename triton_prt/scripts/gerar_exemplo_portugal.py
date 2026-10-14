# -*- coding: utf-8 -*-
"""Gera o projeto de demonstração da Edição Portugal: o tutorial do manual levado a Lisboa.

A edificação é a do tutorial (``manual/gerar_tabelas.py``: 150 m² de telhado, quatro
moradores, 150 L/hab·dia, 28% não potável), para que o resultado se compare com o de
Florianópolis. Muda o que é português:

- chuva: base E-OBS por concelho (Lisboa, normal 1991–2020); o arquivo guarda a referência
  da série, e o programa a recompõe da base ao abrir;
- tarifa: o tarifário transcrito de Lisboa (EPAL + Câmara Municipal), com o saneamento por
  escalões sobre 90% do volume (``triton/data/portugal_tarifarios.json``);
- custos: zerados, como em todo projeto novo fora da Brasil — o investimento em euros é o
  que o utilizador informa (etapa 5), e sem ele a análise mostra só a economia na fatura.

    python scripts/gerar_exemplo_portugal.py
"""

from __future__ import annotations

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "manual"))

from gerar_tabelas import TUTORIAL  # noqa: E402

from triton.core import base_climatica_portugal as pt  # noqa: E402
from triton.core import tarifarios_portugal as tarifas  # noqa: E402
from triton.core.edition import neutralizar_para_a_internacional  # noqa: E402
from triton.core.parser import TritonConfig, export_triton_json, serie_da_climbra  # noqa: E402

DESTINO = os.path.join(RAIZ, "examples", "portugal", "lisboa_tutorial_eobs.triton")


def projeto():
    cfg = TritonConfig()
    neutralizar_para_a_internacional(cfg)
    cfg.project_name = "Demonstração Portugal - moradia em Lisboa (E-OBS 1991-2020)"
    cfg.area = TUTORIAL["area"]
    cfg.runoff_coeff = TUTORIAL["runoff_coeff"]
    cfg.discard = TUTORIAL["discard_mm"]
    cfg.discard_mode = TUTORIAL["discard_mode"]
    cfg.residents_count = TUTORIAL["moradores"]
    cfg.demand_value = TUTORIAL["per_capita"]
    cfg.rainwater_share = TUTORIAL["rainwater_share"]
    cfg.first_flush_system_enabled = True
    # Varredura de volumes, como o capítulo do tutorial: a curva é o que se mostra.
    cfg.lower_tank_mode = 1
    cfg.lower_tank_max = 20000.0
    cfg.lower_tank_step = 1000.0
    cfg.delta_ideal = 1.0
    cfg.supply_arrangement = "pressurizacao"
    cfg.upper_tank_used = 0
    cfg.upper_tank_vol = 0.0
    cfg.pump_count = 1
    # Chuva: referência à base E-OBS.
    cfg.climate_source_mode = "national_db"
    cfg.climate_city_uf, cfg.climate_city_name = pt.DISTRITO_PADRAO, pt.CONCELHO_PADRAO
    cfg.climate_model, cfg.climate_scenario = pt.MODELO_EOBS, pt.CENARIO_EOBS
    cfg.climate_start_date, cfg.climate_end_date = pt.INICIO_PADRAO, pt.FIM_PADRAO
    cfg.start_date = pt.INICIO_PADRAO
    cfg.precip_file = ""
    # Tarifa: o tarifário transcrito de Lisboa.
    assert tarifas.aplicar("Lisboa", cfg)
    cfg.elec_city_uf, cfg.elec_city_name = cfg.tariff_city_uf, cfg.tariff_city_name
    estado = {"project": {"source_mode": "national_db", "climate_uf": pt.DISTRITO_PADRAO,
                          "climate_city": pt.CONCELHO_PADRAO, "climate_model": pt.MODELO_EOBS,
                          "climate_scenario": pt.CENARIO_EOBS, "start_date": pt.INICIO_PADRAO,
                          "end_date": pt.FIM_PADRAO}}
    return cfg, serie_da_climbra(cfg), estado


def main():
    cfg, chuva, estado = projeto()
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    export_triton_json(cfg, DESTINO, precip_data=chuva, ui_state=estado)
    print(f"{DESTINO}: {len(chuva)} dias, {chuva.sum() / 30:.0f} mm/ano")


if __name__ == "__main__":
    main()
