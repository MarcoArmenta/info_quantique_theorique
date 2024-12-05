# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 19:38:52 2024

@author: iphone
"""

import numpy as np

class QuantumCircuit:
    
    def __init__(self, json_data):              #generer par claud.ai
        self.num_qubits = []              #generer par claud.ai
        self.observable = []              #generer par claud.ai
        self.eigenvalues = []              #generer par claud.ai
        self.gates = []              #generer par claud.ai
        for circuit_info in json_data:              #generer par claud.ai
            self.num_qubits.append(circuit_info[0])              #generer par claud.ai
            self.observable.append(circuit_info[1])              #generer par claud.ai
            self.eigenvalues.append(circuit_info[2])              #generer par claud.ai
            self.gates.append(circuit_info[3:])              #generer par claud.ai
            

    def apply_hadamard(self, stabilizers, targets):
        
        for i in range(len(stabilizers)):
            for target in targets:
                if not np.array_equal(stabilizers[i][target], np.eye(2, dtype=int)):
                    stabilizers[i][target] = np.round(np.dot(self.hadamard(), np.round(np.dot(stabilizers[i][target], self.hadamard())).astype(int))).astype(int)
        
        return stabilizers
    
    def apply_s(self, stabilizers, targets):
        
        for i in range(len(stabilizers)):
            for target in targets:
                if not np.array_equal(stabilizers[i][target], np.eye(2, dtype=int)):
                    stabilizers[i][target] = np.dot(self.s_gate(), np.dot(stabilizers[i][target], self.s_dag()))
        
        return stabilizers
    
    def apply_pauli(self, gate_type, stabilizers, targets):
        
        for i in range(len(stabilizers)):
            for target in targets:
                if not np.array_equal(stabilizers[i][target], np.eye(2, dtype=int)):
                    stabilizers[i][target] = np.dot(self.pauli_gate(gate_type), np.dot(stabilizers[i][target], self.pauli_gate(gate_type)))
        
        return stabilizers
    
    def apply_cx(self, stabilizers, targets):
        
        for i in range(len(stabilizers)):
            for target in targets:
                target0 = list(target)[0]
                target1 = list(target)[1]
                np.eye(2, dtype=int)
                px = np.eye(2, dtype=int)
                pz = np.eye(2, dtype=int)
                if stabilizers[i][target0][0][1] != 0:
                    px = self.pauli_gate('x')
                if stabilizers[i][target1][0][1] + stabilizers[i][target1][1][0] == 0 and not np.array_equal(stabilizers[i][target1], np.eye(2, dtype=int)):
                    pz = self.pauli_gate('z')
                
                stabilizers[i][target0] = np.dot(stabilizers[i][target0], pz)
                stabilizers[i][target1] = np.dot(px, stabilizers[i][target1])
                
        return stabilizers                

    
    
    def hadamard(self): # cette methode generer par claud.ai
        
        # Matrice de Hadamard
        H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        return H

    def s_gate(self): # cette methode generer par claud.ai
        
        # Matrice de la porte S (pi/2 rotation sur l'axe Z)
        S = np.array([[1, 0], [0, 1j]])
        return S

    def s_dag(self): #generer par claud.ai
        
        
        S = np.array([[1, 0], [0, -1j]])
        return S

    def cx_gate(self, control_qubit, target_qubit): # cette methode generer par claud.ai
        
        # Matrice de la porte CX
        CX = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 1],
                       [0, 0, 1, 0]])
        return CX

    def pauli_gate(self, pauli_type): # cette methode generer par claud.ai
        
        # pauli_type : 'X', 'Y' ou 'Z'
        if pauli_type == 'x':
            matrix = np.array([[0, 1], [1, 0]])
        elif pauli_type == 'y':
            matrix = np.array([[0, -1j], [1j, 0]])
        elif pauli_type == 'z':
            matrix = np.array([[1, 0], [0, -1]])
        else:
            raise ValueError("Type de Pauli non reconnu. Utilisez 'X', 'Y' ou 'Z'.")
        
        
        return matrix

    

    