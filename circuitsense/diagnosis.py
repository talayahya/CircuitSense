"""Rule-based fault diagnosis for voltage dividers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .formatting import require_positive
from .voltage_divider import analyze_voltage_divider


@dataclass(frozen=True)
class Diagnosis:
    expected_vout: float
    measured_vout: float
    absolute_deviation: float
    percent_deviation: float
    confidence: str
    most_likely: str
    alternatives: list[str]
    explanation: str


def diagnose_voltage_divider(vin: float, r1: float, r2: float, measured_vout: float) -> Diagnosis:
    require_positive("Vin", vin)
    result = analyze_voltage_divider(vin, r1, r2)
    expected = result.vout
    deviation = measured_vout - expected
    percent_deviation = deviation / expected * 100.0 if expected != 0 else 0.0
    ratio = measured_vout / vin

    if ratio < 0.08:
        return Diagnosis(expected, measured_vout, deviation, percent_deviation, "High", "R2 short circuit", ["R1 open circuit"], "The output is very close to ground, which matches faults that pull or leave Vout near 0 V.")
    if ratio > 0.92:
        return Diagnosis(expected, measured_vout, deviation, percent_deviation, "High", "R1 short circuit", ["R2 open circuit"], "The output is very close to Vin, which matches faults that remove most of the upper voltage drop.")
    if abs(percent_deviation) <= 5.0:
        return Diagnosis(expected, measured_vout, deviation, percent_deviation, "Low", "Likely normal variation", ["Measurement noise", "Component tolerance"], "The measurement is close to the ideal calculation.")
    if percent_deviation > 5.0:
        return Diagnosis(expected, measured_vout, deviation, percent_deviation, "Medium", "R2 drift high or R1 drift low", ["Measurement error"], "The output is higher than expected, so the divider ratio may have shifted upward.")
    return Diagnosis(expected, measured_vout, deviation, percent_deviation, "Medium", "R1 drift high or R2 drift low", ["Measurement error"], "The output is lower than expected, so the divider ratio may have shifted downward.")


def simulate_measurement_noise(value: float, noise_percent: float, seed: int | None = None) -> float:
    """Apply uniform measurement noise around an ideal voltage."""

    if noise_percent < 0:
        raise ValueError("Noise percentage cannot be negative.")
    if noise_percent == 0:
        return value
    rng = np.random.default_rng(seed)
    span = abs(value) * noise_percent / 100.0
    return float(value + rng.uniform(-span, span))
