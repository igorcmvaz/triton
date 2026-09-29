import pytest
from netuno.core.water_quality import (
    calculate_first_flush_washoff,
    size_etap,
    WATER_QUALITY_CLASSES,
    EtapSizingResult,
    FirstFlushAnalysis
)


def test_first_flush_washoff_defaults():
    res = calculate_first_flush_washoff(
        discard_mm=2.0,
        roof_area_m2=200.0,
        annual_precipitation_mm=1400.0,
        roof_runoff_coeff=0.85
    )
    assert isinstance(res, FirstFlushAnalysis)
    assert res.discard_mm == 2.0
    assert res.annual_discard_volume_m3 > 0
    assert 0 < res.removal_coarse_solids_pct <= 100.0
    assert res.estimated_raw_turbidity_ntu > res.estimated_post_discard_turbidity_ntu


def test_first_flush_zero_discard():
    res = calculate_first_flush_washoff(
        discard_mm=0.0,
        roof_area_m2=150.0,
        annual_precipitation_mm=1200.0
    )
    assert res.annual_discard_volume_m3 == 0.0
    assert res.removal_coarse_solids_pct == 0.0


def test_water_quality_classes_nbr15527():
    assert "classe_1" in WATER_QUALITY_CLASSES
    assert "classe_2" in WATER_QUALITY_CLASSES
    assert "classe_3" in WATER_QUALITY_CLASSES
    assert "classe_4" in WATER_QUALITY_CLASSES

    c1 = WATER_QUALITY_CLASSES["classe_1"]
    assert c1.turbidez_max_ntu <= 5.0
    assert c1.exige_desinfeccao is True


def test_size_etap():
    res = size_etap(
        target_class_id="classe_1",
        annual_pluvial_consumed_m3=300.0,
        roof_area_m2=250.0,
        disinfection_choice="cloro",
        include_polishing_filter=True
    )
    assert isinstance(res, EtapSizingResult)
    assert res.total_etap_capex > 0
    assert res.total_etap_annual_opex > 0
    assert res.total_etap_co2e_kg_yr >= 0
    assert res.annual_chlorine_kg > 0


def test_size_first_flush_system_small_diverter():
    from netuno.core.water_quality import size_first_flush_system, FirstFlushSizingResult
    # 1.0 mm em 100 m² = 100 Litros
    res = size_first_flush_system(discard_mm=1.0, roof_area_m2=100.0)
    assert isinstance(res, FirstFlushSizingResult)
    assert res.diverter_volume_liters == 100.0
    assert "PVC" in res.diverter_tank_type
    assert res.leaf_filter_capex > 0
    assert res.diverter_tank_capex > 0
    assert res.first_flush_total_capex == res.leaf_filter_capex + res.diverter_tank_capex
    assert res.first_flush_embodied_co2_kg > 0
    assert res.first_flush_annual_opex > 0


def test_size_first_flush_system_large_diverter():
    from netuno.core.water_quality import size_first_flush_system
    # 2.0 mm em 500 m² = 1000 Litros
    res = size_first_flush_system(discard_mm=2.0, roof_area_m2=500.0)
    assert res.diverter_volume_liters == 1000.0
    assert "PEAD" in res.diverter_tank_type
    assert res.first_flush_total_capex > 0
    assert res.first_flush_embodied_co2_kg > 0


def test_size_first_flush_system_zero():
    from netuno.core.water_quality import size_first_flush_system
    res = size_first_flush_system(discard_mm=0.0, roof_area_m2=100.0)
    assert res.diverter_volume_liters == 0.0
    assert res.first_flush_total_capex == 0.0
    assert res.first_flush_embodied_co2_kg == 0.0


def test_size_etap_with_first_flush_integration():
    from netuno.core.water_quality import size_etap
    # Sem descarte
    res_sem = size_etap(
        target_class_id="classe_1",
        annual_pluvial_consumed_m3=120.0,
        roof_area_m2=100.0,
        discard_mm=1.0,
        include_first_flush=False,
    )
    # Com descarte
    res_com = size_etap(
        target_class_id="classe_1",
        annual_pluvial_consumed_m3=120.0,
        roof_area_m2=100.0,
        discard_mm=1.0,
        include_first_flush=True,
    )
    assert res_com.first_flush is not None
    assert res_com.first_flush_diverter_vol_l == 100.0
    assert res_com.first_flush_capex > 0
    assert res_com.total_etap_capex == pytest.approx(res_sem.total_etap_capex + res_com.first_flush_capex)

