"""Small nodal-analysis solver for resistive networks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .formatting import require_positive


GROUND = "GND"


@dataclass(frozen=True)
class Resistor:
    name: str
    node_a: str
    node_b: str
    resistance: float


@dataclass(frozen=True)
class BranchResult:
    name: str
    node_a: str
    node_b: str
    resistance: float
    voltage_a: float
    voltage_b: float
    voltage_drop_a_to_b: float
    current_a_to_b: float
    power: float


@dataclass(frozen=True)
class NodalResult:
    unknown_nodes: list[str]
    fixed_voltages: dict[str, float]
    matrix_a: np.ndarray
    vector_b: np.ndarray
    node_voltages: dict[str, float]
    branches: list[BranchResult]


def _node_voltage(node: str, solved: dict[str, float], fixed: dict[str, float]) -> float:
    if node == GROUND:
        return 0.0
    if node in fixed:
        return fixed[node]
    return solved[node]


def solve_resistive_network(
    unknown_nodes: list[str],
    fixed_voltages: dict[str, float],
    resistors: list[Resistor],
) -> NodalResult:
    """Solve a ground-referenced resistive network with KCL and Ax=b."""

    if not unknown_nodes:
        raise ValueError("At least one unknown node is required.")
    if GROUND in unknown_nodes:
        raise ValueError("Ground cannot be an unknown node.")
    if len(set(unknown_nodes)) != len(unknown_nodes):
        raise ValueError("Unknown node names must be unique.")
    if GROUND in fixed_voltages:
        raise ValueError("Ground is fixed at 0 V and should not be listed.")
    if not fixed_voltages:
        raise ValueError("At least one fixed voltage source is required.")
    if not resistors:
        raise ValueError("At least one resistor is required.")

    for resistor in resistors:
        require_positive(resistor.name, resistor.resistance)

    unknown_set = set(unknown_nodes)
    fixed_set = set(fixed_voltages)
    valid_nodes = unknown_set | fixed_set | {GROUND}
    for resistor in resistors:
        if resistor.node_a not in valid_nodes or resistor.node_b not in valid_nodes:
            raise ValueError(f"{resistor.name} references a node that is not defined.")
        if resistor.node_a == resistor.node_b:
            raise ValueError(f"{resistor.name} connects a node to itself.")

    index = {node: i for i, node in enumerate(unknown_nodes)}
    matrix = np.zeros((len(unknown_nodes), len(unknown_nodes)), dtype=float)
    rhs = np.zeros(len(unknown_nodes), dtype=float)

    for resistor in resistors:
        g = 1.0 / resistor.resistance
        a_unknown = resistor.node_a in unknown_set
        b_unknown = resistor.node_b in unknown_set

        if a_unknown:
            i = index[resistor.node_a]
            matrix[i, i] += g
            if b_unknown:
                matrix[i, index[resistor.node_b]] -= g
            elif resistor.node_b != GROUND:
                rhs[i] += g * fixed_voltages[resistor.node_b]

        if b_unknown:
            i = index[resistor.node_b]
            matrix[i, i] += g
            if a_unknown:
                matrix[i, index[resistor.node_a]] -= g
            elif resistor.node_a != GROUND:
                rhs[i] += g * fixed_voltages[resistor.node_a]

    try:
        solution = np.linalg.solve(matrix, rhs)
    except np.linalg.LinAlgError as exc:
        raise ValueError(
            "The resistor network cannot be solved. Check for disconnected nodes or missing paths to a source/ground."
        ) from exc

    solved = {node: float(solution[index[node]]) for node in unknown_nodes}
    node_voltages = {**{GROUND: 0.0}, **fixed_voltages, **solved}
    branch_results: list[BranchResult] = []

    for resistor in resistors:
        va = _node_voltage(resistor.node_a, solved, fixed_voltages)
        vb = _node_voltage(resistor.node_b, solved, fixed_voltages)
        drop = va - vb
        current = drop / resistor.resistance
        branch_results.append(
            BranchResult(
                name=resistor.name,
                node_a=resistor.node_a,
                node_b=resistor.node_b,
                resistance=resistor.resistance,
                voltage_a=va,
                voltage_b=vb,
                voltage_drop_a_to_b=drop,
                current_a_to_b=current,
                power=current**2 * resistor.resistance,
            )
        )

    return NodalResult(
        unknown_nodes=list(unknown_nodes),
        fixed_voltages=dict(fixed_voltages),
        matrix_a=matrix,
        vector_b=rhs,
        node_voltages=node_voltages,
        branches=branch_results,
    )


def default_network() -> tuple[list[str], dict[str, float], list[Resistor]]:
    return (
        ["A", "B"],
        {"VIN": 12.0},
        [
            Resistor("R1", "VIN", "A", 1000.0),
            Resistor("R2", "A", GROUND, 2000.0),
            Resistor("R3", "A", "B", 3000.0),
            Resistor("R4", "B", GROUND, 4000.0),
        ],
    )

