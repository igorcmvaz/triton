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
