""" 
This module contains the function benchmark_stim, which benchmarks the performance of the stabilizer simulator.
"""

import numpy as np
import stim


def benchmark_stim(quantum_circuit):
    """
    Benchmark the performance of the stabilizer simulator.

    Parameters:
    -----------
    quantum_circuit : QuantumCircuit
        Quantum circuit to simulate.
    """

    tableau = stim.TableauSimulator()

    # To make sure that the size is correct
    tableau.h(quantum_circuit.num_qubits[0] - 1)
    tableau.h(quantum_circuit.num_qubits[0] - 1)

    for block in quantum_circuit.gates[0]:
        for gate, qubits in block.items():

            if gate == "h":
                tableau.h(*qubits)
            elif gate == "x":
                tableau.x(*qubits)
            elif gate == "y":
                tableau.y(*qubits)
            elif gate == "z":
                tableau.z(*qubits)
            elif gate == "cx":
                tableau.cnot(qubits[0][0], qubits[0][1])
            elif gate == "s":
                tableau.s(*qubits)
            else:
                raise ValueError("Invalid gate.")

    observable = stim.PauliString("".join(quantum_circuit.obs_pauli).upper())

    current_tableau = tableau.current_inverse_tableau()

    pauli, signs = transform_stim_tableau(current_tableau)

    observable_expectation = {"+1": 0, "-1": 0}
    expect = tableau.peek_observable_expectation(observable)

    if expect == 1:
        observable_expectation["+1"] = 1

    elif expect == -1:
        observable_expectation["-1"] = 1

    elif expect == 0:
        observable_expectation["+1"] = 0.5
        observable_expectation["-1"] = 0.5

    else:
        raise ValueError("Invalid observable expectation value.")

    if "+" not in quantum_circuit.eigenvalues[0]:
        observable_expectation.pop("+1", None)

    if "-" not in quantum_circuit.eigenvalues[0]:
        observable_expectation.pop("-1", None)

    return pauli, signs, observable_expectation


def transform_stim_tableau(tableau):
    """
    Transform the STIM tableau to the format used in the benchmark.

    Parameters:
    -----------
    tableau : stim.Tableau
        STIM tableau.
    """

    n = len(tableau.z_output(0))

    pauli = np.zeros((2 * n, n, 2), dtype="bool")
    signs = np.zeros(2 * n, dtype="bool")

    for i in range(n):
        for k in range(2):
            for j in range(n):

                if k == 0:
                    stab = tableau.x_output_pauli(i, j)
                else:
                    stab = tableau.z_output_pauli(i, j)

                if stab == 0:
                    stab = (0, 0)
                elif stab == 1:
                    stab = (1, 0)
                elif stab == 2:
                    stab = (1, 1)
                else:
                    stab = (0, 1)

                pauli[2 * i + k, j, :] = stab

            if k == 0:
                signs[2 * i + k] = (tableau.x_sign(i) - 1) / 2
            else:
                signs[2 * i + k] = (tableau.z_sign(i) - 1) / 2

    return pauli, signs
