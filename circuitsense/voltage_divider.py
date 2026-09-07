"""Voltage divider analysis."""

from __future__ import annotations

from dataclasses import dataclass

from .formatting import require_positive


@dataclass(frozen=True)
class VoltageDividerResult:
    vin: float
    r1: float
    r2: float
    total_resistance: float
    current: float
    v_r1: float
    v_r2: float
    vout: float
    p_r1: float
    p_r2: float
    total_power: float
    output_percent: float


def analyze_voltage_divider(vin: float, r1: float, r2: float) -> VoltageDividerResult:
    require_positive("R1", r1)
    require_positive("R2", r2)

    total = r1 + r2
    current = vin / total
    v_r1 = current * r1
    v_r2 = current * r2
    p_r1 = current**2 * r1
    p_r2 = current**2 * r2

    return VoltageDividerResult(
        vin=vin,
        r1=r1,
        r2=r2,
        total_resistance=total,
        current=current,
        v_r1=v_r1,
        v_r2=v_r2,
        vout=v_r2,
        p_r1=p_r1,
        p_r2=p_r2,
        total_power=p_r1 + p_r2,
        output_percent=(v_r2 / vin * 100.0) if vin != 0 else 0.0,
    )

