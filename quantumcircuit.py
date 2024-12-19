# -*- coding: utf-8 -*-
"""
Créé le Mer 4 Déc 2024 à 14:40:00

@author: lenovo
"""
import numpy as np

class QuantumCircuit:
    def __init__(self, circuits):
       
        self.circuits = []
        for circuit_description in circuits:
            circuit = {
                "num_qubits": circuit_description[0],
                "observable": circuit_description[1],
                "eigenvalues": circuit_description[2],
                "gates": circuit_description[3:]
            }
            circuit["stabilizer_table"] = self._initialize_stabilizer_table(circuit["num_qubits"])
            self.circuits.append(circuit)

    def _initialize_stabilizer_table(self, num_qubits):
       
        stabilizer_table = []
        for i in range(num_qubits):
            z = [1 if j == i else 0 for j in range(num_qubits)]
            x = [0] * num_qubits
            stabilizer_table.append((z, x))
        return stabilizer_table

    def apply_gate(self, circuit, gate, targets):
       
        if gate == "h":
            self._apply_hadamard(circuit, targets[0])
        elif gate == "s":
            self._apply_s_gate(circuit, targets[0])
        elif gate == "x":
            self._apply_pauli_x(circuit, targets[0])
        elif gate == "z":
            self._apply_pauli_z(circuit, targets[0])
        elif gate == "y":
            self._apply_pauli_y(circuit, targets[0])
        elif gate == "cx":
            self._apply_cx_gate(circuit, targets[0], targets[1])
        else:
            raise ValueError(f"Porte inconnue : {gate}")

    def _apply_hadamard(self, circuit, qubit):
       
        for z, x in circuit["stabilizer_table"]:
            z[qubit], x[qubit] = x[qubit], z[qubit]

    def _apply_s_gate(self, circuit, qubit):
        
        for z, x in circuit["stabilizer_table"]:
            if x[qubit] == 1:
                z[qubit] ^= x[qubit]

    def _apply_pauli_x(self, circuit, qubit):
       
        for z, x in circuit["stabilizer_table"]:
            x[qubit] ^= 1

    def _apply_pauli_z(self, circuit, qubit):
        
        for z, x in circuit["stabilizer_table"]:
            z[qubit] ^= 1

    def _apply_pauli_y(self, circuit, qubit):
        
        for z, x in circuit["stabilizer_table"]:
            z[qubit] ^= 1
            x[qubit] ^= 1

    def _apply_cx_gate(self, circuit, control, target):
        
        for z, x in circuit["stabilizer_table"]:
            z[target] ^= z[control]
            x[control] ^= x[target]
