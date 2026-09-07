"""Series RLC resonance calculations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .formatting import require_positive


@dataclass(frozen=True)
class RLCResult:
    resistance: float
    inductance: float
    capacitance: float
    amplitude: float
    resonant_frequency: float
    quality_factor: float
    bandwidth: float


def rlc_summary(resistance: float, inductance: float, capacitance: float, amplitude: float = 1.0) -> RLCResult:
    require_positive("Resistance", resistance)
    require_positive("Inductance", inductance)
    require_positive("Capacitance", capacitance)
    f0 = 1.0 / (2.0 * np.pi * np.sqrt(inductance * capacitance))
    q = (1.0 / resistance) * np.sqrt(inductance / capacitance)
    bandwidth = f0 / q if q > 0 else float("inf")
    return RLCResult(resistance, inductance, capacitance, amplitude, f0, q, bandwidth)


def rlc_frequency_axis(resonant_frequency: float, points: int = 600) -> np.ndarray:
    low = max(resonant_frequency / 20.0, 1e-3)
    high = resonant_frequency * 20.0
    return np.logspace(np.log10(low), np.log10(high), points)


def series_rlc_response(
    resistance: float,
    inductance: float,
    capacitance: float,
    amplitude: float,
    frequencies: np.ndarray,
) -> dict[str, np.ndarray]:
    summary = rlc_summary(resistance, inductance, capacitance, amplitude)
    omega = 2.0 * np.pi * frequencies
    xl = omega * inductance
    xc = 1.0 / (omega * capacitance)
    reactance = xl - xc
    impedance = np.sqrt(resistance**2 + reactance**2)
    current = amplitude / impedance
    phase = np.degrees(np.arctan2(reactance, resistance))
    return {
        "frequency": frequencies,
        "xl": xl,
        "xc": xc,
        "impedance": impedance,
        "current": current,
        "phase_deg": phase,
        "resonant_frequency": np.full_like(frequencies, summary.resonant_frequency),
    }

