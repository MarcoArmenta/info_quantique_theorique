# -*- coding: utf-8 -*-
"""

@author: lenovo
"""

import numpy as np

class PauliObservable:
    def __init__(self, pauli_string):
        self.pauli_string = pauli_string.upper()
        self.num_qubits = len(self.pauli_string)
        self.x_vector, self.z_vector, self.phase = self.pauli_string_to_vectors()

    def pauli_string_to_vectors(self):
        x_vector = np.zeros(self.num_qubits, dtype=int)
        z_vector = np.zeros(self.num_qubits, dtype=int)
        phase = 0  

        for idx, pauli in enumerate(self.pauli_string):
            if pauli == 'I':
                continue
            elif pauli == 'X':
                x_vector[idx] = 1
            elif pauli == 'Y':
                x_vector[idx] = 1
                z_vector[idx] = 1
                phase += 1  
            elif pauli == 'Z':
                z_vector[idx] = 1
            else:
                raise ValueError(f"Opérateur de Pauli invalide à la position {idx}: '{pauli}'.")

        phase = phase % 4
        return x_vector, z_vector, phase

    def to_matrix(self):
        from functools import reduce

        pauli_matrices = {
            'I': np.array([[1, 0], [0, 1]], dtype=complex),
            'X': np.array([[0, 1], [1, 0]], dtype=complex),
            'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
            'Z': np.array([[1, 0], [0, -1]], dtype=complex)
        }

        matrices = [pauli_matrices[pauli] for pauli in self.pauli_string]
        return reduce(np.kron, matrices)
