"""
Auteur: Jérémie Boudreault
"""

import numpy as np


class PauliObservable:
    def __init__(self, pauli_str) -> None:
        self.pauli_str = pauli_str
        self.n_qubits = len(pauli_str)
        xs = np.zeros(self.n_qubits, dtype = bool)
        zs = np.zeros(self.n_qubits, dtype = bool)
        for idx in range(self.n_qubits):
            if self.pauli_str[idx] == "x":
                xs[idx] = True
            elif self.pauli_str[idx] == "z":
                zs[idx] = True
            elif self.pauli_str[idx] == "y":
                xs[idx] = True
                zs[idx] = True
            np.concatenate([xs, zs])

        self.paulis_vec = np.concatenate([xs, zs])



