# -*- coding: utf-8 -*-
"""
Créé le Mer 4 Déc 2024 à 14:40:00

@author: lenovo
"""

import numpy as np

class QuantumCircuit:
    def __init__(self, données_circuit):
        self.nombre_qubits = données_circuit[0]
        self.observable = données_circuit[1]
        self.valeurs_propres = données_circuit[2]
        self.portes = données_circuit[3]
        self.table_stabilisateurs = np.eye(2 * self.nombre_qubits, dtype=int)

    def appliquer_porte(self, porte, cibles):
        if porte == "h":
            self._appliquer_hadamard(cibles[0])
        elif porte == "s":
            self._appliquer_phase(cibles[0])
        elif porte == "x":
            self._appliquer_pauli_x(cibles[0])
        elif porte == "z":
            self._appliquer_pauli_z(cibles[0])
        elif porte == "cx":
            self._appliquer_cnot(*cibles[0])

    def _appliquer_hadamard(self, qubit):
        self.table_stabilisateurs[:, [qubit, qubit + self.nombre_qubits]] = self.table_stabilisateurs[:, [qubit + self.nombre_qubits, qubit]]

    def _appliquer_phase(self, qubit):
        self.table_stabilisateurs[:, qubit + self.nombre_qubits] ^= self.table_stabilisateurs[:, qubit]

    def _appliquer_pauli_x(self, qubit):
        self.table_stabilisateurs[:, qubit] ^= 1

    def _appliquer_pauli_z(self, qubit):
        self.table_stabilisateurs[:, qubit + self.nombre_qubits] ^= 1

    def _appliquer_cnot(self, contrôle, cible):
        self.table_stabilisateurs[:, cible] ^= self.table_stabilisateurs[:, contrôle]
        self.table_stabilisateurs[:, cible + self.nombre_qubits] ^= self.table_stabilisateurs[:, contrôle + self.nombre_qubits]

    def exécuter(self):
        for porte, cibles in self.portes.items():            
            self.appliquer_porte(porte, cibles)
