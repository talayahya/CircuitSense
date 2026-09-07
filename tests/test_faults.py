import pytest

from circuitsense.faults import rc_low_pass_fault, voltage_divider_fault


def test_divider_r2_short_fault():
    result = voltage_divider_fault(12.0, 1000.0, 2000.0, "R2 short")
    assert result.faulty_vout == 0.0
    assert result.faulty_current == pytest.approx(0.012)


def test_divider_r2_open_fault():
    result = voltage_divider_fault(12.0, 1000.0, 2000.0, "R2 open")
    assert result.faulty_vout == 12.0


def test_rc_drift_changes_cutoff():
    result = rc_low_pass_fault(1000.0, 1e-6, "resistor drift +25%")
    assert result.faulty_cutoff < result.healthy_cutoff

