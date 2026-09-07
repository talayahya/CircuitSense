"""Reverse-design calculations for simple circuits."""

from __future__ import annotations

from dataclasses import dataclass
from math import log10

import numpy as np

from .formatting import require_positive
from .voltage_divider import analyze_voltage_divider


E12_BASE = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24_BASE = [
    1.0,
    1.1,
    1.2,
    1.3,
    1.5,
    1.6,
    1.8,
    2.0,
    2.2,
    2.4,
    2.7,
    3.0,
    3.3,
    3.6,
    3.9,
    4.3,
    4.7,
    5.1,
    5.6,
    6.2,
    6.8,
    7.5,
    8.2,
    9.1,
]


@dataclass(frozen=True)
class DesignResult:
    target: float
    theoretical: float
    practical: float | None
    achieved: float
    error_percent: float


def nearest_standard_resistor(value: float, series: str = "E12") -> float:
    require_positive("Resistance", value)
    base = E24_BASE if series.upper() == "E24" else E12_BASE
    decade = int(np.floor(log10(value)))
    candidates = []
    for offset in (-1, 0, 1):
        candidates.extend(b * 10 ** (decade + offset) for b in base)
    return min(candidates, key=lambda x: abs(x - value))


def design_voltage_divider(vin: float, desired_vout: float, known_value: float, known_component: str) -> DesignResult:
    require_positive("Vin", vin)
    require_positive("Known resistor", known_value)
    if not 0 < desired_vout < vin:
        raise ValueError("Desired Vout must be between 0 V and Vin.")

    known_component = known_component.upper()
    if known_component == "R2":
        theoretical_r1 = known_value * (vin / desired_vout - 1.0)
        practical = nearest_standard_resistor(theoretical_r1)
        achieved = analyze_voltage_divider(vin, practical, known_value).vout
        theoretical = theoretical_r1
    elif known_component == "R1":
        theoretical_r2 = desired_vout * known_value / (vin - desired_vout)
        practical = nearest_standard_resistor(theoretical_r2)
        achieved = analyze_voltage_divider(vin, known_value, practical).vout
        theoretical = theoretical_r2
    else:
        raise ValueError("Known component must be R1 or R2.")

    return DesignResult(desired_vout, theoretical, practical, achieved, (achieved - desired_vout) / desired_vout * 100.0)


def design_rc_filter(cutoff_frequency: float, known_value: float, known_component: str) -> DesignResult:
    require_positive("Cutoff frequency", cutoff_frequency)
    require_positive("Known component", known_value)
    known_component = known_component.upper()

    if known_component == "C":
        theoretical_r = 1.0 / (2.0 * np.pi * cutoff_frequency * known_value)
        practical = nearest_standard_resistor(theoretical_r)
        achieved_fc = 1.0 / (2.0 * np.pi * practical * known_value)
        theoretical = theoretical_r
    elif known_component == "R":
        theoretical_c = 1.0 / (2.0 * np.pi * cutoff_frequency * known_value)
        practical = None
        achieved_fc = cutoff_frequency
        theoretical = theoretical_c
    else:
        raise ValueError("Known component must be R or C.")

    return DesignResult(cutoff_frequency, theoretical, practical, achieved_fc, (achieved_fc - cutoff_frequency) / cutoff_frequency * 100.0)


def design_rlc_resonance(target_frequency: float, known_value: float, known_component: str) -> DesignResult:
    require_positive("Target frequency", target_frequency)
    require_positive("Known component", known_value)
    known_component = known_component.upper()
    omega_squared = (2.0 * np.pi * target_frequency) ** 2

    if known_component == "C":
        theoretical_l = 1.0 / (omega_squared * known_value)
        achieved = 1.0 / (2.0 * np.pi * np.sqrt(theoretical_l * known_value))
        theoretical = theoretical_l
    elif known_component == "L":
        theoretical_c = 1.0 / (omega_squared * known_value)
        achieved = 1.0 / (2.0 * np.pi * np.sqrt(known_value * theoretical_c))
        theoretical = theoretical_c
    else:
        raise ValueError("Known component must be L or C.")

    return DesignResult(target_frequency, theoretical, None, achieved, (achieved - target_frequency) / target_frequency * 100.0)

