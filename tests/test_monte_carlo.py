import pytest

from circuitsense.monte_carlo import rc_filter_tolerance, voltage_divider_tolerance


def test_voltage_divider_monte_carlo_sample_count_and_seed():
    a = voltage_divider_tolerance(12.0, 1000.0, 2000.0, 5.0, 100, seed=7)
    b = voltage_divider_tolerance(12.0, 1000.0, 2000.0, 5.0, 100, seed=7)
    assert len(a.samples) == 100
    assert a.samples.tolist() == b.samples.tolist()
    assert a.mean == pytest.approx(8.0, rel=0.03)


def test_rc_filter_monte_carlo_sample_count_and_range():
    result = rc_filter_tolerance(1000.0, 1e-6, 10.0, 500, seed=3)
    assert len(result.samples) == 500
    assert result.minimum < result.nominal < result.maximum
    assert result.percent_spread > 0

