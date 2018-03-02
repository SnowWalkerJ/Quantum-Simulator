# Quantum Simulator

You can run quantum experiments on this simulator. It simulates the parallel and entanglement effect of quantum systems.

Refer to [this reading](QuantumComputing.pdf) for principals and mathematical techniques.

## Built-in operations

- Pauli X (`X`)
- Pauli Y (`Y`)
- Pauli Z (`Z`)
- Identity (`I`)
- Phase shifter (`Phase`)
- Swap (`Swap`)
- Harmard (`H`)
- Measure (`Measure`)
- Controlled Not (`CNot=X.controlled()`)

For any given operator, you can create its controlled version or adjoint version by call `operator.controlled()` and `operator.adjoint()` respectively.

## Observe the state of the system

Unlike a real quantum computer, in which your observations cause collapsion of the state, this quantum simulator allows you to "watch" the state (vector) of the system without interfering with it. It should help understand the quantum mechanism and debug.

## Examples

In `examples/bell.py` we show how to create, observe and inspect an entangled 2-bit system.