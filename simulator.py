"""
This is the main module of the project. It simulates Clifford circuits efficiently using the stabilizer formalism.
"""

import json
import re
from multiprocessing import pool

import numpy as np


class GKSimulator:
    """
    This class simulates Clifford circuits efficiently using the stabilizer formalism. The simulator uses the tableau representation of the stabilizer formalism inspired by the STIM library (https://github.com/quantumlib/Stim).

    Attributes
    ----------
    pauli : np.ndarray
        The Pauli matrices of the tableau.
    signs : np.ndarray
        The signs of the tableau.
    observable_expectation : dict
        The expectation value of the observable.
    """

    def __init__(self):

        self.pauli = None
        self.signs = None
        self.observable_expectation = None

    def _init_tableau(self, n):
        """
        Initialize the initial stabilizer tableau with an identity stabilizer pauli.

        Parameters
        ----------
        n : int
            The number of qubits in the circuit.
        """

        pauli = np.zeros((2 * n, n, 2), dtype="bool")
        signs = np.zeros(2 * n, dtype="bool")

        pauli[::2, :, 0] = np.eye(n, dtype="bool")
        pauli[1::2, :, 1] = np.eye(n, dtype="bool")

        self.pauli = pauli
        self.signs = signs

        return pauli, signs

    def apply_gate(self, gate, qubits):
        """
        Apply a gate to the stabilizer tableau.

        Parameters
        ----------
        gate : Gate
            The gate to apply.
        qubits : list
            The qubits the gate acts on.
        """

        # Adapt to the notation of one vs. multiple qubits
        if not isinstance(qubits, list):
            qubits = [qubits]

        pauli = self.pauli.copy()
        signs = self.signs.copy()

        for i, qubit_row in enumerate(qubits):
            for j in range(2):

                stabilizer = gate.pauli[2 * i + j, :, :]
                new_stabilizer = np.zeros_like(pauli[2 * qubit_row, :, :])
                new_sign = gate.signs[2 * i + j]

                for k, qubit_col in enumerate(qubits):

                    if np.all(stabilizer[k, :] == (0, 0)):
                        pass

                    elif np.all(stabilizer[k, :] == (1, 0)):

                        new_stabilizer, new_sign = self.multiply_pauli_chains(
                            new_stabilizer,
                            new_sign,
                            pauli[2 * qubit_col, :, :],
                            signs[2 * qubit_col],
                        )

                    elif np.all(stabilizer[k, :] == (0, 1)):

                        new_stabilizer, new_sign = self.multiply_pauli_chains(
                            new_stabilizer,
                            new_sign,
                            pauli[2 * qubit_col + 1, :, :],
                            signs[2 * qubit_col + 1],
                        )

                    elif np.all(stabilizer[k, :] == (1, 1)):

                        temp1, temp2 = self.multiply_pauli_chains(
                            pauli[2 * qubit_col, :, :],
                            signs[2 * qubit_col],
                            pauli[2 * qubit_col + 1, :, :],
                            signs[2 * qubit_col + 1],
                        )

                        new_stabilizer, new_sign = self.multiply_pauli_chains(
                            new_stabilizer,
                            new_sign,
                            temp1,
                            temp2,
                        )

                self.pauli[2 * qubit_row + j, :, :] = new_stabilizer
                self.signs[2 * qubit_row + j] = new_sign

        return self.pauli, self.signs

    def multiply_pauli_chains(self, chain1, sign1, chain2, sign2):
        """
        STRONGLY INSPIRED BY LLM'S. Multiply two Pauli chains.

        Parameters
        ----------
        chain1 : np.ndarray
            The first Pauli chain.
        sign1 : np.ndarray
            The first sign of the Pauli chain.
        chain2 : np.ndarray
            The second Pauli chain.
        sign2 : np.ndarray
            The second sign of the Pauli chain.
        """

        # Compute the result of the multiplication up to a global phase
        result_chain = np.logical_xor(chain1, chain2)

        # Find where are the Paulis in the Pauli chains
        x1 = (chain1[:, 0] == 1) & (chain1[:, 1] == 0)
        y1 = (chain1[:, 0] == 1) & (chain1[:, 1] == 1)
        z1 = (chain1[:, 0] == 0) & (chain1[:, 1] == 1)
        x2 = (chain2[:, 0] == 1) & (chain2[:, 1] == 0)
        y2 = (chain2[:, 0] == 1) & (chain2[:, 1] == 1)
        z2 = (chain2[:, 0] == 0) & (chain2[:, 1] == 1)

        # Add the signs due to the anti-commutation of the Paulis
        w = np.sum(y1 & x2) + np.sum(z1 & y2) + np.sum(x1 & z2)

        # Add the signs due to the imaginary unit
        q = (
            np.sum(x1 & y2)
            + np.sum(x1 & z2)
            + np.sum(y1 & x2)
            + np.sum(y1 & z2)
            + np.sum(z1 & x2)
            + np.sum(z1 & y2)
        )

        result_sign = (sign1 ^ sign2 ^ w ^ (q // 2)) % 2

        return result_chain, result_sign

    def measure_observable(self, pauli_observable, eigenvalue):
        """
        Measure the expectation value of an Pauli observable.

        Parameters
        ----------
        pauli_observable : PauliObservable
            The Pauli observable to measure.
        eigenvalue : str
            The eigenvalue to measure.
        """

        observable_expectation = {"+1": 0, "-1": 0}

        # Case of the identity observable
        if len(pauli_observable.i_qubits) == pauli_observable.num_qubits:
            observable_expectation["+1"] = 1
            observable_expectation["-1"] = 0

        else:

            pauli = np.zeros((pauli_observable.num_qubits, 2), dtype="bool")
            signs = np.zeros(1, dtype="bool")

            for qubit in pauli_observable.x_qubits:

                pauli, signs = self.multiply_pauli_chains(
                    pauli,
                    signs,
                    self.pauli[2 * qubit],
                    self.signs[2 * qubit],
                )

            for qubit in pauli_observable.z_qubits:

                pauli, signs = self.multiply_pauli_chains(
                    pauli,
                    signs,
                    self.pauli[2 * qubit + 1],
                    self.signs[2 * qubit + 1],
                )

            for qubit in pauli_observable.y_qubits:

                temp1, temp2 = self.multiply_pauli_chains(
                    self.pauli[2 * qubit],
                    self.signs[2 * qubit],
                    self.pauli[2 * qubit + 1],
                    self.signs[2 * qubit + 1],
                )

                pauli, signs = self.multiply_pauli_chains(
                    pauli,
                    signs,
                    temp1,
                    temp2,
                )

            if np.any((pauli[:, 0] == 1) & (pauli[:, 1] == 0)) or np.any(
                (pauli[:, 0] == 1) & (pauli[:, 1] == 1)
            ):
                observable_expectation["+1"] = 0.5
                observable_expectation["-1"] = 0.5

            else:
                if np.any(signs.sum() % 2 == 0):
                    observable_expectation["+1"] = 1
                if np.any(signs.sum() % 2 == 1):
                    observable_expectation["-1"] = 1

        if "+" not in eigenvalue:
            observable_expectation.pop("+1", None)
        if "-" not in eigenvalue:
            observable_expectation.pop("-1", None)

        return observable_expectation

    def evolve_tableau(self, num_qubits, gates, observables, eigenvalues, verbose=True):
        """
        Evolve the stabilizer tableau with a list of gates.

        Parameters
        ----------
        num_qubits : int
            The number of qubits in the circuit.
        gates : list
            The list of gates to apply.
        observables : list
            The list of observables to measure.
        eigenvalues : list
            The list of eigenvalues to measure.
        verbose : bool
            Whether to print the tableau at each step.
        """

        self._init_tableau(num_qubits)

        if verbose:
            self.show_tableau(self.pauli, self.signs, "I")

        for bloc in gates:
            for gate, qubits_list in bloc.items():
                for qubits in qubits_list:
                    self.apply_gate(Gate(gate), qubits)

                    if verbose:
                        self.show_tableau(self.pauli, self.signs, gate)

        self.observable_expectation = self.measure_observable(observables, eigenvalues)

        if verbose:
            self.show_tableau(self.pauli, self.signs, "Final tableau")

            print(
                "Observable expectation:",
                self.observable_expectation,
            )

        return self.observable_expectation

    def run(self, quantumcircuit, save_results=True):
        """
        Run the simulation of the quantum circuit using multiprocessing.

        Parameters
        ----------
        quantumcircuit : QuantumCircuit
            The quantum circuit to simulate.
        save_results : bool
            Whether to save the results in a JSON file.
        """

        num_qubits = quantumcircuit.num_qubits
        observables = quantumcircuit.observables
        eigenvalues = quantumcircuit.eigenvalues
        gates = quantumcircuit.gates

        with pool.Pool() as p:
            observable_expectation = p.starmap(
                self.evolve_tableau, zip(num_qubits, gates, observables, eigenvalues)
            )

            # probabilities.append(observable_expectation)

        if save_results:
            with open("results.json", "w", encoding="utf-8") as file:
                json.dump(observable_expectation, file, ensure_ascii=False, indent=4)

    def show_tableau(self, pauli, signs, name="Tableau"):
        """
        Visualize the stabilizer pauli.
        """

        n = len(signs) // 2

        pauli_visual = np.zeros((2 * n, n + 1), dtype="str")
        signs_visual = np.zeros(2 * n, dtype="str")

        pauli_visual[:, 1:] = pauli[:, :, 0] + 2 * pauli[:, :, 1]

        # Map the Pauli matrices to their corresponding letters
        mapping = {0: "I", 1: "X", 2: "Z", 3: "Y"}
        for key, value in mapping.items():
            pauli_visual[:, 1:][pauli_visual[:, 1:] == str(key)] = value

        signs_visual[~signs] = "+"
        signs_visual[signs] = "-"

        pauli_visual[:, 0] = signs_visual

        # Print the visualized tableau
        print(name)
        for row in pauli_visual.T:
            print(" ".join(row))


class Gate:
    """
    This class implements the gates for the stabilizer formalism under the tableau representation. The implemented gates are the identity, Pauli-X, Pauli-Y, Pauli-Z, S, H, and CX gates.
    """

    def __init__(self, gate):

        implemented_gates = {
            "I": self.I,
            "x": self.X,
            "y": self.Y,
            "z": self.Z,
            "s": self.S,
            "h": self.H,
            "cx": self.CX,
        }

        self.pauli, self.signs = implemented_gates[gate]()

    def I(self):
        """Initialize the identity stabilizer pauli."""

        pauli = np.zeros((2, 1, 2), dtype="bool")
        signs = np.zeros(2, dtype="bool")

        pauli[0, :, 0] = 1
        pauli[1, :, 1] = 1

        return pauli, signs

    def X(self):
        """Initialize the Pauli-X stabilizer pauli."""

        pauli = np.zeros((2, 1, 2), dtype="bool")
        signs = np.zeros(2, dtype="bool")

        pauli[0, 0, 0] = 1
        pauli[1, 0, 1] = 1

        signs[1] = 1

        return pauli, signs

    def Y(self):
        """Initialize the Pauli-Y stabilizer pauli."""

        pauli = np.zeros((2, 1, 2), dtype="bool")
        signs = np.zeros(2, dtype="bool")

        pauli[0, 0, 0] = 1
        pauli[1, 0, 1] = 1

        signs[0] = 1
        signs[1] = 1

        return pauli, signs

    def Z(self):
        """Initialize the Pauli-Z stabilizer pauli."""

        pauli = np.zeros((2, 1, 2), dtype="bool")
        signs = np.zeros(2, dtype="bool")

        pauli[0, 0, 0] = 1
        pauli[1, 0, 1] = 1

        signs[0] = 1

        return pauli, signs

    def S(self):
        """Initialize the S stabilizer pauli."""

        pauli = np.zeros((2, 1, 2), dtype="bool")
        signs = np.zeros(2, dtype="bool")

        pauli[0, 0, 0] = 1
        pauli[0, 0, 1] = 1
        pauli[1, 0, 1] = 1

        return pauli, signs

    def H(self):
        """Initialize the H stabilizer pauli."""

        pauli = np.zeros((2, 1, 2), dtype="bool")
        signs = np.zeros(2, dtype="bool")

        pauli[0, 0, 1] = 1
        pauli[1, 0, 0] = 1

        return pauli, signs

    def CX(self):
        """Initialize the CX stabilizer pauli."""

        pauli = np.zeros((4, 2, 2), dtype="bool")
        signs = np.zeros(4, dtype="bool")

        pauli[0, 0, 0] = 1
        pauli[0, 1, 0] = 1
        pauli[1, 0, 1] = 1
        pauli[2, 1, 0] = 1
        pauli[3, 0, 1] = 1
        pauli[3, 1, 1] = 1

        return pauli, signs
