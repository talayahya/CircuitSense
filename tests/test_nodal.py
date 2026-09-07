import pytest

from circuitsense.nodal import GROUND, Resistor, solve_resistive_network


def test_one_node_divider_network():
    result = solve_resistive_network(
        ["A"],
        {"VIN": 12.0},
        [Resistor("R1", "VIN", "A", 1000.0), Resistor("R2", "A", GROUND, 2000.0)],
    )
    assert result.node_voltages["A"] == pytest.approx(8.0)


def test_two_node_default_style_network():
    result = solve_resistive_network(
        ["A", "B"],
        {"VIN": 12.0},
        [
            Resistor("R1", "VIN", "A", 1000.0),
            Resistor("R2", "A", GROUND, 2000.0),
            Resistor("R3", "A", "B", 3000.0),
            Resistor("R4", "B", GROUND, 4000.0),
        ],
    )
    assert result.node_voltages["A"] == pytest.approx(7.3043478261)
    assert result.node_voltages["B"] == pytest.approx(4.1739130435)
    assert len(result.branches) == 4


def test_singular_network_reports_helpful_error():
    with pytest.raises(ValueError, match="cannot be solved"):
        solve_resistive_network(["A"], {"VIN": 12.0}, [Resistor("R1", "VIN", GROUND, 1000.0)])


def test_invalid_node_is_rejected():
    with pytest.raises(ValueError, match="not defined"):
        solve_resistive_network(["A"], {"VIN": 12.0}, [Resistor("R1", "VIN", "B", 1000.0)])
