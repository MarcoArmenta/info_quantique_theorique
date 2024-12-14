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
            

    def apply_hadamard(self, stabilizers, targets, phase):
        
        for i in range(len(stabilizers)):
            for target in targets:
                if not stabilizers[i][target] == "i":
                    if stabilizers[i][target] == "z":
                        stabilizers[i][target] = "x" 
                        
                    elif stabilizers[i][target] == "x":
                        stabilizers[i][target] = "z"
                        
                    elif stabilizers[i][target] == "y":
                        phase[i] = -1 * phase[i]
                    
        
        return stabilizers, phase
    
    def apply_s(self, stabilizers, targets, phase):
        
        for i in range(len(stabilizers)):
            for target in targets:
                if not stabilizers[i][target] == "i":
                    if stabilizers[i][target] == "z":
                        True 
                    elif stabilizers[i][target] == "x":
                        stabilizers[i][target] = "y"
                        
                    elif stabilizers[i][target] == "y":
                        stabilizers[i][target] = "x"
                        phase[i] = -1 * phase[i]
                    #stabilizers[i][target] = np.dot(self.s_gate(), np.dot(stabilizers[i][target], self.s_dag()))
        
        return stabilizers, phase
    
    def apply_pauli(self, gate_type, stabilizers, targets, phase):
        
        for i in range(len(stabilizers)):
            for target in targets:
                if not stabilizers[i][target] == "i":
                    if gate_type == "x":
                        if stabilizers[i][target] == "x":
                             
                            True
                        elif stabilizers[i][target] == "y":
                            phase[i] = -1 * phase[i]
                            
                        elif stabilizers[i][target] == "z":
                        
                            phase[i] = -1 * phase[i]
                    
                    if gate_type == "y":
                        if stabilizers[i][target] == "y":
                             
                            True
                        elif stabilizers[i][target] == "x":
                            phase[i] = -1 * phase[i]
                            
                        elif stabilizers[i][target] == "z":
                        
                            phase[i] = -1 * phase[i]
                            
                    if gate_type == "z":
                        if stabilizers[i][target] == "z":
                             
                            True
                        elif stabilizers[i][target] == "x":
                            phase[i] = -1 * phase[i]
                            
                        elif stabilizers[i][target] == "y":
                        
                            phase[i] = -1 * phase[i]
                    
        
        return stabilizers, phase
    
    def apply_cx(self, stabilizers, targets, phase):
        
        pauli_mult = {"ii": ("i", 1), "iz": ("z", 1), "ix": ("x", 1), "iy": ("y",1), "zi": ("z", 1), "xi": ("x", 1), "yi": ("y", 1), "zx": ("y", 1j), "xy": ("z", 1j), "yz": ("x", 1j), "xz": ("y", -1j), "yx": ("z", -1j), "zy": ("x", -1j)}
        
        for i in range(len(stabilizers)):
            for target in targets:
                target0 = list(target)[0]
                target1 = list(target)[1]
                
                cible = "ii"
                controle = "ii"
                if stabilizers[i][target0] == "z":
                    cible = "i" + stabilizers[i][target1] 
                elif stabilizers[i][target0] == "x":
                    cible = "x" + stabilizers[i][target1]
                        
                elif stabilizers[i][target0] == "y":
                    cible = "x" + stabilizers[i][target1]
                    #phase[i] = -1 * phase[i]
                
                if stabilizers[i][target1] == "x":
                    controle = stabilizers[i][target0] + "i"
                elif stabilizers[i][target1] == "z":
                    controle = stabilizers[i][target0] + "z"
                        
                elif stabilizers[i][target1] == "y":
                    controle = stabilizers[i][target0] + "z"
                    #phase[i] = -1 * phase[i]
                
                stabilizers[i][target0] = list(pauli_mult[controle])[0]
                phase[i] = phase[i] * list(pauli_mult[controle])[1]
                stabilizers[i][target1] = list(pauli_mult[cible])[0]
                phase[i] = phase[i] * list(pauli_mult[cible])[1]
        
        return stabilizers, phase                

    
    
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

    

    