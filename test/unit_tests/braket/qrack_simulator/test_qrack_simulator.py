# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import cmath
import numpy as np
import pytest

from braket.circuits import Circuit
from braket.devices import LocalSimulator

from braket.default_simulator.result_types import StateVector


def test_simulator_bell_state_m():
    device = LocalSimulator(backend="qrack")
    bell = Circuit().h(0).cnot(0, 1)
    results_dict = device.run(bell, shots=100).result().measurement_counts.items()
    for key, val in results_dict:
        assert (val > 40) and (val < 60)


def test_simulator_bell_state_sv():
    device = LocalSimulator(backend="qrack")
    bell = Circuit().h(0).cnot(0, 1).state_vector()
    state_vec = device.run(bell, shots=0).result().values[0]
    assert cmath.isclose(state_vec[0] * np.conj(state_vec[0]), 0.5, abs_tol=1e-5)
    assert cmath.isclose(state_vec[1] * np.conj(state_vec[1]), 0, abs_tol=1e-5)
    assert cmath.isclose(state_vec[2] * np.conj(state_vec[2]), 0, abs_tol=1e-5)
    assert cmath.isclose(state_vec[3] * np.conj(state_vec[3]), 0.5, abs_tol=1e-5)
