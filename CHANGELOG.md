# Changelog

## v0.4.0

Update Qiskit API usage.

## v0.3.1

Bug fix / feature addition: "uncompute" after observable calculation (to allow different bases of observation for the same qubits).

## v0.3.0 (2024-02-25)

Features added:
- `Probability` and `Variance` observables for available bases can be calculated exactly for 0 shots.
- `Sample` observable can be simulated for 0 shots

This release was tested by running the notebooks in the [examples](https://github.com/vm6502q/amazon-braket-qrack-simulator-python/tree/main/examples) folder.

## v0.2.0 (2024-02-25)

Features added:
- Available observable bases are now (tensor products of) x, y, z, i, and h.
- `Expectation` observables for available bases can be calculated exactly for 0 shots.

In a future release, exact calculation of `Probability` and `Variance` will require Qrack to expose the `ProbBitsAll()` method on `QInterface`. (The method already exists in the C++ code, but there was no demand for this method to be exposed via the shared library API, previously.)

## v0.1.2 (2024-02-24)

Features added (for reporting observables estimated from measurement shots):
- `Sample`
- `Variance`
- `Expectation`

This release was tested by running the notebooks in the [examples](https://github.com/vm6502q/amazon-braket-qrack-simulator-python/tree/main/examples) folder.

## v0.1.1 (2024-02-24)

Bugs fixed:
- Hex measurements are now parsed correctly
- Extra simulator arguments are parsed correclty

This release was tested by running the notebooks in the [examples](https://github.com/vm6502q/amazon-braket-qrack-simulator-python/tree/main/examples) folder.

## v0.1.0 (2024-02-23)

This is the first (pre-)release of the Qrack Simulator for Amazon Braket SDK!

The (Amazon Braket SDK) Qrack Simulator is a Python open source library that provides an implementation of a quantum simulator that you can run locally. Qrack is a well-rounded simulator in development for over six years, with GPU acceleration, "ideal" and approximate modes, and novel approaches to canonical algorithms. Both OpenCL and CUDA back ends are available (supporting general GPU and accelerator vendors through the open standard of OpenCL).
