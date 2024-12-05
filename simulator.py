# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:54:34 2024

@author: lenovo
"""

from multiprocessing import Pool
from quantumcircuit import QuantumCircuit
from observables import PauliObservable



class GKSimulator:
    
    ''' cette partie initialise le simulateur sans dépendre d'un circuit spécifique'''
       
    def __init__(self):
        
   
        pass
    ''' Cette méthode executer exécute les portes du circuit  '''
    def executer(self,circuit):
        
        circuit.executer()
        observable=PauliObservable(circuit.observable)
        return observable.mesurer(circuit.stabilisateurs)
    
    
    ''' cette partie simule plusieurs circuits en parallèle'''

    def executermultiple(self,circuits):
       
   #cette partie est généré par IA
        
        with Pool(8) as pool:
            resultats = pool.map(self.executer, circuits)
        return resultats
