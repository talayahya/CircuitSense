# Interview Guide

## 30-Second Explanation

CircuitSense is a Python and Streamlit app I built to analyse simple electrical circuits. It covers voltage dividers, RC filters, RLC resonance, nodal analysis for resistor networks, fault diagnosis and Monte Carlo tolerance simulation. I built it to connect computer engineering theory with practical software structure and testing.

## 60-Second Explanation

CircuitSense is an interactive engineering tool for analysing and designing simple circuits. The strongest part is the nodal-analysis solver, which builds a conductance matrix from a resistor network and uses NumPy to solve for unknown node voltages. The app also calculates frequency response for RC filters and RLC circuits, injects simplified faults, diagnoses likely voltage-divider faults and runs Monte Carlo tolerance simulations. I kept the maths explainable and wrote pytest tests for the core calculations.

## 2-Minute Technical Explanation

CircuitSense separates the user interface from the engineering logic. The Streamlit app collects component values and sends SI-unit values to small Python modules. The voltage-divider module calculates current, voltage drops and power. The RC and RLC modules calculate cutoff frequency, frequency response, impedance, phase and resonance. The nodal-analysis module turns a resistor network into `Ax = b`, where `A` contains conductance relationships, `x` is the unknown node-voltage vector and `b` contains fixed voltage-source contributions. NumPy solves that matrix equation. After the voltages are found, the app calculates current and power for each branch. The fault and diagnosis modules use idealised rules rather than machine learning so the reasoning stays transparent.

## Likely Questions

1. What does CircuitSense do?
   - Simple answer: It analyses, designs and diagnoses simple circuits.
   - More technical answer: It combines voltage-divider analysis, nodal analysis, RC/RLC frequency response, fault modelling and Monte Carlo tolerance simulation.
   - Testing: Whether you understand the project scope.
   - Know first: The main screens and what each module calculates.

2. Why did you build it?
   - Simple answer: To connect electronics theory with software engineering.
   - More technical answer: It let me practise numerical methods, matrix solving, plotting, modular Python and tests around circuit models.
   - Testing: Motivation and project ownership.
   - Know first: Which parts you personally understand best.

3. Why Python?
   - Simple answer: Python is strong for numerical work and quick interfaces.
   - More technical answer: NumPy, Plotly, pytest and Streamlit make it practical to build tested engineering analysis tools.
   - Testing: Technology choice.
   - Know first: What each dependency does.

4. What is Ohm's law?
   - Simple answer: Voltage equals current times resistance.
   - More technical answer: `V = IR`, so current through a resistor is `I = V/R`.
   - Testing: Fundamentals.
   - Know first: Units of volts, amps and ohms.

5. What is Kirchhoff's Current Law?
   - Simple answer: Current entering a node equals current leaving it.
   - More technical answer: The algebraic sum of currents at a node is zero.
   - Testing: Circuit-analysis foundation.
   - Know first: What a node is.

6. What is nodal analysis?
   - Simple answer: A method for finding unknown node voltages.
   - More technical answer: Apply KCL at unknown nodes, write currents with conductance, form `Ax = b`, then solve for node voltages.
   - Testing: Your strongest technical feature.
   - Know first: The full guide in `NODAL_ANALYSIS_GUIDE.md`.

7. Why use conductance?
   - Simple answer: It makes the equations cleaner.
   - More technical answer: Since `G = 1/R`, resistor current can be written as `G(Va - Vb)`.
   - Testing: Whether matrix construction makes sense.
   - Know first: How conductance terms enter the matrix.

8. What does `Ax = b` represent?
   - Simple answer: The circuit equations in matrix form.
   - More technical answer: `A` contains conductances, `x` contains unknown voltages and `b` contains fixed source contributions.
   - Testing: Linear algebra understanding.
   - Know first: A simple two-node example.

9. What happens if the matrix is singular?
   - Simple answer: The circuit cannot be solved as defined.
   - More technical answer: The equations do not have a unique solution, often because a node is disconnected or under-constrained.
   - Testing: Error handling and numerical awareness.
   - Know first: Why disconnected circuits are ambiguous.

10. How does a voltage divider work?
    - Simple answer: Two resistors split the input voltage.
    - More technical answer: `Vout = Vin * R2 / (R1 + R2)`.
    - Testing: Basic circuit understanding.
    - Know first: How R1 and R2 affect Vout.

11. What happens when R1 increases?
    - Simple answer: Vout decreases.
    - More technical answer: R1 takes a larger share of the voltage drop, leaving less across R2.
    - Testing: Intuition.
    - Know first: Divider ratio.

12. What happens when R2 increases?
    - Simple answer: Vout increases.
    - More technical answer: A larger R2 receives a larger share of the input voltage.
    - Testing: Intuition.
    - Know first: Divider ratio.

13. What is an RC circuit?
    - Simple answer: A resistor-capacitor circuit.
    - More technical answer: It has time-dependent and frequency-dependent behaviour because the capacitor impedance changes with frequency.
    - Testing: Filter basics.
    - Know first: Capacitor behaviour.

14. What does a capacitor do?
    - Simple answer: It stores charge and resists sudden voltage changes.
    - More technical answer: Its impedance decreases as frequency increases.
    - Testing: Component intuition.
    - Know first: Low-pass and high-pass layouts.

15. What does an inductor do?
    - Simple answer: It resists sudden current changes.
    - More technical answer: Its reactance increases with frequency: `XL = 2*pi*f*L`.
    - Testing: Component intuition.
    - Know first: RLC resonance.

