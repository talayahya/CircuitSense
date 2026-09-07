from circuitsense.diagnosis import diagnose_voltage_divider, simulate_measurement_noise


def test_near_zero_voltage_diagnosis():
    result = diagnose_voltage_divider(12.0, 1000.0, 2000.0, 0.087)
    assert result.confidence == "High"
    assert result.most_likely == "R2 short circuit"


def test_near_vin_voltage_diagnosis():
    result = diagnose_voltage_divider(12.0, 1000.0, 2000.0, 11.8)
    assert result.confidence == "High"
    assert result.most_likely == "R1 short circuit"


def test_small_deviation_is_normal_variation():
    result = diagnose_voltage_divider(12.0, 1000.0, 2000.0, 8.1)
    assert result.most_likely == "Likely normal variation"


def test_measurement_noise_is_reproducible_and_bounded():
    value = simulate_measurement_noise(8.0, 1.0, seed=10)
    assert 7.92 <= value <= 8.08
    assert value == simulate_measurement_noise(8.0, 1.0, seed=10)
