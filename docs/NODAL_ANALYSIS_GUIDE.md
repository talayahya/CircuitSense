# Nodal Analysis Guide

Nodal analysis is a method for finding unknown voltages in an electrical network.

## What Is A Node?

A node is a point in a circuit where components connect. All wires connected together without resistance are treated as the same node.

## What Is Ground?

Ground is the 0 V reference point. Other voltages are measured relative to ground.

## Kirchhoff's Current Law

Kirchhoff's Current Law says that current entering a node equals current leaving it. In equations, the total current at a node sums to zero.

## Conductance

Conductance is the inverse of resistance:

```text
G = 1 / R
```

It is useful because current through a resistor can be written as:

```text
I = G(Va - Vb)
```

That form is convenient when building matrix equations.

## Example Circuit

Use this network:

```text
12 V source -> R1 -> Node A
Node A -> R2 -> ground
Node A -> R3 -> Node B
Node B -> R4 -> ground
```

Values:

```text
R1 = 1000 ohm
R2 = 2000 ohm
R3 = 3000 ohm
R4 = 4000 ohm
```

Unknown voltages:

```text
Va, Vb
```

## Node A Equation

Currents leaving Node A:

```text
(Va - 12) / R1 + Va / R2 + (Va - Vb) / R3 = 0
```

Using conductance:

```text
(G1 + G2 + G3)Va - G3Vb = G1 * 12
```

## Node B Equation

Currents leaving Node B:

```text
(Vb - Va) / R3 + Vb / R4 = 0
```

Using conductance:

```text
-G3Va + (G3 + G4)Vb = 0
```

## Matrix Form

The equations become:

```text
A x = b
```

Where:

```text
x = [Va, Vb]
```

`A` stores the conductance relationships between unknown nodes.

`b` stores the known source-voltage contribution.

## What NumPy Solves

`numpy.linalg.solve(A, b)` finds the vector `x` that satisfies the simultaneous equations.

In this example, CircuitSense finds approximately:

```text
Va = 7.579 V
Vb = 4.331 V
```

After finding node voltages, CircuitSense calculates each resistor current using:

```text
I = (Va - Vb) / R
```

and power using:

```text
P = I^2 R
```

## Singular Matrix

A singular matrix usually means the circuit does not contain enough information to solve the unknowns. For example, an unknown node might be disconnected from every source and ground path.

CircuitSense catches this and shows a useful error instead of crashing.

