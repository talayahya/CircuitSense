# Engineering Notes

CircuitSense uses simplified ideal component models.

## Assumptions

- Wires have zero resistance.
- Voltage sources are ideal.
- Measurements do not load the circuit unless a fault model says otherwise.
- Resistors, capacitors and inductors use nominal values unless tolerance simulation is enabled.
- Faults are idealised to make behaviour understandable.

## Why This Scope Works

The project stays at an early undergraduate level while still showing useful engineering ideas:

- Formula-based analysis
- Matrix solving
- Frequency response
- Complex impedance concepts
- Component tolerance
- Fault reasoning

## What It Is Not

CircuitSense is not a SPICE simulator. It does not model semiconductor devices, parasitic effects, temperature dependence, physical PCB layout or hardware safety.

