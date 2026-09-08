import numpy as np
import pytest

from netuno.core.topsis import TopsisCandidate, calculate_topsis_scores


def candidate(volume, potential, overflow, vpl, payback, irr, lifecycle_co2, potable):
    return TopsisCandidate(
        lower_tank_vol=volume,
        water_saved_m3_yr=100.0 - potable,
        vpl_brl=vpl,
        co2_saved_kg_lifetime=-lifecycle_co2,
        potential_savings_pct=potential,
        overflow_m3_yr=overflow,
        discounted_payback_years=payback,
        irr_pct=irr,
        potable_consumed_m3_yr=potable,
    )


def test_topsis_uses_all_seven_requested_criteria():
    candidates = [
        candidate(2000, 45, 22, 1000, 9, 8, 800, 55),
        candidate(5000, 70, 12, 4000, 5, 15, 500, 30),
        candidate(10000, 82, 5, 3500, 7, 12, 650, 18),
    ]
    result = calculate_topsis_scores(candidates)

    assert result.decision_matrix.shape == (3, 7)
    assert result.criterion_gap_to_best.shape == (3, 7)
    assert result.criterion_weights.sum() == pytest.approx(1.0)
    assert len(result.criterion_keys) == 7
    assert result.rankings[result.best_index] == 1
    assert np.all((result.scores >= 0) & (result.scores <= 1))


def test_topsis_cost_and_benefit_directions_are_correct():
    # Cada coluna tem seu ótimo em uma linha conhecida.
    candidates = [
        candidate(1000, 90, 30, 10, 9, 3, 900, 70),
        candidate(2000, 70, 5, 20, 3, 8, 400, 20),
        candidate(3000, 80, 15, 30, 6, 12, 700, 40),
    ]
    result = calculate_topsis_scores(candidates)

    expected_best_rows = [0, 1, 2, 1, 2, 1, 1]
    for column, row in enumerate(expected_best_rows):
        assert result.criterion_gap_to_best[row, column] == pytest.approx(0.0)
        assert result.criterion_proximity_to_best[row, column] == pytest.approx(1.0)


def test_three_axis_weights_are_distributed_without_changing_axis_totals():
    result = calculate_topsis_scores(
        [candidate(1000, 50, 10, 10, 5, 8, 300, 50)],
        weights=(0.2, 0.5, 0.3),
    )
    assert result.criterion_weights[:2].sum() == pytest.approx(0.2)
    assert result.criterion_weights[2:5].sum() == pytest.approx(0.5)
    assert result.criterion_weights[5:].sum() == pytest.approx(0.3)


def test_seven_explicit_weights_are_supported():
    weights = (1, 2, 3, 4, 5, 6, 7)
    result = calculate_topsis_scores(
        [candidate(1000, 50, 10, 10, 5, 8, 300, 50)],
        weights=weights,
    )
    assert result.criterion_weights == pytest.approx(np.asarray(weights) / sum(weights))


def test_no_discounted_payback_is_worse_than_any_observed_return():
    candidates = [
        candidate(1000, 50, 10, 10, None, 8, 300, 50),
        candidate(2000, 50, 10, 10, 20, 8, 300, 50),
    ]
    result = calculate_topsis_scores(candidates, weights=(0, 0, 0, 1, 0, 0, 0))
    assert result.best_index == 1
    assert result.decision_matrix[0, 3] > result.decision_matrix[1, 3]


def test_topsis_single_candidate_and_identical_candidates_are_stable():
    one = candidate(5000, 70, 10, 1000, 5, 10, 500, 30)
    result = calculate_topsis_scores([one])
    assert result.best_index == 0
    assert result.scores[0] == 1.0

    tied = calculate_topsis_scores([one, candidate(2000, 70, 10, 1000, 5, 10, 500, 30)])
    assert tied.scores == pytest.approx([0.5, 0.5])
    assert tied.best_candidate.lower_tank_vol == 2000


def test_topsis_empty_and_invalid_inputs():
    assert calculate_topsis_scores([]) is None
    valid = candidate(1000, 50, 10, 10, 5, 8, 300, 50)
    with pytest.raises(ValueError):
        calculate_topsis_scores([valid], weights=(-1.0, 1.0, 1.0))
    with pytest.raises(ValueError):
        calculate_topsis_scores([valid], weights=(0.0, 0.0, 0.0))
    with pytest.raises(ValueError):
        calculate_topsis_scores([valid], weights=(1.0, 2.0))
    invalid = candidate(1000, np.nan, 10, 10, 5, 8, 300, 50)
    with pytest.raises(ValueError, match="technical_potential_pct"):
        calculate_topsis_scores([invalid])


