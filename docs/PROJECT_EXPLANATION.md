# Project Explanation

CircuitSense is an interactive Python application for analysing, designing and diagnosing simple electrical circuits.

## What It Does

The app lets a user choose a circuit, enter values, view calculations, inspect plots and export a short Markdown report.

The project combines electrical engineering fundamentals with Python programming, data visualisation, numerical methods and automated testing.

## Voltage Divider

A voltage divider uses two resistors in series. The output voltage is taken from the connection between them.

```text
Vout = Vin * R2 / (R1 + R2)
```

The app also calculates circuit current, voltage drops and resistor power.

## Nodal Analysis

The nodal solver is the most technical part of the project. It uses Kirchhoff's Current Law to build a matrix equation from a resistor network.

The unknown node voltages are placed into a vector called `x`. NumPy solves the equation `Ax = b`.

## RC Filters

An RC filter combines a resistor and capacitor.

The time constant is:

```text
tau = RC
```

The cutoff frequency is:

```text
fc = 1 / (2*pi*R*C)
```

The app shows Bode magnitude and phase plots, plus a step response for the low-pass filter.

## RLC Resonance

A series RLC circuit contains a resistor, inductor and capacitor. At resonance, inductive and capacitive reactance cancel.

```text
f0 = 1 / (2*pi*sqrt(LC))
```

The app calculates resonance, current, impedance, phase, quality factor and bandwidth.

## Design Mode

Design mode rearranges formulas to calculate missing component values. For example, if the user wants a voltage divider to output 5 V from 12 V, CircuitSense can calculate the required resistor.

For resistors, it can also suggest a nearest E12 preferred value.

## Fault Injection

Fault injection models common simple failures:

- Open circuits
- Short circuits
- Component drift

The models are idealised so the results stay explainable.

## Diagnosis

The diagnosis module is rule-based. It compares a measured voltage to the expected healthy voltage and suggests likely faults.

It does not use machine learning, because the rules are transparent and easier to justify.

## Monte Carlo Analysis

Monte Carlo analysis repeats a calculation many times while randomly changing components within a tolerance range.

CircuitSense uses a uniform distribution for simplicity. This estimates how much real component variation might move the output.

## How The Modules Work Together

The Streamlit app collects user input and sends SI-unit values to calculation modules. The calculation modules return dataclasses or arrays. Plotting functions turn those results into charts, and report functions export summaries.

This structure keeps the project easier to test and easier to explain.

