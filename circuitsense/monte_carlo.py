"""Monte Carlo tolerance simulations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .formatting import require_positive


@dataclass(frozen=True)
class MonteCarloResult:
    nominal: float
    samples: np.ndarray
    mean: float
    minimum: float
    maximum: float
    std_dev: float
    max_abs_deviation: float
    percent_spread: float


def _summarise(nominal: float, samples: np.ndarray) -> MonteCarloResult:
    return MonteCarloResult(
        nominal=nominal,
        samples=samples,
        mean=float(np.mean(samples)),
        minimum=float(np.min(samples)),
        maximum=float(np.max(samples)),
        std_dev=float(np.std(samples, ddof=0)),
        max_abs_deviation=float(np.max(np.abs(samples - nominal))),
        percent_spread=float((np.max(samples) - np.min(samples)) / nominal * 100.0) if nominal else 0.0,
    )


def voltage_divider_tolerance(
    vin: float,
    r1: float,
    r2: float,
    tolerance_percent: float,
    samples: int,
    seed: int | None = None,
) -> MonteCarloResult:
    require_positive("R1", r1)
    require_positive("R2", r2)
    require_positive("Samples", samples)
    rng = np.random.default_rng(seed)
    tol = tolerance_percent / 100.0
    r1_values = rng.uniform(r1 * (1.0 - tol), r1 * (1.0 + tol), samples)
    r2_values = rng.uniform(r2 * (1.0 - tol), r2 * (1.0 + tol), samples)
    outputs = vin * r2_values / (r1_values + r2_values)
    nominal = vin * r2 / (r1 + r2)
    return _summarise(nominal, outputs)


def rc_filter_tolerance(
    resistance: float,
    capacitance: float,
    tolerance_percent: float,
    samples: int,
    seed: int | None = None,
) -> MonteCarloResult:
    require_positive("Resistance", resistance)
    require_positive("Capacitance", capacitance)
    require_positive("Samples", samples)
    rng = np.random.default_rng(seed)
    tol = tolerance_percent / 100.0
    r_values = rng.uniform(resistance * (1.0 - tol), resistance * (1.0 + tol), samples)
    c_values = rng.uniform(capacitance * (1.0 - tol), capacitance * (1.0 + tol), samples)
    cutoffs = 1.0 / (2.0 * np.pi * r_values * c_values)
    nominal = 1.0 / (2.0 * np.pi * resistance * capacitance)
    return _summarise(nominal, cutoffs)

