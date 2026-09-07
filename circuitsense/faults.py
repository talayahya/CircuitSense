"""Idealised fault models for simple circuits."""

from __future__ import annotations

from dataclasses import dataclass

from .filters import rc_summary
from .voltage_divider import VoltageDividerResult, analyze_voltage_divider


@dataclass(frozen=True)
class DividerFaultResult:
    fault: str
    healthy: VoltageDividerResult
    faulty_vout: float
    faulty_current: float
    explanation: str


@dataclass(frozen=True)
class RCFaultResult:
    fault: str
    healthy_cutoff: float
    faulty_cutoff: float | None
    healthy_tau: float
    faulty_tau: float | None
    explanation: str


def voltage_divider_fault(vin: float, r1: float, r2: float, fault: str) -> DividerFaultResult:
    healthy = analyze_voltage_divider(vin, r1, r2)
    f = fault.lower()

    if f == "r1 open":
        return DividerFaultResult(fault, healthy, 0.0, 0.0, "R1 open removes the source path, so Vout is pulled to ground through R2.")
    if f == "r2 open":
        return DividerFaultResult(fault, healthy, vin, 0.0, "With an ideal high-impedance measurement, R2 open lets Vout rise toward Vin.")
    if f == "r1 short":
        return DividerFaultResult(fault, healthy, vin, vin / r2, "R1 short connects Vout almost directly to the source.")
    if f == "r2 short":
        return DividerFaultResult(fault, healthy, 0.0, vin / r1, "R2 short connects Vout directly to ground.")

    drift_map = {
        "r1 drift +10%": (r1 * 1.10, r2),
        "r1 drift +25%": (r1 * 1.25, r2),
        "r1 drift +50%": (r1 * 1.50, r2),
        "r1 drift -10%": (r1 * 0.90, r2),
        "r1 drift -25%": (r1 * 0.75, r2),
        "r2 drift +10%": (r1, r2 * 1.10),
        "r2 drift +25%": (r1, r2 * 1.25),
        "r2 drift +50%": (r1, r2 * 1.50),
        "r2 drift -10%": (r1, r2 * 0.90),
        "r2 drift -25%": (r1, r2 * 0.75),
    }
    if f not in drift_map:
        raise ValueError("Unsupported voltage divider fault.")

    faulty = analyze_voltage_divider(vin, *drift_map[f])
    return DividerFaultResult(fault, healthy, faulty.vout, faulty.current, "A drift fault changes the divider ratio and shifts the measured output voltage.")


def rc_low_pass_fault(resistance: float, capacitance: float, fault: str) -> RCFaultResult:
    healthy = rc_summary(resistance, capacitance)
    f = fault.lower()
    if f == "capacitor open":
        return RCFaultResult(fault, healthy.cutoff_frequency, None, healthy.time_constant, None, "The filtering path to ground is removed in this simplified model.")
    if f == "capacitor short":
        return RCFaultResult(fault, healthy.cutoff_frequency, None, healthy.time_constant, None, "The output node is effectively shorted to ground.")
    if f == "resistor drift +25%":
        faulty = rc_summary(resistance * 1.25, capacitance)
    elif f == "resistor drift -25%":
        faulty = rc_summary(resistance * 0.75, capacitance)
    elif f == "capacitor drift +25%":
        faulty = rc_summary(resistance, capacitance * 1.25)
    elif f == "capacitor drift -25%":
        faulty = rc_summary(resistance, capacitance * 0.75)
    else:
        raise ValueError("Unsupported RC low-pass fault.")
    return RCFaultResult(fault, healthy.cutoff_frequency, faulty.cutoff_frequency, healthy.time_constant, faulty.time_constant, "A component drift changes RC, so the cutoff frequency moves.")

