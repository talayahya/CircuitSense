import numpy as np
import pytest

from circuitsense.filters import high_pass_response, low_pass_response, low_pass_step_response, rc_summary


def test_rc_cutoff_frequency():
    result = rc_summary(1000.0, 1e-6)
    assert result.cutoff_frequency == pytest.approx(159.154943, rel=1e-6)
    assert result.time_constant == pytest.approx(0.001)


def test_low_pass_cutoff_is_minus_3db():
    fc = rc_summary(1000.0, 1e-6).cutoff_frequency
    response = low_pass_response(1000.0, 1e-6, np.array([fc]))
    assert response["magnitude_db"][0] == pytest.approx(-3.0103, rel=1e-3)


def test_high_pass_cutoff_is_minus_3db():
    fc = rc_summary(1000.0, 1e-6).cutoff_frequency
    response = high_pass_response(1000.0, 1e-6, np.array([fc]))
    assert response["magnitude_db"][0] == pytest.approx(-3.0103, rel=1e-3)


def test_low_pass_step_approaches_input():
    step = low_pass_step_response(1000.0, 1e-6, 5.0)
    assert step["output"][-1] == pytest.approx(5.0 * (1 - np.exp(-5)), rel=1e-6)

