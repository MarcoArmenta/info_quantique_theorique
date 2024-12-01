# -*- coding: utf-8 -*-
"""


@author: lenovo
"""



import numpy as np

class QuantumCircuit:
    def __init__(self, circuit_data):
        self.num_qubits = circuit_data[0]
        self.observable = circuit_data[1]
        self.eigenvalues = circuit_data[2]
        self.gates = circuit_data[3:]
        self.stabilizers = self.initialize_stabilizers()

    def initialize_stabilizers(self):
       
        num_stabilizers = self.num_qubits
        x_matrix = np.zeros((num_stabilizers, self.num_qubits), dtype=int)
        z_matrix = np.identity(self.num_qubits, dtype=int)
        phase = np.zeros(num_stabilizers, dtype=int)
        return {'X': x_matrix, 'Z': z_matrix, 'phase': phase}

    def apply_gate(self, gate_type, qubits):
        if gate_type == 'h':
            self.apply_hadamard(qubits)
        elif gate_type == 's':
            self.apply_s(qubits)
        elif gate_type == 'x' or gate_type == 'y' or gate_type == 'z':
            self.apply_pauli(gate_type, qubits)
        elif gate_type == 'cx':
            self.apply_cx(qubits)
        else:
            raise ValueError(f"Porte non prise en charge: {gate_type}")

    def apply_hadamard(self, qubits):
        for qubit in qubits:
         
            pass

    def apply_s(self, qubits):
        for qubit in qubits:
           
            pass

    def apply_pauli(self, gate, qubits):
        for qubit in qubits:
            if gate == 'x':
                pass
            elif gate == 'y':
            
                pass
            elif gate == 'z':
               
                pass

    def apply_cx(self, qubit_pairs):
        for control, target in qubit_pairs:

            
            pass

    def build_circuit(self):
        for gate_dict in self.gates:
            for gate, qubits in gate_dict.items():
                self.apply_gate(gate, qubits)