def test_topsis_translation_is_invariant_to_column_origin():
    base = [
        candidate(1000, 10, 30, -100, 9, -3, 30, 70),
        candidate(2000, 15, 20, -50, 6, -2, 20, 50),
        candidate(3000, 20, 10, 10, 3, -1, 10, 30),
    ]
    shifted = [
        candidate(
            c.lower_tank_vol,
            c.potential_savings_pct + 100,
            c.overflow_m3_yr + 100,
            c.vpl_brl + 5000,
            c.discounted_payback_years + 10,
            c.irr_pct + 30,
            c.lifecycle_co2_kg + 300,
            c.potable_consumed_m3_yr + 1000,
        )
        for c in base
    ]
    assert calculate_topsis_scores(base).scores == pytest.approx(calculate_topsis_scores(shifted).scores)


def test_optima_indices_follow_potential_vpl_and_minimum_lifecycle_co2():
    candidates = [
        candidate(1000, 90, 30, 10, 9, 3, 900, 70),
        candidate(2000, 70, 5, 30, 3, 8, 400, 20),
        candidate(3000, 80, 15, 20, 6, 12, 700, 40),
    ]
    result = calculate_topsis_scores(candidates)
    assert result.technical_best_index == 0
    assert result.financial_best_index == 1
    assert result.environmental_best_index == 1


def test_financial_best_prefers_shorter_payback_over_higher_vpl():
    # Candidato 0 tem VPL muito maior (50k vs 30k), mas Payback mais longo (6 anos vs 2 anos)
    # Pela diretriz do usuário, o ótimo econômico padrão deve ser o de menor payback (Candidato 1)
    c_high_vpl_long_pb = candidate(5000, 85, 10, 50000, 6.0, 10, 500, 30)
    c_low_vpl_short_pb = candidate(2000, 65, 5, 30000, 2.0, 18, 200, 15)
    candidates = [c_high_vpl_long_pb, c_low_vpl_short_pb]

    res = calculate_topsis_scores(candidates)
    assert res.financial_best_index == 1


def test_topsis_proximity_chart_renders_seven_criterion_series(qapp):
    from netuno.ui.charts import TOPSISProximityChart

    candidates = [
        candidate(3000, 80, 15, 20, 6, 12, 700, 40),
        candidate(1000, 90, 30, 10, 9, 3, 900, 70),
        candidate(2000, 70, 5, 30, 3, 8, 400, 20),
    ]
    result = calculate_topsis_scores(candidates)
    chart = TOPSISProximityChart()
    chart.update_chart(result)

    ax = chart.figure.axes[0]
    # Sete critérios, além da linha vertical que destaca o vencedor.
    assert len(ax.lines) == 8
    for line in ax.lines[:7]:
        assert list(line.get_xdata()) == [1000.0, 2000.0, 3000.0]
        assert max(line.get_ydata()) == pytest.approx(100.0)
    chart.close()


def test_zero_liter_is_never_financial_or_technical_optimum():
    # Candidato 0 é 0 L (baseline sem cisterna, payback 0, capex 0)
    # Candidato 1 é 2500 L (payback 3.2 anos, marcado como ótimo técnico do threshold)
    # Candidato 2 é 5000 L (payback 4.5 anos)
    c_zero = candidate(0, 0, 0, 0, 0.0, 0, 0, 100)
    c_2500 = candidate(2500, 60, 5, 20000, 3.2, 15, 200, 40)
    c_2500.is_technical_optimum = True
    c_5000 = candidate(5000, 80, 15, 25000, 4.5, 12, 400, 20)

    candidates = [c_zero, c_2500, c_5000]
    res = calculate_topsis_scores(candidates)

    # 0 L NUNCA pode ser o ótimo econômico ou técnico
    assert res.financial_best_index == 1
    assert candidates[res.financial_best_index].lower_tank_vol == 2500.0
    assert res.technical_best_index == 1
    assert candidates[res.technical_best_index].lower_tank_vol == 2500.0
