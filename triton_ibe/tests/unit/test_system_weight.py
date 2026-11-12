# -*- coding: utf-8 -*-
"""Testes unitários para a calculadora de peso e cargas estruturais do sistema."""

import pytest
import numpy as np

from triton.core.system_weight import (
    calculate_system_weight,
    calculate_system_weight_from_config,
    ZONE_SUBSOLO,
    ZONE_SUPERIOR,
    ZONE_REDE,
    ComponentWeight,
    SystemWeightResult,
)
from triton.core.lca.environmental import PipeInput, PumpInput
from triton.core.parser import TritonConfig


def test_system_weight_zero_volume():
    res = calculate_system_weight(lower_tank_vol_l=0.0, upper_tank_vol_l=0.0, pipes=[])
    assert res.total_dry_mass_kg == 0.0
    assert res.total_water_mass_kg == 0.0
    assert res.total_operating_mass_kg == 0.0
    assert res.total_operating_weight_kn == 0.0
    assert len(res.components) == 0
    assert len(res.structural_alerts) == 0


def test_system_weight_dry_and_water_loads_pead():
    # 5.000 L cisterna PEAD + 500 L reservatório superior PEAD + bomba 0.5 CV
    res = calculate_system_weight(
        lower_tank_vol_l=5000.0,
        lower_material_key="PEAD",
        upper_tank_vol_l=500.0,
        upper_material_key="PEAD",
        pump_power_cv=0.5,
    )
    # 5.000 L PEAD = 5 * 22 = 110 kg seco; água = 5.000 kg
    # 500 L PEAD = 0.5 * 22 = 11 kg seco; água = 500 kg
    # Bomba 0.5 CV = 10.5 kg seco
    assert res.total_dry_mass_kg > 110.0 + 11.0 + 10.5
    assert res.total_water_mass_kg >= 5500.0
    assert res.total_operating_mass_kg == pytest.approx(res.total_dry_mass_kg + res.total_water_mass_kg, rel=1e-4)
    expected_kn = res.total_operating_mass_kg * 9.80665 / 1000.0
    assert res.total_operating_weight_kn == pytest.approx(expected_kn, rel=1e-3)


def test_system_weight_zones_discrimination():
    res = calculate_system_weight(
        lower_tank_vol_l=5000.0,
        lower_material_key="PEAD",
        upper_tank_vol_l=500.0,
        upper_material_key="PEAD",
        pump_power_cv=0.75,
    )

    # Subsolo deve conter cisterna e motobomba
    assert res.substructure.zone == ZONE_SUBSOLO
    assert res.substructure.dry_mass_kg > 0
    assert res.substructure.water_mass_kg >= 5000.0
    sub_cats = {c.category for c in res.substructure.components}
    assert "cisterna" in sub_cats
    assert "motobomba" in sub_cats

    # Cobertura deve conter reservatório superior
    assert res.superstructure.zone == ZONE_SUPERIOR
    assert res.superstructure.dry_mass_kg > 0
    assert res.superstructure.water_mass_kg >= 500.0
    sup_cats = {c.category for c in res.superstructure.components}
    assert "reservatorio_superior" in sup_cats

    # Rede deve conter tubulações
    assert res.network.zone == ZONE_REDE
    assert res.network.dry_mass_kg > 0
    assert res.network.water_mass_kg > 0
    net_cats = {c.category for c in res.network.components}
    assert "tubulacao" in net_cats

    # A soma das 3 zonas deve ser igual ao total geral
    sum_dry = res.substructure.dry_mass_kg + res.superstructure.dry_mass_kg + res.network.dry_mass_kg
    sum_water = res.substructure.water_mass_kg + res.superstructure.water_mass_kg + res.network.water_mass_kg
    assert res.total_dry_mass_kg == pytest.approx(sum_dry, rel=1e-4)
    assert res.total_water_mass_kg == pytest.approx(sum_water, rel=1e-4)


def test_system_weight_structural_alerts():
    from triton.core.system.system_weight import LIMIAR_COBERTURA_KG, LIMIAR_SUBSOLO_SECO_KG
    # Caixa superior de 1000 L cheia passa do limiar de atenção da cobertura: um alerta.
    res = calculate_system_weight(
        lower_tank_vol_l=3000.0,
        upper_tank_vol_l=1000.0,
        upper_material_key="PEAD",
    )
    assert res.superstructure.total_operating_mass_kg >= LIMIAR_COBERTURA_KG
    assert len(res.structural_alerts) == 1
    # O limiar é do programa, não de norma: nenhum alerta o atribui a uma norma.
    assert "NBR" not in " ".join(res.structural_alerts)

    # Cisterna de concreto de 5000 L (cerca de 6000 kg a seco): peso próprio e material.
    res_conc = calculate_system_weight(
        lower_tank_vol_l=5000.0,
        lower_material_key="CONCRETO",
    )
    assert res_conc.substructure.dry_mass_kg >= LIMIAR_SUBSOLO_SECO_KG
    assert len(res_conc.structural_alerts) == 2

    # Sistema leve, sem caixa superior: nenhum alerta.
    assert calculate_system_weight(lower_tank_vol_l=1000.0, upper_tank_vol_l=0.0).structural_alerts == []


def test_system_weight_from_config():
    cfg = TritonConfig()
    cfg.lower_tank_vol = 4000.0
    cfg.upper_tank_used = 1
    cfg.upper_tank_vol = 500.0

    raw_env = {
        "lower_material_key": "PEAD",
        "upper_material_key": "PEAD",
        "pump": {"power_cv": 0.5},
        "pipes": [
            {"diameter_mm": 100, "length_m": 15.0},
            {"diameter_mm": 32, "length_m": 15.0},
        ],
    }

    res = calculate_system_weight_from_config(cfg, environmental_raw=raw_env)
    assert isinstance(res, SystemWeightResult)
    assert res.total_dry_mass_kg > 0
    assert res.total_water_mass_kg >= 4500.0
    assert res.substructure.water_mass_kg >= 4000.0
    assert res.superstructure.water_mass_kg >= 500.0

    # Conversão para dicionário serializável
    d = res.to_dict()
    assert "total_dry_mass_kg" in d
    assert "substructure" in d
    assert "superstructure" in d
    assert "network" in d
    assert "structural_alerts" in d


def test_material_do_projeto_vale_sem_a_etapa_ambiental():
    """Sem material na etapa ambiental, vale o do projeto (`lower_tank_material`), como na ACV.

    Até a correção, o programa procurava `lower_material_key` na configuração, que não existe,
    e calculava a massa de uma cisterna de concreto como se fosse de polietileno.
    """
    concreto = TritonConfig()
    concreto.lower_tank_material = "CONCRETO"
    pead = TritonConfig()
    pead.lower_tank_material = "PEAD"
    m_conc = calculate_system_weight_from_config(concreto, lower_tank_vol_l=5000.0).substructure.dry_mass_kg
    m_pead = calculate_system_weight_from_config(pead, lower_tank_vol_l=5000.0).substructure.dry_mass_kg
    assert m_conc > 10 * m_pead
    # A etapa ambiental, quando declara o material, prevalece
    m_raw = calculate_system_weight_from_config(
        concreto, lower_tank_vol_l=5000.0, environmental_raw={"lower_material_key": "PEAD"}).substructure.dry_mass_kg
    assert m_raw == pytest.approx(m_pead)
