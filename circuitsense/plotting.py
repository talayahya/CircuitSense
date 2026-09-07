"""Plotly chart builders for CircuitSense."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go


def bode_figure(response: dict[str, np.ndarray], cutoff_frequency: float, title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=response["frequency"],
            y=response["magnitude_db"],
            mode="lines",
            name="Magnitude",
            hovertemplate="%{x:.3g} Hz<br>%{y:.3f} dB<extra></extra>",
        )
    )
    fig.add_vline(x=cutoff_frequency, line_dash="dash", annotation_text="Cutoff")
    fig.update_layout(title=title, xaxis_title="Frequency (Hz)", yaxis_title="Magnitude (dB)", xaxis_type="log")
    return fig


def phase_figure(response: dict[str, np.ndarray], cutoff_frequency: float, title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=response["frequency"],
            y=response["phase_deg"],
            mode="lines",
            name="Phase",
            hovertemplate="%{x:.3g} Hz<br>%{y:.2f} degrees<extra></extra>",
        )
    )
    fig.add_vline(x=cutoff_frequency, line_dash="dash", annotation_text="Cutoff")
    fig.update_layout(title=title, xaxis_title="Frequency (Hz)", yaxis_title="Phase (degrees)", xaxis_type="log")
    return fig


def step_figure(step: dict[str, np.ndarray], title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=step["time"], y=step["output"], mode="lines", name="Vout"))
    fig.update_layout(title=title, xaxis_title="Time (s)", yaxis_title="Output voltage (V)")
    return fig


def rlc_figures(response: dict[str, np.ndarray], resonant_frequency: float) -> tuple[go.Figure, go.Figure, go.Figure]:
    current = go.Figure()
    current.add_trace(go.Scatter(x=response["frequency"], y=response["current"], mode="lines", name="Current"))
    current.add_vline(x=resonant_frequency, line_dash="dash", annotation_text="Resonance")
    current.update_layout(title="Series RLC current response", xaxis_title="Frequency (Hz)", yaxis_title="Current (A)", xaxis_type="log")

    impedance = go.Figure()
    impedance.add_trace(go.Scatter(x=response["frequency"], y=response["impedance"], mode="lines", name="Impedance"))
    impedance.add_vline(x=resonant_frequency, line_dash="dash", annotation_text="Resonance")
    impedance.update_layout(title="Series RLC impedance", xaxis_title="Frequency (Hz)", yaxis_title="Impedance (ohm)", xaxis_type="log")

    phase = go.Figure()
    phase.add_trace(go.Scatter(x=response["frequency"], y=response["phase_deg"], mode="lines", name="Phase"))
    phase.add_vline(x=resonant_frequency, line_dash="dash", annotation_text="Resonance")
    phase.update_layout(title="Series RLC phase", xaxis_title="Frequency (Hz)", yaxis_title="Phase (degrees)", xaxis_type="log")
    return current, impedance, phase


def monte_carlo_histogram(samples: np.ndarray, nominal: float, title: str, x_label: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=samples, nbinsx=40, name="Simulated samples"))
    fig.add_vline(x=nominal, line_dash="dash", annotation_text="Nominal")
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title="Count", bargap=0.03)
    return fig


def healthy_faulty_bar(healthy: float, faulty: float, title: str, y_label: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Healthy", "Faulty"], y=[healthy, faulty], text=["Healthy", "Faulty"], name="Comparison"))
    fig.update_layout(title=title, yaxis_title=y_label, showlegend=False)
    return fig

