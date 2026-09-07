import numpy as np
import pytest

from circuitsense.rlc import rlc_summary, series_rlc_response


def test_rlc_resonant_frequency():
    result = rlc_summary(100.0, 10e-3, 100e-9)
    expected = 1.0 / (2.0 * np.pi * np.sqrt(10e-3 * 100e-9))
    assert result.resonant_frequency == pytest.approx(expected)


def test_rlc_current_peaks_near_resonance():
    result = rlc_summary(100.0, 10e-3, 100e-9, 1.0)
    response = series_rlc_response(100.0, 10e-3, 100e-9, 1.0, np.array([result.resonant_frequency]))
    assert response["impedance"][0] == pytest.approx(100.0)
    assert response["current"][0] == pytest.approx(0.01)

