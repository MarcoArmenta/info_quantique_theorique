# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:54:34 2024

@author: lenovo
"""
from quantumcircuit import QuantumCircuit
from multiprocessing import Pool
from observables import PauliObservable

class GKSimulator:
    def __init__(self):
        # No arguments should be expected here
        pass

    def executer(self, circuit):
        """
        Execute the quantum circuit and measure the observable.
        """
        circuit.exécuter()
        observable = PauliObservable(circuit.observable)
        return observable.mesurer(circuit.table_stabilisateurs)

    def executermultiple(self, circuits):
        """
        Execute multiple quantum circuits in parallel.
        """
        with Pool(8) as pool:
            resultats = pool.map(self.executer, circuits)
        return resultats
