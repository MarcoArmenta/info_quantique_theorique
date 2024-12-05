"""
This module defines the QuantumCircuit class, which is used to store the quantum circuits
"""

from observables import PauliObservable


class QuantumCircuit:
    """
    Class to store quantum circuits.

    Attributes:
    ----------
    num_circuits : int
        Number of circuits.
    num_qubits : list
        Number of qubits in each circuit.
    observables : list
        PauliObservable objects for each circuit.
    obs_pauli : list
        Pauli strings for each circuit.
    eigenvalues : list
        Eigenvalues for each circuit.
    gates : list
        List of gates for each circuit.
    """

    def __init__(self, circuits):
        self._load_circuits(circuits)

    def _load_circuits(self, circuits):
        """
        Load circuits.

        Parameters:
        -----------
        circuits : list
            List of circuits.
        """

        num_qubits = []
        observables = []
        obs_pauli = []
        eigenvalues = []
        gates = []

        for circuit in circuits:
            num_qubits.append(circuit[0])
            observables.append(PauliObservable(circuit[1]))
            obs_pauli.append(circuit[1])
            eigenvalues.append(circuit[2])
            gates.append(circuit[3:])

        self.num_circuits = len(circuits)
        self.num_qubits = num_qubits
        self.observables = observables
        self.obs_pauli = obs_pauli
        self.eigenvalues = eigenvalues
        self.gates = gates
