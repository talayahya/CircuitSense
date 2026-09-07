"""CircuitSense Streamlit application."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from numpy.random import default_rng

from circuitsense.design import design_rc_filter, design_rlc_resonance, design_voltage_divider
from circuitsense.diagnosis import diagnose_voltage_divider, simulate_measurement_noise
from circuitsense.faults import rc_low_pass_fault, voltage_divider_fault
from circuitsense.filters import frequency_axis, high_pass_response, low_pass_response, low_pass_step_response, rc_summary
from circuitsense.formatting import (
    CAPACITANCE_UNITS,
    INDUCTANCE_UNITS,
    RESISTANCE_UNITS,
    format_engineering,
    percent,
    to_si,
)
from circuitsense.monte_carlo import rc_filter_tolerance, voltage_divider_tolerance
from circuitsense.nodal import GROUND, Resistor, default_network, solve_resistive_network
from circuitsense.plotting import bode_figure, healthy_faulty_bar, monte_carlo_histogram, phase_figure, rlc_figures, step_figure
from circuitsense.reports import markdown_report
from circuitsense.rlc import rlc_frequency_axis, rlc_summary, series_rlc_response
from circuitsense.schematics import ASCII_SCHEMATICS, rc_high_pass_svg, rc_low_pass_svg, rlc_svg, voltage_divider_svg
from circuitsense.voltage_divider import analyze_voltage_divider


st.set_page_config(page_title="CircuitSense", page_icon="CS", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 8px;
        padding: 14px 16px;
        background: rgba(128,128,128,.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def unit_input(label: str, default: float, units, default_unit: str | None = None) -> float:
    unit_labels = [unit.label for unit in units]
    default_index = unit_labels.index(default_unit) if default_unit in unit_labels else 0
    col1, col2 = st.columns([2, 1])
    with col1:
        value = st.number_input(label, min_value=0.0, value=default, step=max(default / 20.0, 0.001))
    with col2:
        unit = st.selectbox("Unit", units, index=default_index, format_func=lambda u: u.label, key=f"{label}-unit")
    return to_si(value, unit.multiplier)


def render_schematic(svg: str | None, fallback: str) -> None:
    if svg:
        st.image(svg)
    else:
        st.code(fallback)


def results_table(items: dict[str, str]) -> None:
    st.dataframe(pd.DataFrame(items.items(), columns=["Quantity", "Value"]), hide_index=True, use_container_width=True)


def overview() -> None:
    st.title("CircuitSense")
    st.subheader("Interactive Circuit Analysis, Design & Fault Diagnosis")
    st.write(
        "A Python engineering workstation for analysing simple circuits, solving resistive networks, modelling frequency response, "
        "testing component faults and exploring tolerance variation."
    )
    cols = st.columns(5)
    cards = [
        ("Circuit Analysis", "Voltages, currents, power and frequency response."),
        ("Network Solver", "Nodal analysis with matrix equations."),
        ("Circuit Design", "Reverse-calculate component values from targets."),
        ("Fault Diagnostics", "Compare healthy and faulty behaviour."),
        ("Monte Carlo", "Estimate the effect of component tolerance."),
    ]
    for col, (title, body) in zip(cols, cards):
        col.metric(title, body)
    st.info("CircuitSense uses idealised circuit models for engineering education and software-based analysis.")


def voltage_divider_workspace() -> None:
    st.header("Voltage Divider")
    vin = st.number_input("Vin (V)", value=12.0, step=1.0)
    r1 = unit_input("R1", 1.0, RESISTANCE_UNITS, default_unit="kohm")
    r2 = unit_input("R2", 2.0, RESISTANCE_UNITS, default_unit="kohm")
    result = analyze_voltage_divider(vin, r1, r2)
    render_schematic(voltage_divider_svg(), ASCII_SCHEMATICS["divider"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vout", format_engineering(result.vout, "V"))
    c2.metric("Current", format_engineering(result.current, "A"))
    c3.metric("Total resistance", format_engineering(result.total_resistance, "ohm"))
    c4.metric("Output ratio", percent(result.output_percent))
    table = {
        "Voltage across R1": format_engineering(result.v_r1, "V"),
        "Voltage across R2": format_engineering(result.v_r2, "V"),
        "Power in R1": format_engineering(result.p_r1, "W"),
        "Power in R2": format_engineering(result.p_r2, "W"),
        "Total power": format_engineering(result.total_power, "W"),
    }
    results_table(table)
    with st.expander("Equations"):
        st.latex(r"I = \frac{V_{in}}{R_1 + R_2}")
        st.latex(r"V_{out} = V_{in}\frac{R_2}{R_1 + R_2}")

    report = markdown_report(
        "CircuitSense Analysis Report",
        "Voltage Divider",
        {"Vin": format_engineering(vin, "V"), "R1": format_engineering(r1, "ohm"), "R2": format_engineering(r2, "ohm")},
        {"Vout": format_engineering(result.vout, "V"), "Current": format_engineering(result.current, "A")},
    )
    st.download_button("Export Markdown report", report, file_name="circuitsense_voltage_divider_report.md")


def nodal_workspace() -> None:
    st.header("Resistive Network Solver")
    unknown_nodes, fixed, resistors = default_network()
    st.write("Example network: a 12 V source feeds two unknown nodes through four resistors.")
    result = solve_resistive_network(unknown_nodes, fixed, resistors)
    c1, c2 = st.columns(2)
    for node in unknown_nodes:
        c1.metric(f"Node {node}", format_engineering(result.node_voltages[node], "V"))
    branch_rows = [
        {
            "Resistor": b.name,
            "Connection": f"{b.node_a} to {b.node_b}",
            "Current A->B": format_engineering(b.current_a_to_b, "A"),
            "Power": format_engineering(b.power, "W"),
        }
        for b in result.branches
    ]
    c2.dataframe(pd.DataFrame(branch_rows), hide_index=True, use_container_width=True)
    with st.expander("How the matrix is constructed"):
        st.write("Each unknown node gets one KCL equation. Resistors add conductance terms, where G = 1/R.")
        st.write("Matrix A")
        st.dataframe(pd.DataFrame(result.matrix_a, index=unknown_nodes, columns=unknown_nodes))
        st.write("Vector b")
        st.dataframe(pd.DataFrame({"b": result.vector_b}, index=unknown_nodes))


def rc_workspace(kind: str) -> None:
    title = "RC Low-Pass Filter" if kind == "low" else "RC High-Pass Filter"
    st.header(title)
    resistance = unit_input("Resistance", 1.0, RESISTANCE_UNITS)
    capacitance = unit_input("Capacitance", 1.0, CAPACITANCE_UNITS)
    amplitude = st.number_input("Input amplitude (V)", value=1.0, min_value=0.0, step=0.5)
    summary = rc_summary(resistance, capacitance, amplitude)
    render_schematic(rc_low_pass_svg() if kind == "low" else rc_high_pass_svg(), ASCII_SCHEMATICS["lowpass" if kind == "low" else "highpass"])
    c1, c2 = st.columns(2)
    c1.metric("Time constant", format_engineering(summary.time_constant, "s"))
    c2.metric("Cutoff frequency", format_engineering(summary.cutoff_frequency, "Hz"))
    frequencies = frequency_axis(summary.cutoff_frequency)
    response = low_pass_response(resistance, capacitance, frequencies) if kind == "low" else high_pass_response(resistance, capacitance, frequencies)
    st.plotly_chart(bode_figure(response, summary.cutoff_frequency, f"{title} magnitude"), use_container_width=True)
    st.plotly_chart(phase_figure(response, summary.cutoff_frequency, f"{title} phase"), use_container_width=True)
    if kind == "low":
        st.plotly_chart(step_figure(low_pass_step_response(resistance, capacitance, amplitude), "Low-pass step response"), use_container_width=True)


def rlc_workspace() -> None:
    st.header("Series RLC Resonance")
    resistance = unit_input("Resistance", 100.0, RESISTANCE_UNITS)
    inductance = unit_input("Inductance", 10.0, INDUCTANCE_UNITS)
    capacitance = unit_input("Capacitance", 100.0, CAPACITANCE_UNITS)
    amplitude = st.number_input("Input amplitude (V)", value=1.0, min_value=0.0, step=0.5)
    summary = rlc_summary(resistance, inductance, capacitance, amplitude)
    render_schematic(rlc_svg(), ASCII_SCHEMATICS["rlc"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Resonant frequency", format_engineering(summary.resonant_frequency, "Hz"))
    c2.metric("Quality factor", f"{summary.quality_factor:.3g}")
    c3.metric("Bandwidth", format_engineering(summary.bandwidth, "Hz"))
    response = series_rlc_response(resistance, inductance, capacitance, amplitude, rlc_frequency_axis(summary.resonant_frequency))
    for fig in rlc_figures(response, summary.resonant_frequency):
        st.plotly_chart(fig, use_container_width=True)


def design_workspace() -> None:
    st.header("Design Workspace")
    tab1, tab2, tab3 = st.tabs(["Voltage Divider", "RC Filter", "RLC Resonance"])
    with tab1:
        vin = st.number_input("Vin (V)", value=12.0)
        desired = st.number_input("Desired Vout (V)", value=5.0)
        known_component = st.radio("Known component", ["R2", "R1"], horizontal=True)
        known = unit_input("Known resistor", 10.0, RESISTANCE_UNITS)
        result = design_voltage_divider(vin, desired, known, known_component)
        results_table(
            {
                "Theoretical resistor": format_engineering(result.theoretical, "ohm"),
                "Nearest standard resistor": format_engineering(result.practical or result.theoretical, "ohm"),
                "Resulting Vout": format_engineering(result.achieved, "V"),
                "Error": percent(result.error_percent),
            }
        )
    with tab2:
        target = st.number_input("Desired cutoff frequency (Hz)", value=500.0)
        known_component = st.radio("Known component", ["C", "R"], horizontal=True, key="rc-known")
        known = unit_input("Known value", 100.0, CAPACITANCE_UNITS if known_component == "C" else RESISTANCE_UNITS)
        result = design_rc_filter(target, known, known_component)
        unit = "ohm" if known_component == "C" else "F"
        results_table(
            {
                "Theoretical value": format_engineering(result.theoretical, unit),
                "Practical value": format_engineering(result.practical, unit) if result.practical else "Use calculated capacitor value",
                "Actual cutoff": format_engineering(result.achieved, "Hz"),
                "Error": percent(result.error_percent),
            }
        )
    with tab3:
        target = st.number_input("Desired resonant frequency (Hz)", value=1000.0)
        known_component = st.radio("Known component", ["C", "L"], horizontal=True, key="rlc-known")
        known = unit_input("Known reactive component", 100.0, CAPACITANCE_UNITS if known_component == "C" else INDUCTANCE_UNITS)
        result = design_rlc_resonance(target, known, known_component)
        unit = "H" if known_component == "C" else "F"
        results_table({"Required value": format_engineering(result.theoretical, unit), "Predicted resonance": format_engineering(result.achieved, "Hz")})


def fault_workspace() -> None:
    st.header("Fault & Diagnostics")
    tab1, tab2, tab3 = st.tabs(["Fault Injection", "Measurement Diagnosis", "Mystery Fault Challenge"])
    with tab1:
        fault = st.selectbox(
            "Voltage divider fault",
            ["R1 open", "R2 open", "R1 short", "R2 short", "R1 drift +25%", "R1 drift -25%", "R2 drift +25%", "R2 drift -25%"],
        )
        result = voltage_divider_fault(12.0, 1000.0, 2000.0, fault)
        c1, c2 = st.columns(2)
        c1.metric("Healthy Vout", format_engineering(result.healthy.vout, "V"))
        c2.metric("Faulty Vout", format_engineering(result.faulty_vout, "V"))
        st.plotly_chart(healthy_faulty_bar(result.healthy.vout, result.faulty_vout, "Healthy vs faulty output", "Vout (V)"), use_container_width=True)
        st.write(result.explanation)
        rc_fault = st.selectbox("RC low-pass fault", ["resistor drift +25%", "resistor drift -25%", "capacitor drift +25%", "capacitor drift -25%", "capacitor open", "capacitor short"])
        rc = rc_low_pass_fault(1000.0, 1e-6, rc_fault)
        results_table(
            {
                "Healthy cutoff": format_engineering(rc.healthy_cutoff, "Hz"),
                "Faulty cutoff": format_engineering(rc.faulty_cutoff, "Hz") if rc.faulty_cutoff else "Not applicable in ideal model",
                "Explanation": rc.explanation,
            }
        )
    with tab2:
        noise = st.selectbox("Optional measurement noise", ["Ideal", "+/-0.5%", "+/-1%", "+/-2%"])
        noise_percent = {"Ideal": 0.0, "+/-0.5%": 0.5, "+/-1%": 1.0, "+/-2%": 2.0}[noise]
        baseline = st.number_input("Measured Vout before noise (V)", value=0.087, step=0.1)
        measured = simulate_measurement_noise(baseline, noise_percent, seed=42)
        diagnosis = diagnose_voltage_divider(12.0, 1000.0, 2000.0, measured)
        st.metric("Most likely", diagnosis.most_likely)
        results_table(
            {
                "Expected healthy Vout": format_engineering(diagnosis.expected_vout, "V"),
                "Measured Vout": format_engineering(diagnosis.measured_vout, "V"),
                "Deviation": percent(diagnosis.percent_deviation),
                "Confidence": diagnosis.confidence,
                "Alternative": ", ".join(diagnosis.alternatives),
            }
        )
        st.write(diagnosis.explanation)
        st.caption("Real measurements are not perfectly exact. Noise can create small deviations even when a circuit is healthy.")
    with tab3:
        if "mystery_fault" not in st.session_state:
            st.session_state.mystery_fault = default_rng(12).choice(["R1 open", "R2 open", "R1 short", "R2 short"]).item()
        if "mystery_score" not in st.session_state:
            st.session_state.mystery_score = 0
        guess = st.selectbox("What do you think failed?", ["R1 open", "R2 open", "R1 short", "R2 short"])
        hidden = voltage_divider_fault(12.0, 1000.0, 2000.0, st.session_state.mystery_fault)
        st.metric("Measured Vout", format_engineering(hidden.faulty_vout, "V"))
        if st.button("Check answer"):
            if guess == st.session_state.mystery_fault:
                st.session_state.mystery_score += 1
                st.success("Correct")
            else:
                st.warning(f"Not quite. Actual fault: {st.session_state.mystery_fault}")
            st.write(hidden.explanation)
        if st.button("New mystery fault"):
            st.session_state.mystery_fault = default_rng().choice(["R1 open", "R2 open", "R1 short", "R2 short"]).item()
            st.rerun()
        st.metric("Session score", st.session_state.mystery_score)


def monte_carlo_workspace() -> None:
    st.header("Monte Carlo Analysis")
    st.write("This estimates how uniform random component tolerance affects circuit behaviour.")
    circuit = st.radio("Circuit", ["Voltage divider", "RC low-pass cutoff"], horizontal=True)
    tolerance = st.selectbox("Tolerance", [1, 5, 10], index=1)
    samples = st.selectbox("Samples", [100, 500, 1000, 5000], index=1)
    if circuit == "Voltage divider":
        result = voltage_divider_tolerance(12.0, 1000.0, 2000.0, tolerance, samples, seed=42)
        label = "Vout (V)"
    else:
        result = rc_filter_tolerance(1000.0, 1e-6, tolerance, samples, seed=42)
        label = "Cutoff frequency (Hz)"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nominal", f"{result.nominal:.4g}")
    c2.metric("Mean", f"{result.mean:.4g}")
    c3.metric("Minimum", f"{result.minimum:.4g}")
    c4.metric("Maximum", f"{result.maximum:.4g}")
    st.plotly_chart(monte_carlo_histogram(result.samples, result.nominal, f"{circuit} tolerance spread", label), use_container_width=True)


def reference() -> None:
    st.header("Engineering Reference")
    concepts = {
        "Ohm's Law": "Voltage equals current multiplied by resistance: V = IR.",
        "Kirchhoff's Current Law": "At a node, current entering equals current leaving.",
        "Conductance": "Conductance is 1/R. It makes nodal equations easier to write.",
        "Nodal Analysis": "Choose ground, label unknown node voltages, write KCL, build Ax = b, then solve for x.",
        "Cutoff Frequency": "For an RC filter, fc = 1/(2*pi*R*C).",
        "Bode Plot": "A frequency-response plot showing gain and phase across a log frequency axis.",
        "Resonance": "In a series RLC circuit, inductive and capacitive reactance cancel at f0.",
        "Monte Carlo Simulation": "Repeated random trials estimate how uncertain component values affect results.",
        "Open Circuit": "A broken path where ideal current is zero.",
        "Short Circuit": "A near-zero-resistance path that can force a node to another voltage.",
    }
    for title, body in concepts.items():
        with st.expander(title):
            st.write(body)


PAGES = [
    "Overview",
    "Analysis: Voltage Divider",
    "Analysis: Network Solver",
    "Analysis: RC Low-Pass",
    "Analysis: RC High-Pass",
    "Analysis: Series RLC",
    "Design Workspace",
    "Fault & Diagnostics",
    "Monte Carlo Analysis",
    "Engineering Reference",
]

requested_page = st.query_params.get("page", "Overview")
default_page_index = PAGES.index(requested_page) if requested_page in PAGES else 0
page = st.sidebar.radio("CircuitSense", PAGES, index=default_page_index)

try:
    if page == "Overview":
        overview()
    elif page == "Analysis: Voltage Divider":
        voltage_divider_workspace()
    elif page == "Analysis: Network Solver":
        nodal_workspace()
    elif page == "Analysis: RC Low-Pass":
        rc_workspace("low")
    elif page == "Analysis: RC High-Pass":
        rc_workspace("high")
    elif page == "Analysis: Series RLC":
        rlc_workspace()
    elif page == "Design Workspace":
        design_workspace()
    elif page == "Fault & Diagnostics":
        fault_workspace()
    elif page == "Monte Carlo Analysis":
        monte_carlo_workspace()
    else:
        reference()
except ValueError as exc:
    st.error(str(exc))
