"""RC filter calculations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .formatting import require_positive


@dataclass(frozen=True)
class RCFilterResult:
    resistance: float
    capacitance: float
    amplitude: float
    time_constant: float
    cutoff_frequency: float


def rc_summary(resistance: float, capacitance: float, amplitude: float = 1.0) -> RCFilterResult:
    require_positive("Resistance", resistance)
    require_positive("Capacitance", capacitance)
    return RCFilterResult(
        resistance=resistance,
        capacitance=capacitance,
        amplitude=amplitude,
        time_constant=resistance * capacitance,
        cutoff_frequency=1.0 / (2.0 * np.pi * resistance * capacitance),
    )


def frequency_axis(cutoff_frequency: float, points: int = 500) -> np.ndarray:
    require_positive("Cutoff frequency", cutoff_frequency)
    low = max(cutoff_frequency / 100.0, 1e-3)
    high = cutoff_frequency * 100.0
    return np.logspace(np.log10(low), np.log10(high), points)


def low_pass_response(resistance: float, capacitance: float, frequencies: np.ndarray) -> dict[str, np.ndarray]:
    summary = rc_summary(resistance, capacitance)
    omega_rc = 2.0 * np.pi * frequencies * summary.time_constant
    magnitude = 1.0 / np.sqrt(1.0 + omega_rc**2)
    phase = -np.degrees(np.arctan(omega_rc))
    return {
        "frequency": frequencies,
        "magnitude": magnitude,
        "magnitude_db": 20.0 * np.log10(magnitude),
        "phase_deg": phase,
    }


def high_pass_response(resistance: float, capacitance: float, frequencies: np.ndarray) -> dict[str, np.ndarray]:
    summary = rc_summary(resistance, capacitance)
    omega_rc = 2.0 * np.pi * frequencies * summary.time_constant
    magnitude = omega_rc / np.sqrt(1.0 + omega_rc**2)
    phase = 90.0 - np.degrees(np.arctan(omega_rc))
    return {
        "frequency": frequencies,
        "magnitude": magnitude,
        "magnitude_db": 20.0 * np.log10(np.maximum(magnitude, 1e-15)),
        "phase_deg": phase,
    }


def low_pass_step_response(
    resistance: float,
    capacitance: float,
    amplitude: float = 1.0,
    points: int = 300,
) -> dict[str, np.ndarray]:
    summary = rc_summary(resistance, capacitance, amplitude)
    time = np.linspace(0.0, 5.0 * summary.time_constant, points)
    output = amplitude * (1.0 - np.exp(-time / summary.time_constant))
    return {"time": time, "output": output}

