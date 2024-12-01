# -*- coding: utf-8 -*-
"""

@author: lenovo
"""


import numpy as np
from quantumcircuit import QuantumCircuit
from multiprocessing import Pool

class GKSimulator:
    def __init__(self, quantum_circuit):
        self.quantum_circuit = quantum_circuit

    def measure_pauli(self, observable):
        circuit_matrix = np.array(self.quantum_circuit.stabilizers['Z'])
        observable_matrix = np.array(observable.z_vector)
        result = np.dot(circuit_matrix, observable_matrix)
        return result

    def run(self, circuits):
        with Pool(processes=8) as pool:
            results = pool.map(self.simulate_single_circuit, circuits)
        return results

    def simulate_single_circuit(self, circuit):
        return self.measure_pauli(circuit)
