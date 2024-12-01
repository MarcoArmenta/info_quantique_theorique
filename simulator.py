# -*- coding: utf-8 -*-
"""

@author: lenovo
"""


from quantumcircuit import QuantumCircuit
from multiprocessing import Pool

class GKSimulator:
    def __init__(self, quantum_circuit):
        self.quantum_circuit = quantum_circuit

    def measure_pauli(self, observable):
        pass

    def run(self, circuits):
        with Pool(processes=8) as pool:
            results = pool.map(self.simulate_single_circuit, circuits)
        return results

    
    def simulate_single_circuit(self, circuit):
        return self.measure_pauli(circuit)
