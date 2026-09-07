"""Markdown report generation."""

from __future__ import annotations

from datetime import datetime


DISCLAIMER = (
    "CircuitSense uses simplified idealised circuit models and is intended for "
    "educational and engineering exploration rather than safety-critical electrical design."
)


def markdown_report(title: str, circuit_type: str, inputs: dict[str, str], results: dict[str, str], notes: str = "") -> str:
    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"## Circuit Type",
        circuit_type,
        "",
        "## Inputs",
    ]
    lines.extend(f"- {key}: {value}" for key, value in inputs.items())
    lines.extend(["", "## Calculated Results"])
    lines.extend(f"- {key}: {value}" for key, value in results.items())
    if notes:
        lines.extend(["", "## Notes", notes])
    lines.extend(["", "## Model Limitation", DISCLAIMER, ""])
    return "\n".join(lines)

