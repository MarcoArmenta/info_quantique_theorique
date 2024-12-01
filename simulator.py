# -*- coding: utf-8 -*-
"""
@author: lenovo
"""

import numpy as np
from quantumcircuit import QuantumCircuit
from multiprocessing import Pool

class GKSimulator :
    def __init__(self, quantum_circuit) :
        self.quantum_circuit=quantum_circuit
        self.stabilizers=self.initialize_stabilizers()

    def initialize_stabilizers(self) :
        num_qubits= self.quantum_circuit.num_qubits
        x_matrix= np.zeros((num_qubits, num_qubits), dtype=int)
        z_matrix=np.identity(num_qubits, dtype=int)
        phase= np.zeros(num_qubits, dtype=int)
        return {'X': x_matrix, 'Z': z_matrix, 'phase': phase}

    def apply_hadamard(self, qubit):
        self.stabilizers['X'][:, qubit], self.stabilizers['Z'][:,qubit] = (
            self.stabilizers['Z'][:, qubit], 
            self.stabilizers['X'][:, qubit] )
      
        self.stabilizers['phase'][qubit]= (self.stabilizers['phase'][qubit] + 1) % 2

    def apply_s(self, qubit):
        self.stabilizers['Z'][:, qubit]= (self.stabilizers['Z'][:, qubit] + self.stabilizers['X'][:, qubit]) % 2

    
    def apply_cx(self, control, target):
        self.stabilizers['X'][:, target]= (self.stabilizers['X'][:, target] + self.stabilizers['X'][:, control]) % 2
        self.stabilizers['Z'][:, control]= (self.stabilizers['Z'][:, control] + self.stabilizers['Z'][:, target]) % 2

    def measure_pauli(self, observable):
        x_vector= observable.x_vector
        z_vector= observable.z_vector
        commutes= True
        for i in range(self.quantum_circuit.num_qubits):
            if np.dot(self.stabilizers['X'][i], z_vector) % 2 != np.dot(self.stabilizers['Z'][i], x_vector) % 2:
                commutes = False
                break
        if commutes:
            return {"+1": 1.0, "-1": 0.0}
        else:
            return {"+1": 0.5, "-1": 0.5}
    def run(self, circuits):
        with Pool(processes=8) as pool:
            results= pool.map(self.simulate_single_circuit, circuits)
        return results

    
    def simulate_single_circuit(self, circuit):
        for gate, qubits in circuit.gates:
            if gate == 'h':
                for qubit in qubits:
                    self.apply_hadamard(qubit)
            elif gate == 's':
                for qubit in qubits:
                    self.apply_s(qubit)
            elif gate == 'cx':
                for control, target in qubits:
                    self.apply_cx(control, target)


        return self.measure_pauli(circuit.observable)
