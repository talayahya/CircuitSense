"""Engineering unit conversion and display helpers."""

from __future__ import annotations

from dataclasses import dataclass


PREFIXES = {
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,
    "": 1.0,
    "k": 1e3,
    "M": 1e6,
}


@dataclass(frozen=True)
class UnitOption:
    label: str
    multiplier: float


RESISTANCE_UNITS = [
    UnitOption("ohm", 1.0),
    UnitOption("kohm", 1e3),
    UnitOption("Mohm", 1e6),
]
CAPACITANCE_UNITS = [
    UnitOption("pF", 1e-12),
    UnitOption("nF", 1e-9),
    UnitOption("uF", 1e-6),
    UnitOption("mF", 1e-3),
    UnitOption("F", 1.0),
]
INDUCTANCE_UNITS = [
    UnitOption("uH", 1e-6),
    UnitOption("mH", 1e-3),
    UnitOption("H", 1.0),
]
VOLTAGE_UNITS = [UnitOption("mV", 1e-3), UnitOption("V", 1.0)]


def to_si(value: float, multiplier: float) -> float:
    return float(value) * float(multiplier)


def require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def require_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")


def format_engineering(value: float, unit: str, precision: int = 3) -> str:
    """Format a value using a simple engineering-scale prefix."""

    if value == 0:
        return f"0 {unit}"

    abs_value = abs(value)
    if unit == "ohm":
        scales = [(1e6, "Mohm"), (1e3, "kohm"), (1.0, "ohm")]
    elif unit == "F":
        scales = [(1e-3, "mF"), (1e-6, "uF"), (1e-9, "nF"), (1e-12, "pF")]
    elif unit == "H":
        scales = [(1.0, "H"), (1e-3, "mH"), (1e-6, "uH")]
    elif unit == "A":
        scales = [(1.0, "A"), (1e-3, "mA"), (1e-6, "uA"), (1e-9, "nA")]
    elif unit == "Hz":
        scales = [(1e6, "MHz"), (1e3, "kHz"), (1.0, "Hz")]
    elif unit == "V":
        scales = [(1.0, "V"), (1e-3, "mV")]
    elif unit == "W":
        scales = [(1.0, "W"), (1e-3, "mW"), (1e-6, "uW")]
    else:
        scales = [(1.0, unit)]

    for scale, label in scales:
        if abs_value >= scale or scale == scales[-1][0]:
            display = value / scale
            return f"{display:.{precision}g} {label}"
    return f"{value:.{precision}g} {unit}"


def percent(value: float, precision: int = 2) -> str:
    return f"{value:.{precision}f}%"

