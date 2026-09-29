import pytest
import numpy as np
from netuno.core.topsis import TopsisCandidate
from netuno.core.mcdm_methods import (
    run_vikor,
    run_smaa_analysis,
    run_smaa_vikor,
    VikorResult,
    SmaaResult
)


@pytest.fixture
def sample_candidates():
    return [
        TopsisCandidate(
            lower_tank_vol=1000.0,
            water_saved_m3_yr=80.0,
            vpl_brl=3500.0,
            co2_saved_kg_lifetime=1200.0,
            capex_brl=4000.0,
            upper_tank_vol=500.0,
            technical_threshold_met=True,
            potential_savings_pct=40.0,
            overflow_m3_yr=120.0,
            discounted_payback_years=4.5,
            irr_pct=18.5,
            potable_consumed_m3_yr=120.0
        ),
        TopsisCandidate(
            lower_tank_vol=3000.0,
            water_saved_m3_yr=140.0,
            vpl_brl=6200.0,
            co2_saved_kg_lifetime=2100.0,
            capex_brl=6500.0,
            upper_tank_vol=500.0,
            technical_threshold_met=True,
            potential_savings_pct=70.0,
            overflow_m3_yr=60.0,
            discounted_payback_years=5.2,
            irr_pct=16.0,
            potable_consumed_m3_yr=60.0
        ),
        TopsisCandidate(
            lower_tank_vol=5000.0,
            water_saved_m3_yr=165.0,
            vpl_brl=5800.0,
            co2_saved_kg_lifetime=2500.0,
            capex_brl=8500.0,
            upper_tank_vol=500.0,
            technical_threshold_met=True,
            potential_savings_pct=82.5,
            overflow_m3_yr=35.0,
            discounted_payback_years=6.8,
            irr_pct=13.2,
            potable_consumed_m3_yr=35.0
        )
    ]


def test_run_vikor(sample_candidates):
    res = run_vikor(sample_candidates, weights=(0.333, 0.333, 0.334), v_param=0.5)
    assert isinstance(res, VikorResult)
    assert len(res.q_scores) == len(sample_candidates)
    assert len(res.ranks) == len(sample_candidates)
    assert 0 <= res.best_index < len(sample_candidates)
    assert 1 in res.ranks


def test_run_smaa_vikor(sample_candidates):
    res = run_smaa_vikor(sample_candidates, v_param=0.75, num_samples=1000)
    assert isinstance(res, SmaaResult)
    assert res.engine == "vikor"
    assert res.v_weight == 0.75
    assert len(res.first_rank_acceptabilities) == len(sample_candidates)
    assert np.isclose(np.sum(res.first_rank_acceptabilities), 1.0, atol=0.05)
    assert 0 <= res.best_index < len(sample_candidates)
    assert res.acceptability_matrix.shape == (3, 3)
    assert len(res.confidence_factors) == len(sample_candidates)
    assert res.num_samples == 1000
    assert res.num_simulations == 1000

    # Testa pesos centrais por dimensão (Técnica, Econômica, Ambiental)
    w_t, w_f, w_e = res.get_central_dimension_weights(res.best_index)
    assert np.isclose(w_t + w_f + w_e, 1.0, atol=0.01)
    assert 0.0 <= w_t <= 1.0
    assert 0.0 <= w_f <= 1.0
    assert 0.0 <= w_e <= 1.0


def test_run_smaa_analysis(sample_candidates):
    res = run_smaa_analysis(sample_candidates, num_samples=1000, engine="vikor")
    assert isinstance(res, SmaaResult)
    assert res.engine == "vikor"
    assert len(res.first_rank_acceptabilities) == len(sample_candidates)
    assert np.isclose(np.sum(res.first_rank_acceptabilities), 1.0, atol=0.05)
    assert 0 <= res.best_index < len(sample_candidates)
    assert res.acceptability_matrix.shape == (3, 3)

    res_topsis = run_smaa_analysis(sample_candidates, num_samples=1000, engine="topsis")
    assert res_topsis.engine == "topsis"
    assert len(res_topsis.first_rank_acceptabilities) == len(sample_candidates)


@pytest.mark.parametrize("num_samples", [0, -1, 1.5])
def test_smaa_rejects_invalid_number_of_simulations(sample_candidates, num_samples):
    with pytest.raises(ValueError, match="inteiro positivo"):
        run_smaa_vikor(sample_candidates, num_samples=num_samples)

