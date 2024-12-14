# -*- coding: utf-8 -*-
"""
Créé le Mer 4 Déc 2024 à 14:40:00

@author: lenovo
"""
import numpy as np
class QuantumCircuit:
    def __init__(self, données_circuit):
        self.n_qubits = données_circuit[0]
        self.stabilisateurs = []
        for i in range(self.n_qubits):
            V_x = [0] * self.n_qubits  
            V_z = [0] * self.n_qubits 
            V_z[i] = 1  
            self.stabilisateurs.append({'V_x': V_x, 'V_z': V_z})

    def appliquer_hadamard(self, q):
        for stabilisateur in self.stabilisateurs:
            valeur_temporaire = stabilisateur['V_x'][q]
            stabilisateur['V_x'][q] = stabilisateur['V_z'][q]
            stabilisateur['V_z'][q] = valeur_temporaire

    def appliquer_phase_S(self, q):
        for stabilisateur in self.stabilisateurs:
            stabilisateur['V_z'][q] = (stabilisateur['V_z'][q] + stabilisateur['V_x'][q]) % 2

    def appliquer_CNOT(self, cible, controle):
        for stabilisateur in self.stabilisateurs:
            stabilisateur['V_z'][controle] = (stabilisateur['V_z'][controle] + stabilisateur['V_z'][cible]) % 2
            stabilisateur['V_x'][cible] = (stabilisateur['V_x'][cible] + stabilisateur['V_x'][controle]) % 2

    def appliquer_pauli(self, q, pauli):
        for stabilisateur in self.stabilisateurs:
            if pauli == 'X':
                stabilisateur['V_x'][q], stabilisateur['V_z'][q] = stabilisateur['V_z'][q], stabilisateur['V_x'][q]
            elif pauli == 'Z':
                stabilisateur['V_x'][q] = (stabilisateur['V_x'][q] + stabilisateur['V_z'][q]) % 2
            elif pauli == 'Y':
                stabilisateur['V_x'][q] = (stabilisateur['V_x'][q] + stabilisateur['V_z'][q]) % 2
                stabilisateur['V_z'][q] = (stabilisateur['V_z'][q] + stabilisateur['V_x'][q]) % 2
