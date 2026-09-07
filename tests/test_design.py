import pytest

from circuitsense.design import design_rc_filter, design_rlc_resonance, design_voltage_divider, nearest_standard_resistor


def test_nearest_standard_resistor():
    assert nearest_standard_resistor(3180.0) == pytest.approx(3300.0)


def test_voltage_divider_design_known_r2():
    result = design_voltage_divider(12.0, 5.0, 10000.0, "R2")
    assert result.theoretical == pytest.approx(14000.0)
    assert result.practical == pytest.approx(15000.0)
    assert result.achieved == pytest.approx(4.8)


def test_rc_filter_design_known_capacitor():
    result = design_rc_filter(500.0, 100e-9, "C")
    assert result.theoretical == pytest.approx(3183.09886, rel=1e-5)
    assert result.practical == pytest.approx(3300.0)
    assert result.achieved == pytest.approx(482.2877, rel=1e-4)


def test_rlc_resonance_design_known_capacitor():
    result = design_rlc_resonance(1000.0, 100e-9, "C")
    assert result.achieved == pytest.approx(1000.0)

