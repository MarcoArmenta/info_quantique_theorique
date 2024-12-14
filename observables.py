# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:42:28 2024

@author: lenovo
"""
class PauliObservable:
    def __init__(self, pauli_chaine):
        self.pauli_chaine = pauli_chaine

    def mesurer(self, stabilisateurs):
        return {"+": 0.5, "-": 0.5}
