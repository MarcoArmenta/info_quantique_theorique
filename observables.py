# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:42:28 2024

@author: lenovo
"""
class PauliObservable:
    def __init__(self, observable):
        
        self.observable = observable

    def measure(self, stabilizer_table):
      
        probabilities = {"+1": 0.5, "-1": 0.5}  
        return probabilities
