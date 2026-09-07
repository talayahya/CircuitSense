# CircuitSense Architecture

CircuitSense is split into a user interface layer and small engineering modules.

```text
Streamlit UI
    |
    v
Circuit modules
    |
    v
Analysis and design engines
    |
    v
Fault, diagnosis and Monte Carlo modules
    |
    v
Plotting and report export
```

## Streamlit UI

`app.py` provides the screens, controls, tabs, metric cards and report-download buttons. It does not own the maths. When a user changes a value, the UI passes clean SI-unit values to the calculation modules.

## Circuit Modules

The circuit modules each focus on one kind of engineering calculation:

- `voltage_divider.py` calculates current, output voltage, voltage drops and power.
- `filters.py` calculates RC time constants, cutoff frequency, Bode response and step response.
- `rlc.py` calculates resonance, impedance, current, phase, quality factor and bandwidth.
- `nodal.py` solves small resistor networks using matrix-based nodal analysis.

## Design Engines

`design.py` rearranges the normal circuit equations. Instead of asking, "what is the output?", it asks, "what component value gives the output I want?"

## Fault and Diagnosis Modules

`faults.py` contains simplified open-circuit, short-circuit and drift models. `diagnosis.py` compares measured output to the healthy expected output and uses transparent rules to suggest likely faults.

## Monte Carlo Module

`monte_carlo.py` randomly varies component values within a tolerance range. It repeats the calculation many times and summarises the spread of possible outputs.

## Plotting and Reporting

`plotting.py` builds Plotly figures. `reports.py` creates Markdown reports containing inputs, outputs and model limitations.

## Design Choice

The project deliberately avoids advanced simulation internals. The goal is to show strong software structure and explainable engineering, not to recreate a full SPICE simulator.

