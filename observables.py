# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:42:28 2024

@author: lenovo
"""

class PauliObservable:
    ''' Initialise une observable de Pauli'''
    def __init__(self,pauli_chaine):
   
   
        self.pauli_chaine=pauli_chaine
        
    ''' Mesure l'observable en fonction des stabilisateurs'''
#cette partie est généré par IA
    def mesurer(self, stabilisateurs):
        
        return {"+":0.5, "-":0.5}
