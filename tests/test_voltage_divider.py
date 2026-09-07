from circuitsense.voltage_divider import analyze_voltage_divider


def test_voltage_divider_known_example():
    result = analyze_voltage_divider(12.0, 1000.0, 2000.0)
    assert result.current == 0.004
    assert result.vout == 8.0
    assert result.total_power == 0.048


def test_voltage_divider_rejects_zero_resistor():
    try:
        analyze_voltage_divider(12.0, 0.0, 2000.0)
    except ValueError as exc:
        assert "R1" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

