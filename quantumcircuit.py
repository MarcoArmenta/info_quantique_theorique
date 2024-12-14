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
        # Vérifiez que les cibles sont fournies en nombre approprié
        if porte in ["h", "s", "x", "z"] and len(cibles) != 1:
            raise ValueError(f"Not enough targets provided for gate {porte}. Required: 1, Given: {len(cibles)}")
        if porte == "cx" and len(cibles) != 2:
            raise ValueError(f"Not enough targets provided for CNOT gate. Required: 2, Given: {len(cibles)}")
        
        # Appliquer les portes en fonction du type
        if porte == "h":
            self._appliquer_hadamard(cibles[0])
        elif porte == "s":
            self._appliquer_phase(cibles[0])
        elif porte == "x":
            self._appliquer_pauli_x(cibles[0])
        elif porte == "z":
            self._appliquer_pauli_z(cibles[0])
        elif porte == "cx":
            self._appliquer_cnot(cibles[0], cibles[1])

    def _appliquer_hadamard(self, qubit):
        idx = qubit, qubit + self.nombre_qubits
        self.table_stabilisateurs[:, idx] = self.table_stabilisateurs[:, idx[::-1]]

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