16. What is cutoff frequency?
    - Simple answer: The frequency where filter output has dropped by about 3 dB.
    - More technical answer: For RC filters, `fc = 1/(2*pi*R*C)`.
    - Testing: Filter understanding.
    - Know first: Time constant.

17. What does a Bode plot show?
    - Simple answer: How gain and phase change with frequency.
    - More technical answer: It plots magnitude in dB and phase in degrees on a logarithmic frequency axis.
    - Testing: Data visualisation and signals.
    - Know first: Why log scale is useful.

18. Why use a logarithmic frequency axis?
    - Simple answer: It shows a wide frequency range clearly.
    - More technical answer: Circuit behaviour often changes across decades of frequency.
    - Testing: Plot interpretation.
    - Know first: Frequency decades.

19. What does -3 dB mean?
    - Simple answer: The output power is about half the passband level.
    - More technical answer: The voltage magnitude is `1/sqrt(2)` of the original level.
    - Testing: Filter terminology.
    - Know first: dB relationship.

20. What is resonance?
    - Simple answer: A frequency where the inductor and capacitor effects cancel.
    - More technical answer: In a series RLC circuit, `XL = XC`, so impedance is mainly resistive.
    - Testing: RLC understanding.
    - Know first: Reactance.

21. What is quality factor?
    - Simple answer: A measure of how sharp the resonance is.
    - More technical answer: For a series RLC circuit, `Q = (1/R) * sqrt(L/C)`.
    - Testing: Resonance concepts.
    - Know first: Bandwidth.

22. How does design mode work?
    - Simple answer: It rearranges equations to solve for a missing component.
    - More technical answer: It calculates theoretical values, then suggests practical standard resistor values where useful.
    - Testing: Algebra and practical design.
    - Know first: Voltage-divider and RC equations.

23. What is component tolerance?
    - Simple answer: Real components are not exactly their labelled value.
    - More technical answer: A 5% resistor can vary between 95% and 105% of nominal value.
    - Testing: Engineering realism.
    - Know first: Why simulation uses ranges.

24. What is Monte Carlo analysis?
    - Simple answer: Repeating random trials to estimate possible outcomes.
    - More technical answer: CircuitSense randomly varies component values within tolerance and recalculates output many times.
    - Testing: Numerical methods.
    - Know first: Mean, min, max and standard deviation.

25. Why uniform random variation?
    - Simple answer: It is simple and explainable.
    - More technical answer: It assumes any value inside the tolerance band is equally likely, which is enough for an educational model.
    - Testing: Assumptions.
    - Know first: Limitations of the model.

26. How does fault injection work?
    - Simple answer: It changes a component into an ideal fault case.
    - More technical answer: It models open circuits, short circuits and value drift, then compares healthy and faulty behaviour.
    - Testing: Fault reasoning.
    - Know first: The ideal assumptions.

27. How does diagnosis work?
    - Simple answer: It compares measured output to expected output.
    - More technical answer: Near-zero output suggests R2 short or R1 open; near-Vin output suggests R1 short or R2 open.
    - Testing: Reasoning transparency.
    - Know first: Voltage-divider fault signatures.

28. Why not use machine learning?
    - Simple answer: The rules are simpler and easier to explain.
    - More technical answer: The supported fault cases have clear physical signatures, so rule-based diagnosis is appropriate.
    - Testing: Avoiding unnecessary complexity.
    - Know first: ML is not always the right tool.

29. What is measurement noise?
    - Simple answer: Real measurements are not perfectly exact.
    - More technical answer: Small random deviations can appear even when a circuit is healthy.
    - Testing: Practical awareness.
    - Know first: Difference between noise and faults.

30. How did you test it?
    - Simple answer: I wrote pytest tests for the core calculations.
    - More technical answer: Tests cover known voltage-divider values, cutoff frequency, RLC resonance, nodal solving, faults, diagnosis and Monte Carlo reproducibility.
    - Testing: Software discipline.
    - Know first: Run `pytest`.

31. What are the limitations?
    - Simple answer: It uses simplified ideal models.
    - More technical answer: It does not model transistors, parasitics, temperature effects, real measurement loading or SPICE-level behaviour.
    - Testing: Honesty.
    - Know first: Scope boundaries.

32. What would you add with physical hardware?
    - Simple answer: Real multimeter or microcontroller measurements.
    - More technical answer: I would compare measured data against the ideal model and use it for calibration or diagnosis.
    - Testing: Future thinking.
    - Know first: Hardware safety and measurement limits.

35. What part are you most proud of?
    - Simple answer: The nodal-analysis solver.
    - More technical answer: It turns a circuit definition into matrix equations and solves actual node voltages programmatically.
    - Testing: Ownership.
    - Know first: How to walk through the example by hand.

## CV Versions

**CircuitSense | Python, NumPy, SciPy, Plotly**

- Developed an interactive Python circuit-analysis platform supporting automated nodal analysis, RC/RLC frequency-response modelling and component-level electrical calculations.
- Implemented design tools for selecting component values against target voltage, cutoff-frequency and resonance specifications.
- Built rule-based fault diagnosis and Monte Carlo tolerance simulation with automated pytest validation and GitHub Actions CI.

**Short CV Version**

- Built CircuitSense, a Python/Streamlit engineering app for nodal circuit analysis, RC/RLC modelling, component design, fault diagnosis and Monte Carlo tolerance simulation.

**Technical CV Version**

- Created CircuitSense, a tested Python engineering tool using NumPy linear algebra to solve resistive networks via nodal analysis, with Plotly visualisations for RC/RLC response and tolerance behaviour.

