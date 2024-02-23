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

import sys
import uuid
from abc import ABC

from braket.device_schema.simulators import (
    GateModelSimulatorDeviceCapabilities,
    GateModelSimulatorDeviceParameters,
)

from braket.task_result import (
    AdditionalMetadata,
    GateModelTaskResult,
    TaskMetadata
)

from braket.ir.openqasm import Program as OQ3Program

from qiskit.compiler.transpiler import transpile
from qiskit.qasm3 import loads

from pyqrack import QrackSimulator


class BraketQrackSimulator(ABC):
    """An abstract simulator that locally runs a quantum task.

    The task can be either a quantum circuit defined in an OpenQASM or JAQCD program,
    or an analog Hamiltonian simulation (AHS) program.

    For users creating their own simulator: to register a simulator so the
    Braket SDK recognizes its name, the name and class must be added as an
    entry point for "braket.simulators". This is done by adding an entry to
    entry_points in the simulator package's setup.py:

    >>> entry_points = {
    >>>     "braket.simulators": [
    >>>         "backend_name = <backend_class>"
    >>>     ]
    >>> }
    """

    DEVICE_ID = "BraketQrackSimulator"

    def run(self, ir: OQ3Program, shots=1, is_reactively_separated=False, sdrp=-1, ncrp=-1, *args, **kwargs) -> GateModelTaskResult:
        """
        Run the task specified by the given IR.

        Extra arguments will contain any additional information necessary to run the task,
        such as number of qubits.

        Args:
            ir (OQ3Program): The IR representation of the program

        Returns:
            GateModelTaskResult: An object
            representing the results of the simulation.
        """
        basis_gates = [
            'id', 'u', 'u1', 'u2', 'u3', 'r', 'rx', 'ry', 'rz',
            'h', 'x', 'y', 'z', 's', 'sdg', 'sx', 'sxdg', 'p', 't', 'tdg',
            'cu', 'cu1', 'cu2', 'cu3', 'cx', 'cy', 'cz', 'ch', 'cp', 'csx', 'csxdg', 'dcx',
            'ccx', 'ccy', 'ccz', 'mcx', 'mcy', 'mcz', 'mcu', 'mcu1', 'mcu2', 'mcu3',
            'swap', 'iswap', 'cswap', 'mcswap', 'reset', 'measure', 'barrier'
        ]

        src = ir.source.replace("cnot", "cx")
        variables = list(ir.inputs.keys())
        for v in variables:
            src = src.replace(v, str(variables[v]))

        src_lines = src.splitlines()
        if len(src_lines) == 0:
            raise ValueError("OpenQASM program is empty!")

        inc_line = 'include "stdgates.inc";'
        if (len(src_lines) > 1) and (inc_line not in src_lines[1]):
            src_lines.insert(1, inc_line)

        is_measured = False
        for l in reversed(src_lines):
            if "measure" in l:
               is_measured = True
               break

        circ = transpile(loads("\n".join(src_lines)), basis_gates=basis_gates)
        qsim = QrackSimulator(circ.width(), *args, **kwargs)
        qsim.set_reactive_separate(is_reactively_separated)
        if sdrp >= 0:
            qsim.set_sdrp(sdrp)
        if ncrp >= 0:
            qsim.set_ncrp(ncrp)

        state_vector = None
        measurements = None
        resultTypes = None
        values = None
        if shots == 0:
            qsim.run_qiskit_circuit(circ, 0)
            resultTypes = [ResultTypeValue.construct(type="StateVector", value=qsim.out_ket())]
        else:
            if not is_measured:
                circ.measure_all()
            _measurements = qsim.run_qiskit_circuit(circ, shots)
            measurements = []
            bit_len = len(qsim._sample_qubits)
            for m in _measurements:
                integer = int(m.split("x", 1)[1])
                bit_string = [int(digit) for digit in bin(integer)[2:]]
                if len(bit_string) < bit_len:
                    bit_string = bit_string + [0] * (bit_len - len(bit_string))
                measurements.append(bit_string)

        return GateModelTaskResult.construct(
            taskMetadata=TaskMetadata(
                id=str(uuid.uuid4()),
                shots=shots,
                deviceId=self.DEVICE_ID,
            ),
            additionalMetadata=AdditionalMetadata(
                action=ir,
            ),
            resultTypes=resultTypes,
            measurements=measurements,
            measuredQubits=qsim._sample_qubits,
        )

    @property
    def properties(self) -> GateModelSimulatorDeviceCapabilities:
        """
        Device properties for the StateVectorSimulator.

        Returns:
            GateModelSimulatorDeviceCapabilities: Device capabilities for this simulator.
        """
        observables = ["x", "y", "z", "h", "i", "hermitian"]
        max_shots = sys.maxsize
        # Default Qrack build can have 2 ** 12 low-entanglement qubits in one simulator instance:
        qubit_count = 1 << 12
        return GateModelSimulatorDeviceCapabilities.parse_obj(
            {
                "service": {
                    "executionWindows": [
                        {
                            "executionDay": "Everyday",
                            "windowStartHour": "00:00",
                            "windowEndHour": "23:59:59",
                        }
                    ],
                    "shotsRange": [0, max_shots],
                },
                "action": {
                    "braket.ir.openqasm.program": {
                        "actionType": "braket.ir.openqasm.program",
                        "version": ["1"],
                        "supportedOperations": [
                            # OpenQASM primitives
                            "U",
                            "GPhase",
                            # builtin Braket gates
                            "ccnot",
                            "cnot",
                            "cphaseshift",
                            "cphaseshift00",
                            "cphaseshift01",
                            "cphaseshift10",
                            "cswap",
                            "cv",
                            "cy",
                            "cz",
                            "ecr",
                            "gpi",
                            "gpi2",
                            "h",
                            "i",
                            "iswap",
                            "ms",
                            "pswap",
                            "phaseshift",
                            "rx",
                            "ry",
                            "rz",
                            "s",
                            "si",
                            "swap",
                            "t",
                            "ti",
                            "unitary",
                            "v",
                            "vi",
                            "x",
                            "xx",
                            "xy",
                            "y",
                            "yy",
                            "z",
                            "zz",
                        ],
                        "supportedModifiers": [
                            {
                                "name": "ctrl",
                            },
                            {
                                "name": "negctrl",
                            },
                            {
                                "name": "pow",
                                "exponent_types": ["int", "float"],
                            },
                            {
                                "name": "inv",
                            },
                        ],
                        "supportedPragmas": [
                            "braket_unitary_matrix",
                            "braket_result_type_state_vector",
                            "braket_result_type_density_matrix",
                            "braket_result_type_sample",
                            "braket_result_type_expectation",
                            "braket_result_type_variance",
                            "braket_result_type_probability",
                            "braket_result_type_amplitude",
                        ],
                        "forbiddenPragmas": [
                            "braket_noise_amplitude_damping",
                            "braket_noise_bit_flip",
                            "braket_noise_depolarizing",
                            "braket_noise_kraus",
                            "braket_noise_pauli_channel",
                            "braket_noise_generalized_amplitude_damping",
                            "braket_noise_phase_flip",
                            "braket_noise_phase_damping",
                            "braket_noise_two_qubit_dephasing",
                            "braket_noise_two_qubit_depolarizing",
                            "braket_result_type_adjoint_gradient",
                        ],
                        "supportedResultTypes": [
                            {
                                "name": "Sample",
                                "observables": observables,
                                "minShots": 1,
                                "maxShots": max_shots,
                            },
                            {
                                "name": "Expectation",
                                "observables": observables,
                                "minShots": 0,
                                "maxShots": max_shots,
                            },
                            {
                                "name": "Variance",
                                "observables": observables,
                                "minShots": 0,
                                "maxShots": max_shots,
                            },
                            {"name": "Probability", "minShots": 0, "maxShots": max_shots},
                            {"name": "StateVector", "minShots": 0, "maxShots": 0},
                            {"name": "DensityMatrix", "minShots": 0, "maxShots": 0},
                            {"name": "Amplitude", "minShots": 0, "maxShots": 0},
                        ],
                        "supportPhysicalQubits": False,
                        "supportsPartialVerbatimBox": False,
                        "requiresContiguousQubitIndices": True,
                        "requiresAllQubitsMeasurement": True,
                        "supportsUnassignedMeasurements": True,
                        "disabledQubitRewiringSupported": False,
                    },
                },
                "paradigm": {"qubitCount": qubit_count},
                "deviceParameters": GateModelSimulatorDeviceParameters.schema(),
            }
        )
